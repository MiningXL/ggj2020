#   Global Game Jam 2020
#   2020-01-31 bis 2020-02-03

# im
import os
import pygame
from map import Map
from render import RenderGrid, RenderUnits, SQRT3



# define secondary functions
def _grid(surface, grid):


    surface.fill(pygame.Color('white'))
    grid.draw()

    surface.blit(grid, (0, 0))

    #m.units[(0, 0)] = Unit(m)
    #m.units[(3, 2)] = Unit(m)



    #pygame.draw.rect(surface, (255,0,0), ((50,50),(100,100)))

# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("First Try")

    # Define Screen Size
    disp_height = 600
    disp_width = 800
    screen = pygame.display.set_mode((disp_width, disp_height))

    # define a variable to control the main loop
    running = True

    current_path = os.path.dirname(__file__)

    grid_horizontal = 15
    grid_vertical = 20
    m = Map(grid_horizontal, grid_vertical)
    grid = RenderGrid(m, radius=16)
    units = RenderUnits(m, radius=16)

    # main loop
    while running:
        _grid(screen, grid)
        #
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        pygame.display.flip()
        # draw a line


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()