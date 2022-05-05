from pdb import set_trace as T

class Material:
   harvestable = False
   capacity    = 1
   def __init__(self, config):
      pass

   def __eq__(self, mtl):
      return self.index == mtl.index

   def __equals__(self, mtl):
      return self == mtl

class Lava(Material):
   tex   = 'lava'
   index = 0

class Water(Material):
   tex   = 'water'
   index = 7

class Grass(Material):
   tex   = 'grass'
   index = 2

class Scrub(Material):
   tex = 'scrub'
   index = 6

class Forest(Material):
   tex   = 'forest'
   index = 8

   harvestable = True
   degen       = Scrub

   def __init__(self, config):
      if config.game_system_enabled('Resource'):
         self.capacity = config.RESOURCE_FOREST_CAPACITY
         self.respawn  = config.RESOURCE_FOREST_RESPAWN


class Stone(Material):
   tex   = 'stone'
   index = 5


class ScrubImpassible(Scrub):
   index = 3


class BalancedWater(Forest):
   degen = ScrubImpassible
   tex = 'water'
   index = 1


class BalancedForest(Forest):
   degen = ScrubImpassible
   tex = 'forest'
   index = 4


class Meta(type):
   def __init__(self, name, bases, dict):
      self.indices = {mtl.index for mtl in self.materials}

   def __iter__(self):
      yield from self.materials

   def __contains__(self, mtl):
      if isinstance(mtl, Material):
         mtl = type(mtl)
      if isinstance(mtl, type):
         return mtl in self.materials
      return mtl in self.indices

class All(metaclass=Meta):
   '''List of all materials'''
   materials = {Lava, Water, Grass, Scrub, Forest, Stone, ScrubImpassible, BalancedForest, BalancedWater}

class Impassible(metaclass=Meta):
   '''Materials that agents cannot walk through'''
   materials = {Lava, Stone, ScrubImpassible, BalancedForest, BalancedWater}

class Habitable(metaclass=Meta):
   '''Materials that agents cannot walk on'''
   materials = {Grass, Scrub, Forest}
