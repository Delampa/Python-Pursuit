from graphics import *
import simpleaudio as sa
import time

import grid
import snake
import food

mainWindow = GraphWin("G2", width=480, height=480)
mainWindow.setBackground('black')

# windowRect = Rectangle(Point(0, 0), Point(mainWindow.width, mainWindow.height))
windowRect = Rectangle(Point(16, 32), Point(380, 460))

mainGrid = grid.Grid(windowRect, 20, 20)
mainGrid.draw(mainWindow)

player = snake.Snake(mainGrid, Point(mainGrid.gridX//2, mainGrid.gridY//2))
player.isOver = True
player.draw(mainWindow)

scoreText = Text(Point(432, 40), 'SCORE: 0')
scoreText.setTextColor('white')
scoreText.draw(mainWindow)

highscoreText = Text(Point(432, 60), 'HIGH: 0')
highscoreText.setTextColor('white')
highscoreText.draw(mainWindow)
highscoreVal = 0

pauseText = Text(Point(16 + (380/2), 32 + (460/2)), 'Pause')
pauseText.setStyle('bold')
pauseText.setTextColor('white')
pauseText_drawn = False
# pauseText.draw(mainWindow)

# gameOverText = Text(pauseText.anchor, 'GAME OVER')
gameOverText = Text(pauseText.anchor, 'PYTHON PURSUIT')
gameOverText.setTextColor('white')
gameOverText.setStyle('bold')
gameOverText.draw(mainWindow)

# gameOver2Text = Text(Point(pauseText.getAnchor().x, pauseText.getAnchor().y + 24), 'Press \'p\' to try again.')
gameOver2Text = Text(Point(pauseText.getAnchor().x, pauseText.getAnchor().y + 24), 'Press \'p\' to play.')
gameOver2Text.setTextColor('white')
gameOver2Text.draw(mainWindow)

# Difficulties
diffTextStringList: list[str] = ['NORMAL', 'HARD']
diffTextList: list[Text] = []
diffSelectionID = 0
diffSelectionDelay = 0
normalDiffText = Text(Point(gameOver2Text.getAnchor().x, gameOver2Text.getAnchor().y + 36), diffTextStringList[0])
normalDiffText.setTextColor('white')
normalDiffText.setStyle('bold')
hardDiffText = Text(Point(normalDiffText.getAnchor().x, normalDiffText.getAnchor().y + 20), diffTextStringList[1])
hardDiffText.setTextColor('white')
hardDiffText.setStyle('bold')

diffTextList.append(normalDiffText)
diffTextList.append(hardDiffText)
diffTextList[diffSelectionID].setTextColor('yellow')
diffTextList[diffSelectionID].setText(f'[{diffTextStringList[diffSelectionID]}]')
for txt in diffTextList:
	txt.draw(mainWindow)

food = food.Food(mainGrid)
food.draw(mainWindow)

def toggleDiffTextVisibility(isVisible: bool):
	if isVisible:
		for txt in diffTextList:
			txt.draw(mainWindow)
	else:
		for txt in diffTextList:
			txt.undraw()

def selectDiffID(val: int):
	global diffSelectionID
	global diffSelectionDelay
	diffTextList[diffSelectionID].setTextColor('white')
	diffTextList[diffSelectionID].setText(diffTextStringList[diffSelectionID])
	diffSelectionID = (diffSelectionID + val) % len(diffTextList)
	diffTextList[diffSelectionID].setTextColor('yellow')
	diffTextList[diffSelectionID].setText(f'[{diffTextStringList[diffSelectionID]}]')
	diffSelectionDelay = 0.25

# SFX
# Audios originated from free-sound-effects.net
eatSound = sa.WaveObject.from_wave_file('assets/eat.wav')
highscoreSound = sa.WaveObject.from_wave_file('assets/highscore.wav')
gameOverSound = sa.WaveObject.from_wave_file('assets/gameOver.wav')

musicSound = sa.WaveObject.from_wave_file('assets/music.wav')
musicSoundPlay: sa.PlayObject = None

# fpsCounter = 0
# fpsDelta = 0
prevTime = time.time()
while True:
	now = time.time()
	delta = (now - prevTime)
	prevTime = now

	# fpsDelta += delta
	# fpsCounter += 1
	# if(fpsDelta >= 1):
	#     print(f'FPS: {fpsCounter}')
	#     fpsCounter = 0
	#     fpsDelta = 0

	if diffSelectionDelay >= 0:
		diffSelectionDelay -= delta
	key = mainWindow.checkKey()
	if(key == 'Escape'):
		break
	elif(key == 'Up'):
		if(player.isOver and diffSelectionDelay <= 0):
			selectDiffID(-1)
		else:
			if(player.facing != 2):
				player.facing = 0
	elif(key == 'Right' and player.facing != 3):
		player.facing = 1
	elif(key == 'Down'):
		if(player.isOver and diffSelectionDelay <= 0):
			selectDiffID(1)
		else:
			if(player.facing != 0):
				player.facing = 2
	elif(key == 'Left' and player.facing != 1):
		player.facing = 3
	elif(key == 'p'):
		if(player.isOver == False):
			player.isPaused = not player.isPaused
		else:
			if(musicSoundPlay == None):
				musicSoundPlay = musicSound.play()
			else:
				musicSoundPlay.stop()
				musicSoundPlay = musicSound.play()

			player.isOver = False
			food.undraw()
			mainGrid.undrawWall()
			mainGrid.clearWall()
			player.resetGame(True)
			player.moveDelay = player.MOVECONSTANT
			if(diffSelectionID == 1):
				for _ in range(15):
					mainGrid.createWall(player.startP)
				mainGrid.drawWall(mainWindow)
			scoreText.setText(f'SCORE: {player.score}')
			food.reset()
			while(player.isFoodInsideSnake(food) or food.isInsideWall()):
				food.reset()
			food.draw(mainWindow)
			gameOverText.undraw()
			gameOver2Text.undraw()
			toggleDiffTextVisibility(False)
	
	# MUSIC LOOP
	if(musicSoundPlay is not None):
		if(not musicSoundPlay.is_playing() and not player.isOver):
			musicSoundPlay.stop()
			musicSoundPlay = musicSound.play()

	if(player.update(delta)):
		player.undraw()
		
		if(player.isFoodInsideSnake(food)):
			player.expandSnake(food.foodCol)
			food.undraw()
			food.reset()
			while(player.isFoodInsideSnake(food)):
				food.reset()
			player.score += 1
			if(player.score % player.FoodPerSpeedup == 0):
				player.moveDelay -= player.moveDelay/4
			scoreText.setText(f'SCORE: {player.score}')
			food.draw(mainWindow)
			
			eatSound.play()

		player.draw(mainWindow)
		if(player.isOutsideOfGrid() or player.isSnakeInsideSnake() or player.isTouchingWall()):
			musicSoundPlay.stop()
			if(player.score > highscoreVal):
				gameOverText.setText('NEW HIGHSCORE')
				gameOverText.setTextColor('yellow')
				highscoreSound.play()
			else:
				gameOverText.setText('GAME OVER')
				gameOverText.setTextColor('white')
				gameOverSound.play()
			gameOver2Text.setText('Press \'p\' to try again.')
			gameOverText.draw(mainWindow)
			gameOver2Text.draw(mainWindow)
			player.isOver = True
			toggleDiffTextVisibility(True)
			if(player.score > highscoreVal):
				highscoreVal = player.score
				highscoreText.setText(f'HIGH: {highscoreVal}')
			player.score = 0
			scoreText.setText(f'SCORE: {player.score}')
		
	if(not player.isPaused and pauseText_drawn):
		pauseText.undraw()
		pauseText_drawn = False
	elif(player.isPaused and not pauseText_drawn):
		pauseText.draw(mainWindow)
		pauseText_drawn = True

	mainWindow.update()
	time.sleep(0.01)