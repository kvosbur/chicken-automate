#Improvements for current implementation
- detect return screen and tap to close on start

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
- disconnect from image size and screen size. (uggghhhhh)


#Setup Notes:
- Appium must be running on your machine
- Setup notes for the Appium server is [here](https://appium.io/docs/en/about-appium/getting-started/?lang=en) 
