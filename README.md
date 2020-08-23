# emotion-recognition-test
This is an emotion recognition testing tool I designed for my undergraduate dissertation, using Pygame. It's fully customisable (see the 'how can I customise this?' secction), so you can change the number of emotions, emotion types and stimuli presentation times to suit your needs.

## How does it work?
It works like a multiple choice quiz. A face displaying a certain emotion is presented for x amount of seconds. The user is then given the opportunity to select from a range of buttons corresponding to different emotions. Their answer is then stored in a list. Once y number of faces have been presented, the quiz finishes and the user's results (their answer, the emotion displayed and the image title) are saved to a CSV file in a directory of your choice, entitled the participant ID number (which you will be prompted to enter at the beginning).

## How do you get it to work on your computer?
There are a few things you must do first in order to ensure this program will run on your own computer, these are:
1. Ensure you have two folders, one containing images for the "practice" condition (this allows users to familiarise themselves with the methodology - these answers are not stored) and one containing images for the "main" condition.
2. Ensure every image in this folder has a name which includes the emotion type, for example "manangry" or "womanafraid". I used a naming convention such as "man04angry30" with the first number representing the actor and the second number displaying the emotion intensity as a percentage. You're free to use whatever naming convention you want, as long as you have the correct emotion in the image name (this is not case sensitive).
3. Change the 'noQuestions' and 'noPracticeQuestions' to the number of main questions and practice questions you want, respectively. Ensure you have enough images to cover the question numbers.
4. Change the following directories:
BASE_DIRECTORY to the directory in which you want the final results CSV file to be stored in
IMAGE_DIRECTORY to the directory in which your main condition images are stored
PRACTICE_IMAGE_DIRECTORY to the directory in which your practice condition images are stored
5. By default, the experiment will only work with "happy", "sad", "neutral", "angry" and "afraid" emotions. To change this, modify the "emotionTypes" list. Feel free to add more emotion types, remove emotion types or modify the emotion types in this list. The buttons presented in the experiment will be automatically updated to account for any changes you make.

After making these changes, the experiment should run on your computer. However, there are further customisations you can make if you wish to tinker a little more:

## How can you customise the experiment?
1. If you wish to change the colours for the buttons, you can do so by changing the RGB values for "buttonNormalColour" and "buttonHoverColour" (for the normal colour of the buttons and the colour when the cursor is hovering over them, respectively)
2. If you wish to change the display time for the stimuli, you can change the variable displayTime. By default, this is set to 1000ms.
3. If you want to change the size of the screen, change "displayWidth"
4. Modify the arguments passed to the "instructions" function, which is called three times towards the bottom of the code. The first instruction screen is designed to explain the experiment to users and inform them that the first condition is a practice condition. The second instruction screen is designed to inform them that the practice condition is now over and the final instruction screen is designed to say "thanks for participating". Feel free to modify the text presented on these screens as you see fit. 


I hope you find some use with this experiment. If you encounter any issues, please let me know and I'll do my best to fix them.
