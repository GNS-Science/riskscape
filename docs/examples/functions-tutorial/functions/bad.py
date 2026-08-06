def function(building, hazard):
    construction = building['Construction']

    if hazard is None or hazard <= 0 or construction != 'timber':
        return 0
    else:
        return 1
