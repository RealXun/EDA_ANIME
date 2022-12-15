import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.stats import shapiro
from scipy.stats import anderson
from scipy.stats import normaltest
from scipy.stats import spearmanr

os.chdir(os.path.dirname(sys.path[0])) # This command makes the notebook the main path and can work in cascade.
main_folder = sys.path[0]
data_folder = (main_folder + "\data")
img_folder = (main_folder + "\images")

'''
To predict the missing information in the rank column
'''
def predict(df):

    # df with the zero values in rank column
    with_zeros = df[['Score','Scored_by','Rank']].copy()

    # setup x and y for training
    # drop data with zero in the row
    clean_df = with_zeros[with_zeros.Rank  != 0]

    # separate variables into my x and y
    x = clean_df[['Score','Scored_by']].values
    y = clean_df['Rank'].values

    # fit my model (adjusting the parameters in the model to improve accuracy.)
    lm = LinearRegression()
    lm.fit(x, y)

    # get the rows I am trying to do my prediction on
    predict_x = with_zeros[with_zeros['Rank'] == 0][['Score','Scored_by']].values

    # perform my prediction
    lm.predict(predict_x)

    # Get index of missing data
    missing_index = with_zeros[with_zeros['Rank'] == 0].index

    # Replace
    df.loc[missing_index, 'Rank'] = lm.predict(predict_x)



'''
Convert the string time to just minutes
'''
def to_minutes(df):
    df['Duration'] = df['Duration'].apply(lambda positions : positions.split(' ')).apply(lambda positions : positions[0] if len(positions) <= 1 else # is lenght of the word 1 or is less than 1 then zero
            (int(positions[0]) / 60 if positions[1] == 'sec' else # If position 1 is sec, then we devide position 1 by 60
            (int(positions[0]) if positions[1] == 'min' else # if potision 1 is min, then pring position 0
            (int(positions[0]) * 60 if positions[1] == 'hr' and len(positions) == 2 else # If position 1 is hr and lenght of the string equals 2 (3 words), then we multiply position 1 by 60
            (int(positions[0]) * 60 + int(positions[2]) if positions[1] == 'hr' and positions[2] != 'per' and positions[2] != 'min'  else # If position 1 is hr and position 2 is not ped, then we multiply position 1 by 60 and sum to position 2
            int(positions[0]) * 60  )))))


'''
Pichart unidemensioanl
'''
def pieplot(data, graph_name):
    # Create an axis object
    fig, ax = plt.subplots(1, 1, figsize = (15, 8))
    
    # Get the data in the right format
    piedata = Counter(data)

    height = list(piedata.keys()) # Assign keys to height
    bars  = list(piedata.values())# Assign values to bars
    
    # Assign explode value automatically depending on the data and
    # declaring the exploding pie to separate one of the parts, in this case, the higher
    max_val = max(bars)
    max_index = bars.index(max_val)
    length =len(bars)
    explode_value = tuple([0 if i!=max_index else 0.2 for i in range(length)])

    ax.pie(bars, labels = height, shadow = False, explode=explode_value ,startangle = 0, autopct = "%1.2f%%") # Plot the pie chart

    ax.set_title(f"Pie chart for {graph_name} category.")
    
    plt.savefig(os.path.join(img_folder, 'Pichart_unidemensional_' + graph_name + '.png'),dpi=600)# Saving the image to the images folder

    plt.show() # Show graphic

    plt.close()# Close the plot


'''
Histplot 
'''
def hist_plot(df,data1,name):
    # set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above) 
    sns.set(style="darkgrid")

    sns.histplot(data=df, x=data1, bins=50)

    plt.savefig(os.path.join(img_folder +  "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic

    plt.close()# Close the plot



'''
Histplot with line
'''
def hist_plot_line(df,data1,name):
    # set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above) 
    sns.set(style="darkgrid")

    sns.histplot(data=df, x=data1, kde = True, palette="light:m_r", log_scale=False, edgecolor=".3", linewidth=.5)

    plt.savefig(os.path.join(img_folder +  "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic

    plt.close()# Close the plot


'''
Histplot with line log_scale
'''
def hist_plot_line_logscale(df,data1,name):
    # set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above) 
    sns.set(style="darkgrid")

    sns.histplot(data=df, x=data1, kde = True, palette="light:m_r", log_scale=True, edgecolor=".3", linewidth=.5)

    plt.savefig(os.path.join(img_folder +  "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic

    plt.close()# Close the plot



'''
Displot 
'''
def dis_plot(df, data1,name):
    sns.displot(data = df , x = data1 , kde = True) #anderson darling
    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic

    plt.close()# Close the plot



'''
Barplot unidemensioanl
'''
def simple_barplot(data,col, name):

    bar_date_dict = Counter(data)
    
    barplot_df=pd.DataFrame.from_dict(bar_date_dict,orient='index').reset_index() # creating a df from

    barplot_df=barplot_df.rename(columns={'index':col, 0:'Count'}) # renaming the columns of the df

    plt.figure(figsize=(20,10))

    bar_plot = sns.barplot(x=barplot_df["Count"],y=barplot_df[col]) #assigning values to the plot

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top

    
    plt.xticks(rotation=90) # rotate the name of the bars

    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder

    plt.show() # Show graphic

    plt.close()# Close the plot 



'''
Countplot unidmensional
'''
def simple_countplot(df, info,name):
    plt.figure(figsize = (9,6))
    plot = sns.countplot(x = info, 
                data = df
    )
    plot.bar_label(plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top
    plt.xticks(rotation = 90)
    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show()
    plt.close()# Close the plot 



'''
Countplot unidmensional where the information taken is a list
'''
def countplot(df,column):
    # Process the genre column to split on comma and append resulting
    # genres all to a single list
    all = []
    for item in df:
        item = item.strip()
        all.extend(item.split(','))

    df_all = pd.DataFrame (all, columns = [column]) # Creation of a df in order to be able to order by descending in the plot

    # Plot the genres and their count respectively
    fig, ax = plt.subplots(1, 1, figsize = (20, 10))
    ax = sns.countplot(y= column, data = df_all, palette=['#FF9999',"#99CC99"],order=df_all[column].value_counts().index)
    ax.bar_label(ax.containers[0], label_type='edge') # add values above each bar in countplot

    # Set the axes and title of the plot
    plt.xticks(rotation = 45)
    plt.savefig(os.path.join(img_folder,"Countplot_Unidimensional_"+ column + '.png'),dpi=600)# Saving the image to the images folder
    plt.tight_layout()
    plt.show() # Show graphic
    plt.close()# Close the plot 

'''
Density plot
'''

def density(df,column, values,name):
# Converting to wide dataframe
    data_wide = df.pivot(columns = column,
                        values = values)
    
    # plotting multiple density plot
    data_wide.plot.kde(figsize = (8, 6),
                    linewidth = 4)
    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic
    plt.close()# Close the plot 


'''
Barplot unidmensional where the information taken is a list
'''
def complex_barplot(data, data1, name):
    # Process the genre column to split on comma and append resulting
    # genres all to a single list
    categ_list = []
    for item in data:
        item = item.strip().split(',')
        categ_list.extend(item)

    # creating a dict from the data
    bar_dict = Counter(categ_list)
    
    barplot_df=pd.DataFrame.from_dict(bar_dict,orient='index').reset_index() # creating a df from

    plt.figure(figsize=(20,10))

    barplot_df=barplot_df.rename(columns={'index':data1, 0:'Count'}) # renaming the columns of the df

    bar_plot = sns.barplot(x=barplot_df[data1],y=barplot_df["Count"]) #assigning values to the plot

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top
    

    plt.xticks(rotation=90) # rotate the name of the bars
    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show()
    plt.close()# Close the plot



'''
Barplot for top 10 Unidimensional strings
'''
def complex_barplot_top10(data,name):
    splitted_data = data.str.split(',').explode().value_counts().head(10)
    splitted_index = data.str.split(',').explode().value_counts().head(10).index

    plt.figure(figsize=(20, 6))

    bar_plot = sns.barplot(y = splitted_index , x = splitted_data )

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top
    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic
    plt.close()# Close the plot 



'''
Barplot for top 10 Unidimensional
'''
def barplot_top10(data,name):

    splitted_data = data.value_counts().head(10)
    splitted_index = data.value_counts().head(10).index

    plt.figure(figsize=(10,8))

    bar_plot = sns.barplot(y = splitted_data , x = splitted_index )

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top
    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic
    plt.close()# Close the plot





'''
Heatmap correlation
'''
def heat(df):
    # Checking possible correlations for future studies.
    plt.rc("figure", figsize=(16,8))

    corr = df.corr()
    sns.heatmap(corr, annot=True)
    plt.title('Correlation matrix')
    plt.savefig(os.path.join(img_folder, 'Correlation matrix.png'),dpi=600)# Saving the image to the images folder
    plt.show()
    plt.close()# Close the plot


'''
Boxplot unidimensinal
'''
def box(df,cat,name):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data = df , x = cat,showmeans=True,meanprops={"marker":"o",
                       "markerfacecolor":"white", 
                       "markeredgecolor":"black",
                      "markersize":"10"})
    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic
    plt.close()# Close the plot

'''
Lineplot
'''
def line_plot(df, data1,data2,title,name):
    df_type_year =(df.assign(genre=df[data1])
      .groupby([data2,data1]).size()
      .reset_index(name='counts')
    )

    sns.lineplot(data=df_type_year, x=data2, y='counts', hue=data1)
    plt.tick_params(axis='x', labelrotation = 70)
    plt.title(title)
    plt.legend(loc='upper left')
    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic
    plt.close()# Close the plot 


'''
Calculo de media, meiana, max y min
'''
def various(df,x,y): # we pass de dataframe, the categorical column and the numerical column
    return df.groupby([x] , as_index=True).agg({y: ['mean', 'median','min', 'max']}).sort_values(by=(y, 'mean'),ascending=False).head(10)


'''
Calculo de mediana
'''
def median(df,x,y): # we pass de dataframe, the categorical column and the numerical column
    return df.groupby([x] , as_index=False).agg({y:'median'}).sort_values(y , ascending = False).head(10)


'''
Calculo de las media
'''
def mean(df,x,y): # we pass de dataframe, the categorical column and the numerical column
    return df.groupby([x] , as_index=False).agg({y : 'mean'}).sort_values(y , ascending = False).head(10)

'''
Calculo de suma
'''
def sum(df,x,y): # we pass de dataframe, the categorical column and the numerical column
    return df.groupby([x] , as_index=False).agg({y:'sum'}).sort_values(y , ascending = False).head(10)

'''
Boxplot bidimensional
'''
def box_bidi(df,arithmetic,value1,value2):
    plt.figure(figsize=(20,8))
    sns.boxplot(x= value1 , y = value2, data = df , order= arithmetic[value1] ,showmeans=True, meanprops={"marker":"o",
                       "markerfacecolor":"white", 
                       "markeredgecolor":"black",
                      "markersize":"10"})
    plt.savefig(os.path.join(img_folder, 'bidimensional_' + value1+ "_" + value2+ '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic
    plt.close()# Close the plot 



'''
Scaterplot
'''
def scat(df_copy,value1,value2,name):
    plt.figure(figsize=(15,5))
    sns.scatterplot(data = df_copy , x = value1 , y= value2 , hue = value2 , size = value2 , sizes = (20,200))
    plt.savefig(os.path.join(img_folder + "/" + name + '.png'),dpi=600)# Saving the image to the images folder
    plt.show() # Show graphic
    plt.close()# Close the plot




'''
Function to extract the data of a columns with respect to another column.

'''
def series_extract(df,index_name , target_name): #Col name is the column to which we want to extract the data.

  datos = [] #Store the data
  cont = 0
  index = df.columns.get_loc(target_name) #To know the index of the desired column

  for list_items in df[index_name]:

    for gen in list_items:
        
        value = df.iloc[cont , index ] #Find the value of the desired column 
        datos.append(value) #Store values from the value to the data list

    cont += 1   

  return pd.Series(datos)


'''
Function to check if the data normally distributed - normality_test

'''

def normality_test(df):
    # D'Agostino (kurtosis and skewness) normality test
    stat, p = normaltest(df)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha: # null hypothesis: x comes from a normal distribution
        print("P-Values is bigger than 0.05")
        print('We fail to reject the null hypothesis. The data is normally distributed')
    else: # alternative hypothesis: x comes from a not normal distribution
        print("P-Values is smaller than 0.05")
        print('We reject the null hypothesis and We fail to reject the alternative hypothesis. The data is not normally distributed')


'''
Function to check if the data normally distributed - Shapiro-Wilk  normality test

'''

def shapiro_test(df):
    # Shapiro-Wilk  normality test
    stat, p = shapiro(df)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpretation
    alpha = 0.05
    if p > alpha: # null hypothesis: x comes from a normal distribution
        print("P-Values is bigger than 0.05")
        print('We fail to reject the null hypothesis. The data is normally distributed')
    else: # alternative hypothesis: x comes from a not normal distribution
        print("P-Values is smaller than 0.05")
        print('We reject the null hypothesis and We fail to reject the alternative hypothesis. The data is not normally distributed')



'''
Function to check if the data normally distributed - Anderson-Darling normality test

'''
def anderson_test(df):
    # Anderson-Darling normality test
    result = anderson(df)
    print('Statistic: %.3f' % result.statistic)
    for i in range(len(result.critical_values)):
        sl, cv = result.significance_level[i], result.critical_values[i]
        if result.statistic < result.critical_values[i]: # null hypothesis: x comes from a normal distribution
            print('%.3f: %.3f, data looks normally distributed. We fail to reject the null hypothesis.' % (sl, cv))
        else: # alternative hypothesis: x comes from a not normal distribution
            print('%.3f: %.3f, data does not looks normally distributed. We reject the null hypothesis and We fail to reject the alternative hypothesis. ' % (sl, cv))




'''
Function to check if the data correlation - Spearman's dependency test

'''
def spearman(data1, data2):
    # Spearman's dependency test
    stat, p = spearmanr(data1, data2)
    print('Spearmans correlation coefficient: %.3f' % stat)
    # interpret the significance
    alpha = 0.05
    if p > alpha:
        print("'P-value equals %.3f. The two samples are independent. We fail to reject the null hypothesis" % p)
    else:
        print('P-value equals %.3f. There is a dependency between the samples. We reject the null hypothesis and We fail to reject the alternative hypothesis'% p)


'''
Function that devide the columna 1 (it should be a strings separated by commas) and extract the data from extra columns with respect to columna 1. *args should be numerical or string we will not separate

'''
def x_by_y(main_df,column1,*args):
    # Create a copy of df_copy
    def_df = main_df.copy()
    #Since the infomation are in lists we separate the information to have a better analysis of them. 
    def_df[f'{column1}_Split'] = def_df[column1].apply(lambda x : x.split(',')) # split the information by comma.

    #create a new auxiliar dataframe
    aux_df = pd.DataFrame() 
    #Set the columns with their score and scored_by
    aux_df[column1] = pd.Series([x for _list in def_df[f'{column1}_Split'] for x in _list]) # remove corchetes.
    for i in args:
        aux_df[i] = series_extract(def_df,f'{column1}_Split', i) #Funciton to extract the data of a column with respect to another column.
    return aux_df