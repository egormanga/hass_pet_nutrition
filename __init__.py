from homeassistant.const import CONF_DEVICE_ID, Platform
from homeassistant.helpers.device import async_remove_stale_devices_links_keep_current_device


PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass, entry) -> bool:
    async_remove_stale_devices_links_keep_current_device(hass, entry.entry_id, entry.options.get(CONF_DEVICE_ID))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(config_entry_update_listener))

    return True


async def config_entry_update_listener(hass, entry):
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass, entry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
