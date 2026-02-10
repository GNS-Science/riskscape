# Copyright 2025 The New Zealand Institute for Earth Science Limited (Earth Sciences New Zealand).
# This is Python code is licensed under CC BY-NC 4.0. To view a copy of this license, visit:
#  https://creativecommons.org/licenses/by-nc/4.0/deed.en
#
# Risk function lasted updated on 21/07/2024 by Josh Hayes
#
# Determines the probability of a rail line being in a given Impact State (IS) or higher:
# * IS0: No disruption
# * IS1: Speed reductions, timetable alterations
# * IS2: Closure possible
# * IS3: Closure likely
#
import random

def function(rail, multihazard, seed=None):
    pIS0 = pIS1 = pIS2 = pIS3 = 0.0

    # Extract hazard values from multihazard dictionary
    tephra_hazardValue = multihazard.get('tephra_HIM')
    lahar_hazardValue = multihazard.get('lahar_HIM')
    edifice_hazardValue = multihazard.get('edifice_HIM')
    lava_hazardValue = multihazard.get('lava_HIM')
    PDC_hazardValue = multihazard.get('pdc_HIM')
    crater_hazardValue = multihazard.get('crater_HIM')

    # Tephra impact assessment
    if tephra_hazardValue:

        if tephra_hazardValue >= 306:
            pIS0 = pIS1 = pIS2 = pIS3 = 1

        elif tephra_hazardValue >= 206:
            pIS0 = pIS1 = pIS2 = 1
            pIS3 = 0.003 * tephra_hazardValue + 0.081

        elif tephra_hazardValue >= 57:
            pIS0 = pIS1 = 1
            pIS2 = 0.003 * tephra_hazardValue + 0.381
            pIS3 = 0.003 * tephra_hazardValue + 0.081

        elif tephra_hazardValue >= 7:
            pIS0 = 1
            pIS1 = 0.003 * tephra_hazardValue + 0.831
            pIS2 = 0.003 * tephra_hazardValue + 0.381
            pIS3 = 0.003 * tephra_hazardValue + 0.081

        elif tephra_hazardValue >= 1.75:
            pIS0 = 1
            pIS1 = 0.019 * tephra_hazardValue + 0.717
            pIS2 = 0.038 * tephra_hazardValue + 0.133
            pIS3 = 0.01 * tephra_hazardValue + 0.033

        elif tephra_hazardValue > 0.0:
            pIS0 = 0.571 * tephra_hazardValue
            pIS1 = 0.429 * tephra_hazardValue
            pIS2 = 0.114 * tephra_hazardValue
            pIS3 = 0.029 * tephra_hazardValue

    # Impact assessment for PDC, edifice, lava, lahar, and crater.
    # Based on assumed binary impacts, i.e. impacted if hazard is present
    if (PDC_hazardValue or
        edifice_hazardValue or
        lahar_hazardValue or
        lava_hazardValue or
        crater_hazardValue):
        pIS0 = pIS1 = pIS2 = pIS3 = 1

    # Determine impact state through weighted random choice
    if seed:
        random.seed(seed)
    weights = [1 - pIS1,
               pIS1 - pIS2,
               pIS2 - pIS3,
               pIS3]
    impact_state = random.choices([0,1,2,3], weights=weights)[0]

    # Summarize the outputs for the given rail line and hazard scenario
    return {
        'pIS0': pIS0,
        'pIS1': pIS1,
        'pIS2': pIS2,
        'pIS3': pIS3,
        'impact_state': impact_state
    }
