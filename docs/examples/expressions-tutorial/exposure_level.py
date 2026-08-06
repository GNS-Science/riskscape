def function(building, hazard_depth):
    result = {}

    if hazard_depth is None or hazard_depth <= 0:
        result['exposed'] = 0
        result['level'] = 'N/A'
        return result

    if hazard_depth > 3.0:
        level = 'Exposure >3.0m'
    elif hazard_depth > 2.0:
        level = 'Exposure >2.0m to <=3.0m'
    elif hazard_depth > 1.0:
        level = 'Exposure >1.0m to <=2.0m'
    else:
        level = 'Exposure >0.0m to <=1.0m'

    result['exposed'] = 1
    result['level'] = level

    return result 
