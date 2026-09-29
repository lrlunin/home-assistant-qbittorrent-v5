"""Support for setting qBittorrent transfer speed limits."""
from __future__ import annotations

import logging

from qbittorrentapi import Client

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL, UnitOfDataRate
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import *
from .helpers import get_version, get_speed_limit, set_speed_limit
from urllib.parse import urlparse

_LOGGER = logging.getLogger(__name__)

NUMBER_TYPES: tuple[NumberEntityDescription, ...] = (
    NumberEntityDescription(
        key=NUMBER_TYPE_DOWNLOAD_LIMIT,
        name="download limit",
        icon="mdi:cloud-download",
    ),
    NumberEntityDescription(
        key=NUMBER_TYPE_UPLOAD_LIMIT,
        name="upload limit",
        icon="mdi:cloud-upload",
    ),
    NumberEntityDescription(
        key=NUMBER_TYPE_ALT_DOWNLOAD_LIMIT,
        name="alternative download limit",
        icon="mdi:cloud-download-outline",
    ),
    NumberEntityDescription(
        key=NUMBER_TYPE_ALT_UPLOAD_LIMIT,
        name="alternative upload limit",
        icon="mdi:cloud-upload-outline",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    """Set up qBittorrent number entries."""
    client: Client = hass.data[DOMAIN][config_entry.entry_id]
    qb_version = await hass.async_add_executor_job(get_version, client)

    entities = [
        QBittorrentSpeedLimitNumber(hass, description, config_entry, client, qb_version)
        for description in NUMBER_TYPES
    ]

    async_add_entities(entities, True)


class QBittorrentSpeedLimitNumber(NumberEntity):
    """Representation of a qBittorrent global speed limit."""

    _attr_native_min_value = 0
    _attr_native_max_value = MAX_SPEED_LIMIT_KIBIBYTES
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfDataRate.KIBIBYTES_PER_SECOND
    _attr_mode = NumberMode.BOX

    def __init__(
        self,
        hass,
        description: NumberEntityDescription,
        config_entry: ConfigEntry,
        qbittorrent_client: Client,
        qb_version: str,
    ) -> None:

        """Initialize the qBittorrent speed limit number entity."""
        self.hass = hass
        self.entity_description = description
        self.config_entry = config_entry
        self.client = qbittorrent_client
        self.qb_version = qb_version
        self.preference_key = NUMBER_TYPE_PREFERENCE_KEY[description.key]

        self._attr_unique_id = f"{config_entry.entry_id}-{description.key}"
        self._attr_name = f"{config_entry.title} {description.name}"

    def update(self) -> None:
        """Get the current speed limit from qBittorrent."""
        value = get_speed_limit(self.client, self.preference_key)

        self._attr_available = value is not None
        self._attr_native_value = value

    def set_native_value(self, value: float) -> None:
        """Set a new speed limit on qBittorrent."""
        set_speed_limit(self.client, self.preference_key, int(value))
        self._attr_native_value = value

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
