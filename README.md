#Noticed Bugs
- Occasionally when I have interacted with the app, it gets stuck in a held down state which if not helped will result in an appium crash
  - It is probably due to my interference and am unsure if I can actually prevent this besides just stopping from doing any actions when nothing is happening

#Improvements for current implementation
- detect return screen and tap to close on start
- periodically cleanup images


#Next To Do
- Get chicken run and research to run together

#Priorities of features to do in game
- (DONE) do chicken runs (basic image parse, Appium)
    - Figure out if hatchery is empty and decide whether to continue or not
- farm upgrades (dumb) (basic image parse, Appium)
    - find first set of upgrades that aren't finished. If any are green then click them
- collect gifts (Appium, basic image parse)
- play ads and close them automatically (Accessiblity Service / Appium)
- farm upgrades (smart) (OCR, Appium)
    - Figure out costs of upgrades
    - figure out current money
    - buy upgrades as the money is available
    - weight upgrades by importance
- upgrade farm (basic image parse, Appium)
    - detect when farm is ready to be finished
    - start next farm
- enable auto prestige (OCR?, Appium)
    - figure out metrics to decide when I should prestige
- do artifact missions (OCR, Appium)
- take down the drones :) (?????, Appium)


#Learned items:
- Must have app closed before starting appium client (otherwise app will crash / freeze)
- long_press will continue to press at the location until you press somewhere else (only tried with real phone)
- long_press is synchronous code for the duration given
- ~~disconnect from image size and screen size. (uggghhhhh)~~
  - The problem is actually with the accuracy of driver.get_window_size(). It is not correct. Image coords are source of truth


#Setup Notes:
- Appium must be running on your machine
- Setup notes for the Appium server is [here](https://appium.io/docs/en/about-appium/getting-started/?lang=en) 
