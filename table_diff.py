import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
matplotlib.rcParams['font.sans-serif'] = 'Arial'

df = pd.read_csv('points_positions.csv')
df['Team'] = df['Team'].str.lstrip()

years = tuple(df['Year'].unique())
leagues = tuple(df['League'].unique())

#RELEGATION 10 POINT GAPS
rel_pos = {} #Relegation position for leagues with different #s of teams
dict_rel_pts = {} #The teams in relegation position
for league in leagues :
    val_rel_pos = len(df[(df['Year'] == 2018) & (df['League'] == league)]) - 2
    rel_pos[league] = val_rel_pos
    for year in years :
        rel = df[(df['Year'] == year) & (df['League'] == league)].set_index('Pos').loc[rel_pos[league], ['Pts', 'League']]
        dict_rel_pts[year, rel[1]] = [rel[0], rel_pos[league]]

dict_10_pts = {} #Teams within 10 points of the drop
for a, b in dict_rel_pts.keys() :
    eg = df.loc[(df['Year'] == a) & (df['League'] == b) & (df['Pts'] <= dict_rel_pts[a, b][0] + 10)].index[0]
    rel_10 = df.ix[eg, ['Pts', 'Pos']]
    dict_10_pts[a, b] = [rel_10[0], rel_10[1]]

def lister(dic, league) : #Creating lists to be zipped for plotting for each league
    results = list()
    for a, b in dic.keys() :
        if b == league :
            results.append(([a, b], dic[a, b]))
    return results

eng_zip = zip(lister(dict_rel_pts, 'England'), lister(dict_10_pts, 'England'))
fra_zip = zip(lister(dict_rel_pts, 'France'), lister(dict_10_pts, 'France'))
ita_zip = zip(lister(dict_rel_pts, 'Italy'), lister(dict_10_pts, 'Italy'))
ger_zip = zip(lister(dict_rel_pts, 'Germany'), lister(dict_10_pts, 'Germany'))
spa_zip = zip(lister(dict_rel_pts, 'Spain'), lister(dict_10_pts, 'Spain'))

def plotter_rel(zipped, league, offset) :
    for a, b in zipped :
        plt.plot([a[0][0] + offset, b[0][0] + offset], [a[1][1], b[1][1]], ls = '-', marker = '_', label = league, color = colors[league])

colors = {'England': '#be2a2a', 'France': '#052690', 'Italy': '#408f4e', 'Germany': '#000000', 'Spain': '#f6c644'}

plt.figure()
plotter_rel(eng_zip, 'England', -0.3)
plotter_rel(fra_zip, 'France', -0.15)
plotter_rel(ita_zip, 'Italy', 0)
plotter_rel(ger_zip, 'Germany', 0.15)
plotter_rel(spa_zip, 'Spain', 0.3)
plt.ylim(20, 1)
plt.yticks(np.arange(1, 21))
plt.xlim(df['Year'].min() - 1, df['Year'].max() + 1)
plt.xlabel('Year')
plt.ylabel('League position')
plt.title('Teams within 10 points of the drop (by league position)')
plt.legend(mode = 'expand', ncol = 5)
plt.show()

#PER GAME GOALS
df = df[df['Year'] != 2018]

for league in leagues :
    games = df[(df['Year'] == 2017) & (df['League'] == league)]['GP'].iloc[0]
    df.loc[df['League'] == league, 'GD / G'] = df['GD'] / games
    df.loc[df['League'] == league, 'GF / G'] = df['GF'] / games
    df.loc[df['League'] == league, 'GA / G'] = df['GA'] / games
    df.loc[df['League'] == league, 'Pts / G'] = df['Pts'] / games

def plot_goals(league, x, y, scale, alpha, color, ax) :
    df[df['League'] == league].plot(kind = 'scatter', x = x, y = y, s = (1 / df[df['League'] == league]['Pos']) * scale, alpha = alpha, color = color, label = league, ax = ax)

fig, axes = plt.subplots(nrows = 3, ncols = 4, figsize = (10, 8))
#GD
ax1 = plt.subplot2grid((3, 4), (0, 0), colspan = 4, rowspan = 2)
ax1.set_title('GOAL DIFFERENTIAL')
plot_goals('England', 'GD', 'Pts', 200, 0.35, '#be2a2a', ax1)
plot_goals('France', 'GD', 'Pts', 200, 0.35, '#052690', ax1)
plot_goals('Germany', 'GD', 'Pts', 200, 0.35, '#000000', ax1)
plot_goals('Spain', 'GD', 'Pts', 200, 0.35, '#f6c644', ax1)
plot_goals('Italy', 'GD', 'Pts', 200, 0.35, '#408f4e', ax1)
ax1.set_ylabel('Points')
ax1.set_xlabel('Goal differential')
ax1.legend(loc = 'upper left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
#GA
ax2 = plt.subplot2grid((3, 4), (2, 0), colspan = 2)
ax2.set_title('CONCEDED')
plot_goals('England', 'GA', 'Pts', 100, 0.2, '#be2a2a', ax2)
plot_goals('France', 'GA', 'Pts', 100, 0.2, '#052690', ax2)
plot_goals('Germany', 'GA', 'Pts', 100, 0.2, '#000000', ax2)
plot_goals('Spain', 'GA', 'Pts', 100, 0.2, '#f6c644', ax2)
plot_goals('Italy', 'GA', 'Pts', 100, 0.2, '#408f4e', ax2)
ax2.set_ylabel('Points')
ax2.set_xlabel('Goals against')
ax2.legend_.remove()
ax2.invert_xaxis()
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
#GF
ax3 = plt.subplot2grid((3, 4), (2, 2), colspan = 2)
ax3.set_title('SCORED')
plot_goals('England', 'GF', 'Pts', 100, 0.2, '#be2a2a', ax3)
plot_goals('France', 'GF', 'Pts', 100, 0.2, '#052690', ax3)
plot_goals('Germany', 'GF', 'Pts', 100, 0.2, '#000000', ax3)
plot_goals('Spain', 'GF', 'Pts', 100, 0.2, '#f6c644', ax3)
plot_goals('Italy', 'GF', 'Pts', 100, 0.2, '#408f4e', ax3)
ax3.set_ylabel('Points')
ax3.set_xlabel('Goals for')
ax3.legend_.remove()
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
plt.tight_layout()
plt.show()

#GOALS
fig, axes = plt.subplots(nrows = 3, ncols = 4, figsize = (10, 8))
#GD
ax1 = plt.subplot2grid((3, 4), (0, 0), colspan = 4, rowspan = 2)
ax1.set_title('GOAL DIFFERENTIAL PER GAME')
plot_goals('England', 'GD / G', 'Pts / G', 200, 0.35, '#be2a2a', ax1)
plot_goals('France', 'GD / G', 'Pts / G', 200, 0.35, '#052690', ax1)
plot_goals('Germany', 'GD / G', 'Pts / G', 200, 0.35, '#000000', ax1)
plot_goals('Spain', 'GD / G', 'Pts / G', 200, 0.35, '#f6c644', ax1)
plot_goals('Italy', 'GD / G', 'Pts / G', 200, 0.35, '#408f4e', ax1)
ax1.set_ylabel('Points per game')
ax1.set_xlabel('Goal differential per game')
ax1.legend(loc = 'upper left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
#GA
ax2 = plt.subplot2grid((3, 4), (2, 0), colspan = 2)
ax2.set_title('CONCEDED PER GAME')
plot_goals('England', 'GA / G', 'Pts / G', 100, 0.2, '#be2a2a', ax2)
plot_goals('France', 'GA / G', 'Pts / G', 100, 0.2, '#052690', ax2)
plot_goals('Germany', 'GA / G', 'Pts / G', 100, 0.2, '#000000', ax2)
plot_goals('Spain', 'GA / G', 'Pts / G', 100, 0.2, '#f6c644', ax2)
plot_goals('Italy', 'GA / G', 'Pts / G', 100, 0.2, '#408f4e', ax2)
ax2.set_ylabel('Points per game')
ax2.set_xlabel('Goals against per game')
ax2.legend_.remove()
ax2.invert_xaxis()
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
#GF
ax3 = plt.subplot2grid((3, 4), (2, 2), colspan = 2)
ax3.set_title('SCORED PER GAME')
plot_goals('England', 'GF / G', 'Pts / G', 100, 0.2, '#be2a2a', ax3)
plot_goals('France', 'GF / G', 'Pts / G', 100, 0.2, '#052690', ax3)
plot_goals('Germany', 'GF / G', 'Pts / G', 100, 0.2, '#000000', ax3)
plot_goals('Spain', 'GF / G', 'Pts / G', 100, 0.2, '#f6c644', ax3)
plot_goals('Italy', 'GF / G', 'Pts / G', 100, 0.2, '#408f4e', ax3)
ax3.set_ylabel('Points per game')
ax3.set_xlabel('Goals scored per game')
ax3.legend_.remove()
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
plt.tight_layout()
plt.show()
