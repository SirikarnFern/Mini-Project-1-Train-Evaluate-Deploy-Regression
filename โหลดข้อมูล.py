import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# โหลดข้อมูล
df = pd.read_csv('commute_data.csv')

print(df.describe())