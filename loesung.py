import numpy as np
import random
import pandas as pd

# Read the Excel files into a Pandas DataFrame

# Read classes excel file
classes = pd.read_excel('Data/classes.xlsx')
# Extract specific columns by column name for exams
exam_id = classes['Ders Kodu']
num_students = classes['Sınava Girecek Öğrenci Sayısı']

classData = classes[["Ders Kodu", "Ders Adı", "Sınava Girecek Öğrenci Sayısı", "Sınav Süresi (Slot Sayısı)", 
              "Gözetmenlik Öncesi Boşluk Süresi (Slot Sayısı)", "Gözetmenlik Sonrası Boşluk Süresi (Slot Sayısı)"]]
classData = classData.set_index("Ders Adı").to_dict(orient='records')

# print the resulting dictionary
# print(classData)

# Read classrooms excel file
classrooms = pd.read_excel('Data/classrooms.xlsx')
# Extract specific columns by column name for classrooms
room_id = classrooms['DERSLİK KODU']
capacity = classrooms['SINAV KAPASİTESİ']
availability = classrooms['DURUM']

classroomsData = classrooms[["DERSLİK KODU", "DERSLİK ADI", "SINAV KAPASİTESİ", "DURUM"]]
classroomsData = classroomsData.set_index("DERSLİK ADI").to_dict(orient='records')
# available, if classroomsData ["DURUM"] is equal to 1 
# unavailable, if classroomsData ["DURUM"] is equal to 0
for record in classroomsData:
    if record["DURUM"] == 1:
        record["DURUM"] = "available"
    elif record["DURUM"] == 0:
        record["DURUM"] = "unavailable"
# print(classroomsData)

# Read student_class excel file
student_class = pd.read_excel('Data/student_class.xlsx')
# Extract specific columns by column name for classrooms
student_id = student_class['Öğrenci No']
# Group the DataFrame by student ID and aggregate the taken exams as a list
taken_exams = student_class.groupby('Öğrenci No')['Ders Kodu'].agg(list)
# Create a dictionary to store the results
student_exams = dict()
# Iterate over the groupby object and store the taken exams for each student
for student, exams in taken_exams.items():
    student_exams[student] = exams

# print(student_exams)


"""
# Define the data
exams = [{'id': 'exam1', 'num_students': 50},
         {'id': 'exam2', 'num_students': 30},
         {'id': 'exam3', 'num_students': 80},
         {'id': 'exam4', 'num_students': 20},
         {'id': 'exam5', 'num_students': 40}]

rooms = [{'id': 'room1', 'capacity': 60, 'availability': [1, 2, 3]},
         {'id': 'room2', 'capacity': 40, 'availability': [1, 3, 5]},
         {'id': 'room3', 'capacity': 30, 'availability': [2, 4, 5]},
         {'id': 'room4', 'capacity': 50, 'availability': [1, 2, 5]}]

students = [{'id': 'student1', 'taken_exams': ['exam1', 'exam2', 'exam4']},
            {'id': 'student2', 'taken_exams': ['exam2', 'exam3', 'exam5']},
            {'id': 'student3', 'taken_exams': ['exam1', 'exam3', 'exam4', 'exam5']},
            {'id': 'student4', 'taken_exams': ['exam1', 'exam4']},
            {'id': 'student5', 'taken_exams': ['exam1', 'exam2', 'exam5']}]
"""

# Generate the available timeslots
num_timeslots = 337
generated_available_timeslots = list(range(1, num_timeslots+1))

# Define the constraint (non-conforming exam)
non_conforming_exam = {'MEC311', 'MEC313'}

# Define the cost function
def calculate_cost(solution):
    # Initialize the cost to zero
    cost = 0
    # Count the number of students taking exams at the same time in the same room
    for timeslot in generated_available_timeslots:
        for room in classroomsData:
            students_in_room = []
            for exam, assigned_timeslot in solution.items():
                if assigned_timeslot == timeslot:
                    if exam in non_conforming_exam:
                        cost += 1
                    if room['DURUM'] == "available":
                        for iter in classData:
                            if iter['Ders Kodu'] == exam:
                                num_students = iter['Sınava Girecek Öğrenci Sayısı']
                        if len(students_in_room) + num_students <= room['SINAV KAPASİTESİ']:
                            students_in_room.extend(k for k, v in student_exams.items() if exam in v)
                        else:
                            cost += 1
                    else:
                        cost += 1
            cost += len(students_in_room) * (len(students_in_room) - 1) / 2
    return cost

# Define the perturbation function
def perturb_solution(solution):
    # Create a copy of the solution to modify
    new_solution = solution.copy()
    # Choose an exam to reassign to a new timeslot
    exam_id = random.choice(list(new_solution.keys()))
    new_timeslot = random.choice(generated_available_timeslots)
    # Assign the exam to the new timeslot
    new_solution[exam_id] = new_timeslot
    return new_solution

def simulated_annealing(current_solution, initial_temperature, cooling_factor, num_iterations):
    # Set the initial temperature
    current_temperature = initial_temperature
    # Set the current solution and cost as the best solution and cost found so far
    best_solution = current_solution
    best_cost = calculate_cost(current_solution)
    # Calculate the cost of the initial solution
    current_cost = calculate_cost(current_solution)
    # Iterate for the specified number of iterations
    for i in range(num_iterations):
        # Perturb the current solution
        new_solution = perturb_solution(current_solution)
        # Calculate the cost of the new solution
        new_cost = calculate_cost(new_solution)
        # Calculate the change in cost
        delta_cost = new_cost - current_cost
        # If the new solution is better, accept it
        if delta_cost < 0:
            current_solution = new_solution
            current_cost = new_cost
            # If the new solution is the best found so far, update the best solution
            if current_cost < best_cost:
                best_solution = current_solution
                best_cost = current_cost
        # If the new solution is worse, accept it with a certain probability
        else:
            acceptance_probability = np.exp(-delta_cost / current_temperature)
            if random.random() < acceptance_probability:
                current_solution = new_solution
                current_cost = new_cost
        # Reduce the temperature
        current_temperature *= cooling_factor
    # Return the best solution found
    return best_solution



initial_solution = {}
for exam in classData:
    initial_solution[exam['Ders Kodu']] = random.choice(generated_available_timeslots)

"""
exam = 'ENG301'
students_took_exam = [k for k, v in student_exams.items() if exam in v]
print(students_took_exam)

# print(initial_solution)
"""

optimized_solution = simulated_annealing(initial_solution, initial_temperature=100, cooling_factor=0.99, num_iterations=1000)

print("Optimized solution:")
for exam_id, timeslot in optimized_solution.items():
    print(f"{exam_id} assigned to timeslot {timeslot}")





"""

timeslots = []
bau_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
bwl_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
ete_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
huk_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
inf_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
mec_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
mwt_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
kkw_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
pol_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
mab_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
mbt_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
win_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists
vwl_exam_timetable = [[] for _ in range(10)] # Create 5 empty lists


for exam_id, timeslot in optimized_solution.items():
    if exam_id[:3] == "BAU" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" or exam_id[:3] == "PHY":
        bau_exam_timetable.append(exam_id, )
        bau_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "BWL" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" :
        bwl_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "ETE" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" or exam_id[:3] == "PHY" :
        ete_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "HUK" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" :
        huk_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " +  timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "INF" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" or exam_id[:3] == "PHY":
        inf_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "MEC" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" or exam_id[:3] == "PHY":
        mec_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "MWT" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" or exam_id[:3] == "PHY":
        mwt_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "KKW" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI":
        kkw_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "POL" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI":
        pol_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "MAB" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" :
        mab_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "MBT" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" :
        mbt_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "WIN" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" :
        win_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    if exam_id[:3] == "VWL" or exam_id[:3] == "ENG" or exam_id[:3] == "DEU" or exam_id[:3] == "NWI" :
        vwl_exam_timetable[int(generated_available_timeslots.index(timeslot) / slots_per_day)].insert(generated_available_timeslots.index(timeslot) % slots_per_day, exam_id + " " + timeslot)# Append element to the list based on the mod of its index
    
    # print(f"{exam_id} assigned to timeslot {timeslot}")


print(bau_exam_timetable)
print(bwl_exam_timetable)
print(ete_exam_timetable)
print(huk_exam_timetable)
print(inf_exam_timetable)
print(mec_exam_timetable)
print(mwt_exam_timetable)
print(kkw_exam_timetable)
print(pol_exam_timetable)
print(mab_exam_timetable)
print(mbt_exam_timetable)
print(win_exam_timetable)
print(vwl_exam_timetable)
"""