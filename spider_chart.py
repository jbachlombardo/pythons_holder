import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from math import pi
from sklearn import preprocessing

# df = pd.DataFrame({
# 'group': ['A','B','C','D'],
# 'var1': [38, 1.5, 30, 4],
# 'var2': [29, 10, 9, 34],
# 'var3': [8, 39, 23, 24],
# 'var4': [7, 31, 33, 14],
# 'var5': [28, 15, 32, 14]
# })

def to_100(x) :
    if type(x) == int :
        return x * (100 / df.iloc[:, 1:].values.max())
    else :
        return x

def log(x) :
    if type(x) == int :
        return np.log(x)
    else :
        return x

df = pd.read_csv('countrydata.csv')
df_scaled_100 = df.copy()
df_scaled_log = df.copy()
df_scaled_scaler = df.copy()
df_scaled_normalizer = df.copy()

df_scaled_100 = df_scaled_100.applymap(to_100)
df_scaled_100.iloc[:, 1:] -= df_scaled_100.iloc[:, 1:].values.min()

df_scaled_log = df_scaled_log.applymap(log)
df_scaled_log.iloc[:, 1:] -= df_scaled_log.iloc[:, 1:].values.min()

scaler = preprocessing.StandardScaler()
df_scaled_scaler.iloc[: , 1:] = scaler.fit_transform(df_scaled_scaler.iloc[: , 1:])
df_scaled_scaler.iloc[:, 1:] -= df_scaled_scaler.iloc[:, 1:].values.min()

normalizer = preprocessing.Normalizer()
df_scaled_normalizer.iloc[: , 1:] = normalizer.fit_transform(df_scaled_normalizer.iloc[: , 1:])

def radar_plot(df, cntry, subplot_1, subplot_2, subplot_loc, color) :
    ymax = df.iloc[:, 1:].values.max()
    ymin = df.iloc[:, 1:].values.min()
    categories = list(df.columns)[1:]
    N = len(categories)

    values = list(df.iloc[cntry, 1:])
    values += values[:1]

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    plt.figure(figsize = [6, 6])

    ax = plt.subplot(subplot_1, subplot_2, subplot_loc, polar = True)

    ax.set_theta_offset(pi / 2)

    plt.xticks(angles[:-1], categories, color = 'black', size = 10)

    ax.set_rlabel_position(0)
    #plt.yticks([], [])
    plt.yticks(color = 'black', size = 7)
    plt.ylim(ymin, ymax)

    ax.plot(angles, values, linewidth = 1,linestyle = 'solid', color = color)

    ax.fill(angles, values, color = color, alpha = 0.1)

    plt.title(df.iloc[cntry, 0])
palette = plt.cm.get_cmap('Set2', len(df))

#radar_plot(df, cntry, subplot_1, subplot_2, subplot_loc, color) :
for row in range(0, len(df_scaled_scaler)) :
    radar_plot(df_scaled_scaler, row, 1, 1, 1, palette(row))
plt.show()
# #
# for row in range(0, len(df_scaled_log)) :
#     radar_plot(df_scaled, row, 1, 1, 1, palette(row))

# print ('df')
# print (df)
# radar_plot(df, 1, 1, 1, 1, palette(1))
# print ('df_scaled_100')
# print (df_scaled_100)
# radar_plot(df_scaled_100, 1, 1, 1, 1, palette(1))
# print ('df_scaled_log')
# print (df_scaled_log)
# radar_plot(df_scaled_log, 1, 1, 1, 1, palette(1))
# print ('df_scaled_scaler')
# print (df_scaled_scaler)
# radar_plot(df_scaled_scaler, 1, 1, 1, 1, palette(1))
# print ('df_scaled_normalizer')
# print (df_scaled_normalizer)
# radar_plot(df_scaled_normalizer, 1, 1, 1, 1, palette(1))
