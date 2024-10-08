from typing import Dict, Tuple
from enum import Enum
from appiumService import AppiumService
from ImageParser.GetUiComponents import get_ui_component_locations, UIComponents
from ImageParser.Dialogs import Dialogs
from Player.DiscoverComponents import (
    discover_component_screen_locations,
    DiscoveredDialog,
)


class UILocations:

    dialogs: Dict[Dialogs, DiscoveredDialog]
    ui_components: Dict[UIComponents, Tuple[int, int]]
    appium_service: AppiumService

    def __init__(self, appium_service: AppiumService):
        self.appium_service = appium_service
        self._get_ui_components()
        self._get_dialog_locations()

    def _get_ui_components(self):
        self.ui_components = get_ui_component_locations()

    def _get_dialog_locations(self):
        self.dialogs = discover_component_screen_locations(
            self.appium_service, self.ui_components
        )
