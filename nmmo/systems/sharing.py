def share(entity, targ, resourceFn, amount):
    entity_resource = resourceFn(entity)
    targ_resource = resourceFn(targ)
    amount = min(entity_resource.val, amount, targ_resource.max - targ_resource.val)
    entity_resource.decrease(amount)
    targ_resource.increase(amount)

    return amount
