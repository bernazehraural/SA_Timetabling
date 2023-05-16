import random
import math
import pandas as pd

# get the number of exams
# Read the Excel file into a pandas DataFrame
df = pd.read_excel('Data/classes.xlsx')
# Convert the DataFrame to a list of dictionaries
data = df['Ders Kodu']

print(data)

# Define the cost function that returns the total number of conflicts
def cost_function(solution):
    conflicts = 0
    for i in range(len(solution)):
        for j in range(i+1, len(solution)):
            if solution[i] == solution[j]:
                conflicts += 1
            if abs(i-j) == abs(solution[i]-solution[j]):
                conflicts += 1
    return conflicts

# Define the initial state function that generates a random solution
def initial_state(num_exams, num_timeslots):
    return [random.randint(1, num_timeslots) for _ in range(num_exams)]

# Define the neighbor function that generates a random neighboring solution
def neighbor(state, num_timeslots):
    neighbor_state = state[:]
    index = random.randint(0, len(state)-1)
    neighbor_state[index] = random.randint(1, num_timeslots)
    return neighbor_state

# Define the acceptance probability function that returns the probability of accepting a worse solution
def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)

# Define the simulated annealing function that returns the best solution found
def simulated_annealing(num_exams, num_timeslots, max_iterations, initial_temperature, cooling_rate):
    # Initialize the current state and cost
    current_state = initial_state(num_exams, num_timeslots)
    current_cost = cost_function(current_state)
    print(current_cost)
    
    # Initialize the best state and cost
    best_state = current_state[:]
    best_cost = current_cost
    
    # Initialize the temperature
    temperature = initial_temperature
    
    # Loop over the iterations
    for i in range(max_iterations):
        # Generate a neighboring solution
        new_state = neighbor(current_state, num_timeslots)
        new_cost = cost_function(new_state)
        
        # Decide whether to accept the new solution
        if acceptance_probability(current_cost, new_cost, temperature) > random.random():
            current_state = new_state[:]
            current_cost = new_cost
            
        # Update the best solution
        if current_cost < best_cost:
            best_state = current_state[:]
            best_cost = current_cost
            
        # Cool down the temperature
        temperature *= cooling_rate
        
    return best_state, best_cost



num_exams = len(data) # number of exams
num_timeslots = sum(data["Sınav Süresi (Slot Sayısı)"].values()) # number of total timeslots
timeslots = data["Sınav Süresi (Slot Sayısı)"] # list that contains timeslots for each class 
max_iterations = 5000
initial_temperature = 100.0
cooling_rate = 0.8

best_state, best_cost = simulated_annealing(num_exams, num_timeslots, max_iterations, initial_temperature, cooling_rate)

print("Best solution:", best_state)
print("Best cost:", best_cost)

