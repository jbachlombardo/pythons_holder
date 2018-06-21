import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 10)

paramedics = pd.read_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/Remodel tests/test_remodel_paramedics.csv')
talrumeidah = pd.read_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/Remodel tests/test_remodel_talrumeidah.csv')
womenathletes = pd.read_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/Remodel tests/test_remodel_womenathletes.csv')

weight_names = paramedics.columns[:7]

paramedics_max_te = paramedics[paramedics['Total engagements'] == paramedics['Total engagements'].max()]
talrumeidah_max_te = talrumeidah[talrumeidah['Total engagements'] == talrumeidah['Total engagements'].max()]
womenathletes_max_te = womenathletes[womenathletes['Total engagements'] == womenathletes['Total engagements'].max()]

paramedics_weights_te = list()
for x in range(len(paramedics_max_te)) :
    weights = tuple(paramedics_max_te.iloc[x, :7])
    paramedics_weights_te.append(weights)

talrumeidah_weights_te = list()
for x in range(len(talrumeidah_max_te)) :
    weights = tuple(talrumeidah_max_te.iloc[x, :7])
    talrumeidah_weights_te.append(weights)

womenathletes_weights_te = list()
for x in range(len(womenathletes_max_te)) :
    weights = tuple(womenathletes_max_te.iloc[x, :7])
    womenathletes_weights_te.append(weights)

common_te = list(set(paramedics_weights_te) & set(talrumeidah_weights_te) & set(womenathletes_weights_te))

print ('Total engagements')
print ('Paramedics', len(paramedics_weights_te))
print ('Tal Rumeidah', len(talrumeidah_weights_te))
print ('Women athletes', len(womenathletes_weights_te))

paramedics_max_tr = paramedics[paramedics['Total results'] == paramedics['Total results'].max()]
talrumeidah_max_tr = talrumeidah[talrumeidah['Total results'] == talrumeidah['Total results'].max()]
womenathletes_max_tr = womenathletes[womenathletes['Total results'] == womenathletes['Total results'].max()]

paramedics_weights_tr = list()
for x in range(len(paramedics_max_tr)) :
    weights = tuple(paramedics_max_tr.iloc[x, :7])
    paramedics_weights_tr.append(weights)

talrumeidah_weights_tr = list()
for x in range(len(talrumeidah_max_tr)) :
    weights = tuple(talrumeidah_max_tr.iloc[x, :7])
    talrumeidah_weights_tr.append(weights)

womenathletes_weights_tr = list()
for x in range(len(womenathletes_max_tr)) :
    weights = tuple(womenathletes_max_tr.iloc[x, :7])
    womenathletes_weights_tr.append(weights)

common_tr = list(set(paramedics_weights_tr) & set(talrumeidah_weights_tr) & set(womenathletes_weights_tr))

print ('Total results')
print ('Paramedics', len(paramedics_weights_tr))
print ('Tal Rumeidah', len(talrumeidah_weights_tr))
print ('Women athletes', len(womenathletes_weights_tr))

paramedics_max_tpr = paramedics[paramedics['Total cost per result'] == paramedics['Total cost per result'].min()]
talrumeidah_max_tpr = talrumeidah[talrumeidah['Total cost per result'] == talrumeidah['Total cost per result'].min()]
womenathletes_max_tpr = womenathletes[womenathletes['Total cost per result'] == womenathletes['Total cost per result'].min()]

paramedics_weights_tpr = list()
for x in range(len(paramedics_max_tpr)) :
    weights = tuple(paramedics_max_tpr.iloc[x, :7])
    paramedics_weights_tpr.append(weights)

talrumeidah_weights_tpr = list()
for x in range(len(talrumeidah_max_tpr)) :
    weights = tuple(talrumeidah_max_tpr.iloc[x, :7])
    talrumeidah_weights_tpr.append(weights)

womenathletes_weights_tpr = list()
for x in range(len(womenathletes_max_tpr)) :
    weights = tuple(womenathletes_max_tpr.iloc[x, :7])
    womenathletes_weights_tpr.append(weights)

common_tpr = list(set(paramedics_weights_tpr) & set(talrumeidah_weights_tpr) & set(womenathletes_weights_tpr))

print ('Total cost per result')
print ('Paramedics', len(paramedics_weights_tpr))
print ('Tal Rumeidah', len(talrumeidah_weights_tpr))
print ('Women athletes', len(womenathletes_weights_tpr))

tpr = pd.DataFrame(columns = weight_names)
for x in range(len(common_tpr)) :
    tpr.loc[x] = list(common_tpr[x])
tpr['Measure'] = 'Total cost per result'
tpr = tpr.set_index('Measure')

te = pd.DataFrame(columns = weight_names)
for x in range(len(common_te)) :
    te.loc[x] = list(common_te[x])
te['Measure'] = 'Total engagements'
te = te.set_index('Measure')

tr = pd.DataFrame(columns = weight_names)
for x in range(len(common_tr)) :
    te.loc[x] = list(common_tr[x])
tr['Measure'] = 'Total engagements'
tr = tr.set_index('Measure')

weights_df = pd.concat([tpr, te, tr])

# weights_dict = {}

# for x in range(len(weight_names)) :
#     weights_dict[weight_names[x]] = (common_te[0][x], common_te[1][x])
    # weights_dict['Measure'] = 'Total engagements'
    # weights_dict[weight_names[x]] = (common_tr[0][x], common_tr[1][x])

# for x in range(len(weight_names)) :
#     weights_dict[weight_names[x]] = (common_tpr[0][x], common_tpr[1][x])
#     # weights_dict['Measure'] = 'Total cost per result'
#
# weights_df = pd.DataFrame.from_dict(weights_dict)#.set_index('Measure')

print (weights_df)
