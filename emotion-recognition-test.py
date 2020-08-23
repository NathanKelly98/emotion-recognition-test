import pygame
import os
import random
import time
from enum import Enum
import csv
import sys
import pathlib

#Modify button colours if you wish (RGB)
buttonNormalColour = (20, 40, 170)
buttonHoverColour = (19, 47, 230)

#Directories - modify to point to your own directories
BASE_DIRECTORY = pathlib.Path("C:/Python 3.8/Projects/Emotion Recognition Test")
IMAGE_DIRECTORY = pathlib.Path("C:/Python 3.8/Projects/Emotion Recognition Test/All images")
PRACTICE_IMAGE_DIRECTORY = pathlib.Path("C:/Python 3.8/Projects/Emotion Recognition Test/Practice images")

#Image display time in ms - modify if you wish to display face for more/less time
displayTime = 1000

#Modify number of questions to display more/less faces in total
noQuestions = 4
noPracticeQuestions = 4

#All emotion types, modify if you wish to use different emotions
emotionTypes = ["Happy", "Sad", "Neutral", "Afraid", "Angry"]

displayWidth = 1200
displayHeight = 800

rectDict = {}
#This populates rectDict with button positions based on no. of emotions in emotionTypes
startPos = 0
for emotion in emotionTypes:
	rectDict[emotion] = pygame.Rect(startPos, 700, (displayWidth/len(emotionTypes) - 50), 100)
	startPos += (displayWidth/len(emotionTypes))

rectList = list(rectDict.values())

#Define class to keep track of states
class States(Enum):
    VIEWING = 1
    ANSWERING = 2

def displayImage(images, imageNumber):
    """Displays image to centre of screen"""
    imageWidth, imageHeight = images[imageNumber].get_size()
    xCoord = (displayWidth/2) - (imageWidth/2)
    yCoord = (displayHeight/2) - (imageHeight/2)
    screen.blit(images[imageNumber], ((xCoord, yCoord)))

def displayText(someText, xpos, ypos):
    font = pygame.font.SysFont('Arial', 22)
    text = font.render(someText, True, (0, 0, 0))
    text_rect = text.get_rect(center=(xpos, ypos))
    screen.blit(text, text_rect)

def displayButtons():
    """This function uses rectDict to create buttons for every emotion in emotionTypes"""
    mouse = pygame.mouse.get_pos()
    for name, rect in rectDict.items():
        if rect.collidepoint(mouse):
            pygame.draw.rect(screen, buttonHoverColour, (rect))
        else:
            pygame.draw.rect(screen, buttonNormalColour, (rect))

        displayText(name, (rect[0]+(rect[2]/2)), (rect[1]+(rect[3]/2)))
    
participantId = input("Please enter the participant ID number: \n")

#initialising pygame and setting display
pygame.init()
screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Emotion Recognition Test")

#loading images
imageList = []
imageNames = []
practiceImages = []

def loadImages(directory, practiceDirectory):
        os.chdir(practiceDirectory)
        for image in random.sample(os.listdir(practiceDirectory), noPracticeQuestions):
                practiceImages.append(pygame.image.load(image).convert_alpha())

        os.chdir(directory)
        for image in random.sample(os.listdir(directory), noQuestions):
                imageList.append(pygame.image.load(image).convert_alpha())
                imageNames.append(image)
        
def instructions(instructionsText):
    """This function creates a new game loop to display text as an instruction screen"""
    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
            elif event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
             
        displayText(instructionsText, (displayWidth/2), (displayHeight/2))
        pygame.display.update()

def mainDisplay():
    """Displays a fixation circle and the answer buttons"""
    pygame.draw.circle(screen, (0,0,0), (int(displayWidth/2), int(displayHeight/2)), 10, 2)
    displayButtons()

def mainGame(images, practice):
    """Main game loop"""
    answers = []
    #dt is delta time, used to measure time
    dt = 0
    timer = displayTime
    clock = pygame.time.Clock()
    imageNumber = 0
    gameState = States.VIEWING
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))
        mainDisplay()
        dt = clock.tick_busy_loop(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()


        if ( gameState == States.VIEWING):
            #timer minus dt, to count down
            timer -= dt
            if timer >= 0:
                displayImage(images, imageNumber)
            else:
                gameState = States.ANSWERING
                

        elif (gameState == States.ANSWERING):
            #timer resets
            timer = displayTime
            screen.fill((255, 255, 255))
            mainDisplay()
            #detecting if a button is clicked
            for emotion, rects in rectDict.items():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rects.collidepoint(mouse):
                        #if button is clicked move back to VIEWING state
                        gameState = States.VIEWING
                        answers.append(emotion)
                        imageNumber += 1
                        break
                    elif not any(rect.collidepoint(mouse) for rect in rectList):
                        displayText("You did not click a button!", 600, 600)
                        

        if practice == True:
            if len(answers) == noPracticeQuestions:
                #reset the answer list as practice answers are not tracked
                answers = []
                break
        else:
            if len(answers) == noQuestions:
                #creates a tuple containing image names, emotion type and participant's answer
                results = list(zip(imageNames, emotions, answers))
                results.insert(0, ("question", "emotion", "answer"))


                #writes results to a CSV file titled with the participant's ID number
                #saved in BASE_DIRECTORY
                os.chdir(BASE_DIRECTORY)
                with open(f"{participantId}.csv", "w", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(results)
                break
                

        pygame.display.update()

loadImages(IMAGE_DIRECTORY, PRACTICE_IMAGE_DIRECTORY)

#creates a list of the emotions taken from the image names
emotions = []                                            
for imageName in imageNames:
	for emotion in emotionTypes:
		if emotion or emotion.lower() or emotion.upper() in imageName:
			emotions.append(emotion)

#First instruction screen - feel free to modify text
instructions("First instruction screen - press spacebar to continue") #inform participants about the game

#Practice game loop
mainGame(practiceImages, practice=True)   #this is the practice loop

#Second instruction screen, used to inform participants that practice mode is over
instructions("Practice mode has ended - press spacebar to continue")

#Non-practice game loop
mainGame(imageList, practice=False)

#Final screen, thanking participants for taking part
instructions("Thank you for taking part")
