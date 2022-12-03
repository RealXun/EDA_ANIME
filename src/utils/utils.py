import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np
import pandas as pd


def pieplot(data, graph_name):
    # Create an axis object
    fig, ax = plt.subplots(1, 1, figsize = (15, 8))
    
    # Get the data in the right format
    piedata = Counter(data)

    height = list(piedata.keys())
    bars  = list(piedata.values())
    
    # Assign explode value automatically depending on the data and
    # declaring the exploding pie to separate one of the parts, in this case, the higher
    max_val = max(bars)
    max_index = bars.index(max_val)
    length =len(bars)
    explode_value = tuple([0 if i!=max_index else 0.2 for i in range(length)])

    # Plot the pie chart
    ax.pie(bars, labels = height, shadow = False, explode=explode_value ,startangle = 0, autopct = "%1.2f%%")

    #ax.axis('equal')
    ax.set_title(f"Pie chart for {graph_name} category.")
    
    # Save the plot to an image

    # Show graphic
    plt.show()

    # Close the plot
    plt.close()

def simple_barplot(data, graph_name):
    # Process the genre column to split on comma and append resulting
    # genres all to a single list
    # all_genres = []
    # for item in anime_df["Genre"]:
    #     item = item.strip()
    #     all_genres.extend(item.split(','))


    # creating a dict from the data
    bar_date_dict = Counter(data)

    barplot_df=pd.DataFrame.from_dict(bar_date_dict,orient='index').reset_index() # creating a df from

    barplot_df=barplot_df.rename(columns={'index':graph_name, 0:'Count'}) # renaming the columns of the df

    bar_plot = sns.barplot(x=barplot_df[graph_name],y=barplot_df["Count"]) #assigning values to the plot

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top

    plt.xticks(rotation=90) # rotate the name of the bars
    plt.show()

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

def complex_barplot_top10(data):
    # Process the genre column to split on comma and append resulting
    # genres all to a single list
    splitted_data = data.str.split(',').explode().value_counts().head(10)
    splitted_index = data.str.split(',').explode().value_counts().head(10).index

    # creating a dict from the data

    plt.figure(figsize=(10,8))

    bar_plot = sns.barplot(y = splitted_index , x = splitted_data )

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top

def barplot_top10(data):
    # Process the genre column to split on comma and append resulting
    # genres all to a single list
    splitted_data = data.value_counts().head(10)
    splitted_index = data.value_counts().head(10).index

    # creating a dict from the data

    plt.figure(figsize=(10,8))

    bar_plot = sns.barplot(y = splitted_data , x = splitted_index )

    bar_plot.bar_label(bar_plot.containers[0],label_type='edge', fontsize=6) # Show the values of each bar at their top

def box(df,cat):
    plt.figure(figsize=(6,6))
    sns.boxplot(data = df , y = cat)





#### OLD ONES


def split(df,categ):
    categ_list = []
    for item in df[categ]:
        item = item.strip().split(',')
        categ_list.extend(item)
    list_data = Counter(categ_list)
    return list_data

def barplot(df, xcolname, ycolname, cmap = 'YlGnBu', quantity = "occurrences"):

    y_pos = np.arange(len(ycolname))

    # Create bars
    plt.bar(y_pos, ycolname)

    # Create names on the x-axis
    plt.xticks(y_pos, xcolname)

    # Show graphic
    plt.show()