from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.offline as pyoff
import plotly.graph_objects as go

df_retail = pd.read_csv('OnlineRetail.csv', encoding='unicode_escape')
df_retail.info()
df_retail['InvoiceDate'] = pd.to_datetime(df_retail['InvoiceDate'])

#Thêm các cột cho việc thống kê
df_retail['InvoiceYearMonth'] = df_retail['InvoiceDate'].map(lambda x: x.year*100 + x.month)
df_retail['Revenue'] = df_retail['UnitPrice'] * df_retail['Quantity']
df_retail['InvoiceYearMonth'].unique()



#Tỷ lệ tăng trưởng doanh thu qua các tháng
df_revenue = df_retail.groupby('InvoiceYearMonth')['Revenue'].sum().reset_index()
pct_change_ = [0]
for i in range (len(df_revenue)):
    pct_change  = (df_revenue['Revenue'][i+1] - df_revenue['Revenue'][i])/df_revenue['Revenue'][i]
    pct_change_.append(pct_change)
df_revenue['pct_change'] = pct_change_
plot_data_revenue = [
    go.Scatter(
    x=df_revenue['InvoiceYearMonth'],
    y=df_revenue['pct_change']
)]
plot_layout  = go.Layout(xaxis = {'type':'category'}, title = 'MonthlyGrowRate')
fig_revenue = go.Figure(data = plot_data_revenue, layout= plot_layout)
pyoff.plot(fig_revenue)



#hơn 90% dữ liệu là ở Mỹ, nên chỉ thống kê ở Mỹ cho cụ thể
df_uk = df_retail[df_retail['Country'] == 'United Kingdom'].reset_index(drop=True)



#số khách mua hàng mỗi tháng
df_monthly_active = df_uk.groupby('InvoiceYearMonth')['CustomerID'].nunique().reset_index()

plot_data_active = [
    go.Bar(
    x=df_monthly_active['InvoiceYearMonth'],
    y=df_monthly_active['CustomerID']
)]

plot_layout_active  = go.Layout(xaxis = {'type':'category'}, title = 'MonthlyActiveCustomer')

fig_revenue_active = go.Figure(data = plot_data_active, layout= plot_layout_active)
pyoff.plot(fig_revenue_active)

df_monthly_active['CustomerID'].mean()


#lượng sản phẩm bán mỗi tháng
df_monthly_sales = df_uk.groupby('InvoiceYearMonth')['Quantity'].sum().reset_index()

plot_data_sales= [
    go.Bar(
    x=df_monthly_sales['InvoiceYearMonth'],
    y=df_monthly_sales['Quantity']
)]

plot_layout_sales = go.Layout(xaxis = {'type':'category'}, title = 'MonthlySales')

fig_revenue_sales = go.Figure(data = plot_data_sales, layout= plot_layout_sales)
pyoff.plot(fig_revenue_sales)

df_monthly_sales['Quantity'].mean()

#doanh thu trung bình tháng
df_monthly_revenue_avg = df_uk.groupby('InvoiceYearMonth')['Revenue'].mean().reset_index()
plot_data_revenue_avg= [
    go.Bar(
    x=df_monthly_revenue_avg['InvoiceYearMonth'],
    y=df_monthly_revenue_avg['Revenue']
)]

plot_layout_revenue_avg = go.Layout(xaxis = {'type':'category'}, title = 'MonthlySales')

fig_revenue_revenue_avg = go.Figure(data = plot_data_revenue_avg, layout= plot_layout_revenue_avg)
pyoff.plot(fig_revenue_revenue_avg)


#so sánh doanh thu của khách hàng cũ và mới mỗi tháng
df_min_purchase = df_uk.groupby('CustomerID')['InvoiceDate'].min().reset_index()
df_min_purchase.columns = ['CustomerID','MinPurchaseDate']
df_uk = pd.merge(df_uk, df_min_purchase, on='CustomerID')
df_uk['UserType'] = 'New'
df_uk.loc[df_uk['InvoiceDate'] != df_uk['MinPurchaseDate'], 'UserType'] = 'Existing'
df_uk['UserType'].value_counts()


df_user_type_revenue = df_uk.groupby(['InvoiceYearMonth','UserType'])['Revenue'].sum().reset_index()
df_user_type_revenue = df_user_type_revenue.query('InvoiceYearMonth != 201112')

plot_data_type = [
    go.Scatter(
        x=df_user_type_revenue.query("UserType == 'Existing'")['InvoiceYearMonth'],
        y=df_user_type_revenue.query("UserType == 'Existing'")['Revenue'],
        name='Existing'
    ),
    go.Scatter(
        x=df_user_type_revenue.query("UserType == 'New'")['InvoiceYearMonth'],
        y=df_user_type_revenue.query("UserType == 'New'")['Revenue'],
        name='New'
    ),
]
plot_layout_type = go.Layout(
    xaxis={'type':'category'},
    title='Revenue of New vs Existing Customer'
)
fig_type = go.Figure(data=plot_data_type,layout=plot_layout_type)
pyoff.plot(fig_type)

#tỷ lệ khách hàng cũ và mới
NewCustomer = df_uk.query("UserType == 'New'").groupby('InvoiceYearMonth')['CustomerID'].nunique()
ExistingCustomer = df_uk.query("UserType == 'Existing'").groupby('InvoiceYearMonth')['CustomerID'].nunique()

df_user_ratio = NewCustomer/ExistingCustomer
df_user_ratio = df_user_ratio.reset_index()
df_user_ratio.columns = ['InvoiceYearMonth','Ratio']

plot_data_ratio = [
    go.Bar(
        x=df_user_ratio['InvoiceYearMonth'],
        y=df_user_ratio['Ratio']
    )
]

plot_layout_ratio = go.Layout(
    xaxis={'type':'category'},
    title='Ratio of New vs Existing Customer')

fig_ratio = go.Figure(data=plot_data_ratio,layout=plot_layout_ratio)
pyoff.plot(fig_ratio)

