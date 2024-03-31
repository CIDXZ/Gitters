import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('company_sales_data.csv')


monthly_profit = df.groupby('month_number')['total_profit'].sum()


plt.hist(monthly_profit, bins=10, color='blue', edgecolor='black')


plt.title('Total Profit by Month')
plt.xlabel('Total Profit')
plt.ylabel('Frequency')


plt.show()
