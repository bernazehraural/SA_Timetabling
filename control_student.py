import pandas as pd

# İlk Excel dosyasını oku
df1 = pd.read_excel("Data/student_class.xlsx")

# İkinci Excel dosyasını oku
df2 = pd.read_excel("exam_schedule.xlsx")

# İki veri kümesini "Ders Kodu" sütunu üzerinde birleştir
merged_df = pd.merge(df1, df2, left_on="Ders Kodu", right_on="Exam ID", how="inner")

# Çakışan verileri kontrol etmek için bir filtreleme yap
conflict_df = merged_df[["Öğrenci No", "Ders Kodu", "Timeslot", "Room Info"]]

# Çakışan verileri görüntüle
print(conflict_df)

merged_df.to_excel("summary.xlsx", index=False)