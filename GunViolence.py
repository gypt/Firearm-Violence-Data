
# coding: utf-8

# In[15]:


import pandas as p
import matplotlib.pyplot as mpl
k = 1
m = 2    
def plot(x):
    t_month = x.groupby('month')['total_victims'].sum() 
    t_year = x.groupby('year', as_index = False)['total_victims'].sum() 
    t_year = t_year[t_year['year'].str.contains('2022') == False]
    mpl.figure(1)
    t_month.plot(kind = 'bar')
    mpl.xlabel('Month')
    mpl.ylabel('Average Victims')
    mpl.suptitle("Average Victims per Month 2014-2021")
    mpl.savefig('MonthlyVictimBar.png')
    mpl.figure(2)
    t_year.plot(kind = 'line', legend = False)
    mpl.xlabel('Year')
    mpl.ylabel('Total Victims')
    mpl.suptitle("Annual Gun Violence Victims 2014-2021")
    mpl.savefig('YearlyVictimLine.png')      
def sort_st(x): #x['column_name'].describe() was used to determine quartile values
    a = x.groupby('state', as_index = False).agg({'n_kill':'sum','total_victims':'sum'})
    a['Fatal Chance(%)'] = (a['n_kill'] / a['total_victims'] * 100).apply(lambda x: round(x, k))
    a['Risk Value'] = ((a['n_kill'] * a['Fatal Chance(%)']) / 1000).apply(lambda x: round(x, m))
    a.loc[(a['Risk Value'] >= 132.05), 'Risk'] = 'High'
    a.loc[(a['Risk Value'] >= 68.44) & (a['Risk Value'] <= 132.05), 'Risk'] = 'Moderate'
    a.loc[(a['Risk Value'] >= 17.51) & (a['Risk Value'] <= 68.44), 'Risk'] = 'Low'
    a.loc[(a['Risk Value'] <= 17.51), 'Risk'] = 'Very Low'
    a.drop(['n_kill'], axis = 1, inplace = True)
    a.sort_values('Risk Value', inplace = True, ascending = True) 
    print('\nSafest States\n\n', a.head(15))
    a.sort_values('Risk Value', inplace = True, ascending = False)
    print('\nLeast Safe States\n\n', a.head(15))
def sort_city(x):
    x['Frequency'] = x.groupby('city')['city'].transform('count')
    x = x[x['Frequency'] >= 500] 
    b = x.groupby('city', as_index = False).agg({'state': 'first', 'n_kill': 'sum', 'total_victims':'sum'}) 
    b['Fatal Chance(%)'] = (b['n_kill'] / b['total_victims'] * 100).apply(lambda x: round(x, k))
    b['Risk Value'] = ((b['n_kill'] * b['Fatal Chance(%)']) / 1000).apply(lambda x: round(x, m))
    b.loc[(b['Risk Value'] >= 17.40), 'Risk'] = 'High'
    b.loc[(b['Risk Value'] <= 17.40) & (b['Risk Value'] >= 8.64), 'Risk'] = 'Moderate'
    b.loc[(b['Risk Value'] >= 4.40) & (b['Risk Value'] <= 8.64), 'Risk'] = 'Low'
    b.loc[(b['Risk Value'] <= 4.40), 'Risk'] = 'Very Low'
    b.drop(['n_kill'], axis = 1, inplace = True)
    b.sort_values('Risk Value', inplace = True, ascending = True) 
    print('\nSafest Cities\n\n', b.head(15))
    b.sort_values('Risk Value', inplace = True, ascending = False) 
    print('\nLeast Safe Cities\n\n', b.head(15))  
    
x = p.read_csv('gunv.csv') 
x['total_victims'] = x['n_kill'] + x['n_inj'] 
x[['month', 'day', 'year']] = x['date'].str.split('/', expand = True) 
x['month'] = p.to_numeric(x['month']) 
x.drop(['incident_id', 'address', 'operations', 'day', 'date'], axis = 1, inplace = True)
plot(x)
sort_st(x)
sort_city(x)

