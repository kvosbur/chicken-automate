import os
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time
from typing import List

# https://stackoverflow.com/questions/4032960/how-do-i-get-an-apk-file-from-an-android-device
# adb shell pm list packages
# adb shell pm path com.auxbrain.egginc
# adb pull /data/app/~~tweXlYiQgWJQJgvXJMtepw==/com.auxbrain.egginc-FWJI9t5kEQOcevIqVQZziA==/base.apk ./eggInc.apk
# https://stackoverflow.com/questions/12698814/get-launchable-activity-name-of-package-from-adb
# /Users/kvosburgh_mac/Library/Android/sdk/build-tools/31.0.0/aapt dump configurations eggInc.apk
# alternative below
# adb shell pm dump com.auxbrain.egginc | grep -A 1 MAIN

# get screenshot: adb exec-out screencap -p > screen.png


ANDROID_BASE_CAPS = {
    # 'app': os.path.abspath('../apps/ApiDemos-debug.apk'),
    'automationName': 'UiAutomator2',
    'platformName': 'Android',
    'platformVersion': os.getenv('ANDROID_PLATFORM_VERSION') or '12.0',
    # 'deviceName': os.getenv('ANDROID_DEVICE_VERSION') or 'Android Emulator',
    'name': 'test-session',
    'appPackage': 'com.auxbrain.egginc',
    'app': os.path.join(os.path.dirname(__file__), "eggInc.apk"),
    'udid': 'RFCT70B6C8P',
    'appActivity': 'com.auxbrain.egginc.EggIncActivity',
    'newCommandTimeout': 600,
    'noReset': True,
    'fullReset': False,
    'dontStopAppOnReset': True,
    'autoLaunch': True,
    'skipLogcatCapture': True
}

EXECUTOR = 'http://127.0.0.1:4723/wd/hub'

class AppiumService:

    def __init__(self) -> None:
        self.driver = webdriver.Remote(
            command_executor=EXECUTOR,
            desired_capabilities=ANDROID_BASE_CAPS
        )
        print("done initializing")

    # Note that press_for_time is in milli-seconds
    def long_press_at_coords(self, x, y, press_for_time):
        print("do touch", x, y, self.driver.get_window_size())
        action = TouchAction(self.driver)
        action.long_press(x=x, y=y, duration=press_for_time)
        action.perform()
        # print("after touch")

    def tap_at_coords(self, x, y, count=1):
        print("do tap", x, y, self.driver.get_window_size())
        action = TouchAction(self.driver)
        action.tap(x=x, y=y, count=count)
        action.perform()

    def drag_from_to(self, from_coords, to_coords):
        action = TouchAction(self.driver)
        action.press(x=from_coords[0], y=from_coords[1])
        action.move_to(x=to_coords[0], y=to_coords[1])
        action.release()
        action.perform()

    def meaningless_tap(self):
        self.tap_at_coords(0, 0, 1)

    def get_page_source(self) -> str:
        return self.driver.page_source

    def cleanup(self):
        self.driver.close_app()

if __name__ == "__main__":
    service = AppiumService()
    # driver.start_activity(ANDROID_BASE_CAPS['appPackage'], ANDROID_BASE_CAPS["appActivity"])
    for i in range(100):
        time.sleep(5)
        print("\n\n\n\n BLARG", i)
        print(service.get_page_source())


    service.cleanup()
    # time.sleep(10000)