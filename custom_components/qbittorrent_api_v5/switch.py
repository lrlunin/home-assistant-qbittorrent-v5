"""Support for toggling qBittorrent's alternative speed limits."""
from __future__ import annotations

import logging

from qbittorrentapi import Client

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import *
from .helpers import (
    get_version,
    get_alternative_speed_limits_enabled,
    set_alternative_speed_limits_enabled,
)
from urllib.parse import urlparse

_LOGGER = logging.getLogger(__name__)

SWITCH_TYPES: tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key=SWITCH_TYPE_ALTERNATIVE_SPEED_LIMITS,
        name="alternative speed limits",
        icon="mdi:speedometer-slow",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    """Set up qBittorrent switch entries."""
    client: Client = hass.data[DOMAIN][config_entry.entry_id]
    qb_version = await hass.async_add_executor_job(get_version, client)

    entities = [
        QBittorrentAlternativeSpeedLimitsSwitch(hass, description, config_entry, client, qb_version)
        for description in SWITCH_TYPES
    ]

    async_add_entities(entities, True)


class QBittorrentAlternativeSpeedLimitsSwitch(SwitchEntity):
    """Representation of qBittorrent's alternative speed limits toggle."""

    def __init__(
        self,
        hass,
        description: SwitchEntityDescription,
        config_entry: ConfigEntry,
        qbittorrent_client: Client,
        qb_version: str,
    ) -> None:

        """Initialize the qBittorrent alternative speed limits switch."""
        self.hass = hass
        self.entity_description = description
        self.config_entry = config_entry
        self.client = qbittorrent_client
        self.qb_version = qb_version

        self._attr_unique_id = f"{config_entry.entry_id}-{description.key}"
        self._attr_name = f"{config_entry.title} {description.name}"

    def update(self) -> None:
        """Get the current alternative speed limits state from qBittorrent."""
        value = get_alternative_speed_limits_enabled(self.client)

        self._attr_available = value is not None
        self._attr_is_on = value

    def turn_on(self, **kwargs) -> None:
        """Enable alternative speed limits."""
        set_alternative_speed_limits_enabled(self.client, True)
        self._attr_is_on = True

    def turn_off(self, **kwargs) -> None:
        """Disable alternative speed limits."""
        set_alternative_speed_limits_enabled(self.client, False)
        self._attr_is_on = False

    @property
    def device_info(self):
        """Return device info for this entity."""
        return {
            "identifiers": {(DOMAIN, urlparse(self.config_entry.data[CONF_URL]).hostname)},
            "name": f"qBittorrent - {urlparse(self.config_entry.data[CONF_URL]).hostname}",
            "manufacturer": "The qBittorrent project",
            "model": self.qb_version,
            "configuration_url": self.config_entry.data[CONF_URL],
        }
