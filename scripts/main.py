import pygame as py
from button import Button
from screen import Screen


# INITIALIZATION OF THE PYGAME
py.init()
# INITIALIZATION OF SYSTEM FONTS
py.font.init()

# CREATING THE OBJECT OF THE
# CLASS Screen FOR MENU SCREEN
menuScreen = Screen("Menu Screen")

# CREATING THE OBJECT OF THE
# CLASS Screen FOR GAME SCREEN
game_bar = Screen("Game Screen")

# CALLING OF THE FUNCTION TO
# MAKE THE SCREEN FOR THE WINDOW
win = menuScreen.makeCurrentScreen()

# MENU BUTTON
MENU_BUTTON = Button(150, 150, 150, 50, (255, 250, 250),
					(255, 0, 0), "TimesNewRoman",
					(255, 255, 255), "Main Menu")

# CONTROL BUTTON
CONTROL_BUTTON = Button(150, 150, 150, 50,
						(0, 0, 0), (0, 0, 255),
						"TimesNewRoman",
						(255, 255, 255), "Back")

done = False

toggle = False

# MAIN LOOPING
while not done:
	# CALLING OF screenUpdate 
	# function FOR MENU SCREEN
	menuScreen.screenUpdate()
	
	# CALLING THE FUNCTION OF CONTROL BAR
	game_bar.screenUpdate()
	# STORING THE MOUSE EVENT TO
	# CHECK THE POSITION OF THE MOUSE
	mouse_pos = py.mouse.get_pos()
	# CHECKING THE MOUSE CLICK EVENT
	mouse_click = py.mouse.get_pressed()
	# KEY PRESSED OR NOT
	keys = py.key.get_pressed()

# MENU BAR CODE TO ACCESS
	# CHECKING MENU SCREEN FOR ITS UPDATE
	if menuScreen.checkUpdate((25, 0, 255)):
		game_barbutton = MENU_BUTTON.focusCheck(mouse_pos,
												mouse_click)
		MENU_BUTTON.showButton(menuScreen.returnTitle())

		if game_barbutton:
			win = game_bar.makeCurrentScreen()
			menuScreen.endCurrentScreen()

	# CONTROL BAR CODE TO ACCESS
	# CHECKING CONTROL SCREEN FOR ITS UPDATE
	elif game_bar.checkUpdate((255, 0, 255)):
		return_back = CONTROL_BUTTON.focusCheck(mouse_pos,
												mouse_click)
		CONTROL_BUTTON.showButton(game_bar.returnTitle())

		if return_back:
			game_bar.endCurrentScreen()
			win = menuScreen.makeCurrentScreen()
			
	# CHECKING IF THE EXIT BUTTON HAS BEEN CLICKED OR NOT
	for event in py.event.get():
	
		# IF CLICKED THEN CLOSE THE WINDOW
		if(event.type == py.QUIT):
			done = True

	py.display.update()
	
# CLOSE THE PROGRAM
py.quit()
