import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. توليد بيانات OBD-II افتراضية لمحرك يحاكي عطل في الحساسات
np.random.seed(42)
timestamps = pd.date_range(start="2026-06-01 09:00:00", periods=200, freq="s")

# بيانات طبيعية في الأول
rpm = np.random.normal(loc=2500, scale=300, size=200)
speed = rpm * 0.02 + np.random.normal(0, 2, 200)
engine_load = np.random.normal(loc=60, scale=10, size=200)
# افتراض حدوث خلل في قراءة حساس الصفع (Knock Sensor Voltage) بعد السطر رقم 120
knock_voltage = np.random.normal(loc=1.2, scale=0.1, size=200)
knock_voltage[120:] = knock_voltage[120:] + np.random.normal(loc=1.5, scale=0.4, size=80) 

# تجميع الداتا في جدول (DataFrame)
obd_data = pd.DataFrame({
    'Timestamp': timestamps,
    'Engine_RPM': rpm,
    'Vehicle_Speed_kmh': speed,
    'Engine_Load_Percent': engine_load,
    'Knock_Sensor_Voltage': knock_voltage,
    'DTC_Status': ['Clear' if i < 125 else 'P0325 - Knock Sensor Circuit Malfunction' for i in range(200)]
})

# 2. تحليل البيانات (Data Analysis)
print("--- تحليل البيانات الأولي لمعاملات الـ OBD-II ---")
# حساب متوسطات القراءات قبل وبعد ظهور كود العطل
clear_status = obd_data[obd_data['DTC_Status'] == 'Clear']
fault_status = obd_data[obd_data['DTC_Status'] != 'Clear']

print(f"متوسط جهد حساس الصفع الطبيعي: {clear_status['Knock_Sensor_Voltage'].mean():.2f}V")
print(f"متوسط جهد حساس الصفع أثناء الخطأ: {fault_status['Knock_Sensor_Voltage'].mean():.2f}V")

# 3. رسم بياني يوضح المشكلة (Data Visualization)
plt.figure(figsize=(10, 5))
plt.plot(obd_data['Timestamp'], obd_data['Knock_Sensor_Voltage'], label='Knock Sensor Voltage (V)', color='blue')
plt.axvline(x=obd_data['Timestamp'][120], color='red', linestyle='--', label='Fault Detection Point (DTC P0325)')
plt.title('OBD-II Data Analysis: Knock Sensor Anomaly Detection')
plt.xlabel('Time')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True)
# يمكنك حفظ هذه الصورة لرفعها في المعرض
plt.savefig('obd_analysis_chart.png') 
print("\n[نجاح] تم تحليل البيانات وحفظ الرسم البياني كـ obd_analysis_chart.png")
