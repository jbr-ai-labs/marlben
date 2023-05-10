import marlben
from marlben.entity import entity
from marlben.systems.achievement import Diary


class Player(entity.Entity):
    def __init__(self, realm, pos, agent, color, pop, skills, visible_colors, accessible_colors):
        super().__init__(realm, pos, agent.iden, agent.name, color, pop, skills)

        self.agent = agent
        self.pop = pop

        # Scripted hooks
        self.target = None
        self.food = None
        self.water = None
        self.vision = 7

        # Submodules
        self.diary = None
        if tasks := realm.config.TASKS:
            self.diary = Diary(tasks)

        self.visible_colors = visible_colors
        self.accessible_colors = accessible_colors

        self.dataframe.init(marlben.Serialized.Entity, self.entID, self.pos)

    @property
    def serial(self):
        return self.population, self.entID

    @property
    def isPlayer(self) -> bool:
        return True

    @property
    def population(self):
        return self.pop

    def applyDamage(self, dmg, style, stealing_enabled=True):
        if dmg > 0 and stealing_enabled:
            self.resources.food.increment(dmg)
            self.resources.water.increment(dmg)
        self.skills.applyDamage(dmg, style)

    def receiveDamage(self, source, dmg, stealing_enabled=True):
        if not super().receiveDamage(source, dmg, stealing_enabled):
            if source:
                source.history.playerKills += 1
            return
        if dmg > 0 and stealing_enabled:
            self.resources.food.decrement(dmg)
            self.resources.water.decrement(dmg)
        self.skills.receiveDamage(dmg, stealing_enabled)

    def receiveLoot(self, loadout):
        if loadout.chestplate.level > self.loadout.chestplate.level:
            self.loadout.chestplate = loadout.chestplate
        if loadout.platelegs.level > self.loadout.platelegs.level:
            self.loadout.platelegs = loadout.platelegs

    def packet(self):
        data = super().packet()

        data['entID'] = self.entID
        data['annID'] = self.population

        data['base'] = self.base.packet()
        data['resource'] = self.resources.packet()
        data['skills'] = self.skills.packet()

        return data

    def update(self, realm, actions):
        """Post-action update. Do not include history"""
        super().update(realm, actions)

        if not self.alive:
            return

        self.resources.update(realm, self, actions)
        self.skills.update(realm, self, actions)

    def update_diary(self, realm):
        if self.diary:
            self.diary.update(realm, self)
