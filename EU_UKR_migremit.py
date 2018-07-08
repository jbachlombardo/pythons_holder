from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_columns', 20)

migs_all = pd.read_excel('/Users/jbachlombardo/Downloads/bilateralmigrationmatrix20170_Apr2018.xlsx', skiprows = 1, index_col = 0)
rems_all = pd.read_excel('/Users/jbachlombardo/Downloads/bilateralremittancematrix2017_Apr2018.xlsx', skiprows = 1, index_col = 0)

#Destination (across), Source (down)

eu_countries = ['Austria',
'Belgium',
'Bulgaria',
'Croatia',
'Cyprus',
'Czech Republic',
'Denmark',
'Estonia',
'Finland',
'France',
'Germany',
'Greece',
'Hungary',
'Ireland',
'Italy',
'Latvia',
'Lithuania',
'Luxembourg',
'Malta',
'Netherlands',
'Poland',
'Portugal',
'Romania',
'Slovak Republic',
'Slovenia',
'Spain',
'Sweden',
'United Kingdom']

def get_to_from(df1, df2, country_list, target_country) :
    data = dict()
    for i in country_list :
        data[i] = [df1.loc[i, target_country], df1.loc[target_country, i], df2.loc[i, target_country], df2.loc[target_country, i]]
    df_total = pd.DataFrame.from_dict(data, orient = 'index', columns = ['# migrants from EU in ' + str(target_country), '# migrants from ' + str(target_country) + ' in EU', 'Remittances from EU to ' + str(target_country), 'Remittances from ' + str(target_country) + ' to EU'])
    df_total.iloc[:, 2:] = df_total.iloc[:, 2:] * 10 ** 6
    df_total.loc['EU TOTALS'] = df_total.sum()
    df_total['Value remittance per person from EU to ' + str(target_country)] = df_total.iloc[:, 2] / df_total.iloc[:, 1]
    df_total['Value remittance per person from ' + str(target_country) + ' to EU'] = df_total.iloc[:, 3] / df_total.iloc[:, 0]
    a, b, c, d, e, f = df_total.columns
    ordered_cols = [b, c, e, a, d, f]
    df_total = df_total[ordered_cols]
    df_total = df_total.fillna(0)
    return df_total

ukraine = get_to_from(migs_all, rems_all, eu_countries, 'Ukraine')
georgia = get_to_from(migs_all, rems_all, eu_countries, 'Georgia')
serbia = get_to_from(migs_all, rems_all, eu_countries, 'Serbia')
albania = get_to_from(migs_all, rems_all, eu_countries, 'Albania')
moldova = get_to_from(migs_all, rems_all, eu_countries, 'Moldova')
turkey = get_to_from(migs_all, rems_all, eu_countries, 'Turkey')

writer = pd.ExcelWriter('/Users/jbachlombardo/Documents/Tere International/Clients/Portland/Ukraine/Migration data.xlsx')
albania.to_excel(writer, sheet_name = 'Albania')
georgia.to_excel(writer, sheet_name = 'Georgia')
moldova.to_excel(writer, sheet_name = 'Moldova')
serbia.to_excel(writer, sheet_name = 'Serbia')
turkey.to_excel(writer, sheet_name = 'Turkey')
ukraine.to_excel(writer, sheet_name = 'Ukraine')
writer.close()
print ('Done!')
