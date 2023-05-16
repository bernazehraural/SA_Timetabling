import matplotlib.pyplot as plt
import numpy as np
import datetime

# Define the number of days, time slots per day, and total time slots
num_days = 10
time_slots_per_day = 5
total_time_slots = num_days * time_slots_per_day

# Define the exam schedule as a 2D numpy array
# where each row represents a day and each column represents a time slot
exam_schedule = [['BAU091', 'BAU109', 'BAU201', 'BWL036', 'BWL205', 'BWL207', 'BWL407', 'BWL413', 'ENG103', 'ETE303', 'ETE311', 'ETE331', 'HUK159', 'HUK161', 'HUK251', 'HUK255', 'HUK257', 'HUK461', 'HUK553', 'HUK561', 'HUK763', 'HUK913', 'INF201', 'INF606', 'INF701', 'INF714', 'KKW251', 'MAB091', 'MAB203', 'MAB311', 'MBT473', 'MEC215', 'MWT201', 'MWT301', 'MWT311', 'POL101', 'POL303', 'POL411', 'ÜSDNWI321']
                 , ['BAU107', 'BWL030', 'BWL105', 'BWL403', 'ENG101', 'ENG201', 'ENG303', 'ETE321', 'ETE441', 'HUK353', 'INF107', 'INF523', 'KKW307', 'MAB107', 'MAB213', 'MBT475', 'MEC313', 'MEC319', 'NWI201', 'POL403', 'VWL203', 'VWL301', 'VWL327', 'VWL403', 'WIN405']
                 , ['BAU202', 'BAU301', 'BAU302', 'BAU303', 'BWL033', 'BWL109', 'ETE201', 'ETE475', 'HUK151', 'HUK155', 'HUK157', 'HUK351', 'HUK355', 'HUK357', 'HUK359', 'HUK361', 'HUK363', 'HUK365', 'HUK457', 'HUK459', 'HUK555', 'INF103', 'INF203', 'INF503', 'INF511', 'KKW261', 'KKW361', 'MAB109', 'MAB207', 'MBT323', 'MEC091', 'MEC213', 'MEC311', 'MEC321', 'MWT305', 'PHY103', 'PHY111', 'POL105', 'POL107', 'POL203', 'POL211', 'POL309', 'POL313', 'POL407', 'POL550', 'ÜSDMBT369', 'VWL205', 'VWL401', 'WIN209', 'WIN313']
                 , ['BIO111', 'BWL037', 'BWL101', 'BWL103', 'CHE111', 'DEU121', 'ETE459', 'HUK153', 'HUK253', 'HUK259', 'HUK451', 'HUK455', 'HUK465', 'HUK563', 'HUK753', 'HUK915', 'HUK931', 'INF101', 'INF209', 'INF510', 'ISG001', 'KKW101', 'KKW161', 'KKW317', 'KKW431', 'KKW439', 'MAB001', 'MAB318', 'MAT201', 'MBT201', 'MBT455', 'MEC209', 'MWT205', 'MWT307', 'MWT309', 'NWI107', 'POL205', 'POL311', 'POL405', 'POL515', 'VWL191', 'VWL428']
                 , ['BWL201', 'BWL211', 'BWL309', 'BWL415', 'BWL417', 'DEU111', 'ENG203', 'ENG301', 'ETE091', 'ETE101', 'HUK163', 'HUK261', 'HUK453', 'HUK463', 'HUK557', 'HUK565', 'HUK755', 'HUK761', 'INF506', 'KKW103', 'KKW219', 'KKW233', 'KKW321', 'MAB301', 'MAT103', 'MBT211', 'MBT361', 'MBT363', 'NWI301', 'NWI401', 'PHY101', 'POL401', 'POL409', 'POL523', 'VWL281', 'VWL303', 'VWL305', 'VWL323', 'WIN103', 'WIN311', 'WIN317']]

print(exam_schedule)

# Define the color map for the plot
cmap = plt.get_cmap('viridis',8)

# Create a figure and axis object
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the timetable as a heat map
im = ax.imshow(exam_schedule, cmap=cmap)


# Define the start date and the number of days
start_date = datetime.date.today()  # yyyy, mm, dd
day_buffer = 14
# Generate a list of dates using a loop and the datetime module
dates = []
for i in range(num_days):
    day = start_date + datetime.timedelta(days=i+14)
    dates.append(day)

"""
Print the list of dates
for day in dates:
    print(day.strftime("%A, %B %d, %Y"))
"""


# Add labels to the plot
ax.set_xticks(np.arange(num_days))
ax.set_yticks(np.arange(time_slots_per_day))
ax.set_yticklabels([f"Time Slot {i+1}" for i in range(time_slots_per_day)])
ax.set_xticklabels([day.strftime("%A, %B %d, %Y") for day in dates])

# Add a colorbar to the plot
cbar = ax.figure.colorbar(im, ax=ax)

# Set the title of the plot
ax.set_title("Exam Timetable")

# Display the plot
plt.show()


"""

# Get the unique 'Ders Kodu' values from the classes list
classes_ders_kodu = df_classes['Ders Kodu'].unique()

# Check if 'Ders Kodu' in students list exists in classes list
mask = df_student_class['Ders Kodu'].isin(classes_ders_kodu)
notin = ~df_student_class['Ders Kodu'].isin(classes_ders_kodu)

# Filter the rows in student_class.xlsx where 'Ders Kodu' does not exist in classes list
df_student_class_filtered = df_student_class[mask]

print(notin)
print(df_student_class_filtered)

"""