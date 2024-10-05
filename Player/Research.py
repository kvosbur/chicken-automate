from appiumService import AppiumService
from ImageParser.GetUiComponents import UIComponents, get_middle_from_box
from ImageParser.Research import get_researches, ResearchStateEnum
from ImageParser.ScreenshotHelper import take_screenshot
import time


def do_research_action(appium_service: AppiumService, ui_components):
    # open research menu
    research_button_coords = ui_components[UIComponents.ResearchButton]
    print(research_button_coords)
    appium_service.tap_at_coords(
        research_button_coords[0], research_button_coords[1], 1
    )
    time.sleep(0.5)

    # swipe to good area
    researches = []
    while len(researches) == 0 or researches[0].state == ResearchStateEnum.Finished:
        ti = take_screenshot()
        print("grab researches")
        researches = get_researches(ti)
        # find first non finished research
        target = None
        for research in researches:
            if research.state != ResearchStateEnum.Finished:
                target = research
                break
        if target == None:
            target = researches[-1]

        # swipe to move target to top of screen
        x = target.box[0] + (target.box[2] - target.box[0]) // 2
        appium_service.drag(x, target.box[1] + 20, x, researches[0].box[1] + 20)

        # target not last item so no need to do again
        if target != researches[-1]:
            break

    tap_coords = []
    for research in researches:
        if research.state == ResearchStateEnum.CanUpgrade:
            tap_coords.append(get_middle_from_box(research.upgrade_location))

    appium_service.multi_tap(tap_coords, 4000)
    appium_service.tap_at_coords(
        research_button_coords[0], research_button_coords[1], 1
    )
