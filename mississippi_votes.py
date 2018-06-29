import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 10)

total = {
    'STATEWIDE': [485131, 700714, 20670, 37881, 1],
    'Clay': [5722, 4150, 17604, 31727, 2],
    'Oktibbeha': [8859, 8576, 19356, 30320, 2],
    'Lowndes': [11819, 13271, 21273, 37607, 2],
    'Sunflower': [6725, 2794, 11993, 25012, 3],
    'Marion': [3677, 7836, 11993, 25012, 3],
    'Hinds': [67594, 25275, 20676, 39215, 3],
    'Attala': [3242, 4897, 17659, 28508, 3],
    'Stone': [1573, 5306, 21691, 43728, 3],
    'Madison': [20343, 28265, 32223, 59730, 3],
    'Harrison': [21169, 40354, 23111, 44550, 3],
    'Amite': [2697, 4289, 16861, 27615, 3],
    'Smith': [1617, 5928, 18686, 37176, 3],
    'Alcorn': [2684, 11819, 17954, 32342, 3],
    'Simpson': [3874, 7393, 18397, 36739, 3],
    'Lincoln': [4458, 10550, 20620, 38405, 3],
    'Grenada': [4424, 5970, 19701, 32901, 3],
    'Chickasaw': [3649, 4127, 15985, 30092, 3],
    'Jackson': [14657, 33629, 23547, 49620, 3],
    'Newton': [2756, 6548, 16727, 36154, 3],
    'Tunica': [2667, 853, 15711, 29994, 3],
    'Tishomingo': [999, 7166, 17017, 30211, 3],
    'Neshoba': [2715, 7679, 17609, 34905, 3],
    'Itawamba': [1117, 8470, 18517, 37588, 3],
    'Carroll': [1680, 3799, 16025, 29290, 3],
    'Calhoun': [1910, 4390, 15183, 28484, 3],
    'Issaquena': [395, 298, 11810, 21360, 3],
    'Tippah': [1842, 7240, 16365, 32109, 3],
    'Tate': [3926, 7495, 18318, 41102, 3],
    'Monroe': [5524, 10167, 18884, 35685, 3],
    'Montgomery': [2115, 2818, 16584, 31488, 3],
    'Humphreys': [3071, 1151, 13282, 25131, 3],
    'Bolivar': [9046, 4590, 16051, 26005, 3],
    'Tallahatchie': [3337, 2462, 12687, 24668, 3],
    'Marshall': [8023, 6587, 16825, 34183, 3],
    'Holmes': [6689, 1309, 11585, 21375, 3],
    'Benton': [1719, 2251, 14998, 29202, 3],
    'Webster': [1019, 3976, 17888, 34107, 3],
    'Pike': [8043, 8009, 17620, 30779, 3],
    'Lafayette': [7969, 10872, 21267, 39080, 3],
    'Copiah': [6741, 6103, 17473, 36637, 3],
    'Wayne': [3524, 5990, 17099, 31081, 3],
    'Perry': [1220, 4135, 18238, 38887, 3],
    'Kemper': [2827, 1778, 12903, 25649, 3],
    'Coahoma': [6378, 2426, 15687, 24726, 3],
    'Washington': [11380, 5244, 15946, 27797, 3],
    'Pearl River': [3604, 17782, 20014, 40038, 3],
    'Jones': [7791, 20133, 18632, 36017, 3],
    'Warren': [9284, 9767, 22079, 40404, 3],
    'Panola': [7431, 7449, 15987, 34030, 3],
    'Jefferson': [3337, 490, 12534, 24304, 3],
    'Clarke': [2585, 5137, 16467, 29103, 3],
    'Walthall': [2790, 4056, 16157, 33054, 3],
    'Jefferson Davis': [3720, 2466, 15120, 25986, 3],
    'Claiborne': [3708, 540, 12571, 24150, 3],
    'Union': [2012, 9235, 17945, 35928, 3],
    'Noxubee': [4347, 1200, 12759, 22178, 3],
    'Choctaw': [1218, 2788, 16545, 30994, 3],
    'Greene': [974, 4335, 14064, 40828, 3],
    'Leflore': [7787, 3212, 12957, 22020, 3],
    'Sharkey': [1479, 692, 14322, 30129, 3],
    'Scott': [4268, 6122, 16608, 35765, 3],
    'Lee': [10029, 22220, 21831, 39049, 3],
    'George': [1027, 8696, 19452, 45492, 3],
    'Franklin': [1502, 2721, 21583, 33324, 3],
    'Leake': [3584, 4782, 14617, 31986, 3],
    'Rankin': [14110, 47178, 27183, 56159, 3],
    'Yazoo': [5369, 4598, 14339, 27356, 3],
    'Yalobusha': [2582, 3376, 16623, 29911, 3],
    'Quitman': [2312, 1001, 13080, 24169, 3],
    'Lawrence': [2195, 4091, 19142, 35593, 3],
    'Forrest': [11716, 15461, 19272, 34448, 3],
    'DeSoto': [20591, 43089, 25065, 59734, 3],
    'Lauderdale': [11269, 17741, 20116, 33926, 3],
    'Prentiss': [2067, 7648, 17068, 31262, 3],
    'Winston': [3850, 4910, 17244, 30738, 3],
    'Wilkinson': [2857, 1318, 14333, 28066, 3],
    'Pontotoc': [2386, 10336, 17820, 38420, 3],
    'Lamar': [5190, 18751, 27399, 50075, 3],
    'Covington': [3276, 5435, 17713, 32456, 3]
}

df = pd.DataFrame.from_dict(data = total, orient = 'index', columns = ['D', 'R', 'per capita', 'Household', 'Slice'])

df['% D'] = df['D'] / (df['D'] + df['R']) * 100
df['% R'] = df['R'] / (df['D'] + df['R']) * 100
df['Absolute +/- D'] = df['% D'] - df['% R']
df['Relative +/- D'] = df['% D'] - df.loc['STATEWIDE', '% D']
df['+/- per capita'] = df['per capita'] - df.loc['STATEWIDE', 'per capita']
df['+/- % per capita'] = (df['per capita'] - df.loc['STATEWIDE', 'per capita']) / df.loc['STATEWIDE', 'per capita'] * 100
df['+/- Household'] = df['Household'] - df.loc['STATEWIDE', 'Household']
df['+/- % Household'] = (df['Household'] - df.loc['STATEWIDE', 'Household']) / df.loc['STATEWIDE', 'Household'] * 100

sort = df.loc[df.index != 'STATEWIDE'].sort_index()
statewide = df.loc[df.index == 'STATEWIDE']
df = pd.concat([statewide, sort])

print (df)

fig, ax = plt.subplots()
# ax.scatter(x = df[df['Slice'] == 1]['Relative +/- D'], y = df[df['Slice'] == 1]['+/- % Household'], c = 'green', label = None)
ax.scatter(x = df[df['Slice'] == 2]['Relative +/- D'], y = df[df['Slice'] == 2]['+/- % Household'], c = 'orange', alpha = 0.5, label = 'Golden Triangle counties')
ax.scatter(x = df[df['Slice'] == 3]['Relative +/- D'], y = df[df['Slice'] == 3]['+/- % Household'], c = 'purple', alpha = 0.5, label = None)
ax.plot([0, 0], [-60, 60], c = 'k', alpha = 0.25, linewidth = 1)
ax.plot([-50, 50], [0, 0], c = 'k', alpha = 0.25, linewidth = 1)
ax.set_xlabel('+/- % D')
ax.set_ylabel('+/- % household')
ax.set_xlim([-50, 50])
ax.set_ylim([-60, 60])
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.legend()
plt.tight_layout()
plt.show()
