import numpy as np
from scipy import stats

def function(building, depth):
    if depth is None:
        depth = 0.0
    const_type = building["Constructi"]
    replacement_cost = building["Rep_Cost"]
    storeys = building["Storeys"]

    # Suppasri 2013 fragility curves DS1, DS2, DS3, DS4, DS5, DS6,
    # Table 3. Note masonry and steel are not dependent on storeys. Timber, RC, are dependent on storeys. 
    # Default, Suppasri all heights
    S13 = {'Timber': [-2.1216, 1.2261, -0.9338, 0.9144, -0.040, 0.7276, 0.6721, 0.4985, 0.7825, 0.5559, 1.2094, 0.5247],
           'RC': [-1.9636, 1.0966, -0.9723, 1.0600, 0.1577, 0.7090, 0.9423, 0.7522, 1.9381, 1.0120, 2.8232, 0.9635],
           'Masonry': [-2.113, 1.3362, -1.1573, 1.0400, 0.1059, 0.7693, 0.9043, 0.5746, 1.1918, 0.6821, 1.6583, 0.6913],
           'Steel': [-1.6956, 1.1013, -0.8982, 0.8835, 0.0662, 0.7171, 0.7061, 0.6680, 1.4575, 0.8938, 2.2790, 0.7362]}
    
    # 1 storey
    if storeys == 1:
        S13 = {'Timber': [-1.7268, 1.1462, -0.8580, 0.9395, 0.0481, 0.7115, 0.6872, 0.5288, 0.8134, 0.5941, 1.1733, 0.5756],
           'RC': [-1.8785, 1.1921, -0.82, 1.0585, 0.1590, 0.8196, 0.8881, 0.8391, 1.6578, 0.8948, 2.4155, 0.869],
           'Masonry': [-2.113, 1.3362, -1.1573, 1.0400, 0.1059, 0.7693, 0.9043, 0.5746, 1.1918, 0.6821, 1.6583, 0.6913],
           'Steel': [-1.6956, 1.1013, -0.8982, 0.8835, 0.0662, 0.7171, 0.7061, 0.6680, 1.4575, 0.8938, 2.2790, 0.7362]}
           
    # 2 storey
    if storeys == 2:
        S13 = {'Timber': [-2.008, 1.1873, -0.8747, 0.9053, 0.035, 0.7387, 0.777, 0.5153, 0.9461, 0.5744, 1.3633, 0.471],
           'RC': [-2.2555, 1.2474, -0.9493, 1.0388, 0.1979, 0.745, 0.925, 0.692, 1.7814, 0.7196, 2.4352, 0.662],
           'Masonry': [-2.113, 1.3362, -1.1573, 1.0400, 0.1059, 0.7693, 0.9043, 0.5746, 1.1918, 0.6821, 1.6583, 0.6913],
           'Steel': [-1.6956, 1.1013, -0.8982, 0.8835, 0.0662, 0.7171, 0.7061, 0.6680, 1.4575, 0.8938, 2.2790, 0.7362]}
           
    # 3 storey
    if storeys > 2: 
            S13 = {'Timber': [-2.1900, 1.3198, -0.8617, 1.224, 0.1137, 0.844, 0.7977, 0.4734, 1.2658, 0.6242, 1.7702, 0.3711],
           'RC': [-2.7757, 1.6594, -0.9784, 1.022, 0.1489, 0.66, 1.1408, 0.7981, 2.3491, 0.7898, 2.7121, 0.4966],
           'Masonry': [-2.113, 1.3362, -1.1573, 1.0400, 0.1059, 0.7693, 0.9043, 0.5746, 1.1918, 0.6821, 1.6583, 0.6913],
           'Steel': [-1.6956, 1.1013, -0.8982, 0.8835, 0.0662, 0.7171, 0.7061, 0.6680, 1.4575, 0.8938, 2.2790, 0.7362]}

    # assign default if material type not in Suppasri options (RC, Timber, Steel, Masonry)
    material = 'Timber'

    if const_type in ['Steel Braced Frame', 'Steel Moment Resisting Frame']:
        material = 'Steel'
	
    if const_type in ['Brick Masonry', 'Concrete Masonry']:
        material = 'Masonry'
	
    if const_type in ['Reinforced Concrete Moment Resisting Frame', 'Reinforced Concrete Shear Wall', 'Industrial', 'Tilt Up Panel']:
        material = 'RC'


    # get dictionary of damage state params for this building
    damagestates = {
            'DS1':    {'median': S13[material][0], 'beta': S13[material][1]},
            'DS2':  {'median': S13[material][2], 'beta': S13[material][3]},
            'DS3': {'median': S13[material][4], 'beta': S13[material][5]},
            'DS4':  {'median': S13[material][6], 'beta': S13[material][7]},
            'DS5':  {'median': S13[material][8], 'beta': S13[material][9]},
            'DS6':  {'median': S13[material][10], 'beta': S13[material][11]}
        }

    # DR for each DS
    drs = { 'DS1': 0.01,
            'DS2': 0.2,
            'DS3': 0.5,
            'DS4': 0.9,
            'DS5': 1,
            'DS6': 1}


    result = {}
    accumulated_prob = 0
    accumulated_dr = 0

    for state in list(reversed(damagestates.keys())):

        median = damagestates[state]['median']
        beta = damagestates[state]['beta']

        prob = stats.lognorm(s=beta, scale=np.exp(median)).cdf(depth) - accumulated_prob
        result[state] = prob
        accumulated_prob += prob

        # weighted damage ratio
        wdr = prob * drs[state]
        accumulated_dr += wdr
        accumulated_dr = round(accumulated_dr, 3)
        result['DR'] = accumulated_dr

    
    result['Loss'] = accumulated_dr * replacement_cost

    return result

