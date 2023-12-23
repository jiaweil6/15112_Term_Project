from game import *

from cmu_graphics import *
from PIL import Image
import os, pathlib


# code from TA
def openImage(fileName):
    file_path = os.path.join(pathlib.Path(__file__).parent, fileName)
    return CMUImage(Image.open(file_path))

def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

# check if new cursor was clicked
def isCursorClicked(app, cursorType, mouseX, mouseY):
    cursor_positions = {
        'classic': (app.bg.LeftTopX + app.bg.rectWidth/4, app.bg.LeftTopY + app.bg.rectHeight/2, 30, 30),
        'modern': (app.bg.LeftTopX + 2*(app.bg.rectWidth/4), app.bg.LeftTopY + app.bg.rectHeight/2, 30, 30),
        'special': (app.bg.LeftTopX + 3*(app.bg.rectWidth/4), app.bg.LeftTopY + app.bg.rectHeight/2, 30, 30)
    }
    x, y, w, h = cursor_positions[cursorType]

    clicked = (x-w <= app.width/2 <= x+w and y-h <= app.height/2 <= y+h)

    return clicked

class Cursor:
    def __init__(self, width=1500, height=800):
        self.width = width
        self.height = height
        self.cursors = {
            'classic': openImage('images/classic.png'), # https://www.pngall.com/wp-content/uploads/14/Crosshair-PNG-Photos.png 
            'modern': openImage('images/modern.png'), # https://tmpfiles.nohat.cc/m2H7i8b1Z5H7i8b1.png
            'special': openImage('images/special.png') # https://www.cs.cmu.edu/~112/images/112-dragon2_inverted.png
        }
        self.current = 'modern'  # default cursor

    # selected cursor
    def draw(self):
        cursor_image = self.cursors[self.current]
        drawImage(cursor_image, self.width/2, self.height/2, align='center', width=35, height=35)

    # selecting cursor page
    def selection(self, app):

        # classic
        drawImage(self.cursors['classic'], app.bg.LeftTopX + app.bg.rectWidth/4, app.bg.LeftTopY + app.bg.rectHeight/2, 
                    width=50, height=50, align='center')
        drawLabel('Classic', app.bg.LeftTopX + app.bg.rectWidth/4, app.bg.LeftTopY + 320, size=20, fill='white', align='center')

        # modern
        drawImage(self.cursors['modern'], app.bg.LeftTopX + 2*(app.bg.rectWidth/4), app.bg.LeftTopY + app.bg.rectHeight/2, 
                    width=50, height=50, align='center')
        drawLabel('Modern', app.bg.LeftTopX + 2*(app.bg.rectWidth/4), app.bg.LeftTopY + 320, size=20, fill='white', align='center')

        # 112 special
        drawImage(self.cursors['special'], app.bg.LeftTopX + 3*(app.bg.rectWidth/4), app.bg.LeftTopY + app.bg.rectHeight/2, 
                    width=50, height=50, align='center')
        drawLabel('112 Special', app.bg.LeftTopX + 3*(app.bg.rectWidth/4), app.bg.LeftTopY + 320, size=20, fill='white', align='center')

        # title
        drawLabel('Choose Your Crosshair', app.bg.LeftTopX + app.bg.rectWidth/2, app.bg.LeftTopY + app.bg.rectHeight/4, size=50, 
                  fill='white', align = 'center', font = 'impact')


class Menu:
    def __init__(self, title, width=1500, height=800, color='white'):
        self.title = title
        self.width = width
        self.height = height
        self.color = color

    def draw(self, app):
        drawLabel(self.title, self.width / 2, self.height / 6, size=150, align='center', fill=self.color, font = 'impact')


class Button:
    def __init__(self, text, x, y, width, height, size, font, opacity, color, hover = False, textColor='white'):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size
        self.font = font
        self.opacity = opacity
        self.color = color
        self.hover = hover
        self.textColor = textColor

    def draw(self, app):
        absX = app.bg.LeftTopX + self.x
        absY = app.bg.LeftTopY + self.y

        drawRect(absX, absY, self.width, self.height, fill=self.color, opacity=self.opacity)
        drawLabel(self.text, absX + self.width / 2, absY + self.height / 2, fill=self.textColor, font=self.font, size=self.size, align='center')

    def checkHover(self, app):
        absX = app.bg.LeftTopX + self.x
        absY = app.bg.LeftTopY + self.y

        if (absX < app.width/2 < absX + self.width and absY < app.height/2 < absY + self.height):
            self.hover = True
        else:
            self.hover = False


def onAppStart(app):

    onAppStartGame(app)  

    app.menu = Menu('112 Aim Trainer')
    app.cursor = Cursor()
    app.start = False
    app.cursorSetting = False

    # score
    app.record = 0
    app.newRecord = False

    # sound
    app.BGM = loadSound('sounds/BGM.mp3') # https://www.youtube.com/watch?v=Rvi6c8toWJM
    app.ready = loadSound('sounds/ready.mp3') # https://www.youtube.com/watch?v=owQHhpv8g44
    app.gameMusic = loadSound('sounds/game.mp3') # https://www.youtube.com/watch?v=OWKXz-lVhlQ
    app.click = loadSound('sounds/click.mp3') # https://www.youtube.com/watch?v=Uzj3CD0FUhA
    app.shot = loadSound('sounds/shot.mp3') # https://www.youtube.com/watch?v=f_SfUHn_9bk


    # buttons
                                        #    x    y    w     h size   font  opacity color text color
    app.startButton = Button('Start Game',  140, 150, 380,  80, 80, 'impact', 100, 'lime', 'white')
    app.settingsButton = Button('Settings', 255, 380, 130,  40, 35, 'impact', 100, 'lime', 'white')
    app.backButton = Button('Back',         40,  440, 50,   23, 20, 'impact', 100, 'lime', 'white')

    app.buttons = [app.startButton, app.settingsButton, app.backButton]

    # time
    app.stepsPerSecond = 30

    # gun
    app.gunImage = openImage('images/gun.png') # https://www.vhv.rs/dpng/d/161-1611167_thumb-image-first-person-gun-png-transparent-png.png
    
    reset(app)

# after game over
def reset(app):
    app.score = 0
    app.gameTime = 16
    app.count = 0
    app.countDown = 3 #3
    app.opacityChange = 50
    app.lastHitScore = []

def onMouseMove(app, mouseX, mouseY):

    # everything when its in game
    onMouseMoveGame(app, mouseX, mouseY)

    # hover effect
    for button in app.buttons:
        button.checkHover(app)
        if button.hover:
            button.opacity = 100
            button.textColor = 'darkGreen'
        else:
            button.opacity = 0
            button.textColor = 'white'


def onMousePress(app, mouseX, mouseY):

    # in game
    if app.start:
        app.shot.play(restart = True) ## latency too high at the moment
        onMousePressGame(app, mouseX, mouseY)
        

    else:

        # settings
        if app.settingsButton.hover:
            app.click.play()
            app.cursorSetting = True
        
        if app.backButton.hover:
            app.click.play()
            app.cursorSetting = False

        # start game
        if app.cursorSetting == False:
            if app.startButton.hover:
                app.click.play()
                app.BGM.pause()
                app.ready.play()
                app.gameMusic.play(restart = True)

                app.start = True
                
                
        # settings
        else:
            # choose cursor
            for name, image in app.cursor.cursors.items():
                if isCursorClicked(app, name, mouseX, mouseY):
                    app.cursor.current = name


def redrawAll(app):
    # mid position of the rectangle
    centerX = app.bg.LeftTopX + app.bg.rectWidth/2
    centerY = app.bg.LeftTopY + app.bg.rectHeight/2

    # background
    app.bg.draw()
    drawRect(0, 0, 1500, 800, fill='black', opacity=app.opacityChange)

    # countdown
    if app.start:
        # countDown
        drawLabel(app.countDown, centerX, centerY, size=200, fill = 'white', font = 'impact', align = 'center')

        if app.countDown < 1:
            # game start
            redrawAllGame(app)
    else:
        app.BGM.play()
        # settings
        if app.cursorSetting == True:
            # setting
            app.cursor.selection(app)
            app.backButton.draw(app)
        
        # menu
        else:
            app.startButton.draw(app)

            # gold text if new record
            if app.newRecord == True:
                drawLabel(f'Highest: {app.record}', centerX, centerY + 55, size = 40, fill = 'gold', font='impact', align='center')
            else:
                drawLabel(f'Highest: {app.record}', centerX, centerY + 55, size = 40, fill = 'white', font='impact', align='center')

            # buttons
            app.settingsButton.draw(app)
            app.menu.draw(app)
            
    # cursor
    app.cursor.draw()

    # gun
    drawImage(app.gunImage, 900, 500, width = 800, height = 300)



def onStep(app):

    if not app.start:
        return

    app.count += 1

    # Decrease opacity
    if app.opacityChange >= 0.3:
        app.opacityChange -= 0.3

    # Handle count down
    if app.count % 40 == 0:
        app.countDown -= 1

        if app.countDown < 1:
            app.ready.pause()
            app.gameTime -= 1

            # Check for game over
            if app.gameTime == 0:
                app.start = False
                app.gameMusic.pause()
                updateRecord(app)
                reset(app)


def updateRecord(app):
    if app.score > app.record:
        app.record = app.score
        app.newRecord = True
        app.count = 0
    else:
        app.newRecord = False

    

def main():
    runApp()

main()
