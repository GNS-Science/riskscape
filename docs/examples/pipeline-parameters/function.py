from nz.org.riskscape.engine.types import Types
from nz.org.riskscape.engine.types import Struct

ID = 'kaiju_stomp'
DESCRIPTION = 'Simple example of a parameterized function'

ARGUMENT_TYPES = [Struct.of('construction', Types.TEXT), \
                  Struct.of('severity', Types.FLOATING), \
                  Struct.of('steel_resilience', Types.FLOATING, \
                            'stone_resilience', Types.FLOATING, \
                            'concrete_resilience', Types.FLOATING) ]

RETURN_TYPE = Struct.of('damage', Types.FLOATING)

def function(building, hazard, options):
    construction = building.get('construction')
    # all the assumptions about how resilient a building is get passed in as model parameters
    resilience = options.get(construction + '_resilience', 0)

    damage = (10 - resilience) * hazard.get('severity')
    if damage > 100:
        damage = 100
    return {
        'damage': damage
    }
