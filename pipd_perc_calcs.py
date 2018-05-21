import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/PIPD-Ads-27-January-201827-January-2018.csv')
df = df[(df['Ad name'] == 'UNRWA homes') | (df['Ad name'] == 'Motivation') | (df['Ad name'] == '3 women') | (df['Ad name'] == 'UNRWA schools') | (df['Ad name'] == 'Music') | (df['Ad name'] == 'Love life') | (df['Ad name'] == 'Main video - 3 generations')]
df = df[(df['Ad set name'] == 'Pro-Palestine orgs') | (df['Ad set name'] == 'Arab counties') | (df['Ad set name'] == 'NY / DC (Con)') | (df['Ad set name'] == 'NY / DC (Lib)') | (df['Ad set name'] == 'Women / Liberal') | (df['Ad set name'] == 'NY / DC (Mod)')]


# 'Palestine' 'PIPD engagement' 'Pro-Palestine orgs' 'Germany'
#  'Arab counties' 'Spain' 'Brussels / Geneva' 'NY / DC (Con)' 'UK'
#  'NY / DC (Lib)' 'Women / Liberal' 'France' 'NY / DC (Mod)'

# ['Reporting starts', 'Reporting ends', 'Ad name', 'Delivery',
#        'People taking action', 'Post reactions', 'Post comments',
#        'Post shares', 'Link clicks', 'Page likes', 'Results',
#        'Result indicator', 'Result rate', 'Frequency', 'Impressions', 'Reach',
#        'Actions', 'Relevance score', 'Positive feedback', 'Negative feedback',
#        'Amount spent (USD)', 'Cost per results', 'Post engagement',
#        'Cost per Page like (USD)', 'Cost per post comment (USD)',
#        'Cost per post engagement (USD)', 'Cost per post reaction (USD)',
#        'Cost per post share (USD)', '3-second video views',
#        '10-second video views', '30-second video views',
#        'Video average watch time', 'Video percentage watched',
#        'Video watches at 100%', 'Video watches at 95%', 'Video watches at 75%',
#        'Video watches at 50%', 'Video watches at 25%',
#        'Cost per 3-second video view (USD)',
#        'Cost per 10-second video view (USD)', 'CTR (all)', 'CPC (all) (USD)',
#        'Ad set name', 'Campaign name']

calcs = ['Result rate', 'Cost per results', 'Amount spent (USD)', 'Post engagement', '3-second video views']
print ('Results as percentage within each ad set (by ad)')
for calc in calcs :
    grouped = df.groupby(['Ad set name', 'Ad name']).agg({calc: 'sum'})
    grouped_pcts = grouped.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))
    # print (calc)
    # print (grouped_pcts)
    print ('')

print (grouped_pcts)
print (grouped)

# print ('results across ad sets so far, grouped by ad (only US ad sets)')
# print ('------')
# print ('Amount spent (USD) (total)')
# print (grouped['Amount spent (USD)'].sum())
# print ('')
# print ('Result rate (avg)')
# print (grouped['Result rate'].mean())
# print ('')
# print ('Post engagement (total)')
# print (grouped['Post engagement'].sum())
# print ('')
# print ('Cost per results (avg)')
# print (grouped['Cost per results'].mean())
# print ('')
# print ('3-second video views (total)')
# print (grouped['3-second video views'].sum())
