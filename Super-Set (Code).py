from cmu_graphics import *
import copy, string, itertools, random

"""
This is a multiplayer game. You could play alone of with a friend. Instead of removing all
features when you press 'h', only one wrong pick is removed. The game displays the person who
finished in the least time at the end. And the person who lost the least amounts of lives (pills).
To keep the user intertained, music which switches with the character was added. When the user is
changing the settings, a different song plays. If the user clicks 'r', they have the option of
reseting the game features and you will be prompted to type yes or no. If they type yes and press enter,
the game resets, and if they enter no and hit enter, they go back to the help screen. The outline was left
red even after you get a correct set since to add to the essence of a fighting game.
"""


####################################################
# onAppStart: called only once when app is launched
####################################################

# more than one five in dims does not work
# write helper function to reset board

def onAppStart(app):
    reset(app)
    app.welcomeUrl = 'cmu://785904/29313421/MAIN-NARUTO_93da9d12-4dc0-421b-b9cd-0b144e4b0e16_2000x.jpg'
    app.chooseCharURL = 'cmu://785904/29313929/4b8cc50d5b9092883f69aecaa23c7d1f.jpg'
    app.naruto = 'cmu://785904/29313900/cca723bebe39c69a9544e5d0a303e477.jpg'
    app.sasuke = 'cmu://785904/29313913/415519.jpg'
    app.jiraiya = 'cmu://785904/29314560/jiraiya-4k-with-naruto-ohcl4ochkraom21j.jpg'
    app.itachi = 'cmu://785904/29314540/35ff7e2ed2bf0d4438ffd4a52ed24ac9.jpg'
    app.kakashi = 'cmu://785904/29314681/kakashi-master-of-lightning-ninjutsu-oy4ggwbgmd1t71bx.jpg'
    narratingURL = 'cmu://785904/29314951/01.mp3'
    narutoURL = 'cmu://785904/29314954/05.mp3'
    sasukeURL = 'cmu://785904/29314953/03.mp3'
    app.sasukeSong = Sound(sasukeURL)
    app.narutoSong = Sound(narutoURL)
    app.narratingSong = Sound(narratingURL)

def reset(app):
    # Set app size
    app.width = 1000
    app.height = 600
    
    # Set screens appearances
    app.welcomeBackgroung = gradient('pink', 'white', start = 'top')
    app.welcomeTextFill = 'gold'
    app.manualBackgroung = gradient('blue', 'white', start = 'bottom')
    app.manualTextFill = 'black'
    app.instructionsBackground = gradient('blue', 'pink', start = 'left')
    app.instructionsFill = 'black'
    app.dimsBackground = gradient('white', 'black')
    app.dimsTextFill = 'black'
    app.themeBackGround = gradient('pink', 'white', start = 'top')
    app.themeTextFill = 'black'
    app.playBackground = gradient('white', 'black', start = 'top')
    app.playTextFill = 'red'
    app.font = 'grenze'
    app.winnerFill = 'gold'
    
    # Welcome screen
    app.welcomeMessage = 'Welcome to SuperSet'
    app.numberOfLettersShown = -1
    app.welcomeCount = 0
    
    # Help screen
    app.storeChar = None
    
    # Instructions
    app.instructions = """Naruto and Sasuke are fighting again.
                        Kakashi decided to give them a mission to decide the winner.
                        They must transport rare pills to a nearby village safely.
                        On their way, dangerous ninjas will attemp to steal the pills.
                        They will fight the ninjas through a card game.
                        They must select a certain number of cards from the deck to form a set.
                        You are expected to know what a set is.
                        If they get a set wrong, they lose a pill.
                        They need to cross 4 villages each on their way to their final destination.
                        They must reach the other village as soon as possible.
                        They may press 'h' to get a hint, but it will cost you 15 seconds.
                        Good luck shinobi and be quick!!!!!!!!!!!!.
                        """
    
    # Dims screen objects
    app.dims = [3,3,3]
    
    # Reset screen objects
    app.typingRestartResponse = ''
    app.drawErroMessage = False
    
    # Themes screen objects
    app.themes = ['letters', 'standard', 'special', 'boss']
    app.currentTheme = 'letters'
    app.featureFont = 'arial'
    # Decides if cards should be rectangles or not could be used to change shape of cards.
    app.themeRect = None
    # Standard Theme
    app.standardThemeShapes = ['oval', 'star', 'diamond']
    app.standardThemeColors = ['gold', 'cyan', 'orange']
    app.standardThemeNum = [1, 2, 3]
    app.standardThemeFill = ['full', 'half-full', 'empty']
    app.standardTheme = [app.standardThemeShapes, app.standardThemeColors,
                        app.standardThemeNum, app.standardThemeFill]
    # Special Theme
    app.specialThemeShapes = ['triangle', 'square', 'pentagon', 'hexagon']
    app.specialThemeColors = ['gold', 'cyan', 'orange', 'purple']
    app.specialThemeRotationSpeed = [5, -5, 10, -10]
    app.specialThemeBorder = ['thick', 'thin', 'dashed']
    app.specialTheme = [app.specialThemeShapes, app.specialThemeColors,
                        app.specialThemeRotationSpeed, app.specialThemeBorder]
    # Boss Theme
    app.bossThemeShapes = ['oval', 'star', 'diamond', 'triangle']
    app.bossThemeColors = [gradient('gold', 'cyan'), gradient('orange', 'cyan'),
                                gradient('gold', 'orange'), 'pink']
    app.bossThemeRotationSpeed = [3, -5, 10, -15]
    app.bossThemeBorder = ['thick', 'thin', 'dashed']
    app.bossTheme = [app.bossThemeShapes, app.bossThemeColors,
                        app.bossThemeRotationSpeed, app.bossThemeBorder]
    
    # Play screen objects
    app.playCount = 0
    app.playScreenCounter = 0
    app.numberOfCards = 8
    app.cardWidth = 120
    app.cardLength = 180
    app.remainingRounds = 4
    app.remainingLives = 2
    app.displayBoard, app.cardSet = getRandomBoardWithSet(app.dims, app.numberOfCards)
    app.indexOfFoundSetOnBoard = []
    app.cardPositions = []
    app.indexOfcardsUserSelected = []
    setIndexOfFoundSetOnBoard(app) # On the board
    app.positionsStored = False
    app.targetNumberOfCards = min(app.dims)
    app.gameOver = False
    app.chooseWrongMessage = "You lost a pill shinobi."
    app.chooseRightMessage = "You crossed a village shinobi!!!!!!!"
    app.gameOverCount = 0
    
    # Naruto play screen objects
    app.narutoPlayCount = 0
    app.narutoPlayScreenCounter = 0
    app.narutoRemainingRounds = 4
    app.narutoRemainingLives = 2
    app.narutoDisplayBoard, app.narutoCardSet = getRandomBoardWithSet(app.dims, app.numberOfCards)
    app.narutoIndexOfFoundSetOnBoard = []
    app.narutoCardPositions = []
    app.narutoIndexOfcardsUserSelected = []
    narutoSetIndexOfFoundSetOnBoard(app) # On the board
    app.narutoPositionsStored = False
    app.narutoTargetNumberOfCards = min(app.dims)
    app.narutoGameOver = False
    app.narutpGameOverCount = 0
    
    # Choose character objects
    app.chooseCharRect = None
    app.chooseCharRects = ['Sasuke', 'Naruto']
    app.character = 'Narator'
    
    # Winner screen objects
    app.showFastest = True
    app.winnerCount = 0
    
    # Levels screen objects
    app.levelNames = ['Light', 'Decent', 'Tuff', 'Make your own!']

def setIndexOfFoundSetOnBoard(app):
    for i in range(app.numberOfCards):
        if app.displayBoard[i] in app.cardSet:
            app.indexOfFoundSetOnBoard.append(i)

def narutoSetIndexOfFoundSetOnBoard(app):
    for i in range(app.numberOfCards):
        if app.narutoDisplayBoard[i] in app.narutoCardSet:
            app.narutoIndexOfFoundSetOnBoard.append(i)

####################################################
# Code used by multiple screens
####################################################

def playSong(app):
    if app.character == 'Sasuke':
        app.sasukeSong.play(loop=True)
        app.narratingSong.pause()
        app.narutoSong.pause()
    elif app.character == 'Naruto':
        app.narutoSong.play(loop=True)
        app.narratingSong.pause()
        app.sasukeSong.pause()
    elif app.character == 'Narator':
        app.narratingSong.play(loop=True)
        app.narutoSong.pause()
        app.sasukeSong.pause()

def onKeyPressHelper(app, key):
    if   key == 'd':
        app.character = 'Narator'
        playSong(app)
        setActiveScreen('setDimsScreen')
    elif key == 't':
        app.character = 'Narator'
        playSong(app)
        setActiveScreen('setThemeScreen')
    elif key == '?':
        app.character = 'Narator'
        playSong(app)
        setActiveScreen('helpScreen')
    elif key == 'p':
        if app.character == 'Naruto':
            playSong(app)
            setActiveScreen('narutoPlayScreen')
        else:
            playSong(app)
            app.character = 'Sasuke'
            setActiveScreen('playScreen')
    elif key == 'r':
        app.character = 'Narator'
        playSong(app)
        setActiveScreen('resetScreen')
    elif key == 'i':
        app.character = 'Narator'
        playSong(app)
        setActiveScreen('instructionScreen')
    elif key == 'c':
        app.character = 'Narator'
        playSong(app)
        setActiveScreen('chooseCharacterScreen')

def drawScreenTitle(app, screenTitle, color):
    drawLabel('SuperSet!', app.width/2, 20, size=20, fill = color, bold=True, font = app.font)
    drawLabel(screenTitle, app.width/2, 50, size=16, fill = color, bold=True, font = app.font)
    
def addUpListValues(l):
    added = 0
    for i in l:
        added += i
    return added

###############################################
# Welcome Screen
############################################### 
def welcomeScreen_redrawAll(app):
    drawImage(app.welcomeUrl, app.width/2, app.height/2, align = 'center')
    #drawRect(0, 0, app.width, app.height, fill = app.welcomeBackgroung)
    for i in range (app.numberOfLettersShown):
        if app.numberOfLettersShown >= 0 and app.numberOfLettersShown <= len(app.welcomeMessage) - 1:
            drawLabel(app.welcomeMessage[app.numberOfLettersShown], app.width / 2, app. height / 2, size = 50,
                        fill = app.welcomeTextFill, bold = True, font = app.font)
        drawLabel(app.welcomeMessage[i], 50 + (i * 50), app. height / 2, size = 50,
                    fill = app.welcomeTextFill, bold = True, font = app.font)
        app.numberOfLettersShown
    

def welcomeScreen_onKeyPress(app, key):
    if key == 's':
        setActiveScreen('chooseCharacterScreen')

def welcomeScreen_onStep(app):
    playSong(app)
    app.welcomeCount += 1
    if app.welcomeCount % 10 == 0 and app.numberOfLettersShown < len(app.welcomeMessage):
        app.numberOfLettersShown += 1
    elif app.welcomeCount % 120 == 0:
        setActiveScreen('chooseCharacterScreen')

###############################################
# Choose Character
###############################################

def chooseCharacterScreen_redrawAll(app):
    drawImage(app.chooseCharURL, app.width/2, app.height/2, width = app.width, height = app.height, align = 'center')
    drawScreenTitle(app, 'Naruto V Sasuke', 'white')
    drawLabel("Use the arrows to select a character before moving on.",
                app.width / 2, app.height/2 + 125, fill = 'black', size = 20)
    drawLabel("Press enter to select", app.width / 2, app.height - 100, fill = 'white', size = 20)
    for i in range(2):
        color = 'black'
        if app.chooseCharRect == i:
            color = 'gold'
        x, y = 150 + (i * app.width / 2), app.height - 150
        drawRect(x, y, app.width / 4, app.height / 4, fill = None,
                    border = color, borderWidth = 20)
        drawLabel(app.chooseCharRects[i], (x + app.width/4) - 125, (y + app.height/4)/2 + 225,
                    size = 50, fill = 'gold')
    
def chooseCharacterScreen_onKeyPress(app, key):
    if key == 'enter' and app.chooseCharRect != None:
        app.character = app.chooseCharRects[app.chooseCharRect]
        playSong(app)
        setActiveScreen('helpScreen')
    if app.chooseCharRect == None:
        if key == 'right':
            app.chooseCharRect = 0
        elif key == 'left':
            app.chooseCharRect = len(app.chooseCharRects) - 1
    else:
        if key == 'right':
            app.chooseCharRect += 1
            app.chooseCharRect = app.chooseCharRect % len(app.chooseCharRects)
        elif key == 'left':
            app.chooseCharRect -= 1
            app.chooseCharRect = app.chooseCharRect % len(app.chooseCharRects)
    onKeyPressHelper(app, key)

###############################################
# Instructions Screen
############################################### 

def instructionScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = app.instructionsBackground)
    drawScreenTitle(app, 'Instructions', app.manualTextFill)
    lineDrawn = 0
    startingY = 200
    for line in app.instructions.splitlines():
        drawLabel(line, app.width / 2, startingY + (lineDrawn * 30),
                    size = 30, fill = app.instructionsFill, font = app.font)
        lineDrawn += 1

def instructionScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)

####################################################
# helpScreen
####################################################

def helpScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = app.manualBackgroung)
    drawScreenTitle(app, 'Manual', app.manualTextFill)
    drawLabel("Press '?' to return to the manual.",
              app.width/2, app.height/2 - 60, size=30, fill = app.manualTextFill, font = app.font)
    drawLabel(" Press 'd' to change the dimensions.",
              app.width/2, app.height/2, size=30, fill = app.manualTextFill, font = app.font)
    drawLabel("Press 't' to change the theme.",
              app.width/2, app.height/2 + 60, size=30, fill = app.manualTextFill, font = app.font)
    drawLabel(" Press 'p' to play.",
              app.width/2, app.height/2 + 120, size=30, fill = app.manualTextFill, font = app.font)
    drawLabel(" Press 'r' to reset the game.",
              app.width/2, app.height/2 + 180, size=30, fill = app.manualTextFill, font = app.font)
    drawLabel(" Press 'i' to read the instructions.",
              app.width/2, app.height/2 + 240, size=30, fill = app.manualTextFill, font = app.font)

def helpScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)

def helpScreen_onStep(app):
    app.storeChar = app.character
    app.character = 'Narator'
    playSong(app)
    app.character = app.storeChar

####################################################
# setDimsScreen
####################################################

def setDimsScreen_onScreenActivate(app):
    app.dimsCount = 0
    app.showErrorSeconds = 0
    app.tempDims =  copy.copy(app.dims)
    app.showErrorMessage = False
    app.dimsSum = 0
    app.colorFlicker = 'red'
    app.tooBigMessage = 'Whoa! Whoa! Whoa! Not too much now playa.\n Dims can only add up to 15.'
    app.tooSmallMessage = 'You need at least 3 values cuz.\n Make it challenging'
    app.themeBeforeNewDims = app.currentTheme

def setDimsScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = app.dimsBackground)
    drawScreenTitle(app, 'Set The Dimensions!', app.dimsTextFill)
    if app.showErrorMessage:
        message = app.tooSmallMessage
        if app.dimsSum > 15:
            message = app.tooBigMessage
        lineDrawn = 0
        for line in message.splitlines():
            drawLabel(line, app.width/2, app.height/2 + (lineDrawn * 40), size = 50,
                        fill = app.colorFlicker, font = app.font)
            lineDrawn += 1
    else:
        drawLabel('Press backspace to delete, type the new dimentions, and press enter to keep playing.',
                    app.width/2, app.height/2 + 100, size= 20, fill='red', font = app.font)
        drawLabel(f'Curent Dimensions: {app.tempDims}',
                    app.width/2, app.height/2, size=30, fill='red', font = app.font)

def setDimsScreen_onKeyPress(app, key):
    if key == 's':
        app.showErrorMessage = False
    if key.isdigit() and 3 <= int(key) <= 5:
        app.tempDims.append(int(key))
    elif key == 'backspace' and len(app.tempDims):
        app.tempDims.pop()
    elif key == 'enter':
        dimSum = addUpListValues(app.tempDims)
        if 6 <= dimSum <= 15:
            app.dims = app.tempDims
            app.narutoTargetNumberOfCards = min(app.dims)
            app.targetNumberOfCards = min(app.dims)
            # Reset board
            app.indexOfcardsUserSelected = []
            app.indexOfCardSelectedOnBoard = []
            setIndexOfFoundSetOnBoard(app)
            app.displayBoard, app.cardSet = getRandomBoardWithSet(app.dims, app.numberOfCards)
            # Reset Naruto board
            app.narutoIndexOfcardsUserSelected = []
            app.narutoIndexOfCardSelectedOnBoard = []
            narutoSetIndexOfFoundSetOnBoard(app)
            app.narutoDisplayBoard, app.narutoCardSet = getRandomBoardWithSet(app.dims, app.numberOfCards)
            app.character = 'Sasuke'
            playSong(app)
            setActiveScreen('playScreen')
        else:
            app.showErrorMessage = True
        
    onKeyPressHelper(app, key)
    
def setDimsScreen_onStep(app):
    if app.showErrorMessage:
        app.dimsCount += 1
        if app.dimsCount % 10 == 0:
            colors = ['red', 'orange', 'pink', 'blue', 'gold']
            app.colorFlicker = random.choice(colors)
        if app.dimsCount % 30 == 0:
            app.showErrorSeconds += 1
            if app.showErrorSeconds == 5:
                app.showErrorMessage = False
                app.showErrorSeconds = 0

####################################################
# setThemeScreen
####################################################

def setThemeScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = app.themeBackGround)
    drawScreenTitle(app, 'Set The Theme Screen!', app.themeTextFill)
    drawLabel('Choose your poison',
              app.width/2, app.height/2 - 100, size=30, fill='blue', font = app.font)
    startingX = 50
    for i in range (len(app.themes) - 1):
        leftX = startingX + (i * 300)
        rightX =leftX + app.width / 4
        if app.themeRect == i:
            drawRect(startingX + (i * 300), (app.height / 2) - 20, app.width / 4, 100,
                        fill = None, border = 'gold', borderWidth = 10, )
            midXVal = (leftX + rightX) / 2
            drawLabel(app.themes[i], midXVal, app.height / 2 + 25, size = 50, font = app.featureFont)
        else:
            drawRect(startingX + (i * 300), (app.height / 2) - 20, app.width / 4, 100,
                        fill = None, border = 'black', borderWidth = 10)
            midXVal = (leftX + rightX) / 2
            drawLabel(app.themes[i], midXVal, app.height / 2 + 25, size = 50, font = app.featureFont)
    color = 'black'
    if app.themeRect == 3:
        color = 'gold'
    drawRect(app.width / 2 - 25, app.height / 2 + 200, app.width / 4, 100, align = 'center',
                    fill = None, border = color, borderWidth = 10, )
    drawLabel(app.themes[3], app.width / 2 - 25, app.height / 2 + 200, size = 50, font = app.featureFont)

def setThemeScreen_onKeyPress(app, key):
    if key == 'enter' and app.themeRect != None:
        app.currentTheme = app.themes[app.themeRect]
        app.character = 'Sasuke'
        playSong(app)
        setActiveScreen('playScreen')
    if app.themeRect == None:
        if key == 'right':
            app.themeRect = 0
        elif key == 'left':
            app.themeRect = len(app.themes) - 1
    else:
        if key == 'right':
            app.themeRect += 1
            app.themeRect = app.themeRect % len(app.themes)
        elif key == 'left':
            app.themeRect -= 1
            app.themeRect = app.themeRect % len(app.themes)
    
    onKeyPressHelper(app, key)

####################################################
# playScreen
####################################################

def storeRectCardsPositions(app):
    for i in range (app.numberOfCards):
        leftX, leftY = 20+(i * app.cardWidth), 200
        rightX, rightY = leftX + app.cardWidth, leftY + app.cardLength
        if i % 2 == 0:
            app.cardPositions.append([leftX, leftY, rightX, rightY])
        else:
            app.cardPositions.append([leftX, leftY + 200, rightX, rightY + 200])
    app.positionsStored = True

def insideRect(app, mouseX, mouseY):
    if not app.positionsStored:
        storeRectCardsPositions(app)
    
    for i in range (app.numberOfCards):
        leftX, rightX = app.cardPositions[i][0], app.cardPositions[i][2]
        leftY, rightY = app.cardPositions[i][1], app.cardPositions[i][3]
        if leftX <= mouseX <= rightX:
            if (leftY <= mouseY <= rightY):
                for ind in range(len(app.indexOfcardsUserSelected)): # Checks if retangle i was previously selected and if it was, removes it from the list
                    if app.indexOfcardsUserSelected[ind] == i:
                        app.indexOfcardsUserSelected.pop(ind)
                        return
                app.indexOfcardsUserSelected.append(i)
                return True # The returned values are never used, but they could be useful in the future
    return False # The returned values are never used, but they could be useful in the future

def playScreen_onMousePress(app, mouseX, mouseY):
    if not app.gameOver:
        if len(app.indexOfcardsUserSelected) < app.targetNumberOfCards:
            insideRect(app, mouseX, mouseY)
        elif len(app.indexOfcardsUserSelected) == app.targetNumberOfCards:
            checkCardsSelected(app)
        if (app.remainingLives == 0) or (app.remainingRounds == 0):
            app.gameOver = True

def drawLetterFeatures(app):
    startingX = 20 + app.cardWidth / 2
    y1, y2 = 200 + (app.cardLength / 2), 400 + (app.cardLength / 2)
    color = gradient('pink', 'white')
    
    for i in range (app.numberOfCards):
        xVal = startingX + (i * app.cardWidth)
        y = 0
        if i % 2 == 0:
            y = y1
        else:
            y = y2
        drawLabel(app.displayBoard[i], xVal, y, fill = color, border = 'black',
                    size = 30, font = app.featureFont)

def drawStandardFeatures(app):
    startingX = 20 + app.cardWidth / 2
    y1, y2 = 200 + (app.cardLength / 2), 400 + (app.cardLength / 2)
    for i in range (app.numberOfCards):
        standardCardFeatures = []
        # Transforming letter features in standard features and adding results to a list
        for featureInd in range (len(app.displayBoard[i])):
            letter = app.displayBoard[i][featureInd]
            letInStand = ord(letter) - ord('A') # The letter index's placement in the standard theme list
            standardEquivalent = app.standardTheme[featureInd][letInStand]
            standardCardFeatures.append(standardEquivalent)
        # Extracting standard features from their list
        color = None
        num = 0
        opacity = 100
        width = 3
        xVal = startingX + (i * app.cardWidth)
        for feature in range (1, len(standardCardFeatures)):
            if feature == 1:
                color = standardCardFeatures[feature]
            elif feature == 2:
                num = standardCardFeatures[feature]
            elif feature == 3:
                if standardCardFeatures[feature] == 'empty':
                    opacity = 0
                elif standardCardFeatures[feature] == 'half-full':
                    opacity = 50
            
        # Drawing the features
        y = 0
        for shapes in range (num):
            if i % 2 == 0:
                y = 200 + (app.cardLength / (num + 1)) + (shapes * (app.cardLength / num)) - 10
            else:
                y = 400 + (app.cardLength / (num + 1)) + (shapes * (app.cardLength / num)) - 10
            if standardCardFeatures[0] == 'oval':
                drawOval(xVal, y, 40, 20, fill = None,
                            border = color, borderWidth = width)
                drawOval(xVal, y, 40, 20, fill = color, opacity = opacity,
                            border = color, borderWidth = width)
            elif standardCardFeatures[0] == 'star':
                drawStar(xVal, y, 20, 5, fill = None,
                            border = color, borderWidth = width)
                drawStar(xVal, y, 20, 5, fill = color, opacity = opacity,
                            border = color, borderWidth = width)
            elif standardCardFeatures[0] == 'diamond':
                drawRegularPolygon(xVal, y, 20, 4, fill = None, align = 'center', rotateAngle = 90,
                                    border = color, borderWidth = width)
                drawRegularPolygon(xVal, y, 20, 4, fill = color, align = 'center', rotateAngle = 90,
                                    opacity = opacity, border = color, borderWidth = width)

def drawSpecialFeatures(app):
    startingX = 20 + app.cardWidth / 2
    y1, y2 = 200 + (app.cardLength / 2), 400 + (app.cardLength / 2)
    for i in range (app.numberOfCards):
        specialCardFeatures = []
        # Transforming letter features in special features and adding results to a list
        for featureInd in range (len(app.displayBoard[i])):
            letter = app.displayBoard[i][featureInd]
            letInStand = ord(letter) - ord('A') # The letter index's placement in the standard theme list
            specialEquivalent = app.specialTheme[featureInd][letInStand]
            specialCardFeatures.append(specialEquivalent)
            
        # Extracting special features from their list
        color = None
        speed = 0
        borderWidth = 5
        dashes = False
        xVal = startingX + (i * app.cardWidth)
        for feature in range (1, len(specialCardFeatures)):
            if feature == 1:
                color = specialCardFeatures[feature]
            elif feature == 2:
                speed = ( app.playCount * specialCardFeatures[feature])
            elif feature == 3:
                if specialCardFeatures[feature] == 'thick':
                    borderWidth = 10
                elif specialCardFeatures[feature] == 'dashed':
                    dashes = True
            
        # Drawing the features
        y = 0
        if i % 2 == 0:
            y = y1
        else:
            y = y2
            
        if specialCardFeatures[0] == 'triangle':
            drawRegularPolygon(xVal, y, 50, 3, fill = color, align = 'center', border = 'Black',
                        rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif specialCardFeatures[0] == 'square':
            drawRegularPolygon(xVal, y, 50, 4, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif specialCardFeatures[0] == 'pentagon':
            drawRegularPolygon(xVal, y, 50, 5, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif specialCardFeatures[0] == 'hexagon':
            drawRegularPolygon(xVal, y, 50, 6, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)

def drawBossFeatures(app):
    startingX = 20 + app.cardWidth / 2
    y1, y2 = 200 + (app.cardLength / 2), 400 + (app.cardLength / 2)
    for i in range (app.numberOfCards):
        bossCardFeatures = []
        # Transforming letter features in boss features and adding results to a list
        for featureInd in range (len(app.displayBoard[i])):
            letter = app.displayBoard[i][featureInd]
            letInStand = ord(letter) - ord('A') # The letter index's placement in the standard theme list
            bossEquivalent = app.bossTheme[featureInd][letInStand]
            bossCardFeatures.append(bossEquivalent)
            
        # Extracting boss features from their list
        color = None
        speed = 0
        borderWidth = 5
        dashes = False
        xVal = startingX + (i * app.cardWidth)
        for feature in range (1, len(bossCardFeatures)):
            if feature == 1:
                color = bossCardFeatures[feature]
            elif feature == 2:
                speed = (app.playCount * bossCardFeatures[feature])
            elif feature == 3:
                if bossCardFeatures[feature] == 'thick':
                    borderWidth = 10
                elif bossCardFeatures[feature] == 'dashed':
                    dashes = True
            
        # Drawing the features
        y = 0
        if i % 2 == 0:
            y = y1
        else:
            y = y2
        if bossCardFeatures[0] == 'star':
            drawStar(xVal, y, 50, 5, fill = color, align = 'center', border = 'Black',
                        rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif bossCardFeatures[0] == 'triangle':
            drawRegularPolygon(xVal, y, 50, 3, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif bossCardFeatures[0] == 'diamond':
            drawRegularPolygon(xVal, y, 50, 8, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif bossCardFeatures[0] == 'oval':
            drawOval(xVal, y, 50, 40, fill = color, align = 'center', border = 'Black',
                        rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)

def checkDimsAndTheme(app):
    dimsSum = addUpListValues(app.dims)
    if (5 in app.dims) or (dimsSum == 15):
        return 'letters'
    elif (4 in app.dims) and (app.currentTheme == 'standard'):
        return 'letters'
    return app.currentTheme

def drawFeatures(app):
    theme = checkDimsAndTheme(app)
    if theme == 'letters':
        drawLetterFeatures(app)
    elif theme == 'standard':
        drawStandardFeatures(app)
    elif theme == 'special':
        drawSpecialFeatures(app)
    elif theme == 'boss':
        drawBossFeatures(app)

def indexToCard(app, l):
    result = []
    for val in l:
        card = app.displayBoard[val]
        result.append(card)
    return result

def correctCardsSelected(app):
        selected = indexToCard(app, app.indexOfcardsUserSelected)
        return isSet(selected)

def drawRectOutlines(app):
    color = gradient('grey', 'white')
    for i in range (app.numberOfCards):
        if i in app.indexOfcardsUserSelected:
            borderColor = 'red'
            dashline = True
        else:
            borderColor = 'black'
            dashline = False
        
        leftX, leftY = 20+(i * app.cardWidth), 200
        if i % 2 == 0: # Draw the rectangles on the first line
            drawRect(leftX, leftY, app.cardWidth, app.cardLength,
                        fill = color, border = borderColor, dashes = dashline)
        else: # Draw the rectangles on the second line
            drawRect(leftX, leftY + 200, app.cardWidth, app.cardLength,
                        fill = color, border = borderColor, dashes = dashline)

def playScreen_redrawAll(app):
    drawImage(app.sasuke, app.width/2, app.height/2,
                width = app.width, height = app.height, align = 'center')
    drawScreenTitle(app, 'Sasuke', app.playTextFill)
    drawLabel(f'Time spent = {app.playScreenCounter}',
              150, 70, fill='green', font = app.font, size = 20)
    drawLabel(f'Villages left to cross = {app.remainingRounds}',
              150, 110, fill='green', font = app.font, size = 20)
    drawLabel(f'Pills Left = {app.remainingLives}',
              150, 140, fill='green', font = app.font, size = 20)
    if not app.gameOver:
        drawRectOutlines(app)
        drawFeatures(app)

    # Draw chose wright/wrong cards message
    if len(app.indexOfcardsUserSelected) == app.targetNumberOfCards:
        if correctCardsSelected(app):
            drawLabel(app.chooseRightMessage, app.width/2, app.height/2,
                        font = app.font, fill = app.playTextFill, size = 50)
        else:
            drawLabel(app.chooseWrongMessage, app.width/2, app.height/2,
                        font = app.font, fill = app.playTextFill, size = 50)

def checkCardsSelected(app):
    if app.targetNumberOfCards <= (len(app.indexOfcardsUserSelected)):
        if correctCardsSelected(app):
            app.remainingRounds -= 1
        else:
            app.remainingLives -= 1
        app.indexOfcardsUserSelected = []
        app.indexOfCardSelectedOnBoard = []
        setIndexOfFoundSetOnBoard(app)
        app.displayBoard, app.cardSet = getRandomBoardWithSet(app.dims, app.numberOfCards)
        if not app.narutoGameOver:
            app.character = 'Naruto'
            playSong(app)
            setActiveScreen('narutoPlayScreen')

def playScreen_onKeyPress(app, key):
    if app.gameOver:
        return
    if key == 'h':
        if (app.remainingLives == 0) or (app.remainingRounds == 0):
            app.gameOver = True
        if app.targetNumberOfCards > (len(app.indexOfcardsUserSelected)):
            app.playScreenCounter += 15
            for i in range(app.targetNumberOfCards):
                solutionCard = app.cardSet[i]
                solutionCardIndexOnBoard = 0
                selected = indexToCard(app, app.indexOfcardsUserSelected)
                for card in selected: # Deletes one  of the cards not in foundset
                    if card not in app.cardSet:
                        for ind in range (app.numberOfCards):
                            if app.displayBoard[ind] == card:
                                app.indexOfcardsUserSelected.remove(ind)
                        return
                
                for ind in range(app.numberOfCards):
                    solutionCardIndexOnBoard = ind
                    if (app.displayBoard[ind] == solutionCard) and (ind not in app.indexOfcardsUserSelected):
                        solutionCardIndexOnBoard = ind
                        app.indexOfcardsUserSelected.append(solutionCardIndexOnBoard)
                        return
        checkCardsSelected(app)
    onKeyPressHelper(app, key)

def playScreen_onStep(app):
    if not app.gameOver:
        app.playCount += 1
        if app.playCount % 30 == 0:
            app.playScreenCounter += 1
    else:
        app.character = 'Narator'
        playSong(app)
        setActiveScreen('winnerScreen')

####################################################
# narutoPlayScreen
####################################################

def narutoStoreRectCardsPositions(app):
    for i in range (app.numberOfCards):
        leftX, leftY = 20+(i * app.cardWidth), 200
        rightX, rightY = leftX + app.cardWidth, leftY + app.cardLength
        if i % 2 == 0:
            app.narutoCardPositions.append([leftX, leftY, rightX, rightY])
        else:
            app.narutoCardPositions.append([leftX, leftY + 200, rightX, rightY + 200])
    app.narutoPositionsStored = True

def narutoInsideRect(app, mouseX, mouseY):
    if not app.narutoPositionsStored:
        narutoStoreRectCardsPositions(app)
    
    for i in range (app.numberOfCards):
        leftX, rightX = app.narutoCardPositions[i][0], app.narutoCardPositions[i][2]
        leftY, rightY = app.narutoCardPositions[i][1], app.narutoCardPositions[i][3]
        if leftX <= mouseX <= rightX:
            if (leftY <= mouseY <= rightY):
                for ind in range(len(app.narutoIndexOfcardsUserSelected)): # Checks if retangle i was previously selected and if it was, removes it from the list
                    if app.narutoIndexOfcardsUserSelected[ind] == i:
                        app.narutoIndexOfcardsUserSelected.pop(ind)
                        return
                app.narutoIndexOfcardsUserSelected.append(i)
                return True # The returned values are never used, but they could be useful in the future
    return False # The returned values are never used, but they could be useful in the future

def narutoPlayScreen_onMousePress(app, mouseX, mouseY):
    if not app.narutoGameOver:
        if len(app.narutoIndexOfcardsUserSelected) < app.targetNumberOfCards:
            narutoInsideRect(app, mouseX, mouseY)
        elif len(app.narutoIndexOfcardsUserSelected) == app.targetNumberOfCards:
            narutoCheckCardsSelected(app)
        if (app.narutoRemainingLives == 0) or (app.narutoRemainingRounds == 0):
            app.narutoGameOver = True

def narutoDrawLetterFeatures(app):
    startingX = 20 + app.cardWidth / 2
    y1, y2 = 200 + (app.cardLength / 2), 400 + (app.cardLength / 2)
    color = gradient('pink', 'white')
    
    for i in range (app.numberOfCards):
        xVal = startingX + (i * app.cardWidth)
        y = 0
        if i % 2 == 0:
            y = y1
        else:
            y = y2
        drawLabel(app.narutoDisplayBoard[i], xVal, y, fill = color, border = 'black',
                    size = 30, font = app.featureFont)

def narutoDrawStandardFeatures(app):
    startingX = 20 + app.cardWidth / 2
    y1, y2 = 200 + (app.cardLength / 2), 400 + (app.cardLength / 2)
    for i in range (app.numberOfCards):
        standardCardFeatures = []
        # Transforming letter features in standard features and adding results to a list
        for featureInd in range (len(app.narutoDisplayBoard[i])):
            letter = app.narutoDisplayBoard[i][featureInd]
            letInStand = ord(letter) - ord('A') # The letter index's placement in the standard theme list
            standardEquivalent = app.standardTheme[featureInd][letInStand]
            standardCardFeatures.append(standardEquivalent)
        # Extracting standard features from their list
        color = None
        num = 0
        opacity = 100
        width = 3
        xVal = startingX + (i * app.cardWidth)
        for feature in range (1, len(standardCardFeatures)):
            if feature == 1:
                color = standardCardFeatures[feature]
            elif feature == 2:
                num = standardCardFeatures[feature]
            elif feature == 3:
                if standardCardFeatures[feature] == 'empty':
                    opacity = 0
                elif standardCardFeatures[feature] == 'half-full':
                    opacity = 50
            
        # Drawing the features
        y = 0
        for shapes in range (num):
            if i % 2 == 0:
                y = 200 + (app.cardLength / (num + 1)) + (shapes * (app.cardLength / num)) - 10
            else:
                y = 400 + (app.cardLength / (num + 1)) + (shapes * (app.cardLength / num)) - 10
            if standardCardFeatures[0] == 'oval':
                drawOval(xVal, y, 40, 20, fill = None,
                            border = color, borderWidth = width)
                drawOval(xVal, y, 40, 20, fill = color, opacity = opacity,
                            border = color, borderWidth = width)
            elif standardCardFeatures[0] == 'star':
                drawStar(xVal, y, 20, 5, fill = None,
                            border = color, borderWidth = width)
                drawStar(xVal, y, 20, 5, fill = color, opacity = opacity,
                            border = color, borderWidth = width)
            elif standardCardFeatures[0] == 'diamond':
                drawRegularPolygon(xVal, y, 20, 4, fill = None, align = 'center', rotateAngle = 90,
                                    border = color, borderWidth = width)
                drawRegularPolygon(xVal, y, 20, 4, fill = color, align = 'center', rotateAngle = 90,
                                    opacity = opacity, border = color, borderWidth = width)

def narutoDrawSpecialFeatures(app):
    startingX = 20 + app.cardWidth / 2
    y1, y2 = 200 + (app.cardLength / 2), 400 + (app.cardLength / 2)
    for i in range (app.numberOfCards):
        specialCardFeatures = []
        # Transforming letter features in special features and adding results to a list
        for featureInd in range (len(app.narutoDisplayBoard[i])):
            letter = app.narutoDisplayBoard[i][featureInd]
            letInStand = ord(letter) - ord('A') # The letter index's placement in the standard theme list
            specialEquivalent = app.specialTheme[featureInd][letInStand]
            specialCardFeatures.append(specialEquivalent)
            
        # Extracting special features from their list
        color = None
        speed = 0
        borderWidth = 5
        dashes = False
        xVal = startingX + (i * app.cardWidth)
        for feature in range (1, len(specialCardFeatures)):
            if feature == 1:
                color = specialCardFeatures[feature]
            elif feature == 2:
                speed = ( app.narutoPlayCount * specialCardFeatures[feature])
            elif feature == 3:
                if specialCardFeatures[feature] == 'thick':
                    borderWidth = 10
                elif specialCardFeatures[feature] == 'dashed':
                    dashes = True
            
        # Drawing the features
        y = 0
        if i % 2 == 0:
            y = y1
        else:
            y = y2
            
        if specialCardFeatures[0] == 'triangle':
            drawRegularPolygon(xVal, y, 50, 3, fill = color, align = 'center', border = 'Black',
                        rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif specialCardFeatures[0] == 'square':
            drawRegularPolygon(xVal, y, 50, 4, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif specialCardFeatures[0] == 'pentagon':
            drawRegularPolygon(xVal, y, 50, 5, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif specialCardFeatures[0] == 'hexagon':
            drawRegularPolygon(xVal, y, 50, 6, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)

def narutoDrawBossFeatures(app):
    startingX = 20 + app.cardWidth / 2
    y1, y2 = 200 + (app.cardLength / 2), 400 + (app.cardLength / 2)
    for i in range (app.numberOfCards):
        bossCardFeatures = []
        # Transforming letter features in boss features and adding results to a list
        for featureInd in range (len(app.narutoDisplayBoard[i])):
            letter = app.narutoDisplayBoard[i][featureInd]
            letInStand = ord(letter) - ord('A') # The letter index's placement in the standard theme list
            bossEquivalent = app.bossTheme[featureInd][letInStand]
            bossCardFeatures.append(bossEquivalent)
            
        # Extracting boss features from their list
        color = None
        speed = 0
        borderWidth = 5
        dashes = False
        xVal = startingX + (i * app.cardWidth)
        for feature in range (1, len(bossCardFeatures)):
            if feature == 1:
                color = bossCardFeatures[feature]
            elif feature == 2:
                speed = (app.narutoPlayCount * bossCardFeatures[feature])
            elif feature == 3:
                if bossCardFeatures[feature] == 'thick':
                    borderWidth = 10
                elif bossCardFeatures[feature] == 'dashed':
                    dashes = True
            
        # Extracting boss features from their list
        color = None
        speed = 0
        borderWidth = 5
        dashes = False
        xVal = startingX + (i * app.cardWidth)
        for feature in range (1, len(bossCardFeatures)):
            if feature == 1:
                color = bossCardFeatures[feature]
            elif feature == 2:
                speed = (app.narutoPlayCount * bossCardFeatures[feature])
            elif feature == 3:
                if bossCardFeatures[feature] == 'thick':
                    borderWidth = 10
                elif bossCardFeatures[feature] == 'dashed':
                    dashes = True
        # Drawing the features
        y = 0
        if i % 2 == 0:
            y = y1
        else:
            y = y2
        if bossCardFeatures[0] == 'star':
            drawStar(xVal, y, 50, 5, fill = color, align = 'center', border = 'Black',
                        rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif bossCardFeatures[0] == 'triangle':
            drawRegularPolygon(xVal, y, 50, 3, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif bossCardFeatures[0] == 'diamond':
            drawRegularPolygon(xVal, y, 50, 8, fill = color, align = 'center', border = 'Black',
                                rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)
        elif bossCardFeatures[0] == 'oval':
            drawOval(xVal, y, 50, 40, fill = color, align = 'center', border = 'Black',
                        rotateAngle = speed, borderWidth = borderWidth, dashes = dashes)

def narutoCheckDimsAndTheme(app):
    dimsSum = addUpListValues(app.dims)
    if (5 in app.dims) or (dimsSum == 15):
        return 'letters'
    elif (4 in app.dims) and (app.currentTheme == 'standard'):
        return 'letters'
    return app.currentTheme

def narutoDrawFeatures(app):
    theme = checkDimsAndTheme(app)
    if theme == 'letters':
        narutoDrawLetterFeatures(app)
    elif theme == 'standard':
        narutoDrawStandardFeatures(app)
    elif theme == 'special':
        narutoDrawSpecialFeatures(app)
    elif theme == 'boss':
        narutoDrawBossFeatures(app)

def narutoIndexToCard(app, l):
    result = []
    for val in l:
        card = app.narutoDisplayBoard[val]
        result.append(card)
    return result

def narutoCorrectCardsSelected(app):
        selected = narutoIndexToCard(app, app.narutoIndexOfcardsUserSelected)
        return isSet(selected)

def narutoDrawRectOutlines(app):
    color = gradient('grey', 'white')
    for i in range (app.numberOfCards):
        if i in app.narutoIndexOfcardsUserSelected:
            borderColor = 'red'
            dashline = True
        else:
            borderColor = 'black'
            dashline = False
        
        leftX, leftY = 20+(i * app.cardWidth), 200
        if i % 2 == 0: # Draw the rectangles on the first line
            drawRect(leftX, leftY, app.cardWidth, app.cardLength,
                        fill = color, border = borderColor, dashes = dashline)
        else: # Draw the rectangles on the second line
            drawRect(leftX, leftY + 200, app.cardWidth, app.cardLength,
                        fill = color, border = borderColor, dashes = dashline)

def narutoPlayScreen_redrawAll(app):
    drawImage(app.naruto, app.width/2, app.height/2,
                    width = app.width, height = app.height, align = 'center')
    drawScreenTitle(app, 'Naruto', app.playTextFill)
    drawLabel(f'Time spent = {app.narutoPlayScreenCounter}',
              150, 70, fill='green', font = app.font, size = 20)
    drawLabel(f'Villages left to cross = {app.narutoRemainingRounds}',
              150, 110, fill='green', font = app.font, size = 20)
    drawLabel(f'Pills Left = {app.narutoRemainingLives}',
              150, 140, fill='green', font = app.font, size = 20)
    if not app.narutoGameOver:
        narutoDrawRectOutlines(app)
        narutoDrawFeatures(app)

    # Draw chose wright/wrong cards message
    if len(app.narutoIndexOfcardsUserSelected) == app.targetNumberOfCards:
        if narutoCorrectCardsSelected(app):
            drawLabel(app.chooseRightMessage, app.width/2, app.height/2,
                        font = app.font, fill = app.playTextFill, size = 50)
        else:
            drawLabel(app.chooseWrongMessage, app.width/2, app.height/2,
                        font = app.font, fill = app.playTextFill, size = 50)

def narutoCheckCardsSelected(app):
    if app.targetNumberOfCards <= (len(app.narutoIndexOfcardsUserSelected)):
        if narutoCorrectCardsSelected(app):
            app.narutoRemainingRounds -= 1
        else:
            app.narutoRemainingLives -= 1
        app.narutoIndexOfcardsUserSelected = []
        app.narutoIndexOfCardSelectedOnBoard = []
        narutoSetIndexOfFoundSetOnBoard(app)
        app.narutoDisplayBoard, app.narutoCardSet = getRandomBoardWithSet(app.dims, app.numberOfCards)
        if not app.gameOver:
            app.character = 'Sasuke'
            playSong(app)
            setActiveScreen('playScreen')

def narutoPlayScreen_onKeyPress(app, key):
    if app.narutoGameOver:
        return
    if key == 'h':
        if (app.narutoRemainingLives == 0) or (app.narutoRemainingRounds == 0):
            app.narutoGameOver = True
        if app.narutoTargetNumberOfCards > (len(app.narutoIndexOfcardsUserSelected)):
            app.narutoPlayScreenCounter += 15
            for i in range(app.targetNumberOfCards):
                solutionCard = app.narutoCardSet[i]
                solutionCardIndexOnBoard = 0
                selected = narutoIndexToCard(app, app.narutoIndexOfcardsUserSelected)
                for card in selected: # Deletes one  of the cards not in foundset
                    if card not in app.narutoCardSet:
                        for ind in range (app.numberOfCards):
                            if app.narutoDisplayBoard[ind] == card:
                                app.narutoIndexOfcardsUserSelected.remove(ind)
                        return
                
                for ind in range(app.numberOfCards):
                    solutionCardIndexOnBoard = ind
                    if (app.narutoDisplayBoard[ind] == solutionCard) and (ind not in app.narutoIndexOfcardsUserSelected):
                        solutionCardIndexOnBoard = ind
                        app.narutoIndexOfcardsUserSelected.append(solutionCardIndexOnBoard)
                        return
        narutoCheckCardsSelected(app)
    onKeyPressHelper(app, key)

def narutoPlayScreen_onStep(app):
    if not app.narutoGameOver:
        app.narutoPlayCount += 1
        if app.narutoPlayCount % 30 == 0:
            app.narutoPlayScreenCounter += 1
    # elif not app.gameOver:
    #     app.gameOverCount += 1
    #     if app.gameOverCount % 150 == 0:
    #         app.character = 'Sasuke'
    #         playSong(app)
    #         setActiveScreen('playScreen')
    else:
        app.character = 'Sasuke'
        playSong(app)
        setActiveScreen('winnerScreen')

###############################################
# resetscreen
###############################################             
def resetScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = app.manualBackgroung)
    drawScreenTitle(app, 'Restart', app.manualTextFill)
    drawLabel("Are you sure you want to reset the game? (type yes or no)",
              app.width/2, app.height/2, size=30, fill = app.manualTextFill, font = app.font)
    drawLabel(app.typingRestartResponse, app.width/2, app.height/2 + 90, size=30,
                fill = app.manualTextFill, font = app.font)
    if app.drawErroMessage:
        drawLabel("I dont't get that. Try typing 'yes' or 'no' in all lowercase.",
              app.width/2, app.height/2 + 180, size=30, fill = app.manualTextFill, font = app.font)

def resetScreen_onKeyPress(app, key):
    if key == 'backspace':
        app.typingRestartResponse = app.typingRestartResponse[:-1]
    elif key == 'enter':
        if app.typingRestartResponse == 'yes':
            reset(app)
            setActiveScreen('welcomeScreen')
        elif app.typingRestartResponse == 'no':
            app.typingRestartResponse = ''
            setActiveScreen('helpScreen')
        else:
            app.drawErroMessage = True
    elif key.isalpha():
        app.typingRestartResponse += key

####################################################
# winnersscreen
####################################################
def winnerScreen_redrawAll(app):
    if app.gameOver and app.narutoGameOver:
        drawLabel("Press 'r' to restart", app.width/2, 20, size = 20,
                    fill = app.winnerFill, font = app.font)
        if app.showFastest:
            if app.playScreenCounter == app.narutoPlayScreenCounter:
                drawImage(app.kakashi, app.width/2, app.height/2,
                            width = app.width, height = app.height, align = 'center')
                message = f'Same speed!!!!. \n You Completed the mission in {app.playScreenCounter} seconds.'
                rand = 0
                for i in message.splitlines():
                    drawLabel(i, app.width/2, app.height/2 + (rand * 50),
                                    font = app.font, fill = app.winnerFill, size = 50)
                    rand += 1
            else:
                winner = 'Naruto'
                image = app.jiraiya
                time = app.narutoPlayScreenCounter
                if app.playScreenCounter < app.narutoPlayScreenCounter:
                    winner = 'Sasuke'
                    image = app.itachi
                    time = app.playScreenCounter
                drawImage(image, app.width/2, app.height/2,
                            width = app.width, height = app.height, align = 'center')
                message = f'{winner} your mission ended in {time}'
                rand = 0
                for i in message.splitlines():
                    drawLabel(i, app.width/2, app.height/2 + (rand * 50),
                                    font = app.font, fill = app.winnerFill, size = 50)
                    rand += 1
    
        else:
            if app.remainingLives == app.narutoRemainingLives:
                drawImage(app.kakashi, app.width/2, app.height/2,
                            width = app.width, height = app.height, align = 'center')
                message = f'Well kids, you tied once again.\n You both held onto {app.remainingLives} pills.'
                rand = 0
                for i in message.splitlines():
                    drawLabel(i, app.width/2, app.height/2 + (rand * 50),
                            font = app.font, fill = app.winnerFill, size = 50)
                    rand += 1
            else:
                winner = 'Naruto'
                loser = 'Sasuke'
                image = app.jiraiya
                numPills = app.narutoPlayScreenCounter - app.playScreenCounter
                if app.playScreenCounter < app.narutoPlayScreenCounter:
                    winner = 'Sasuke'
                    loser = 'Naruto'
                    image = app.itachi
                    numPills = app.remainingLives - app.narutoRemainingLives
                drawImage(image, app.width/2, app.height/2,
                            width = app.width, height = app.height, align = 'center')
                message = f'Nice work {winner},\n you held on to {numPills} more pills left than {loser}.'
                rand = 0
                for i in message.splitlines():
                    drawLabel(i, app.width/2, app.height/2 + (rand * 50),
                                    font = app.font, fill = app.winnerFill, size = 50)
                    rand += 1

def winnerScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)
    
def winnerScreen_onStep(app):
    app.winnerCount += 1
    if app.winnerCount % 300 == 0:
        app.showFastest = not app.showFastest

###############################################
# Functions copied from console-based app
###############################################

# Copy-Paste required code from console-based app here!
# Just copy your helper functions along with stringProduct() and
# combinations().  You do not need to copy the
# "Console-Based playSuperSet (for debugging)" section.

def stringProduct(L):
    resultTuples = list(itertools.product(*L))
    resultStrings = [''.join(t) for t in resultTuples]
    return resultStrings

def combinations(L, n):
    return [list(v) for v in itertools.combinations(L, n)]

def allSame(L):
    firstVal = L[0]
    for index in range(1, len(L)):
        if L[index] != firstVal:
            return False
    return True

def allDiffer(L):
    prevVal = L[0]
    for start in range (len(L) - 1):
        for end in range (start + 1, len(L)):
            if L[start] == L[end]:
                return False
    return True

def isSet(cards):
    lenVal = len(cards[0]) # length of each value in L
    for ind in range (lenVal):
        option = []
        for val in cards:
            option.append(val[ind])
        if not allDiffer(option):
            if not allSame(option):
                return False
    return True

def makeSuperSetDeck(dims):
    deck = []
    for i in range (len(dims)):
        subDim = '' # All dimentions in terms of letters (AB, ABC, etc...)
        for val in range (dims[i]):
            boundedI = val % 26
            shift = ord('A') + boundedI
            letter = chr(shift)
            subDim += letter
        deck.append(subDim)
    deck = stringProduct(deck)
    return deck

def boardContainsSelection(board, selection):
    for card in selection:
        if card not in board:
            return False
    return True

def areDuplicates(selection):
    for start in range (len(selection) - 1):
        for end in range (start + 1, len(selection)):
            if selection[start] == selection[end]:
                return True
    return False

def checkSelectionIsSet(board, selection, cardsPerSet):
    if board == []:
        return 'Empty board!'
    elif len(selection) != cardsPerSet:
        return 'Wrong number of cards!'
    elif not boardContainsSelection(board, selection):
        return 'Some of those cards are not on the board!'
    elif not isSet(selection):
        return 'Those cards do not form a set!'
    elif areDuplicates(selection):
        return 'Some of those cards are duplicates!'
    return True

def findFirstSet(board, cardsPerSet):
    possibleSets = combinations(board, cardsPerSet)
    for candidate in possibleSets:
        if isSet(candidate):
            return candidate

def dealUntilSetExists(deck, cardsPerSet):
    board = []
    firstSet = None
    count = 0
    while firstSet == None:
        board.append(deck[count])
        count += 1
        if count >= cardsPerSet:
            firstSet = findFirstSet(board, cardsPerSet)
    firstSet = sorted(firstSet)
    return firstSet

def getRandomBoardWithSet(dims, targetBoardSize):
    deck = makeSuperSetDeck(dims)
    random.shuffle(deck)
    cardsPerSet = min(dims)
    foundSet = dealUntilSetExists(deck, cardsPerSet)
    board = copy.copy(foundSet)
    currentBoardSize = len(foundSet)
    deckIndex = 0
    while currentBoardSize < targetBoardSize:
        if deck[deckIndex] not in board:
            board.append(deck[deckIndex])
            currentBoardSize += 1
        deckIndex += 1
    board = sorted(board)
    return (board, foundSet)
    
####################################################
# main function
####################################################

def main():
    runAppWithScreens(initialScreen='welcomeScreen')

main()
