import pygame
from environnements import *

"""
Changelog 3:
	Collision entre le joueur et le décor
	Passage en programmation orientée objet -- IMPORTANT
"""


#========== INITIALISATION VARIABLES GLOBALES ==========

ratio = 20 # ratio écran/grille
fps = 60 # images par seconde
counter = 0 # compteur de boucle

# COULEURS
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
green = (0,255,0)
cyan = (0,255,255)
blue = (0,0,255)
purple = (255,0,255)



#========== OBJETS ==========

class Screen():

	def __init__(self):

		self.resolution = (1280,720)
		self.surface = pygame.display.set_mode((self.resolution))
		self.fullscreen = False
		self.icon = pygame.image.load("ressources/icon.jpg")
		pygame.display.set_icon(self.icon) # icône de la fenêtre
		pygame.display.set_caption("Goodoo") # titre de la fenêtre



class Block():

	def __init__(self, pos):

		blocks.append(self) # est ajouté à la liste de tout les blocs
		self.rect = pygame.Rect((pos[0], pos[1]),(ratio,ratio))



class Player():

	def __init__(self, x, y):

		self.width = 1
		self.x = x
		self.y = y
		self.rect = pygame.Rect((self.x*ratio, self.y*ratio), (self.width*ratio,self.width*ratio)) # hitbox
		self.sprites_right = [ pygame.image.load("ressources/goodoo_white/goodoo1.png"),
							pygame.image.load("ressources/goodoo_white/goodoo2.png")]
		self.sprites_left = [ pygame.image.load("ressources/goodoo_white/goodoo3.png"),
							pygame.image.load("ressources/goodoo_white/goodoo4.png")]
		self.animation_counter = 0
		self.sprite = self.sprites_right[self.animation_counter] # sprite courant
		self.last_move = "right"
		self.velocity = list([(i / 20.0) - 1 for i in range(0, 40)]) # plage des vitesses
		self.velocity_index = len(self.velocity)//2 # rang de la plage de vitesse, permet l'accélération
		self.velocity_fixed = 0.2 #self.velocity[1*len(self.velocity)//2 + 1] # rang fixe de la plage de vitesse -- DOIT ETRE SUPERIEUR A 0.5
		self.isjump = False
		self.onground = False
		self.iscollide = False
		self.blockcollide = pygame.Rect( (0, 0) , (0, 0) )
		


	def move(self, vx, vy):
		"""Bouge chaque axe séparemment"""

		if vx != 0:
			self.move_single_axis(vx, 0)
		if vy != 0:
			self.move_single_axis(0, vy)


	def move_single_axis(self, vx, vy):
		"""Bouge en fonction de vx et vy"""

		self.iscollide = False

		# bouge le rect
		self.rect.x += vx*ratio
		self.rect.y += vy*ratio

		# Si collision avec un bloc, se repositionne
		
		for block in blocks:
			if self.rect.colliderect(block.rect):
				self.iscollide = True
				self.blockcollide = block.rect
				if vx > 0:
					self.rect.right = block.rect.left
				if vx < 0:
					self.rect.left = block.rect.right
				if vy > 0:
					self.rect.bottom = block.rect.top
				if vy < 0:
					self.rect.top = block.rect.bottom



	def jump(self):

		if self.isjump:
			self.move_single_axis(0, self.velocity[self.velocity_index])
			self.velocity_index += 1

			if (self.velocity_index >= len(self.velocity)-1):
				self.velocity_index = len(self.velocity)-1

			for block in blocks:
				if self.iscollide == True:

					if self.rect.bottom == block.rect.top:
						self.isjump = False
						self.velocity_index = 0

					if self.rect.top == block.rect.bottom:
						self.velocity_index = len(self.velocity)//2


	def gravity(self):

		self.onground = False

		if self.iscollide and self.blockcollide.top==self.rect.bottom :
			self.onground = True
			self.velocity_index = len(self.velocity)//2

		if not self.onground :
			self.move_single_axis(0, self.velocity[self.velocity_index])
			self.velocity_index += 1

		if (self.velocity_index >= len(self.velocity)-1):
			self.velocity_index = len(self.velocity)-1



	def animation(self, last_move):
		"""Oriente le joueur selon son dernier mouvement"""

		# on passe au sprite suivant toute les 30 images
		if counter%30 == 0:
			self.animation_counter += 1
		# on revient au premier sprite une fois le 2e sprite passé
		if self.animation_counter >= len(self.sprites_right):
			self.animation_counter = 0

		if last_move=="right" :
			self.sprite = self.sprites_right[self.animation_counter]

		elif last_move=="left" :
			self.sprite = self.sprites_left[self.animation_counter]



#========== INITIALISATION PYGAME ==========

pygame.init()

# FENETRE
screen = Screen()

# ENVIRONNEMENT
tab = tab4 # tableau de 1 et 0 du niveau, cf envirronements.py
blocks = [] # liste qui sitock des blocs de l'environnement
# créer tout les blocs de l'environnement
for i in range(0,len(tab)):
	for j in range(0,len(tab[0])):
		if tab[i][j]==1:
			Block( (j*ratio , i*ratio) )

# JOUEUR
player = Player(47.0,2.0)

# MUSIQUE
#pygame.mixer.music.load("ressources/S.Rachmaninov - prelude op 23 no 5.wav")

# HORLOGE
clock = pygame.time.Clock()


#========== CORPS DU PROGRAMME ==========

#pygame.mixer.music.play()
launched = True

while launched:


	# EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			launched = False


	keys = pygame.key.get_pressed()

	# CONTROLE TOUCHES FENETRE
	if keys[pygame.K_ESCAPE]:
		launched = False
	if keys[pygame.K_F11] and screen.fullscreen==False:
		screen.surface = pygame.display.set_mode(screen.resolution, pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		screen.fullscreen = True
	elif keys[pygame.K_F11] and screen.fullscreen==True:
		screen.surface = pygame.display.set_mode(screen.resolution)
		pygame.mouse.set_visible(True)
		screen.fullscreen = False

	# CONTROLE TOUCHES JOUEUR
	if keys[pygame.K_LEFT]:
		if not(keys[pygame.K_RIGHT]):
			player.last_move = "left"
		player.move(-player.velocity_fixed, 0)
	if keys[pygame.K_RIGHT]:
		if not(keys[pygame.K_LEFT]):
			player.last_move = "right"
		player.move(player.velocity_fixed, 0)

	"""
	if keys[pygame.K_UP]:
		player.move(0, -player.velocity_fixed)
	if keys[pygame.K_DOWN]:
		player.move(0, player.velocity_fixed)
	"""

	player.gravity()

	"""
	if player.isjump == False :
		player.gravity()
	if keys[pygame.K_SPACE] and player.isjump == False:
		player.isjump = True
		player.velocity_index = 0
	if player.isjump == True:
		player.jump()
	"""

	print(player.velocity[player.velocity_index])


	# DESSIN DES SURFACES
	screen.surface.fill(black)
	# dessine tout les blocs de la liste blocks
	for block in blocks:
		pygame.draw.rect(screen.surface, white, block.rect)
	#pygame.draw.rect(screen.surface, red, player.rect) # hitbox
	player.animation(player.last_move)
	screen.surface.blit(player.sprite, (player.rect.x, player.rect.y) )

	pygame.display.flip() # actualisation de l'écran



	counter += 1
	clock.tick(fps) # 60 fps


pygame.quit()