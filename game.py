from cmu_graphics import *
import random

def distance(x0, x1, y0, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

class Background:
    def __init__(self, LeftTopX, LeftTopY, width, height, rectWidth=650, rectHeight=500, color='grey', opacity=0):
        self.LeftTopX = LeftTopX
        self.LeftTopY = LeftTopY
        self.rectWidth = rectWidth
        self.rectHeight = rectHeight
        self.color = color
        self.opacity = opacity
        self.width = width
        self.height = height

    def calculateOpacity(self, area):
        maxArea = 800
        ratio = area / maxArea
        if ratio >= 1:
            ratio = 1
        elif ratio <= 0:
            ratio = 0

        minOpacity = 20
        resultOpacity = ratio * 60
        return int(max(resultOpacity, minOpacity))

    def draw(self):
        # shadow
        drawRect(0, 0, 1500, 800, fill='black')

        # shadow opacity
        areaTop = self.LeftTopY + 400
        areaBottom = 800 - (self.LeftTopY + self.rectHeight) + 50
        areaLeft = self.LeftTopX
        areaRight = 1500 - (self.LeftTopX + self.rectWidth) - 50

        opacityTop = self.calculateOpacity(areaTop)
        opacityBottom = self.calculateOpacity(areaBottom)
        opacityLeft = self.calculateOpacity(areaLeft)
        opacityRight = self.calculateOpacity(areaRight)

        # walls
        drawPolygon(0, 0, self.LeftTopX, self.LeftTopY, 
                    self.LeftTopX + self.rectWidth, self.LeftTopY, self.width, 0, 
                    fill='darkGrey', opacity=opacityTop)  # top wall

        drawPolygon(0, self.height, self.width, self.height, 
                    self.LeftTopX + self.rectWidth, self.LeftTopY + self.rectHeight, self.LeftTopX, self.LeftTopY + self.rectHeight, 
                    fill='darkGrey', opacity=opacityBottom)  # bottom wall

        drawPolygon(0, 0, 0, self.height, 
                    self.LeftTopX, self.LeftTopY + self.rectHeight, self.LeftTopX, self.LeftTopY, 
                    fill='darkGrey', opacity=opacityLeft)  # left wall

        drawPolygon(self.width, self.height, self.width, 0, 
                    self.LeftTopX + self.rectWidth, self.LeftTopY, self.LeftTopX + self.rectWidth, self.LeftTopY + self.rectHeight, 
                    fill='darkGrey', opacity=opacityRight)  # right wall

        # main rectangle
        mainOpacity = ((opacityBottom + opacityTop) // 2) + 30
        drawRect(self.LeftTopX, self.LeftTopY, self.rectWidth, self.rectHeight, fill=self.color, opacity=mainOpacity)


############################################################

############################################################


class Target():
    def __init__(self, x, y, size, relX, relY, color='blue'):
        self.x = x
        self.y = y
        self.size = size
        self.relX = relX
        self.relY = relY
        self.color = color
        self.newX = x
        self.newY = y
        self.offsetX = x
        self.offsetY = y

        # hitbox
        self.headCoordinates = []
        self.leftArmCoordinates = []
        self.rightArmCoordinates = []
        self.legsCoordinates = []
        self.bodyCoordinates = []


    def getInitial3DLocation(self, app):
        # Middle of the background
        cx = app.bg.LeftTopX + app.bg.rectWidth / 2
        cy = app.bg.LeftTopY + app.bg.rectHeight / 2

        # Middle of the target
        x = self.x + self.size / 2
        y = self.y + self.size / 2

        offsetX = (abs(cx - x)) / 7
        offsetY = (abs(cy - y)) / 7

        # First quadrant
        if x > cx and y < cy:
            initialOffsetX = -offsetX
            initialOffsetY = offsetY

        # Second quadrant
        elif x < cx and y < cy:
            initialOffsetX = offsetX
            initialOffsetY = offsetY
        
        # Third quadrant
        elif x < cx and y > cy:
            initialOffsetX = offsetX
            initialOffsetY = -offsetY
        
        # Fourth quadrant
        else: # x > cx and y > cy
            initialOffsetX = -offsetX
            initialOffsetY = -offsetY

        initialOffsetX = max(-self.size/3, min(self.size/3, initialOffsetX))
        initialOffsetY = max(-self.size/3, min(self.size/3, initialOffsetY))

        return initialOffsetX, initialOffsetY
    

    def getRealTime3DLocation(self, app):
        # Get initial offsets
        initialOffsetX, initialOffsetY = self.getInitial3DLocation(app)

        centerX = app.width / 2
        centerY = app.height / 2
        x = self.x + self.size / 2
        y = self.y + self.size / 2

        dx = (centerX - x)
        dy = (centerY - y)


        dynamicOffsetX = -(dx / centerX) * self.size * 0.3
        dynamicOffsetY = -(dy / centerY) * self.size * 0.2

        # Apply both initial and dynamic offsets to newX and newY
        self.newX = self.x + initialOffsetX + dynamicOffsetX
        self.newY = self.y + initialOffsetY + dynamicOffsetY

        return self.newX, self.newY
    

    def draw3D(self, x, y, newX, newY, width, height):
        drawRect(newX, newY, width, height, fill='blue')
        
        # left
        drawPolygon(x, y, newX, newY,
                    newX, newY + height, x, y + height, fill='grey')
        # right
        drawPolygon(x + width, y, newX + width, newY,
                    newX + width, newY + height, x + width, y + height, fill='grey')
        # top
        drawPolygon(x, y, newX, newY,
                    newX + width, newY, x + width, y, fill='grey')
        # bottom
        drawPolygon(x, y + height, newX, newY + height,
                    newX + width, newY + height, x + width, y + height, fill='grey')
    

    def drawHead(self, app):
        self.newX, self.newY = self.getRealTime3DLocation(app)

        x = self.x
        y = self.y
        newX = self.newX
        newY = self.newY
        width = self.size
        height = self.size

        # hitbox
        self.headCoordinates = self.hitboxPolygon(x, y, newX, newY, width, height)
        drawPolygon(*self.headCoordinates, fill='hotPink')

        # offset
        self.draw3D(x, y, newX, newY, width, height)

        # main
        drawRect(x, y, width, height, fill=self.color)



    def drawLeftArm(self, app):

        x = self.x - self.size/2
        y = self.y + self.size
        newX = self.newX - self.size/2
        newY = self.newY + self.size
        width = self.size / 2
        height = self.size * 1.5

        # hitbox
        self.leftArmCoordinates = self.hitboxPolygon(x, y, newX, newY, width, height)
        drawPolygon(*self.leftArmCoordinates, fill='hotPink')

        # offset
        self.draw3D(x, y, newX, newY, width, height)

        # main
        drawRect(x, y, width, height, fill='red')


    def drawRightArm(self, app):
        x = self.x + self.size
        y = self.y + self.size
        newX = self.newX + self.size
        newY = self.newY + self.size
        width = self.size / 2
        height = self.size * 1.5

        # hitbox
        self.rightArmCoordinates = self.hitboxPolygon(x, y, newX, newY, width, height)
        drawPolygon(*self.rightArmCoordinates, fill='hotPink')

        # offset
        self.draw3D(x, y, newX, newY, width, height)

        # main
        drawRect(x, y, width, height, fill='red')


    # no need 3D
    def drawBody(self, app):
        x = self.x
        y = self.y + self.size
        width = self.size
        height = self.size * 1.5

        # hitbox
        self.bodyCoordinates = [x, y, x + width, y, x + width, y + height, x, y + height]

        # main
        drawRect(x, y, width, height, fill='lightBlue')

    def drawLegs(self, app):
        x = self.x
        y = self.y + self.size * 2.5
        newX = self.newX
        newY = self.newY + self.size * 2.5
        width = self.size
        height = self.size

        # hitbox
        self.legsCoordinates = self.hitboxPolygon(x, y, newX, newY, width, height)
        drawPolygon(*self.legsCoordinates, fill='hotPink')

        # offset
        self.draw3D(x, y, newX, newY, width, height)

        # main
        drawRect(x, y, width, height, fill='green')
        drawLine(x + width/2, y, x + width/2, y + height, fill='grey')


    def hitboxPolygon(self, x, y, newX, newY, width, height):
        
        if newX <= x and newY >= y:
            # Quadrant 1
            coordinates = [(x, y), (newX, newY), (newX, newY + height), (newX + width, newY + height), (x + width, y + height), (x + width, y)]
        
        elif newX > x and newY >= y:
            # Quadrant 2
            coordinates = [(x, y), (x + width, y), (newX + width, newY), (newX + width, newY + height), (newX, newY + height), (x, y + height)]

        elif newX > x and newY < y:
            # Quadrant 3
            coordinates = [(newX, newY), (x, y), (x, y + height), (x + width, y + height), (newX + width, newY + height), (newX + width, newY)]
        else: # newX <= x and newY < y
            # Quadrant 4
            coordinates = [(newX, newY), (newX, newY + height), (x, y + height), (x + width, y + height), (x + width, y), (newX + width, newY)]

        flattened = []
        for point in coordinates:
            flattened.append(point[0])  # x value
            flattened.append(point[1])  # y value
        return flattened


    def draw(self, app):

        cx = app.bg.LeftTopX + app.bg.rectWidth / 2
        cy = app.bg.LeftTopY + app.bg.rectHeight / 2

        # Middle of the target
        x = self.x + self.size / 2
        y = self.y + self.size / 2

        # first quadrant or second quadrant
        if (x > cx and y < cy) or (x < cx and y < cy):
            self.drawHead(app)
            self.drawLeftArm(app)
            self.drawRightArm(app)
            self.drawBody(app)
            self.drawLegs(app)
        
        # third quadrant or fourth quadrant
        else:
            self.drawLegs(app)
            self.drawLeftArm(app)
            self.drawRightArm(app)
            self.drawBody(app)
            self.drawHead(app)

# ray casting algorithm --> https://www.youtube.com/watch?v=RSXM9bgqxJM
def isInSideHitBox(x, y, coordinates):
    count = 0
    
    n = len(coordinates)

    for i in range(0, n, 2):
        x1, y1 = coordinates[i], coordinates[i + 1]
        x2, y2 = coordinates[(i + 2) % n], coordinates[(i + 3) % n]

        # Check if point is exactly at a vertex
        if (x, y) == (x1, y1) or (x, y) == (x2, y2):
            return True

        # Check if the point is on the border of the polygon
        if (y1 == y and y2 == y) and (x >= min(x1, x2) and x <= max(x1, x2)):
            return True

        # Check for intersections with the polygon's edges
        if y1 != y2: 
            if y >= min(y1, y2) and y < max(y1, y2) and x <= max(x1, x2):
                xIntersect = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                # Check if point is on an edge
                if x == xIntersect:
                    return True
                if x < xIntersect:
                    count += 1

    return count % 2 == 1

def updateTarget(app):
    newTargetX, newTargetY = generateNewTarget(app)
    targetSize = random.randrange(20, 35)  # Random size for new target
    relX = newTargetX - app.bg.LeftTopX  # update relationship between target and background
    relY = newTargetY - app.bg.LeftTopY
    app.target = Target(newTargetX, newTargetY, targetSize, relX, relY)


def generateNewTarget(app):
    # range for the new target
    minX = int(app.bg.LeftTopX + app.target.size) - 150 # added for more range on the x-axis
    maxX = int(app.bg.LeftTopX + app.bg.rectWidth - app.target.size) + 150
    minY = int(app.bg.LeftTopY + app.target.size)
    maxY = int(app.bg.LeftTopY + app.bg.rectHeight)

    if minX > maxX:
        minX, maxX = int(app.bg.LeftTopX), int(app.bg.LeftTopX + app.bg.rectWidth)
    if minY > maxY:
        minY, maxY = int(app.bg.LeftTopY), int(app.bg.LeftTopY + app.bg.rectHeight)

    newTargetX = random.randint(minX, maxX)
    newTargetY = random.randint(minY, maxY)

    # the new target won't be too close to the old one
    if distance(newTargetX, app.target.x, newTargetY, app.target.y) <= 200:
        return generateNewTarget(app)

    return newTargetX, newTargetY


def onAppStartGame(app):

    # screen 
    app.width = 1500
    app.height = 800

    # background
    app.initialBgX = 500
    app.initialBgY = 200
    app.bg = Background(app.initialBgX, app.initialBgY, app.width, app.height)

    # mouse
    app.mouseSensitivity = 1.4

    # target
    app.initialTargetX = random.randrange(400, 800)
    app.initialTargetY = random.randrange(200, 600)
    targetSize = random.randrange(20, 35) # change this for difficulty
    relX = app.initialTargetX - app.initialBgX
    relY = app.initialTargetY - app.initialBgY
    app.target = Target(app.initialTargetX, app.initialTargetY, targetSize, relX, relY)

    # score
    app.lastHitScore = []
    app.score = 0

def onMouseMoveGame(app, mouseX, mouseY):
    dx = (app.width / 2 - mouseX) * app.mouseSensitivity
    dy = (app.height / 2 - mouseY) * app.mouseSensitivity

    # Update background
    newBgX = app.initialBgX + dx
    newBgY = app.initialBgY + dy
    app.bg = Background(newBgX, newBgY, app.width, app.height, app.bg.rectWidth, app.bg.rectHeight, app.bg.color)

    # Update target's position
    app.target.x = newBgX + app.target.relX
    app.target.y = newBgY + app.target.relY



def onMousePressGame(app, mouseX, mouseY):

    targetAreas = {
        'head': (app.target.headCoordinates, 10),
        'legs': (app.target.legsCoordinates, 3),
        'body': (app.target.bodyCoordinates, 5),
        'leftArm': (app.target.leftArmCoordinates, 1),
        'rightArm': (app.target.rightArmCoordinates, 1)
    }

    cx = app.width/2
    cy = app.height/2

    for area, (coordinates, score) in targetAreas.items():
        if isInSideHitBox(cx, cy, coordinates):
            # print(f'{area}')
            app.score += score
            relX = app.target.x - app.bg.LeftTopX
            relY = app.target.y - app.bg.LeftTopY
            app.lastHitScore = [score,[relX, relY]]

            updateTarget(app)
            break

def redrawAllGame(app):

    # background
    app.bg.draw()

    # timer warning
    centerX = app.bg.LeftTopX + app.bg.rectWidth/2
    centerY = app.bg.LeftTopY + app.bg.rectHeight/2
    drawLabel(app.gameTime, centerX, centerY, fill='dimGray', size=200, font='impact', align='center', opacity=100)

    # target
    app.target.draw(app)
    
    # show point awarded
    if len(app.lastHitScore) > 0:

        lastHitRelX, lastHitRelY = app.lastHitScore[1]
        currentHitX = app.bg.LeftTopX + lastHitRelX
        currentHitY = app.bg.LeftTopY + lastHitRelY
        drawLabel(app.lastHitScore[0], currentHitX + 35, currentHitY, size=20, fill='red')

    # cursor
    app.cursor.draw()

    # text
    drawLabel(f"Score: {app.score}", 60, 50, fill='white', font='impact', size=35, align='left')
    # drawLabel(f"Time: {app.gameTime}", 60, 90, fill='white', font='impact', size=35, align='left')

