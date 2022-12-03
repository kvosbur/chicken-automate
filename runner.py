from Player.cycle import run_player, run_test
from appiumService import AppiumService

appium_service = AppiumService()
run_player(appium_service)
# run_test(appium_service)