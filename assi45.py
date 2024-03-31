import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('company_sales_data.csv')


bathing_soap = df['bathingsoap']
facewash = df['facewash']


fig, ax = plt.subplots(1, 2, figsize=(10, 5))


ax[0].plot(bathing_soap)
ax[0].set_xlabel('Month')
ax[0].set_ylabel('Sales')
ax[0].set_title('Bathing Soap Sales')


ax[1].plot(facewash)
ax[1].set_xlabel('Month')
ax[1].set_ylabel('Sales')
ax[1].set_title('Facewash Sales')


plt.show()
