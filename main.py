"""
-- EN COURS
Changelog 6:
	Corrections diverses
	Transition entre les vagues
	Menu et sélection des niveaux
	Game over
	Setup niveaux 1, 2 et 3
	Amélioration IA
	Ennemies 3 et 4?
"""

import inspect
from game import *
from menu import *
from guide import * 
from select import *
from gl0bals import *

# fonction temporaire
def clearall():
	all = [var for var in globals() if var[0] != "_" and inspect.isclass(var)]
	for var in all:
		del globals()[var]


pygame.init()
screen = Screen()

Globals.launched = True

while Globals.launched:

	if Globals.ecran == "game":
		game_initialize()
		while Globals.ecran == "game" and Globals.launched:
			game_body(screen)
			game_display(screen)
		# vidage de la mémoire
		Globals.blocks = []
		Globals.enemies1 = []
		Globals.enemies2 = []
		Globals.enemies3 = []
		Globals.enemies = []
		Globals.projectiles = []
		Globals.mists = []
		Globals.transition = Globals.TRANSITION

	elif Globals.ecran == "menu":
		menu_initialize()
		while Globals.ecran == "menu" and Globals.launched:
			menu_body(screen)
			menu_display(screen)

	elif Globals.ecran == "select":
		select_initialize()
		while Globals.ecran == "select" and Globals.launched:
			select_body(screen)
			select_display(screen)

	elif Globals.ecran == "guide":
		guide_initialize()
		while Globals.ecran == "guide" and Globals.launched:
			guide_body(screen)
			guide_display(screen)

pygame.quit()