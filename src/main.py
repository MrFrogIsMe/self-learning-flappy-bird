import pygame as pg
from sys import exit
import config
import components
import population

pg.init()
clock = pg.time.Clock()
population = population.Population(100)

def generate_pipes():
    config.pipes.append(components.Pipe(config.win_width))

def quit_game():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

def main():
    pipe_spawn_time = 10

    while True:
        quit_game()

        config.window.fill((0, 0, 0))

        config.ground.draw(config.window)

        if pipe_spawn_time <= 0:
            generate_pipes()
            pipe_spawn_time = 200
        pipe_spawn_time -= 1

        for pipe in config.pipes:
            pipe.draw(config.window)
            pipe.update()
            if pipe.off_screen:
                config.pipes.remove(pipe)


        if not population.extinct():
            population.update_live_players()
        else:
            config.pipes.clear()
            print('BEST FITNESS:', population.best_fitness())
            population.natural_selection()

        clock.tick(60 * 1.0)
        pg.display.flip()

if __name__ == '__main__':
    main()
