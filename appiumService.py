import os
from appium import webdriver

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from appium.options.android import UiAutomator2Options
import time

# https://stackoverflow.com/questions/4032960/how-do-i-get-an-apk-file-from-an-android-device
# adb shell pm list packages
# adb shell pm path com.auxbrain.egginc
# adb pull /data/app/~~Ma7I8LwTM5i6QkuRo7t-GQ==/com.auxbrain.egginc-XFV6VdyPInA9M0rQ4UyD0g==/base.apk ./eggInc.apk
# https://stackoverflow.com/questions/12698814/get-launchable-activity-name-of-package-from-adb
# /Users/kvosburgh_mac/Library/Android/sdk/build-tools/31.0.0/aapt dump configurations eggInc.apk
# alternative below
# adb shell pm dump com.auxbrain.egginc | grep -A 1 MAIN
# adb shell am force-stop com.auxbrain.egginc && adb shell pm clear com.auxbrain.egginc
# scrcpy --turn-screen-off --stay-awake --no-audio --record=file.mp4 --print-fps --no-control
# Not good for debugging, but final: scrcpy --turn-screen-off --stay-awake --no-audio --record=file.mp4 --no-window --no-control

# get screenshot: adb exec-out screencap -p > screen.png


ANDROID_BASE_CAPS = {
    # 'app': os.path.abspath('../apps/ApiDemos-debug.apk'),
    "automationName": "UiAutomator2",
    "platformName": "Android",
    "platformVersion": os.getenv("ANDROID_PLATFORM_VERSION") or "12.0",
    # 'deviceName': os.getenv('ANDROID_DEVICE_VERSION') or 'Android Emulator',
    # "name": "test-session",
    "appPackage": "com.auxbrain.egginc",
    # "app": "/Users/kvosburgh_mac/Desktop/Personal Projects/chicken-optim/eggInc.apk",
    # "udid": "RFCT70B6C8P", # personal device
    "udid": "R58MB1C5NGW",  # test device
    "appActivity": "com.auxbrain.egginc.EggIncActivity",
    "newCommandTimeout": 600,
    "noReset": True,
    "fullReset": False,
    "dontStopAppOnReset": True,
    "autoLaunch": True,
    "skipLogcatCapture": True,
}

EXECUTOR = "http://127.0.0.1:4723"
# EXECUTOR = "http://127.0.0.1:4723/wd/hub"


class AppiumService:

    def __init__(self) -> None:
        options = UiAutomator2Options()
        options.load_capabilities(ANDROID_BASE_CAPS)
        # self.driver = webdriver.Remote(
        #     command_executor=EXECUTOR, desired_capabilities=ANDROID_BASE_CAPS
        # )
        self.driver = webdriver.Remote(command_executor=EXECUTOR, options=options)
        print("done initializing")

    # Note that press_for_time is in milli-seconds
    def long_press_at_coords(self, x, y, press_for_time):
        print("do touch")

        action = TouchAction(self.driver)
        action.long_press(x=x, y=y, duration=press_for_time)
        action.perform()
        print("after touch")

    def tap_at_coords(self, x, y, count):
        print("do tap", x, y)
        self.multi_tap([[x, y]], 0.1)
        # action = TouchAction(self.driver)
        # action.tap(x=x, y=y, count=count)
        # action.perform()

    def multi_tap(self, coordinates, duration):
        # action = MultiAction(self.driver)
        print("multi tap", coordinates)
        self.driver.tap(coordinates, duration)

    def drag(self, start_x, start_y, end_x, end_y):
        action = TouchAction(self.driver)
        print("drag from", start_x, start_y, "to:", end_x, end_y)
        action.press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).release()
        action.perform()

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
