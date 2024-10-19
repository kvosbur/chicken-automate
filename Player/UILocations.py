from typing import Dict, Tuple, List
from enum import Enum
from appiumService import AppiumService
from ImageParser.GetUiComponents import get_ui_component_locations, UIComponents
from ImageParser.Dialogs import Dialogs
from Player.DiscoverComponents import (
    discover_component_screen_locations,
    DiscoveredDialog,
)
import os
import json

cache_file_location = os.path.join("Player", "location_cache.json")


class UILocations:

    dialogs: Dict[Dialogs, DiscoveredDialog] = None
    ui_components: Dict[UIComponents, Tuple[int, int]] = None
    tapped_locations: List[Tuple[int, int]] = None
    appium_service: AppiumService = None

    def __init__(self, appium_service: AppiumService):
        self.appium_service = appium_service
        self._load_from_cache()
        if self.ui_components is None:
            self._get_ui_components()
        if self.dialogs is None:
            self._get_dialog_locations()

    def has_tapped_at_location(self, coords: Tuple[int, int]):
        for tapped in self.tapped_locations:
            if tapped[0] == coords[0] and tapped[1] == coords[1]:
                return True
        return False

    def add_tapped_location(self, coords: Tuple[int, int]):
        self.tapped_locations.append(coords)
        self._save_to_cache()

    def add_discovered_dialog(self, dialog: DiscoveredDialog):
        self.dialogs[dialog.name] = dialog
        self._save_to_cache()

    def _load_from_cache(self):
        if not os.path.exists(cache_file_location):
            return
        try:
            with open(cache_file_location, "r") as f:
                cached = json.load(f)
                if "ui_components" in cached:
                    self.ui_components = {
                        UIComponents[key]: value
                        for key, value in cached["ui_components"].items()
                    }
                if "dialogs" in cached:
                    self.dialogs = cached["dialogs"]
                if "tapped_locations" in cached:
                    self.tapped_locations = cached["tapped_locations"]
        except:
            pass

    def _save_to_cache(self):
        with open(cache_file_location, "w") as f:
            cache = {
                "ui_components": {
                    key.value: value for key, value in self.ui_components.items()
                },
                "dialogs": self.dialogs,
                "tapped_locations": self.tapped_locations,
            }
            json.dump(cache, f)

    def _get_ui_components(self):
        print("get ui component locations")
        self.ui_components = get_ui_component_locations()
        self._save_to_cache()

    def _get_dialog_locations(self):
        if self.tapped_locations is None:
            self.tapped_locations = []
        print("get dialog locations")
        self.dialogs = discover_component_screen_locations(
            self.appium_service, self.ui_components
        )
        self._save_to_cache()
