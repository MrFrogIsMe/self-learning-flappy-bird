import config
import player
import math 
import species 
import operator 

class Population:
    def __init__(self, size):
        self.size = size
        self.players: list[player.Player] = []
        self.generations = 1
        self.species: list[species.Species] = []
        for _ in range(0, size):
            self.players.append(player.Player())

    def update_live_players(self):
        for player in self.players:
            if player.isAlive:
                player.look()
                player.think()
                player.draw(config.window)
                player.update()

    def natural_selection(self):
        print('GENERATION:', self.generations)

        print('SPECATE')
        self.speciate()

        print('CALCULATE FITNESS')
        self.calculate_fitness()

        print('SORT BY FITNESS')
        self.sort_species_by_fitness()

        print('CHILDREN FOR NEXT GEN')
        self.next_gen()

        print('\n---------\n')

    def speciate(self):
        for s in self.species:
            s.players = []

        for p in self.players:
            add_to_species = False
            for s in self.species:
                if s.similarity(p.brain):
                    s.add_species(p)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(p))

    def calculate_fitness(self):
        for p in self.players:
            p.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()

    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        children = []

        # Clone of champion is added to each species
        for s in self.species:
            children.append(s.champion.clone())

        # Fill open player slots with children
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for _ in range(0, children_per_species):
                children.append(s.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players.clear()
        self.species.clear()
        for child in children:
            self.players.append(child)
        self.generations += 1

    def best_fitness(self):
        return max([p.fitness for p in self.players])

    def extinct(self):
        extinct = True
        for player in self.players:
            if player.isAlive:
                extinct = False
        return extinct
