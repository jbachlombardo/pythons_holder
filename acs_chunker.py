import pandas as pd
import pickle

# Dictionary of state codes for mapping, from saved pickle file
state_codes = pickle.load(open('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/state_codes.p', 'rb'))#

fnames = ['/Users/jbachlombardo/Downloads/csv_pus/ss16pusa.csv', '/Users/jbachlombardo/Downloads/csv_pus/ss16pusb.csv']

#Initialize empty holders
states = pd.Series()
totals = pd.Series()
all_entries = 0

def read_chunk(fname, states, totals, all_entries) :
    """Function to read chunks of ACS files and apply function to the chunks"""
    df = pd.read_csv(fname, chunksize = 10000)
    for chunk in df :
        st = chunk.loc[chunk['ANC1P'] == 465, 'ST'].value_counts()
        st2 = chunk.loc[chunk['ANC2P'] == 465, 'ST'].value_counts()
        states = states.add(st, fill_value = 0).add(st2, fill_value = 0)
        tot = chunk.groupby('ST')['ST'].count()
        totals = totals.add(tot, fill_value = 0)
        all_entries += int(len(chunk))
        print (all_entries)
    return states, totals, all_entries

for fname in fnames :
    states, totals, all_entries = read_chunk(fname, states = states, totals = totals, all_entries = all_entries)

#Create dataframe for calculations and presentation / saving
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
# pals.to_csv('/Users/jbachlombardo/Downloads/csv_pus/Pal pops.csv')
