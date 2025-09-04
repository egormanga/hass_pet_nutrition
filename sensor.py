import voluptuous as vol

from homeassistant.components import sensor
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import (
    CONF_NAME,
    CONF_UNIQUE_ID,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    UnitOfEnergy,
)
from homeassistant.core import Event, EventStateChangedData, callback
from homeassistant.helpers import (
    config_validation as cv,
    entity_registry as er,
)
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.reload import async_setup_reload_service

from . import PLATFORMS
from .const import (
    CONF_PET_CONDITION,
    CONF_PET_TYPE,
    CONF_PET_WEIGHT_ENTITY,
    DOMAIN,
    MER_FACTORS,
    PET_CONDITIONS,
    PET_TYPES,
)


PLATFORM_SCHEMA = sensor.PLATFORM_SCHEMA.extend({
    vol.Required(CONF_UNIQUE_ID): cv.string,
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_PET_WEIGHT_ENTITY): cv.entity_id,
    vol.Required(CONF_PET_TYPE): vol.All(
        cv.string,
        vol.In(PET_TYPES),
    ),
    vol.Required(CONF_PET_CONDITION): vol.All(
        cv.string,
        vol.In(PET_CONDITIONS),
    ),
})


def _create_sensor(hass, unique_id, config):
    registry = er.async_get(hass)
    pet_weight_entity = er.async_validate_entity_id(registry, config[CONF_PET_WEIGHT_ENTITY])

    return PetNutritionSensor(
        unique_id=unique_id,
        name=config[CONF_NAME],
        pet_weight_entity=pet_weight_entity,
        pet_type=config[CONF_PET_TYPE],
        pet_condition=config[CONF_PET_CONDITION],
    )


async def async_setup_entry(hass, config_entry, async_add_entities):
    sensor = _create_sensor(hass, config_entry.entry_id, config_entry.options)
    async_add_entities((sensor,))


async def async_setup_platform(hass, config, async_add_entities, discovery_info):
    sensor = _create_sensor(hass, config[CONF_UNIQUE_ID], config)
    await async_setup_reload_service(hass, DOMAIN, PLATFORMS)
    async_add_entities((sensor,))


class PetNutritionSensor(SensorEntity):
    _attr_translation_key = 'daily_energy_requirement'
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_CALORIE
    _attr_suggested_display_precision = 0
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, unique_id, name, *, pet_weight_entity, pet_type, pet_condition):
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._pet_weight_entity = pet_weight_entity
        self._pet_type = pet_type
        self._pet_condition = pet_condition

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_track_state_change_event(self.hass, self._pet_weight_entity, self._weight_updated)
        )

        self._update(pet_weight=self.hass.states.get(self._pet_weight_entity).state, initial=True)

    @callback
    def _weight_updated(self, event: Event[EventStateChangedData]):
        pet_weight = event.data['new_state']
        self._update(pet_weight=(pet_weight and pet_weight.state))

    def _update(self, pet_weight, *, initial=False):
        self._attr_native_value = None

        if pet_weight not in (None, STATE_UNKNOWN, STATE_UNAVAILABLE):
            factor = MER_FACTORS[self._pet_condition]
            if isinstance(factor, dict): factor = factor[self._pet_type]

            self._attr_native_value = self.calculate_mer(
                bw=float(pet_weight),
                k=factor,
            )

        if not initial: self.async_write_ha_state()

    @staticmethod
    def calculate_mer(bw, k):
        """ Based on: https://petnutritionalliance.org/wp-content/uploads/2023/03/MER.RER_.PNA_.pdf """

        rer = (70 * bw**0.75)
        mer = (rer * k)

        return mer
