import matplotlib.pyplot as plt
import pandas as pd

# Read the Excel file
df = pd.read_excel('exam_schedule.xlsx')

# Create an empty list to store the rows
data = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Extract the values of each column
    exam_id = row['Exam ID']
    timeslot = row['Timeslot']
    room_info = row['Room Info']
    
    # Append the values as a list to the rows list
    data.append([exam_id, timeslot, room_info])

# Extract timeslots and room info
timeslots = [exam[1] for exam in data]
room_info = [exam[2] for exam in data]

# Create a bar chart
plt.figure(figsize=(20, 12))
plt.bar(timeslots, range(len(timeslots)), color='lightblue')

# Set axis labels and title
plt.xlabel('Timeslot')
plt.ylabel('Exam ID')
plt.title('Exam Schedule')

# Add room info as annotations
for i, room in enumerate(room_info):
    plt.annotate(room, xy=(timeslots[i], i), xytext=(5, 5), textcoords='offset points')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the chart
plt.tight_layout()
plt.show()
