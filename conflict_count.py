import pandas as pd
import openpyxl

# Load the Excel file with the PivotTable
excel_file = 'summary.xlsx'
df = pd.read_excel(excel_file)

results = []
students = df['Öğrenci No'].unique()
timeslots = df['Timeslot'].unique()

for student in students:
    for timeslot in timeslots:
        filtered_df = df[(df['Öğrenci No'] == student) & (df['Timeslot'] == timeslot)]
        count = len(filtered_df)
        results.append({'Öğrenci No': student, 'Timeslot': timeslot, 'Count': count})

# Sonuçları listeleme
result_df = pd.DataFrame(results)
print(df.shape[0])
filtered_df = result_df[result_df['Count'] > 1]
filtered_count = filtered_df.shape[0]
print(filtered_count)
