Improvements for current implementation
- detect return screen and tap to close on start
- have chicken run recover if I interact with the app

* Priorities of features to do in game
- do chicken runs (basic image parse, Appium)
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
- do artifact missions (OCR, Appium)
- upgrade farm (basic image parse, Appium)
    - detect when farm is ready to be finished
    - start next farm
- enable auto prestige (OCR?, Appium)
    - figure out metrics to decide when I should prestige
- take down the drones :) (?????, Appium)


Learned items:
- Must have app closed before starting appium client (otherwise app will crash / freeze)
- long_press will continue to press at the location until you press somewhere else (only tried with real phone)
- long_press is synchronous code for the duration given
- disconnect from image size and screen size. (uggghhhhh)



COMING BACK PRIORITY:
- Chicken run  X
    - tap when high percent
    - tap away when low percent
- Research  X
    - Get boxes around individual items
    - know if item is at top
    - scroll item to top
    - tap and hold any item if green
        - holding could have downsides of how it handles stuff, but would speed up if it has many upgrades possible
    - Scroll past top items if they are finished
- Housing   X
    - Rely on base position when loading in
    - Initial guess taps until it opens up
        - Question: How to verify that dialog is for housing?
    - Add new house if able
    - Prioritize new houses over upgrading existing (if possible)
- Shipping   X
    - Rely on base position when loading in
    - Initial guess taps until it opens up
        - Question: How to verify that dialog is for shipping?
    - Add new transportation if able
    - upgrade if able
    - handle when dialog is scrollable
        - Could use drag
        - take screenshot
        - look for lots of grey space
        - if grey space present then you swiped to the end
        - otherwise make reasonable swipes based on items present
- Farm Upgrade  X
    - ALready know egg location
    - Need to occasionally click and see if button is grey or green
    - If green then click
        - Reset any internal state as needed
- Prestige   X
    - Already know egg location
    - Navigate from blue button there
    - When the hell to press?
        - Maybe add a timeout if you have been on the farm too long
            - Will reset the timer in early game if prestige is not an option
        - Keep in mind that the button is not usable early game till you have reached a certain point
- Gifts/Notifications
    - Notice when there is a gift present
    - Need to identify what kind of gift/notification present
    - Need to figure out approach to dismiss all possible dialogs from this.
    - Don't ever watch ads. That is a whole thing

**** BASIC GAME PLAY DONE ***
**** START GAME THEORY IMPROVEMENTS ****

- Create helper setup to allow for multiple bot playthroughs to happen on separate phones at the same time. Allows for testing of multiple strategies at the same time. 

Strategies to improve bot:
- Take those fucking drones down!
    - Will "need" to use ML object detection resnet with pytorch was what I saw
    - Could cause big increase if doable but is random with what it adds
- Do the chicken run even while navigating and doing other stuff in the app.
    - The button is pretty much always visible
    - Would require a lot of fanciness to pull off code wise
- Better choice of Research:
    - Likely includes OCR to know what the upgrades are and what their costs are. 
    - Requires me to understand a lot more of how game calculations work (especially around farm valuation)
    - Optimize choice of cost to researh gain
- Better choice of when to prestige
    - original way is going to be time based. 
    - There has to be a significantly better way to game this out
    - Will probably want the knowledge gamed from better research choice to know when the farm reaches a state of marginal gains.
- Space?????
    - Do I even try to get the bots to understand the spaceship stuff...........
- Artifacts
    - Requires above
    - Do i want to game out which ones are better and when?
- Simulations
    - If i understand all the calculations I can use simulations to find more optimal paths through the game by brute force
        - Requires an understanding of all costs and how all the math works for everything......
        - Could maybe have more rudimentary versions of this


