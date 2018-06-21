import pandas as pd
import numpy as np
import itertools

df = pd.read_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/IWD results/Daily data/Cumulative/PIPD_ads_cumulative_6.csv')

df = df.loc[df['Campaign name'] == 'Women athletes']

cats2 = ['Results', 'Cost per results', 'Post shares', 'Cost per post share (USD)', 'Post comments', 'Cost per post comment (USD)', 'Video percentage watched', 'Relevance score', 'Positive feedback_High']
cats_lohi2 = ['Cost per results', 'Cost per post share (USD)', 'Cost per post comment (USD)']
cats_hilo2 = ['Results', 'Post shares', 'Post comments', 'Video percentage watched', 'Relevance score', 'Positive feedback_High']

aggs2 = {'Results': np.sum, 'Cost per results': np.mean, 'Post shares': np.sum, 'Cost per post share (USD)': np.mean, 'Post comments': np.sum, 'Cost per post comment (USD)': np.mean, 'Video percentage watched': np.mean, 'Relevance score': np.mean, 'Positive feedback_High': np.sum}

df['Relevance score'] = df['Relevance score'].fillna(df['Relevance score'].mean())
df = pd.get_dummies(df.set_index(['Ad set name', 'Ad name']))
df = df[cats2].reset_index()
df = df.fillna(0)

#BY AUDIENCE & AD
df = df.groupby(['Ad set name', 'Ad name']).agg(aggs2)#[['Ad set name', 'Ad name', 'Results', 'Cost per results', 'Post shares', 'Cost per post share (USD)', 'Post comments', 'Cost per post comment (USD)', 'Video percentage watched', 'Relevance score', 'Positive feedback_High']]

df['Total results'] = df['Results']
df['Total cost per result'] = df['Cost per results']
df['Total engagements'] = df['Post comments'] + df['Post shares']

grouped = pd.DataFrame()

def min_max_na(x) :
    if x.sum() == 0 :
        return (x - x)
    elif all(x.mean() == x) :
        return (x / x)
    else :
        return (x - x.min()) / (x.max() - x.min())

for cat in cats2 :
    if cat in cats_hilo2:
        grouped[cat] = df.groupby(level = 0)[cat].apply(min_max_na)
    else :
        df[cat] = 1 / df[cat]
        df[cat] = df[cat].replace(np.inf, np.nan)
        df[cat] = df[cat].fillna(0)
        grouped[cat] = df.groupby(level = 0)[cat].apply(min_max_na)

grouped['Total results'] = df['Total results']
grouped['Total cost per result'] = df['Total cost per result']
grouped['Total engagements'] = df['Total engagements']

def projecter(df, length) :
    to_project = df['Score'].groupby(level = 'Ad set name').nlargest(2).reset_index(level = 0, drop = True)
    pro = df.loc[to_project.index, ('Total results', 'Total cost per result', 'Total engagements')]
    # pro[['Total results', 'Total engagements']] = pro[['Total results', 'Total engagements']].apply(lambda x: x * length)
    return pro

med = np.arange(0.6, 1.4, 0.1)
low = np.arange(0.3, 1.0, 0.1)

top_tots_total = pd.DataFrame()
count = 0
count2 = 0

for cps, sha, cpc, com, rel, pfh, vpw in itertools.product(med, med, med, med, med, med, low) :
    a = np.array([cps, cpc, sha, com, rel, pfh, vpw])
    conditions = (
    (cps > sha) &
    (cpc > com) &
    all(x > vpw for x in (cps, cpc, sha, com, rel, pfh)) &
    (a.sum() == 6)
    )
    count += 1
    if count % 50000 == 0 :
        print (count)
    if conditions :
        count2 += 1
        weights2 = {
            'Cost per results': 2.0,
            'Cost per post share (USD)': cps,
            'Cost per post comment (USD)': cpc,
            'Results': 2.0,
            'Post shares': sha,
            'Post comments': com,
            'Video percentage watched': vpw,
            'Relevance score': rel,
            'Positive feedback_High': pfh
        }
        grouped['Score'] = (pd.Series(weights2) * grouped[cats2]).sum(axis = 1)
        pros = projecter(grouped, 12)
        print (pros)
        tots = pros.reset_index()
        tots['Weight_cps'], tots['Weight_sha'], tots['Weight_cpc'], tots['Weight_com'], tots['Weight_rel'], tots['Weight_pfh'], tots['Weight_vpw'] = [cps, sha, cpc, com, rel, pfh, vpw]
        tots_total = tots.groupby(['Weight_cps', 'Weight_sha', 'Weight_cpc', 'Weight_com', 'Weight_rel', 'Weight_pfh', 'Weight_vpw']).agg({'Total results': 'sum', 'Total cost per result': 'mean', 'Total engagements': 'sum'})
        top_tots_total = pd.concat([top_tots_total, tots_total])

print (top_tots_total.sort_values(by = 'Total results', ascending = False))
print (count)
print (count2)

top_tots_total.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/Remodel tests/test_remodel_paramedics.csv')
