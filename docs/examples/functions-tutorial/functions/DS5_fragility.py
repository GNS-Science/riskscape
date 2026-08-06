def function(building, hazard_depth):
    construction = building['Cons_Frame']

    if hazard_depth is None or hazard_depth <= 0:
        return 0.0
    elif construction in ['Masonry', 'Steel']:
        return log_normal_cdf(hazard_depth, mean=0.39, stddev=0.4)
    elif construction in ['Reinforced_Concrete', 'Reinforced Concrete']:
        return log_normal_cdf(hazard_depth, mean=0.86, stddev=0.94)
    else: # 'Timber' or unknown
        return log_normal_cdf(hazard_depth, mean=0.1, stddev=0.28)

def log_normal_cdf(x, mean, stddev):
    # this is the Jython-equivalent of the following CPython code:
    #   scipy.stats.lognorm(s=stddev, scale=math.exp(mean)).cdf(x)
    # but it uses the built-in RiskScape 'lognorm_cdf' function instead of scipy
    return functions.get('lognorm_cdf').call(x, mean, stddev)

