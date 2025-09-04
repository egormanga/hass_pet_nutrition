DOMAIN = 'pet_nutrition'

CONF_PET_CONDITION = 'pet_condition'
CONF_PET_TYPE = 'pet_type'
CONF_PET_WEIGHT_ENTITY = 'pet_weight_entity'

PET_TYPES = (
    'cat',
    'dog',
)

PET_CONDITIONS = (
    'intact',
    'neutered',
    'growing',
    'inactive',
    'obese',
    'gestating',
    'lactating',
    'critical',
    'light_working',
    'heavy_working',
)

MER_FACTORS = {
    'intact': {
        'cat': 1.4,
        'dog': 1.8,
    },
    'neutered': {
        'cat': 1.2,
        'dog': 1.6,
    },
    'growing': 2.5,  # 2–3
    'inactive': {
        'cat': 1.0,
        'dog': 1.3,  # 1.2–1.4
    },
    'obese': {
        'cat': 0.9,  # 0.8–1.0
        'dog': 1.0,
    },
    'gestating': {
        'cat': 2.5,  # 2–3
        'dog': 1.8,  # 1.6–2.0
    },
    'lactating': 4,  # 2-6
    'critical': 1.0,
    'light_working': {
        'dog': 2.0,
    },
    'heavy_working': {
        'dog': 6.0,  # 4–8
    },
}
