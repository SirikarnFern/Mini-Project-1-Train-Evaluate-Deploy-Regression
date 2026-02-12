import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# 1. โหลดข้อมูล
df = pd.read_csv('commute_data.csv')

# 2. แยก Features และ Target
X = df[['Day_of_Week', 'Is_Raining', 'Transport_Mode', 'Hour_of_Day', 'Crowd_Level']]
y = df['Buffer_Time_Needed']

# 3. แบ่งข้อมูลสำหรับ Train และ Test (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. สร้าง Multiple Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# 5. วัดผลโมเดล
y_pred = model.predict(X_test)
print(f"R-Squared (ความแม่นยำ): {r2_score(y_test, y_pred):.4f}")
print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")

# 6. บันทึกโมเดลไว้ใช้ใน Web App
with open('commute_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("--- บันทึกไฟล์ 'commute_model.pkl' สำเร็จ ---")