#to generate random numbers
import random

#size of population
N = 10
#number of queens on the board
NQueen = 8

#probability of crossover (pc), and mutation (pm)
pc = 0.7
pm = 0.3

#value for perfect fitness
perfect_fitness = 1

#array to store all the solutions the program finds
globalSolutions = []

#class to store entire population object
class population:

	#constructor with array of individuals and total fitness
	def __init__(self, individuals):
		self.individuals = individuals
		#get total fitness from all individuals
		self.total_fitness = generate_total_fitness(individuals)
	
	#getter for total fitness
	def get_total_fitness(self):
		return self.total_fitness
	
	#getter for an individual n in population
	def get_individual(self, n):
		return self.individuals[n]
		

#class used to construct individual
class individual:

	#constructor with individuals genes, and fitness
	def __init__(self, genes):
		self.genes = genes
		#get fitness from genes 
		self.fitness_value = fitness(genes)
	
	#getter for genes
	def get_genes(self):
		return self.genes
	
	#getter for fitness value
	def get_fitness_value(self):
		return self.fitness_value
		

#function used to generate fitness for a population full of individuals
def generate_total_fitness(individuals):
	total_fitness = 0
	#for every individual, call the fitness function for that individual, and add it to total
	for ind in individuals:
		total_fitness += ind.get_fitness_value()
	
	#return total fitness
	return total_fitness

#function used to generate fitness for one individual	
def fitness(array):

	#if individual is already in global solutions, set fitness to almost zero to not let them propagate their genes, since that solution is already found
	if array in globalSolutions:
		return 0.00001
	
	
	#counter for number of collisions individual has
	counter=0
	
	#these two loops check the individuals genes, or the queens on the board, ever collide with each other
	
	#loop that goes for entire population
	for a in range(NQueen):
		#set secondary loop to next queen
		b = a+1
		while b < NQueen:
			
			#get column, and row difference between queens
			col_diff = abs(a-b)
			row_diff =abs(array[a]-array[b])
			
			#if columns and rows are the same, the queens are diagonal to each other and will collide
			if col_diff==row_diff:
				counter+=1
		
			b+=1
			
	#return fitness where the more collisions individual has, the lower the score
	return (1/(counter+1))**2

	
#function used to perform crossover between two individuals
def crossover(parent1_ref, parent2_ref):
	#clone parent genes
	parent1 = parent1_ref[:]
	parent2 = parent2_ref[:]
	
	#deciding if doing crossover with crossover probability, if not crossover, return parents
	if pc < random.uniform(0, 1):
		return parent1, parent2

	#initialize child genes 
	child1 = [-1,-1,-1,-1,-1,-1,-1,-1]
	child2 = [-1,-1,-1,-1,-1,-1,-1,-1]
	
	#get start of crossover, with random number between 0 and number of queens in genes
	crossover_start = random.randint(0,NQueen-1)
	ci1 = crossover_start
	
	#copy 4 genes from other parent to child starting at random random point
	for n in range(4):
		#set child to parent gene
		child1[ci1] = parent2[ci1]
		child2[ci1] = parent1[ci1]
		
		#increase the index, wrap around to start if it goes past array length, so if there are 8 queens, and at gene 7, wrap around to 0
		ci1 = (ci1+1)%NQueen

	#get other half of the crossover for each child, this fills gives an array of 4 genes the children needs to put inside of it
	for_child1 = get_other_half_crossover(parent1,child1,crossover_start)
	for_child2 = get_other_half_crossover(parent2,child2,crossover_start)
	
	#for number of genes, if the child has a negative 1, fill in that value with the array from the other half of the crossover
	for i in range(NQueen):
		if child1[i] == -1:
			child1[i] = for_child1.pop(0)
		
		if child2[i] == -1:
			child2[i] = for_child2.pop(0)

	#return crossovered children
	return child1, child2

#function to get the other part of the crossover
def get_other_half_crossover(parent_ref,child_ref,start):
	#clone array
	parent = parent_ref[:]
	child = child_ref[:]
	
	#loop until reached length of genes
	p = 0
	while p < len(parent):
		
		#set child index equal to start of crossover 
		ch = start
		#check if child gene at crossover is equal to parent gene at p, if so then delete value from parent and keep the values in the parent that are not in the child 
		for n in range(4):
			if child[ch] == parent[p]:
				del(parent[p])
				p -= 1
				continue
			
			#wrap around array
			ch = (ch+1)%NQueen
		p += 1
	
	#return array of parent that is not in child
	return parent

#function to get 
def mutation(ind_ref):
	ind = ind_ref[:]
	
	#decide whether or not to mutate
	if pm < random.uniform(0, 1):
		return ind
	
	#pick 2 random genes within chromosome
	gene1 = random.randint(0,NQueen-1)
	gene2 = random.randint(0,NQueen-1)	

	#ensure not the same gene
	while gene1 == gene2:
		gene2 = random.randint(0,NQueen-1)
	
	#swap them
	temp = ind[gene1]
	ind[gene1] = ind[gene2]
	ind[gene2] = temp
	return ind
	
#generate the initial population of N individuals
def generate_initial_pop():
	
	array_of_inds = []
	
	#for each individual to be created
	for i in range(N):
		#make base array of values 0 to 7 in order, and then randomly shuffle them
		temp_array = [0,1,2,3,4,5,6,7]
		random.shuffle(temp_array)
		
		#create an individual out of the array, and add it to the array of individuals
		temp_ind = individual(temp_array)
		array_of_inds.append(temp_ind)
	
	#create population object out of the array of individuals
	pop = population(array_of_inds)
	return pop
	
#checks if solution already found this iteration, and if not adds it to the global solution list
def checkSolution(solution):
	#if solution already found, return false without adding it to the global list
	if solution in globalSolutions:
		return False
	else:
		#otherwise, print the solution, and add it to the global list of solutions
		print(solution)
		print(fitness(solution))
		globalSolutions.append(solution)
		print(len(globalSolutions))

		#additionally, if the list has all 92 solutions, return true (signalling program to stop), or return false (meaning to continue)
		if(len(globalSolutions)==92):
			return True
		else:
			return False
			
	
	
#this function selects 5 pairs of individuals for crossover to use, based on the roulette wheel method
def crossover_selection(population):
	
	indices = []
	#loops for half of the population size, picking pairs of individuals to crossover
	for n in range(int(N/2)):
		
		#loop to pick an individual based on their fitness value
		while(1):
			#start with a random individual
			i1 = random.randint(0,N-1)
			
			#if this random number (0 to 1) is less than their ratio of their fitness to the population, select them, else try another individual with a new random number
			if random.uniform(0, 1) < population.get_individual(i1).get_fitness_value() / population.get_total_fitness():
				break

		#repeat again for a second individual, ensuring not to pick the same individual
		while(1):
			i2 = random.randint(0,N-1)
			
			if i2 == i1:
				continue
			
			if random.uniform(0, 1) < population.get_individual(i2).get_fitness_value() / population.get_total_fitness():
				break
		
		#add these two individual's indices to the list to return
		indices.append(i1)
		indices.append(i2)
	
	return indices
	
#print the current generation out to the command line
def print_generation(population):
	print("Overall fitness: ",population.get_total_fitness())
	for n in range(N):
		print("")
		print("Chromosome ",n," fitness: ",population.get_individual(n).get_fitness_value())
		print("Chromosome ",n," genes: ",population.get_individual(n).get_genes())
		
#write the solutions with the # of generations to reach them to a file
def write_to_file(gens):
	file = open("solutions.txt","w")
	file.write("{}\n".format(gens))
	for solution in globalSolutions:
		file.write("{}\n".format(solution))
	file.close()
	
#main function, uses all other functions to implement our genetic algorithm
def genetic_evolution():
	#create an initial population
	current_population = generate_initial_pop()
	
	print("Generation ",0,":")
	print_generation(current_population)
	
	#set flag for if found all solutions, and counter for generation #
	found_soln = 0
	gens = 0
	
	#continually loop (until all solutions found)
	while(1):
		#select the parents for crossover
		crossover_indices = crossover_selection(current_population)
		next_gen_children = []
		
		#loop through each pair of parents for crossover, and perform the function to get the new children
		n = 0
		while n < N:
			child1, child2 = crossover(current_population.get_individual(crossover_indices[n]).get_genes(), current_population.get_individual(crossover_indices[n+1]).get_genes())
			next_gen_children.append(individual(child1))
			next_gen_children.append(individual(child2))
			n+=2
		
		#use the new children, loop through each and decide whether or not to mutate (and if so perform it)
		n = 0
		while n < N:
			next_gen_children[n] = individual(mutation(next_gen_children[n].get_genes()))
			n += 1
				
		#overwrite the previous population, and increment the generation #
		current_population = population(next_gen_children)
		gens+=1
		
		#for each new member of the population, check if they have a perfect fitness value, and if so check if this solution was the last solution (of the 92), if so stopping the evolution
		n = 0
		while n < N:
			if current_population.get_individual(n).get_fitness_value() == perfect_fitness:
				if checkSolution(current_population.get_individual(n).get_genes()):
					print("Found All solution")
					write_to_file(gens)
					found_soln = 1
					break
			n += 1

		if found_soln == 1:
			break

			
def main():
	genetic_evolution()
	
main()
	
	
	
	
