import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

state_codes = {
1: 'Alabama/AL',
2: 'Alaska/AK',
4: 'Arizona/AZ',
5: 'Arkansas/AR',
6: 'California/CA',
8: 'Colorado/CO',
9: 'Connecticut/CT',
10: 'Delaware/DE',
11: 'District Columbia/DC',
12: 'Florida/FL',
13: 'Georgia/GA',
15: 'Hawaii/HI',
16: 'Idaho/ID',
17: 'Illinois/IL',
18: 'Indiana/IN',
19: 'Iowa/IA',
20: 'Kansas/KS',
21: 'Kentucky/KY',
22: 'Louisiana/LA',
23: 'Maine/ME',
24: 'Maryland/MD',
25: 'Massachusetts/MA',
26: 'Michigan/MI',
27: 'Minnesota/MN',
28: 'Mississippi/MS',
29: 'Missouri/MO',
30: 'Montana/MT',
31: 'Nebraska/NE',
32: 'Nevada/NV',
33: 'New Hampshire/NH',
34: 'New Jersey/NJ',
35: 'New Mexico/NM',
36: 'New York/NY',
37: 'North Carolina/NC',
38: 'North Dakota/ND',
39: 'Ohio/OH',
40: 'Oklahoma/OK',
41: 'Oregon/OR',
42: 'Pennsylvania/PA',
44: 'Rhode Island/RI',
45: 'South Carolina/SC',
46: 'South Dakota/SD',
47: 'Tennessee/TN',
48: 'Texas/TX',
49: 'Utah/UT',
50: 'Vermont/VT',
51: 'Virginia/VA',
53: 'Washington/WA',
54: 'West Virginia/WV',
55: 'Wisconsin/WI',
56: 'Wyoming/WY',
72: 'Puerto Rico/PR'
}

df_a = pd.read_csv('/Users/jbachlombardo/Downloads/csv_pus/ss16pusa.csv', chunksize = 10000)
df_b = pd.read_csv('/Users/jbachlombardo/Downloads/csv_pus/ss16pusb.csv', chunksize = 10000)

states = pd.Series()
totals = pd.Series()

all_entries = 0

for chunk in df_a :
    st = chunk.loc[chunk['ANC1P'] == 465, 'ST'].value_counts()
    st2 = chunk.loc[chunk['ANC2P'] == 465, 'ST'].value_counts()
    states = states.add(st, fill_value = 0).add(st2, fill_value = 0)
    tot = chunk.groupby('ST')['ST'].count()
    totals = totals.add(tot, fill_value = 0)
    all_entries += int(len(chunk))
    print (all_entries)

for chunk in df_b :
    st = chunk.loc[chunk['ANC1P'] == 465, 'ST'].value_counts()
    st2 = chunk.loc[chunk['ANC2P'] == 465, 'ST'].value_counts()
    states = states.add(st, fill_value = 0).add(st2, fill_value = 0)
    tot = chunk.groupby('ST')['ST'].count()
    totals = totals.add(tot, fill_value = 0)
    all_entries += int(len(chunk))
    print (all_entries)

pals = pd.DataFrame({'Pals': states, 'All': totals}).reset_index()
pals['State'] = pals['index'].map(state_codes).str[-2:]
del pals['index']
pals['% Pal'] = pals['Pals'] / pals['All'] * 100
pals = pals.set_index('State')

print ('')
print ('Total records:', '{:,}'.format(all_entries))
print ("""
=====
""")
print (pals.sort_values(by = '% Pal', ascending = False))
pals.to_csv('/Users/jbachlombardo/Downloads/csv_pus/Pal pops.csv')
