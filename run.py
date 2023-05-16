import copy
import random
import math

# Define variables for the timetabling problem
num_events = 10  # number of the exams
num_time_slots = 5  # number of the total slots for each day
event_duration = 2  # taken duration for each exams
# more variables are going to be added


# Generate the initial timetable randomly
timetable = [[-1]*num_time_slots for i in range(num_events)]
for i in range(num_events):
    duration_left = event_duration
    while duration_left > 0:
        time_slot = random.randint(0, num_time_slots-1)
        if timetable[i][time_slot] == -1:
            timetable[i][time_slot] = i
            duration_left -= 1

# Define the objective function
def objective_function(timetable):
    hard_constraint_score = 0
    soft_constraint_score = 0

    # Hard constraints: no overlapping events
    for t in range(num_time_slots):
        events_in_slot = [timetable[i][t] for i in range(num_events) if timetable[i][t] != -1]
        if len(events_in_slot) > 1:
            hard_constraint_score -= len(events_in_slot) - 1

    # Soft constraints: minimize the number of gaps between events
    for i in range(num_events):
        last_time_slot = -1
        for t in range(num_time_slots):
            if timetable[i][t] != -1:
                if last_time_slot != -1:
                    soft_constraint_score -= (t - last_time_slot - 1)
                last_time_slot = t

    return hard_constraint_score, soft_constraint_score

# Define the neighborhood function
def neighborhood_function(timetable):
    new_timetable = [row[:] for row in timetable] # make a copy
    i = random.randint(0, num_events-1)
    j = random.randint(0, num_time_slots-1)
    k = random.randint(0, num_time_slots-1)
    if k + event_duration > num_time_slots: # event doesn't fit in new time slot
        return new_timetable
    if new_timetable[i][j] == -1: # event isn't scheduled in current time slot
        return new_timetable
    for t in range(j, j+event_duration):
        new_timetable[i][t] = -1
    for t in range(k, k+event_duration):
        if new_timetable[i][t] != -1: # conflicting event in new time slot
            return new_timetable
    for t in range(k, k+event_duration):
        new_timetable[i][t] = i
    return new_timetable

# Define the acceptance function
def acceptance_function(candidate_score, current_score, temperature):
    delta = candidate_score - current_score
    if delta < 0:
        return 1.0
    else:
        return math.exp(-delta / temperature)

# Define the cooling schedule
initial_temperature = 1.0
cooling_rate = 0.99
num_iterations = 1000

# Simulated annealing search
print(timetable)
print("----")
current_timetable = copy.deepcopy(timetable)
current_score = objective_function(current_timetable)
best_timetable = current_timetable
best_score = current_score
temperature = initial_temperature
for i in range(num_iterations):
    print(current_timetable)
    new_timetable = neighborhood_function(current_timetable)
    new_score = objective_function(new_timetable)
    print(new_score)
    if acceptance_function(new_score[0] + new_score[1], current_score[0] + current_score[1], temperature) > random.random():
        current_timetable = new_timetable
        current_score = new_score
    if current_score[0] + current_score[1] > best_score[0] + best_score[1]:
        best_timetable = current_timetable
        best_score = current_score
    temperature *= cooling_rate 

