# Note: this function was provided by Earth Sciences New Zealand https://earthsciences.nz and has been
# refactored and adapted for this tutorial.

def function(building, hazard_depth):
    DS_1_Prob = 0.0
    DS_2_Prob = 0.0
    DS_3_Prob = 0.0
    DS_4_Prob = 0.0
    DS_5_Prob = 0.0
    construction = building["Cons_Frame"]

    if hazard_depth is not None and hazard_depth > 0:
        DS_1_Prob = log_normal_cdf(hazard_depth, -0.53, 0.46)        
    
        if construction in ['Masonry', 'Steel']:
            DS_2_Prob = log_normal_cdf(hazard_depth, -0.33, 0.4)
            DS_3_Prob = log_normal_cdf(hazard_depth, 0.1, 0.35)
            DS_4_Prob = log_normal_cdf(hazard_depth, 0.26, 0.41)
            DS_5_Prob = log_normal_cdf(hazard_depth, 0.39, 0.4)
        elif construction in ['Reinforced_Concrete', 'Reinforced Concrete']:
            DS_2_Prob = log_normal_cdf(hazard_depth, -0.33, 0.4)
            DS_3_Prob = log_normal_cdf(hazard_depth, 0.13, 0.56)
            DS_4_Prob = log_normal_cdf(hazard_depth, 0.53, 0.54)
            DS_5_Prob = log_normal_cdf(hazard_depth, 0.86, 0.94)
        else: # 'Timber' or unknown
            DS_2_Prob = log_normal_cdf(hazard_depth, -0.33, 0.4)
            DS_3_Prob = log_normal_cdf(hazard_depth, 0.06, 0.38)
            DS_4_Prob = log_normal_cdf(hazard_depth, 0.1, 0.4)
            DS_5_Prob = log_normal_cdf(hazard_depth, 0.1, 0.28)

    result = {}
    result['DS_1'] = DS_1_Prob
    result['DS_2'] = DS_2_Prob
    result['DS_3'] = DS_3_Prob
    result['DS_4'] = DS_4_Prob
    result['DS_5'] = DS_5_Prob
    return result

def log_normal_cdf(x, mean, stddev):
    # this uses the built-in RiskScape 'lognorm_cdf' function
    return functions.get('lognorm_cdf').call(x, mean, stddev)
