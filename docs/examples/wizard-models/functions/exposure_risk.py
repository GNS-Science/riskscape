def function(building, hazard):
    # disclaimer: this is just an simple example and not based on any science
    if hazard is None or hazard == 0:
        return 'None'
    elif hazard <= 0.2:
        return 'Low'
    elif hazard <= 0.5:
        return 'Medium'
    else:
        return 'High'

