import random
import math

class ExamTimetablingProblem:
    def __init__(self, n_exams, n_timeslots, conflicts_matrix):
        self.n_exams = n_exams
        self.n_timeslots = n_timeslots
        self.conflicts_matrix = conflicts_matrix
        self.current_solution = self.generate_initial_solution()

    def generate_initial_solution(self):
        solution = [random.randint(0, self.n_timeslots-1) for i in range(self.n_exams)]
        print(solution)
        return solution

    def get_conflicts(self, solution):
        conflicts = 0
        for i in range(self.n_exams):
            for j in range(i+1, self.n_exams):
                if solution[i] == solution[j] and self.conflicts_matrix[i][j] == 1:
                    conflicts += 1
        return conflicts

    def get_neighbor(self, solution):
        neighbor = list(solution)
        i = random.randint(0, self.n_exams-1)
        j = random.randint(0, self.n_timeslots-1)
        neighbor[i] = j
        return neighbor

    def simulated_annealing(self, initial_temperature=1000, cooling_factor=0.95, stopping_temperature=1e-6, max_iterations=10000):
        temperature = initial_temperature
        current_energy = self.get_conflicts(self.current_solution)
        best_solution = list(self.current_solution)
        best_energy = current_energy
        i = 0
        while temperature > stopping_temperature and i < max_iterations:
            neighbor = self.get_neighbor(self.current_solution)
            neighbor_energy = self.get_conflicts(neighbor)
            delta_energy = neighbor_energy - current_energy
            if delta_energy <= 0 or random.random() < math.exp(-delta_energy/temperature):
                self.current_solution = neighbor
                current_energy = neighbor_energy
            if current_energy < best_energy:
                best_solution = list(self.current_solution)
                best_energy = current_energy
            temperature *= cooling_factor
            i += 1
        return best_solution, best_energy


ExamTimetablingProblem.generate_initial_solution(ExamTimetablingProblem(100,120,[]))