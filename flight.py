import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

years = range(2009, 2019)
files = [f'flight_years/{year}.csv' for year in years]
data = pd.concat([pd.read_csv(file) for file in files])

avg_delay_by_origin = data.groupby('Origin')['ArrDelay'].mean().reset_index()

bar_plot = px.bar(avg_delay_by_origin, x='Origin', y='ArrDelay', 
                  title='Average Arrival Delay by Origin Airport')
bar_plot.update_layout(xaxis_title='Origin Airport', yaxis_title='Average Arrival Delay')
bar_plot.show()

avg_delay_by_dest = data.groupby('Dest')['ArrDelay'].mean().reset_index()

bar_plot_dest = px.bar(avg_delay_by_dest, x='Dest', y='ArrDelay', 
                       title='Average Arrival Delay by Destination Airport')
bar_plot_dest.update_layout(xaxis_title='Destination Airport', yaxis_title='Average Arrival Delay')
bar_plot_dest.show()

numeric_data = data.select_dtypes(include=['number'])
corr_matrix = numeric_data.corr()

plt.figure(figsize=(15, 10))
sns.heatmap(corr_matrix, annot=True)
plt.title('Correlation Matrix')
plt.show()

data['FlightDate'] = pd.to_datetime(data['FlightDate'])

avg_delay_month = data.groupby(data['FlightDate'].dt.month)['is_delay'].mean().reset_index()
fig = px.bar(avg_delay_month, x='FlightDate', y='is_delay', 
             labels={'FlightDate': 'Month', 'is_delay': 'Average Delay'}, 
             title='Average Delay by Month')
fig.update_traces(marker_color='skyblue')
fig.show()

X = data[['AirTime', 'Distance']]
y = data[['ArrDelayMinutes', 'is_delay']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

air_time = float(input("Enter Air Time in minutes: "))
distance = float(input("Enter Distance in miles: "))
user_input = np.array([[air_time, distance]])
user_input_scaled = scaler.transform(user_input)
predictions = model.predict(user_input_scaled)
if predictions[0][1] >= 0.5:
    print(f"The flight is delayed by {predictions[0][0]} minutes.")
else:
    print("The flight is not delayed.")
