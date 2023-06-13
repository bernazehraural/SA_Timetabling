import pandas as pd
import openpyxl

# Load the Excel file with the PivotTable
excel_file = 'exam_schedule.xlsx'
df = pd.read_excel(excel_file)


# Aynı timeslot ve aynı roomda olan sınavları filtreleme
filtered_df = df[df.duplicated(['Timeslot', 'Room Info'], keep=False)]

print(filtered_df.shape[0])
