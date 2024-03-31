import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('company_sales_data.csv')
sum_df = pd.DataFrame({
    'Product': ['Bathing Soap', 'Face Wash', 'Shampoo', 'Moisturizer', 'Face Cream', 'Toothpaste'],
    'Total Sales': [
        df['bathingsoap'].sum(),
        df['facewash'].sum(),
        df['shampoo'].sum(),
        df['moisturizer'].sum(),
        df['facecream'].sum(),
        df['toothpaste'].sum()
    ]
})



plt.pie(sum_df['Total Sales'], labels=sum_df['Product'], autopct='%1.1f%%')
plt.title('Total Sales by Product')
plt.show()







