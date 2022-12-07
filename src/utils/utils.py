import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

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

    plt.show() # Show graphic

    plt.close()# Close the plot



'''
Barplot unidemensioanl
'''
def simple_barplot(data, graph_name):

    bar_date_dict = Counter(data)

    barplot_df=pd.DataFrame.from_dict(bar_date_dict,orient='index').reset_index() # creating a df from

    barplot_df=barplot_df.rename(columns={'index':graph_name, 0:'Count'}) # renaming the columns of the df

    bar_plot = sns.barplot(x=barplot_df["Count"],y=barplot_df[graph_name]) #assigning values to the plot

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top

    plt.xticks(rotation=90) # rotate the name of the bars
    plt.show()



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
    sns.countplot(y= column, data = df_all, palette=['#FF9999',"#99CC99"],order=df_all[column].value_counts().index)

    # Set the axes and title of the plot
    plt.xticks(rotation = 45)
    plt.tight_layout()



'''
Barplot unidmensional where the information taken is a list
'''
def complex_barplot(data, graph_name):
    # Process the genre column to split on comma and append resulting
    # genres all to a single list
    categ_list = []
    for item in data:
        item = item.strip().split(',')
        categ_list.extend(item)

    # creating a dict from the data
    bar_dict = Counter(categ_list)

    barplot_df=pd.DataFrame.from_dict(bar_dict,orient='index').reset_index() # creating a df from

    barplot_df=barplot_df.rename(columns={'index':graph_name, 0:'Count'}) # renaming the columns of the df

    bar_plot = sns.barplot(x=barplot_df[graph_name],y=barplot_df["Count"]) #assigning values to the plot

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top

    plt.xticks(rotation=90) # rotate the name of the bars
    plt.show()



'''
Barplot for top 10 Unidimensional
'''
def complex_barplot_top10(data):
    splitted_data = data.str.split(',').explode().value_counts().head(10)
    splitted_index = data.str.split(',').explode().value_counts().head(10).index

    plt.figure(figsize=(20, 6))

    bar_plot = sns.barplot(y = splitted_index , x = splitted_data )

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top



'''
Barplot for top 10 Unidimensional
'''
def barplot_top10(data):

    splitted_data = data.value_counts().head(10)
    splitted_index = data.value_counts().head(10).index

    plt.figure(figsize=(10,8))

    bar_plot = sns.barplot(y = splitted_data , x = splitted_index )

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top



'''
Boxplot unidimensinal
'''
def box(df,cat):
    plt.figure(figsize=(6,6))
    sns.boxplot(data = df , y = cat)



'''
Find the top ten of a categorical column taking into reference a numerical column
'''
def top_10(df,x,y): # we pass de dataframe, the categorical column and the numerical column
    return df.groupby([x] , as_index=False).agg({y : 'median'}).sort_values(y , ascending = False).head(10)


'''
Find the top ten of a categorical column taking into reference a numerical column
'''
def top_10_multi(df,x,y,z): # we pass de dataframe, the categorical column and the numerical column
    return df.groupby([x] , as_index=False).agg({y : 'median', z: 'median'}).sort_values(y , ascending = False).head(10)


'''
Boxplot bidimensional
'''
def box_bidi(df,value1,value2):
    plt.figure(figsize=(20,8))
    return sns.boxplot(x= value1 , y = value2, data = df , order= top_10(df,value1,value2)[value1] )



'''
Scaterplot
'''
def scat(df_copy,value1,value2):
    plt.figure(figsize=(15,5))
    return sns.scatterplot(data = df_copy , x = value1 , y= value2 , hue = value2 , size = value2 , sizes = (20,200))




'''
Funciton to extract the data of a columns with respect to another column.

'''
def series_extract(df,col_index_name , col_target_name): #Col name is the column to which we want to extract the data.

  datos = [] #Store the data
  cont = 0
  index_column = df.columns.get_loc(col_target_name) #To know the index of the desired column

  for list_gen in df[col_index_name]:

    for gen in list_gen:
        
        val = df.iloc[cont , index_column ] #Find the value of the desired column 
        datos.append(val) #Store values from the value to the data list

    cont += 1   

  return pd.Series(datos)


'''
Boxplot
'''
def aux(df,x,y):
    get_score = series_extract(df,'Studios_Split', 'Score')
    df_anime_aux3 = pd.DataFrame() #New dataframe
    #Set the producers columns with their score
    df_anime_aux3[x] = df[x].str.split(',').explode()
    df_anime_aux3[y] = get_score

    return df_anime_aux3.head()
