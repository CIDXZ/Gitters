import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('company_sales_data.csv')


face_cream_sales = df[['month_number', 'facecream']].set_index('month_number')
face_wash_sales = df[['month_number', 'facewash']].set_index('month_number')


ax = face_cream_sales.plot(kind='bar', color='blue', alpha=0.5)
face_wash_sales.plot(kind='bar', color='green', alpha=0.5, ax=ax)


plt.title('Face Cream and Face Wash Sales Data')
plt.xlabel('Date')
plt.ylabel('Sales')


plt.show()

