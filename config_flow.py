import voluptuous as vol

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import CONF_DEVICE_ID, CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from .const import (
    CONF_PET_CONDITION,
    CONF_PET_TYPE,
    CONF_PET_WEIGHT_ENTITY,
    DOMAIN,
    PET_CONDITIONS,
    PET_TYPES,
)


OPTIONS_SCHEMA = vol.Schema({
    vol.Required(CONF_PET_WEIGHT_ENTITY): selector.EntitySelector(selector.EntitySelectorConfig(
        device_class=SensorDeviceClass.WEIGHT,
    )),
    vol.Required(CONF_PET_TYPE): selector.SelectSelector(selector.SelectSelectorConfig(
        options=list(PET_TYPES),
        translation_key=CONF_PET_TYPE,
    )),
    vol.Required(CONF_PET_CONDITION): selector.SelectSelector(selector.SelectSelectorConfig(
        options=list(PET_CONDITIONS),
        translation_key=CONF_PET_CONDITION,
    )),
    vol.Optional(CONF_DEVICE_ID): selector.DeviceSelector(),
})

CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): selector.TextSelector(),
}).extend(OPTIONS_SCHEMA.schema)

CONFIG_FLOW = {
    'user': SchemaFlowFormStep(CONFIG_SCHEMA),
}

OPTIONS_FLOW = {
    'init': SchemaFlowFormStep(OPTIONS_SCHEMA),
}


class PetNutritionFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    @callback
    def async_config_entry_title(self, options) -> str:
        return options['name']
