import random
import math
import pandas as pd

# get the number of exams
# Read the Excel file into a pandas DataFrame
df = pd.read_excel('Data/classes.xlsx')
data = df.to_dict('Ders Kodu') # Convert the DataFrame to a list of dictionaries
Exams = []

print(type(data['Ders Kodu']))

class Exam:
    def __init__(self, id, timeslot):
        self.id = id
        self.timeslot = timeslot
        Exams.append(self)




class Timeslot:
    def __init__(self, id):
        self.id = id
        self.exams = []

class ExamTimetablingProblem:
    def __init__(self, exams, timeslots, conflicts):
        self.exams = exams
        self.timeslots = timeslots
        self.conflicts = conflicts
        print(self.exams)
        self.current_solution = self.generate_initial_solution()

    def generate_initial_solution(self):
        solution = {}
        for exam in self.exams:
            timeslot_id = random.randint(0, len(self.timeslots)-1)
            timeslot = self.timeslots[timeslot_id]
            solution[exam.id] = timeslot.id
            timeslot.exams.append(exam)
        return solution

    def get_conflicts(self, solution):
        conflicts = 0
        for exam1 in self.exams:
            for exam2 in self.exams:
                if exam1.id < exam2.id and solution[exam1.id] == solution[exam2.id]:
                    conflicts += self.conflicts[exam1.id][exam2.id]
        return conflicts

    def get_neighbor(self, solution):
        neighbor = dict(solution)
        exam_id = random.choice(list(neighbor.keys()))
        old_timeslot_id = neighbor[exam_id]
        new_timeslot_id = random.choice(list(range(len(self.timeslots))))
        while new_timeslot_id == old_timeslot_id:
            new_timeslot_id = random.choice(list(range(len(self.timeslots))))
        new_timeslot = self.timeslots[new_timeslot_id]
        exam = self.exams[exam_id]
        old_timeslot = self.timeslots[old_timeslot_id]
        old_timeslot.exams.remove(exam)
        new_timeslot.exams.append(exam)
        neighbor[exam_id] = new_timeslot_id
        return neighbor

    def simulated_annealing(self, initial_temperature=1000, cooling_factor=0.95, stopping_temperature=1e-6, max_iterations=10000):
        temperature = initial_temperature
        current_energy = self.get_conflicts(self.current_solution)
        best_solution = dict(self.current_solution)
        best_energy = current_energy
        i = 0
        while temperature > stopping_temperature and i < max_iterations:
            neighbor = self.get_neighbor(self.current_solution)
            neighbor_energy = self.get_conflicts(neighbor)
            delta_energy = neighbor_energy - current_energy
            if delta_energy <= 0 or random.random() < math.exp(-delta_energy/temperature):
                self.current_solution = dict(neighbor)
                current_energy = neighbor_energy
            if current_energy < best_energy:
                best_solution = dict(self.current_solution)
                best_energy = current_energy
            temperature *= cooling_factor
            i += 1
        return best_solution, best_energy



# best_state, best_cost = ExamTimetablingProblem(data["Ders Kodu"],data["Sınav Süresi (Slot Sayısı)"],any).simulated_annealing(1000,0.95,0.0000001,10000)


#print("Best solution:", best_state)
#print("Best cost:", best_cost)


#for ind in best_state:
#    for key in data["Ders Kodu"]:
#        if data["Ders Kodu"][key] == ind:
#            print("The key with value", ind, "is", key)
#            break
#        else:
#            print("Value not found in dictionary")