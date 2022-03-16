def share(entity, targ, resourceFn, amount):
    entity_resource = resourceFn(entity)
    targ_resource = resourceFn(targ)
    amount = min(entity_resource.val, amount, targ_resource.max - targ_resource.val)
    entity_resource.decrement(amount)
    targ_resource.increment(amount)

    return amount
