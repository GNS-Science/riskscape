# Note: this function was provided by Earth Sciences New Zealand https://earthsciences.nz and has been
# refactored and adapted for this tutorial.

def function(building, hazard_depth):
    result = { 'DS_1': 0.0, 'DS_2': 0.0, 'DS_3': 0.0, 'DS_4': 0.0, 'DS_5': 0.0 }
    construction = building["Cons_Frame"]

    if hazard_depth is None or hazard_depth <= 0:
        return result

    result['DS_1'] = log_normal_cdf(hazard_depth, -0.53, 0.46)        
    
    if construction in ['Masonry', 'Steel']:
        result['DS_2'] = log_normal_cdf(hazard_depth, -0.33, 0.4)
        result['DS_3'] = log_normal_cdf(hazard_depth, 0.1, 0.35)
        result['DS_4'] = log_normal_cdf(hazard_depth, 0.26, 0.41)
        result['DS_5'] = log_normal_cdf(hazard_depth, 0.39, 0.4)
    elif construction in ['Reinforced_Concrete', 'Reinforced Concrete']:
        result['DS_2'] = log_normal_cdf(hazard_depth, -0.33, 0.4)
        result['DS_3'] = log_normal_cdf(hazard_depth, 0.13, 0.56)
        result['DS_4'] = log_normal_cdf(hazard_depth, 0.53, 0.54)
        result['DS_5'] = log_normal_cdf(hazard_depth, 0.86, 0.94)
    else: # 'Timber' or unknown
        result['DS_2'] = log_normal_cdf(hazard_depth, -0.33, 0.4)
        result['DS_3'] = log_normal_cdf(hazard_depth, 0.06, 0.38)
        result['DS_4'] = log_normal_cdf(hazard_depth, 0.1, 0.4)
        result['DS_5'] = log_normal_cdf(hazard_depth, 0.1, 0.28)

    return result

def log_normal_cdf(x, mean, stddev):
    # this uses the built-in RiskScape 'lognorm_cdf' function
    return functions.get('lognorm_cdf').call(x, mean, stddev)
