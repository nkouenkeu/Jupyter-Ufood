#!/usr/bin/env python
# coding: utf-8

# what is the weight of the five categories(wine,rare meat product,exotic fruits, prepared fish, sweet product)?
# what is the impact of the different campaign of marketing?
# what is the most valuable sell place( Web, store or catalogue)?
# what is the link between the age, income according to the orders?

# HYPOTHESES
# The high order according to the age and income
# The best marketing campaign customer_day
# The best place selling place according to the income
# 

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# ufood = pd.read_csv(r'C:\Users\alain abega\Downloads\Documents\U_food_marketing.csv')
# 
# pd.set_option('display.max.rows', 2260)
# pd.set_option('display.max.columns', 50)

# In[3]:


#pd.options.display.float_format = '{:,.2f}'.format


# In[3]:


ufood.head()


# In[4]:


ufood.drop_duplicates(keep = False, inplace = True)


# In[158]:


ufood['Total_children']=ufood[['Kidhome', 'Teenhome']].sum(axis = 1) 


# In[159]:


ufood[ufood['Marital_Status'] != 0].head()


# In[16]:


ufood['marital_Divorced'] = ufood['marital_Divorced'].replace({1:5, 0:0})
ufood['marital_Married'] = ufood['marital_Married'].replace({1:4, 0:0})
ufood['marital_Single'] = ufood['marital_Single'].replace({1:3, 0:0})
ufood['marital_Together'] = ufood['marital_Together'].replace({1:2, 0:0})
ufood['marital_Widow'] = ufood['marital_Widow'].replace({1:1, 0:0})


# In[24]:


# Sum of the Status columns through a list 
ufood['Marital_Status'] = ufood[['marital_Divorced','marital_Married','marital_Single', 'marital_Together','marital_Widow']].sum(axis=1)


# In[18]:


# transform th int to str, because we want to groupby and do visualization 
ufood['Marital_Status_str'] = ufood['Marital_Status'].map({5:'Divorced', 4:'Married', 3:'Single', 2:'Together', 1:'Widow'})


# In[20]:


ufood.columns


# In[35]:


# let#s use the same process for education level
ufood['education_2n Cycle'] = ufood['education_2n Cycle'].replace({1:1, 0:0})
ufood['education_Basic'] = ufood['education_Basic'].replace({1:2, 0:0})
ufood['education_Graduation'] = ufood['education_Graduation'].replace({1:3, 0:0})
ufood['education_Master'] = ufood['education_Master'].replace({1:4, 0:0})
ufood['education_PhD'] = ufood['education_PhD'].replace({1:5, 0:0})


# In[36]:


ufood['Education_Status'] = ufood[['education_2n Cycle','education_Basic','education_Graduation', 'education_Master','education_PhD']].sum(axis=1)


# In[32]:


ufood[ufood['Education_Status'] != 0].head()


# In[41]:


#ufood['Education_Status_str'] = ufood['Education_Status'].map({1:'education_2n Cycle', 2:'education_Basic', 3:'education_Graduation', 4:'education_Master', 5:'education_PhD'})


# In[73]:


# Just need to add all the campaigns columns in one column.
ufood['Accepted_Campaigns'] =  ufood[['AcceptedCmp3','AcceptedCmp4','AcceptedCmp5', 'AcceptedCmp1','AcceptedCmp2','Response']].sum(axis=1)


# In[74]:


ufood['Accepted_Campaigns'] = (ufood['Accepted_Campaigns'] != 0).astype(int)


# In[75]:


# let's start with the correlation,to improve the performance of marketing activities,a special focus on marketing campaigns
ufood.corr(method = 'pearson',min_periods = 1,numeric_only = True)['Accepted_Campaigns'].sort_values(ascending=False)


# In[76]:


sns.heatmap(ufood.corr(method = 'pearson',min_periods = 0,numeric_only = True))


# In[77]:


all_correlations = ufood.corr(method = 'pearson', min_periods = 0, numeric_only = True)
all_correlations = all_correlations[(all_correlations > 0.3) & (all_correlations < 1)]

sns.heatmap(all_correlations)


# In[78]:


#let's look for the data 
all_correlations['Accepted_Campaigns']


# In[81]:


# The first is to analyze the age 
#ufood['Age'].sort_values()
ufood['Age'].nunique()


# In[100]:


age_groups = [(23,30),(31,40),(41,50), (51,60), (61,70),(71,85)]

def assign_age_group(Age):
    for age_range in age_groups:
        if age_range[0]<= Age <= age_range[1]:
            return f"{age_range[0]} - {age_range[1]}"
    return("unknown")
    
ufood['Age_Group'] = ufood['Age'].apply(assign_age_group)


# In[102]:


ufood[['Age','Age_Group']].head()


# In[108]:


# Try to put the age in the range values.
age_order = ['23 - 30','31 - 40','41 - 50', '51 - 60', '61 - 70','71 - 85']

sns.pointplot(data = ufood, x = 'Age_Group', y = 'Accepted_Campaigns', order = age_order)
plt.title('percentage per age')


# In[110]:


# Find the correct number of cunsummer par age range
counts =ufood['Age_Group'].value_counts()


# In[111]:


percentage = counts / ufood.shape[0]


# In[114]:


# reset_index 
percent_ufood = percentage.reset_index()


# In[118]:


# columns names
percent_ufood.columns = ['age_group','percentage']


# In[120]:


percent_ufood = percent_ufood.sort_values('age_group')


# In[121]:


percent_ufood


# In[123]:


sns.barplot(data = percent_ufood, x = 'age_group', y = 'percentage')
plt.title('percentage per age')
plt.show()


# In[ ]:


# The accepted campaigns is between 31 and 70 age 


# In[134]:


# Now is to know how much they spend per age 
group_ufood = ufood.groupby('Age_Group')[['MntTotal']].sum().reset_index()
sns.barplot(data = group_ufood, x = 'Age_Group', y = 'MntTotal')
plt.title('spending per age')
plt.show()


# In[ ]:


# There is two ways of proposition, the group between 23-30 and 71-85, spend less money than the other group by they are very open to say yes to campaing.


# In[139]:


# The percentage just increased a bit with the accepted_campaigns.
acc_campaign = ufood[ufood['Accepted_Campaigns'] != 0]

group_ufood = acc_campaign.groupby('Age_Group')[['MntTotal']].sum().reset_index()
sns.barplot(data =group_ufood , x = 'Age_Group', y = 'MntTotal')
plt.title('spending per age')
plt.show()


# In[165]:


# The other thing,we can also see it's the place they purchase.
ufood.head()


# In[145]:


sum_ufood = pd.DataFrame(ufood[['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']].sum(), columns =['Sum'])


# In[148]:


sum_ufood = sum_ufood.reset_index()


# In[149]:


sum_ufood.rename(columns={'index':'Purchases'}, inplace=True)


# In[150]:


sum_ufood.head()


# In[151]:


sns.barplot(data =sum_ufood,  x = 'Purchases', y = 'Sum' )


# In[152]:


# Now we want to filter with accepted campaings
acc_campaign = ufood[ufood['Accepted_Campaigns'] != 0]

sum_ufood = pd.DataFrame(ufood[['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']].sum(), columns =['Sum'])
sum_ufood = sum_ufood.reset_index()
sum_ufood.rename(columns={'index':'Purchases'}, inplace=True)
sns.barplot(data =sum_ufood,  x = 'Purchases', y = 'Sum')
plt.show()


# In[157]:


x = sns.jointplot(data = ufood, x = 'MntTotal', y = 'NumWebPurchases', kind = 'kde')
x.plot_joint(sns.regplot, color = 'r')


# In[ ]:


x = sns.jointplot(data = ufood, x = 'MntTotal', y = 'NumCatalogPurchases', kind = 'kde')
x.plot_joint(sns.regplot, color = 'r')


# In[ ]:


x = sns.jointplot(data = ufood, x = 'MntTotal', y = 'NumStorePurchases', kind = 'kde')
x.plot_joint(sns.regplot, color = 'r')


# In[ ]:


#  Boost up the higher percentage or face on stores/web because they have more traffic


# In[161]:


# Child home 
sns.regplot(data = ufood, x = 'Total_children', y = 'Accepted_Campaigns')


# In[ ]:


# no kids ready to accept campaign and spend more money, more kids no campaign accepeted(a bit difficult)


# In[163]:


# Education level
sns.regplot(data = ufood, x = 'Education_Status', y = 'MntTotal')


# In[ ]:


# More educated people tend to accpet campaign, 


# In[169]:


#Status
sns.countplot(data =ufood,  x = 'Marital_Status_str')
plt.show()


# In[170]:


sns.regplot(data = ufood, x = 'Marital_Status', y = 'MntTotal')


# In[174]:


rel_ufood = ufood.groupby('Marital_Status_str')['MntTotal'].sum().reset_index()


# In[175]:


sns.barplot(data= rel_ufood, x = 'Marital_Status_str', y = 'MntTotal')


# In[186]:


total = ufood['Marital_Status_str'].value_counts()
accepted = ufood[ufood['Accepted_Campaigns'] == 1]['Marital_Status_str'].value_counts()


# In[194]:


perc_marital = accepted / total*100
perc_ufood = perc_marital.reset_index()
perc_ufood.columns = ['Marital_Status','Percentage']
sns.barplot(data= perc_ufood, x = 'Marital_Status', y = 'Percentage')
plt.show()


# In[ ]:


# Married people spend more than the others


# In[ ]:





# In[ ]:




