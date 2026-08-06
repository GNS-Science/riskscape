def function(building, hazard_depth):
    if hazard_depth is None or hazard_depth <= 0:
        return 'Not exposed'

    if hazard_depth > 3.0:
        status = 'Exposure >3.0m'
    elif hazard_depth > 2.0:
        status = 'Exposure >2.0m to <=3.0m'
    elif hazard_depth > 1.0:
        status = 'Exposure >1.0m to <=2.0m'
    else:
        status = 'Exposure >0.0m to <=1.0m'

    return status
