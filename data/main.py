import time

import pygame
from numpy import ndarray, array
from pygame.surface import Surface
from pygame.time import Clock

from data.objects.beam_code import update_beam, fire_beam, get_beam_velocity, display_beam
from data.objects.beam_data import Beam
from data.objects.camera_code import update_camera
from data.objects.camera_data import Camera
from data.objects.goal_code import update_goal, display_goal
from data.objects.player_code import update_player, display_player
from data.objects.tile_code import display_tiles
from data.utils.constants import FPS, CURSOR_SPRITE, CURSOR_SIZE, SCREEN_SIZE
from data.utils.functions import generate_world, get_screen_grid


def main() -> None:
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Goodoo")
    pygame.mouse.set_visible(False)

    tile_grid, player, goal = generate_world()
    beam: Beam = Beam()
    camera: Camera = Camera()

    clock: Clock = pygame.time.Clock()
    last_time: float = time.time()

    on_ground: bool = False

    while True:

        # ------
        # Events
        # ------

        click: bool = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # ------------
        # Model update
        # ------------

        delta: float = (time.time() - last_time) * FPS
        last_time = time.time()

        # using an alternate variable rather than player.on_ground
        # because it keeps looping to true/false when on ground due to rect collision
        if player.on_ground:
            on_ground = True

        camera = update_camera(camera, array(player.rect.center), delta)

        beam = update_beam(beam, player, tile_grid, camera.offset, delta)
        if click and on_ground:
            beam = fire_beam(beam)
            on_ground = False

        player = update_player(player, get_beam_velocity(beam), tile_grid, delta)

        # game ends if goal is reached
        if player.rect.colliderect(goal.rect):
            pygame.quit()
            quit()

        goal = update_goal(goal)

        # -------
        # display
        # -------

        screen: Surface = pygame.display.get_surface()
        screen.fill((0, 0, 0))  # refresh screen

        display_goal(goal, screen, camera.offset)
        display_beam(beam, screen, camera.offset)
        display_player(player, screen, camera.offset)

        # only displays tiles visible on screen
        visible_tiles: ndarray = get_screen_grid(tile_grid, camera)
        display_tiles(visible_tiles, screen, camera_offset=camera.offset)

        # display cursor
        cursor_pos: ndarray = array(pygame.mouse.get_pos()) - CURSOR_SIZE * 0.5
        screen.blit(CURSOR_SPRITE, cursor_pos)

        pygame.display.flip()
        clock.tick(FPS)
        # print(int(clock.get_fps()))
