import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# def radar_plot(df, cntry, subplot_1, subplot_2, subplot_loc) :
#     categories = list(df.columns)[2:]
#     N = len(categories)
#     values = list(df.iloc[cntry, 2:])
#     values += values[:1]
#     angles = [n / float(N) * 2 * pi for n in range(N)]
#     angles += angles[:1]
#     plt.figure(figsize = [6, 6])
#     ax = plt.subplot(subplot_1, subplot_2, subplot_loc, polar = True)
#     ax.set_theta_offset(pi / 2)
#     ax.set_rlabel_position(0)
#     plt.xticks(angles[:-1], categories, color = '#888B8D', size = 10, fontname = 'Times New Roman')
#     plt.yticks(color = '#888B8D', size = 7)
#     ax.spines['polar'].set_color('#888B8D')
#     plt.ylim(0, 100)
#     ax.plot(angles, values, linewidth = 1,linestyle = 'solid', color = '#00205B')
#     ax.fill(angles, values, color = '#00205B', alpha = 0.1)
#     plt.title(df.iloc[cntry, 0], fontname = 'Times New Roman', color = '#888B8D', size = 14)
#     plt.show()

#Read in data and convert to 0-100 scale
df = pd.read_csv('SP_combined_results.csv')
df.iloc[:, 2:] = df.iloc[:, 2:] * 100

#Slice dataframe by year
#df = df[df['Year'] == 2017]

#Get countries
# country = np.where(df['Country'] == 'ARGENTINA')[0]

#By comparison countries

#By year
country = input('Which country? ')
country = country.upper()
while country != 'DONE' :
    cntry = np.where(df['Country'] == country)[0]
    yrs = range(len(cntry))
    if len(yrs) == 1 :
        print ('')
        print ('Not two years of data')
        print ('')
        country = input('New country? Or type "done" to quit. ')
        country = country.upper()
        continue
    if len(yrs) == 0 :
        print ('')
        print ('Not in your own dataset you big dummy')
        print ('')
        country = input('New country? Or type "done" to quit. ')
        country = country.upper()
        continue
    rowvals = []
    for yr in yrs :
        rowval = cntry[yr]
        rowvals.append(rowval)

    categories = list(df.columns)[2:9]
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    plt.figure(figsize = [8, 6])
    ax = plt.subplot(1, 1, 1, polar = True)
    ax.set_theta_offset(pi / 2)
    ax.set_rlabel_position(0)
    plt.xticks(angles[:-1], categories, color = '#888B8D', size = 10, fontname = 'Times New Roman')
    plt.yticks(color = '#888B8D', size = 7)
    ax.spines['polar'].set_color('#888B8D')
    plt.ylim(0, 100)
    plt.title(df.iloc[cntry, 0], fontname = 'Times New Roman', color = '#888B8D', size = 14)

    #2016
    values = list(df.iloc[rowvals[0], 2:9])
    values += values[:1]
    ax.plot(angles, values, linewidth = 1,linestyle = 'solid', label = '2016', color = '#00205B')
    ax.fill(angles, values, color = '#00205B', alpha = 0.1)

    #2017
    values = list(df.iloc[rowvals[1], 2:9])
    values += values[:1]
    ax.plot(angles, values, linewidth = 1,linestyle = 'solid', label = '2017', color = '#ED8B00')
    ax.fill(angles, values, color = '#ED8B00', alpha = 0.1)

    plt.legend(bbox_to_anchor = (1.3, 1.1))
    plt.title(df.iloc[rowvals[0], 0], color = '#888B8D', size = 14, fontname = 'Times New Roman')
    plt.show()

    print ('')
    country = input('New country? Or type "done" to quit. ')
    country = country.upper()
else :
    exit()
