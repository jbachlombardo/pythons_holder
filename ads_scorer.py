import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

def min_max(df, cat) :
    df[cat] = (df[cat] - df[cat].min()) / (df[cat].max() - df[cat].min())

cats = ['Results', 'Cost per results', 'Result rate', 'Post shares', 'Cost per post share (USD)', 'Post comments', 'Cost per post comment (USD)', '3-second video views', 'Cost per 3-second video view (USD)', 'Video percentage watched']
cats_lohi = ['Cost per results', 'Cost per post share (USD)', 'Cost per post comment (USD)', 'Cost per 3-second video view (USD)']
cats_hilo = ['Results', 'Result rate', 'Post shares', 'Post comments', '3-second video views', 'Video percentage watched']

weights = {'Cost per results': 2.0, 'Cost per post share (USD)': 1.2, 'Cost per post comment (USD)': 1.1, 'Cost per 3-second video view (USD)': 0.7, 'Results': 2.0, 'Result rate': 0.7, 'Post shares': 0.8, 'Post comments': 0.7, '3-second video views': 0.3, 'Video percentage watched': 0.5}

df = pd.read_csv('filepath')
df[['Ad name', 'C2A']] = df['Ad name'].str.split('_', expand = True)
df['C2A'] = df['C2A'].fillna('None')

df[cats_hilo] = df[cats_hilo].fillna(0)

#BY AD BY AUDIENCE -- TOTALS
grouped_df_ad_aud_totals = df.copy()[['Ad set name', 'Ad name', 'C2A', 'Results', 'Cost per results', 'Result rate', 'Post shares', 'Cost per post share (USD)', 'Post comments', 'Cost per post comment (USD)', '3-second video views', 'Cost per 3-second video view (USD)', 'Video percentage watched', 'Amount spent (USD)']].groupby(['Ad set name', 'Ad name',  'C2A']).agg({'Results': np.sum, 'Cost per results': np.mean, 'Result rate': np.mean, 'Post shares': np.sum, 'Cost per post share (USD)': np.mean, 'Post comments': np.sum, 'Cost per post comment (USD)': np.mean, '3-second video views': np.sum, 'Cost per 3-second video view (USD)': np.mean, 'Video percentage watched': np.mean, 'Amount spent (USD)': np.sum})

df[cats_lohi] = 1 / df[cats_lohi]
df[cats_lohi] = df[cats_lohi].fillna(0)

#ALL AUDIENCES
df_scoring_all = df.copy()[['Ad set name', 'Ad name', 'C2A', 'Results', 'Cost per results', 'Result rate', 'Post shares', 'Cost per post share (USD)', 'Post comments', 'Cost per post comment (USD)', '3-second video views', 'Cost per 3-second video view (USD)', 'Video percentage watched']].set_index('Ad name')
for cat in cats :
    min_max(df_scoring_all, cat)
df_scoring_all['Score'] = (pd.Series(weights) * df_scoring_all[cats]).sum(axis = 1)
df_scoring_all = df_scoring_all.sort_values(by = 'Score', ascending = False)

#BY AUDIENCE
df_scoring_aud = df.copy()[['Ad set name', 'People taking action', 'Results', 'Cost per results', 'Result rate', 'Post shares', 'Cost per post share (USD)', 'Post comments', 'Cost per post comment (USD)', '3-second video views', 'Cost per 3-second video view (USD)', 'Video percentage watched']].groupby('Ad set name').agg({'Results': np.sum, 'Cost per results': np.mean, 'Result rate': np.mean, 'Post shares': np.sum, 'Cost per post share (USD)': np.mean, 'Post comments': np.sum, 'Cost per post comment (USD)': np.mean, '3-second video views': np.sum, 'Cost per 3-second video view (USD)': np.mean, 'Video percentage watched': np.mean})
for cat in cats :
    min_max(df_scoring_aud, cat)
df_scoring_aud['Score'] = (pd.Series(weights) * df_scoring_aud[cats]).sum(axis = 1)
df_scoring_aud = df_scoring_aud.sort_values(by = 'Score', ascending = False)

#BY C2A
df_scoring_c2a = df.copy()[['C2A', 'People taking action', 'Results', 'Cost per results', 'Result rate', 'Post shares', 'Cost per post share (USD)', 'Post comments', 'Cost per post comment (USD)', '3-second video views', 'Cost per 3-second video view (USD)', 'Video percentage watched']].groupby('C2A').agg({'Results': np.sum, 'Cost per results': np.mean, 'Result rate': np.mean, 'Post shares': np.sum, 'Cost per post share (USD)': np.mean, 'Post comments': np.sum, 'Cost per post comment (USD)': np.mean, '3-second video views': np.sum, 'Cost per 3-second video view (USD)': np.mean, 'Video percentage watched': np.mean})
for cat in cats :
    min_max(df_scoring_c2a, cat)
df_scoring_c2a['Score'] = (pd.Series(weights) * df_scoring_c2a[cats]).sum(axis = 1)
df_scoring_c2a = df_scoring_c2a.sort_values(by = 'Score', ascending = False)

#BY AD BY AUDIENCE
grouped_df_scoring_ad_aud = df.copy()[['Ad set name', 'Ad name', 'C2A', 'Results', 'Cost per results', 'Result rate', 'Post shares', 'Cost per post share (USD)', 'Post comments', 'Cost per post comment (USD)', '3-second video views', 'Cost per 3-second video view (USD)', 'Video percentage watched']].groupby(['Ad set name', 'Ad name',  'C2A']).agg({'Results': np.sum, 'Cost per results': np.mean, 'Result rate': np.mean, 'Post shares': np.sum, 'Cost per post share (USD)': np.mean, 'Post comments': np.sum, 'Cost per post comment (USD)': np.mean, '3-second video views': np.sum, 'Cost per 3-second video view (USD)': np.mean, 'Video percentage watched': np.mean})
df_scoring_ad_aud = pd.DataFrame()
for cat in cats :
    df_scoring_ad_aud[cat] = grouped_df_scoring_ad_aud.groupby(level = 0)[cat].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
df_scoring_ad_aud['Score'] = (pd.Series(weights) * df_scoring_ad_aud[cats]).sum(axis = 1)
df_scoring_ad_aud = df_scoring_ad_aud.sort_values('Score', ascending = False).sort_index(level = 'Ad set name', sort_remaining = False)
df_scoring_ad_aud_by_2 = df_scoring_ad_aud.sort_values('Score', ascending = False).sort_index(level = ['Ad set name', 'Ad name'], sort_remaining = False)

#CHI SCORES
df_chi = df.copy()[['Ad set name', 'Ad name', 'C2A', 'Results', 'Post shares']][df['C2A'] != 'C2A3'].fillna(0)
grouped = df_chi.groupby(['Ad set name', 'Ad name'])
pvalues = {}
for group in grouped :
    if len(group[1]) == 2 and group[1].iloc[:, 3:5].values[0, 1] != 0:
        chi2, pvalue, dof, xp = chi2_contingency(group[1].iloc[:, 3:5].values)
        pvalues[group[0]] = pvalue, chi2
df_pvalues = pd.DataFrame.from_dict(pvalues, orient = 'index').reset_index().rename(columns = {'index': 'Ad set', 0: 'p-value', 1: 'chi^2'}).set_index('Ad set').sort_values(by = 'p-value')

#WRITING TO EXCEL MULTIPLE SHEETS
writer = pd.ExcelWriter('filepath')
df_scoring_ad_aud.to_excel(writer, sheet_name = 'By ad - audience')
df_scoring_ad_aud_by_2.to_excel(writer, sheet_name = 'By ad - audience_by C2A')
grouped_df_ad_aud_totals.to_excel(writer, sheet_name = 'By ad - audience (totals)')
df_scoring_all.to_excel(writer, sheet_name = 'All ads')
df_scoring_aud.to_excel(writer, sheet_name = 'By audience')
df_scoring_c2a.to_excel(writer, sheet_name = 'By C2A')
df_pvalues.to_excel(writer, sheet_name = 'P-values')
writer.close()
print ('Done!')
