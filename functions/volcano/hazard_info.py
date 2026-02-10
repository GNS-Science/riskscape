MULTIHAZARD_ATTRIBUTES = {
    'tephra_HIM': 'Tephra',
    'lahar_HIM': 'Lahar',
    'edifice_HIM': 'Edifice',
    'lava_HIM': 'Lava',
    'pdc_HIM': 'PDC',
    'crater_HIM': 'Crater'
}

def function(multihazard):
    present = []
    hazards = []
    missing = []
    spurious = []

    for attribute in multihazard.keys():
        if attribute in MULTIHAZARD_ATTRIBUTES.keys():
            present.append(attribute)
        else:
            spurious.append(attribute)

    # work out what attributes are present through and what's missing
    for attribute, hazard in MULTIHAZARD_ATTRIBUTES.items():
        if attribute in present:
            # convert to 'nice' hazard name
            hazards.append(hazard)
        else:
            missing.append(attribute)

    return {
        'hazards': hazards,
        'missing_attributes': missing,
        'spurious_attributes': spurious
    }

