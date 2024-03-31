import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('company_sales_data.csv')


df.set_index('month_number', inplace=True)


df.plot(kind='line')


plt.title('Product Sales Data')
plt.xlabel('Date')
plt.ylabel('Sales')


plt.show()
