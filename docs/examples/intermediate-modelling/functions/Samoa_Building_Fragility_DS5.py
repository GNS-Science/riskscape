def function(building, hazard_depth):
    DS_5_Prob = 0.0
    construction = building["Cons_Frame"]

    if hazard_depth is not None and hazard_depth > 0:
        if construction in ['Masonry', 'Steel']:
            DS_5_Prob = log_normal_cdf(hazard_depth, 0.39, 0.4)
        elif construction in ['Reinforced_Concrete', 'Reinforced Concrete']:
            DS_5_Prob = log_normal_cdf(hazard_depth, 0.86, 0.94)
        else: # 'Timber' or unknown
            DS_5_Prob = log_normal_cdf(hazard_depth, 0.1, 0.28)

    return DS_5_Prob

def log_normal_cdf(x, mean, stddev):
    # this uses the built-in RiskScape 'lognorm_cdf' function
    return functions.get('lognorm_cdf').call(x, mean, stddev)

