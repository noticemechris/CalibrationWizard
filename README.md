# CalibrationWizard
[Jared tells me to start with "Hi David"]
Hi David. Welcome to the official readme for Adam Goodman's Etch-A-Sketch Laser Cutter calibration app. Although I could make this a long description of my app and senior project, Jared tells me there is a difference between what David COULD read and what David WANTS TO read. Without more to do, let's get into it.

The objectives of this app are as follows:

1. Greet the user when they open the app, and prompt them to connect via bluetooth to the Raspberry Pi controlling the laser cutter. I will use the following code for setting this up with an intent: http://blog.davidvassallo.me/2014/05/11/android-linux-raspberry-pi-bluetooth-communication/
2. Prompt the user to place their preferred medium of engraving onto the 3D printer bed, and secure it. Once this is complete, the app will send a command to the laser cutter to "home" itself and use sensors to find out how far to place the laser above the engraving medium. This is a long process, but it will written onto the Raspberry Pi so I don't feel obligated to explain it here.
3. Prompt the user to set the locations of each corner of the medium. I have an idea for how this will work, you'll kind of see it in the skeleton code.
4. Once calibrated, the app will allow the user to turn or adjust the intensity of the laser on a scale of 1-255. I forget the name for this is called instrumentation-wise but you get the idea. It will also allow the user to re-home and re-calibrate the cutter if the cutting medium is shifted or replaced, and toggle between being "on" and the lowest possible setting (so they can see where the laser is pointing but not do anything else) if the user wants to move the head without engraving anything.
5. I find it imperative that this app is ONLY in light theme. This is because the user will be wearing laser safety glasses (basically sunglasses) whilst operating it, and catastrophe may strike if it's a dark background with skinny, white text.
