import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

df = pd.read_excel('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Ahed results/Ranking of districts_totals & scored_FINAL_TOP 20.xlsx')

# ['Ad name', 'People taking action', 'Post shares', 'Post comments',
#        'Video percentage watched', '3-second video views', 'Result rate',
#        'Cost per post share (USD)', 'Cost per post comment (USD)',
#        'Cost per results', 'Score', 'Is null']

categories = list(df.columns)[1:10] #CUTTING OUT OVERALL SCORE -- TO GO ELSEWHERE
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

plt.figure(figsize = [8, 6])
ax = plt.subplot(1, 1, 1, polar = True)
ax.set_theta_offset(pi / 2)
ax.set_rlabel_position(0)
plt.xticks(angles[:-1], categories, color = '#888B8D', size = 10)
ax.spines['polar'].set_color('#888B8D')
plt.yticks(color = '#888B8D', size = 7)
plt.ylim(0, 1)
plt.title('{} (total score = {})'.format((df.iloc[1, 0]), df.iloc[1, 10]))

#iloc 1 values
values = list(df.iloc[1, 1:10])
values += values[:1]
ax.plot(angles, values, color = '#60398b', linewidth = 1, linestyle = 'solid', label = df.iloc[1, 0])
ax.fill(angles, values, color = '#60398b', alpha = 0.1)

plt.legend()

plt.show()
