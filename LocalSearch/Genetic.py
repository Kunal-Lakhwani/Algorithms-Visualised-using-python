from LocalSearch.Chessboard import Chessboard
import random

class populus:
    # mutation chance dictates the % chance of a mutation occouring
    def __init__(self, mutation_chance:int, people_count:int) -> None:
        # Initialise population with random members
        self.population = [ Chessboard( [ random.randint(1,8) for _ in range(8) ] ) for _ in range(people_count) ]
        self.people_count = people_count
        self.mutation_chance = mutation_chance
        self.generation = 1
    
    def Evolve(self, parent_indexes:list[int]):
        next_generation = []
        parentA_idx = 0
        # What we are doing is, crossing over current parent with 5 next parents.
        # However, when we reach the fifth last index, we instead crossover with the previous two.
        for parentA_idx in range(len(parent_indexes)):
            direction = 1 if parentA_idx < len(parent_indexes) - 5 else -1
            for i in range(1,6):
                offspring1, offspring2 = self.Crossover_and_Mutate(parentA_idx, parentA_idx+i*direction)
                next_generation.append(offspring1)
                next_generation.append(offspring2)
        
        self.population = next_generation
        self.generation += 1
                
    def get_elites(self) -> list[int]:
        # First sort the generation by fittest first.
        fittest_first = sorted(self.population, key=lambda person: person.get_fitness())
        indexes = []
        
        # Elitism:
        #   Only take the best Tenth of current generation
        for person in fittest_first[:self.people_count//10]: 
            indexes.append( self.population.index(person) )

        return indexes

    def get_fittest(self, Elites:list[int]) -> Chessboard:
        min_fitness = 28
        min_idx = 0
        for idx in Elites:
            fitness = self.population[idx].get_fitness()
            if fitness < min_fitness:
                min_fitness = fitness
                min_idx = idx
        
        return self.population[min_idx]

    def Crossover_and_Mutate(self, parent_a_idx:int, parent_b_idx:int) -> tuple[Chessboard, Chessboard]:
        crossover_point = random.randint(0,7)
        parentA = self.population[parent_a_idx]
        parentB = self.population[parent_b_idx]
        # first to crossover point of A + crossover point to last of B
        childA = parentA.QueenRanks[:crossover_point] + parentB.QueenRanks[crossover_point:]
        # crossover point to last of A + first to crossover point of B
        childB = parentA.QueenRanks[crossover_point:] + parentB.QueenRanks[:crossover_point]
        
        if random.random() < self.mutation_chance / 100:
            Queens = list(range(8))
            To_displace_A = random.sample(Queens, 1)
            To_displace_B = random.sample(Queens, 1)

            for displaced in To_displace_A:
                moveTo = random.randint(1,8)
                while moveTo == childA[displaced]: # Ensure we aren't moving to the same spot
                    moveTo = random.randint(1,8)

            for displaced in To_displace_B:
                moveTo = random.randint(1,8)
                while moveTo == childB[displaced]: # Ensure we aren't moving to the same spot
                    moveTo = random.randint(1,8)
            
        return ( Chessboard(childA), Chessboard(childB) )
    