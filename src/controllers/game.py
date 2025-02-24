import random
import neat
import pygame
from src.classes.dino import Dinosaur
from src.classes.obstacles import SmallCactus, LargeCactus, Bird
from src.classes.cloud import Cloud
from src.game_config import *
from src.utils.draw import draw_info, draw_line, draw_net
from src.utils.fs import save_best_genome

best_points = 0
best_round = 0
count_round = 0

def eval_genomes(genomes, config):
    print('Evaluating genomes...')
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, death_count, best_points, best_round, count_round
    obstacles.clear()

    best_roundBypass = True
    count_round+=1
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    
    nets = []
    dinos = []
    ge = []

    clock = pygame.time.Clock()
    cloud = Cloud()
    font = pygame.font.Font('freesansbold.ttf', 20)

    run = True
    winner = None

    # Creation of dinosaurs and neural networks
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinos.append(Dinosaur())
        ge.append(genome)

    # Main loop
    while run and len(dinos) > 0:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            elif event.type == pygame.K_ESCAPE:
                run = False

        # Update the screen
        SCREEN.fill((255, 255, 255))

        # Update dinos
        for x, dino in enumerate(dinos):
            ge[x].fitness += 0.1  # Reward for staying alive

            # Get the neural network outputs for the current dinosaur
            output = nets[x].activate((
                        dino.dino_rect.centerx, # Dino x position
                        dino.dino_rect.centery, # Dino y position
                        obstacles[0].rect.centerx if obstacles else 0, # Obstacle x position
                        obstacles[0].rect.centery if obstacles else 0, # Obstacle y position
                        abs(dino.dino_rect.centerx - obstacles[0].rect.centerx if obstacles else 0), # Distance between dino and obstacle
                        abs(dino.dino_rect.centery - obstacles[0].rect.centery if obstacles else 0) # Height difference between dino and obstacle
                    ))


            if obstacles:
                dino_position = (dino.dino_rect.x + dino.dino_rect.width, dino.dino_rect.y + dino.dino_rect.height // 2)
                if x < 1:
                    draw_line(dino_position, obstacles) # Draw a line between firts dino and obstacle

            # Decide what to do based on the output
            if output[0] > 0.5 and output[0] > output[1] and not dino.dino_jump:
                dino.update(0) # the AI wants to jump
            elif output[1] > 0.5 and output[1] > output[0] and not dino.dino_jump:
                dino.update(1) # the AI wants to duck
            else:
                dino.update(2) # the AI wants to run
            dino.draw(SCREEN) # Draw the dino

        # Generate new obstacles
        # If there are no obstacles or the last obstacle is at a random distance from the screen as long as the score is greater than 1000
        if len(obstacles) == 0 or (len(obstacles) <= 1 and ((not obstacles or obstacles[-1].rect.x < random.choice([300, 400, 500])) and points > 1000)):
            rand = random.randint(0, 2)
            if rand == 0:
                obstacles.append(Bird(BIRD))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif rand == 2:
                obstacles.append(SmallCactus(SMALL_CACTUS))

        # Update obstacles and check for collisions
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dino in enumerate(dinos):
                # check if dino hit cactus
                if dino.dino_rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1  
                    dinos.pop(i)
                    nets.pop(i)
                    winner = ge.pop(i)  # ⚡ Save the last survivor as winner

                # ============================
                # Check if the dino jumped or ducked and receive reward
                # ============================
                # elif dino.dino_rect.x == obstacle.rect.x:
                #     if (dino.dino_rect.y < obstacle.rect.y and obstacle.name == 1):
                #         print("Jumped over obstacle!")
                #         ge[i].fitness += 1  # Reward for jumping over cactus
                #     elif (dino.dino_rect.y > obstacle.rect.y and obstacle.name == 3):
                #         print("Ducked under obstacle!")
                #         ge[i].fitness += 1  # Reward for ducking under bird


        # Update the best score
        if points > best_points:
            best_points = points
            if best_roundBypass:
                best_round=count_round
                best_roundBypass = False
        
        max_fitness = max([genome.fitness for genome in ge]) if ge else 0 # Get the max fitness of the current generation
        draw_info(font, len(dinos), game_speed, points, best_points, count_round, best_round, max_fitness) # Draw the info on the screen

        if max_fitness >= config.fitness_threshold:
            print("Fitness threshold reached! Ending training.")
            run = False
        

        # Update the background and clouds
        background()

        cloud.draw(SCREEN)
        cloud.update()

        # Display the score
        score()

        # Update the screen
        clock.tick(30)
        pygame.display.update()

    print("Round finished.")
    draw_net(config, genome, "neat_network")
    return True

# ============================
# Functions
# ============================

def score(): # Display the score
    global points, game_speed
    points += 1
    if points % 100 == 0:
        game_speed += 1

def background(): # Update the background
    global x_pos_bg, y_pos_bg
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg = 0
    x_pos_bg -= game_speed

def run_game(best_genome=None): # Run the game
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                './config_neat.ini')

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Try to load the best saved genome
    
    if best_genome:
        print("Initializing with the best saved genome.")
        # Adding the best_genome as a new individual to the population
        p.population[0] = best_genome # We replace the first genome in the population with the best_genome
        genomes = [(1, best_genome)] # Adding the best_genome as a new individual to the population
        eval_genomes(genomes, config)
    else:
        print("Inicializando com população aleatória.")
        winner = p.run(eval_genomes, 100)
        # Save genome
        save_best_genome(winner)
    # Train the AI

    # Loop after finishing the game
    while False:
        winner = p.run(eval_genomes, 100)
        # Save genome
        save_best_genome(winner)
    
    #print(f"Best genome: {winner.key}")



