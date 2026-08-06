from scipy.stats import lognorm
import math

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
    return lognorm(s=stddev, scale=math.exp(mean)).cdf(x)
    

# this part just lets us test our function manually
if __name__ == '__main__':
    result = function({'Cons_Frame': 'Timber'}, 1.1)
    print('building=Timber, hazard=1.1, result=%f' % result)
    result = function({'Cons_Frame': 'Masonry'}, 1.1)
    print('building=Masonry, hazard=1.1, result=%f' % result)
    result = function({'Cons_Frame': 'Reinforced Concrete'}, 1.1)
    print('building=Reinforced Concrete, hazard=1.1, result=%f' % result)
