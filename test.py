import os
from appium import webdriver
import time

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
    'deviceName': os.getenv('ANDROID_DEVICE_VERSION') or 'Android Emulator',
    'name': 'test-session',
    'appPackage': 'com.auxbrain.egginc',
    'app': '/Users/kvosburgh_mac/Desktop/Personal Projects/chicken-optim/eggInc.apk',
    'udid': 'RFCT70B6C8P',
    'appActivity': 'com.auxbrain.egginc.EggIncActivity',
    'newCommandTimeout': 600,
    'noReset': True,
    'fullReset': False,
    'dontStopAppOnReset': True,
    'autoLaunch': True
}

EXECUTOR = 'http://127.0.0.1:4723/wd/hub'

driver = webdriver.Remote(
            command_executor=EXECUTOR,
            desired_capabilities=ANDROID_BASE_CAPS
        )

print(driver.get_window_size())

# driver.start_activity(ANDROID_BASE_CAPS['appPackage'], ANDROID_BASE_CAPS["appActivity"])
for i in range(100):
    time.sleep(5)
    print("\n\n\n\n BLARG", i)
    print(driver.page_source)


driver.close_app()
# time.sleep(10000)