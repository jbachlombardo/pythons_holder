import pandas as pd
import numpy as np
import json
from glob import glob
import pprint
pd.set_option('display.max_columns', 50)

with open('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/ad_cat_dict.json', 'r') as inf :
    ad_cat_dict = json.load(inf)
with open('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/aud_cat_dict.json', 'r') as inf :
    aud_cat_dict = json.load(inf)
with open('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/aud_type_dict.json', 'r') as inf :
    aud_type_dict = json.load(inf)
with open('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/aud_size_dict.json', 'r') as inf :
    aud_size_dict = json.load(inf)
with open('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/iampal_dict.json', 'r') as inf :
    iampal_dict = json.load(inf)

fnames = glob('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD-*.csv')

months = []

def make_month(x) :
    """Return month formatted as eg '1. January' """
    try : return str(x.month) + '.' + ' ' + x.strftime('%B')
    except : return np.nan

for f in fnames :
    df = pd.read_csv(f)
    df['Day'] = pd.to_datetime(df['Day'], errors = 'coerce')
    month = df['Day'].apply(lambda x: make_month(x))
    df['Month'] = month.iloc[-1]
    months.append(df)

data = pd.concat(months, ignore_index = True)
data = data.drop(labels = ['Reporting starts', 'Reporting ends', 'Starts', 'Ends', 'Result Type'], axis = 1)

keep_campaigns_mask = (data['Campaign name'] == 'Women athletes') | (data['Campaign name'] == 'Tal Rumeidah') | (data['Campaign name'] == 'Paramedics') | (data['Campaign name'] == 'Jerusalem') | (data['Campaign name'] == 'Nakbeh') | (data['Campaign name'] == 'Bedouins') | (data['Campaign name'] == 'Jerusalem/Gaza') | (data['Campaign name'] == 'Free Ahed Tamimi') | (data['Campaign name'] == 'I Am Palestinian post engagement')

data = data.loc[keep_campaigns_mask]

data['Audience type'] = data['Ad set name'].map(aud_type_dict)
data['Audience category'] = data['Ad set name'].map(aud_cat_dict)
data['Audience size'] = data['Ad set name'].map(aud_size_dict)
data['Ad category'] = data['Ad name'].map(ad_cat_dict)

data.loc[(data['Campaign name'] == 'I Am Palestinian post engagement') & (data['Ad name'] != 'All'), 'Campaign name'] = data.loc[(data['Campaign name'] == 'I Am Palestinian post engagement') & (data['Ad name'] != 'All')]['Ad name'].map(iampal_dict)

length = data.groupby(['Campaign name', 'Ad set name', 'Ad name'])['Day'].nunique().reset_index().rename(columns = {'Day': 'Length'})

data = data.merge(length)

data['Length_max'] = data.groupby(['Campaign name'])['Length'].transform(max)

daily = data.loc[np.isnat(data['Day']) == False]
totals = data.loc[np.isnat(data['Day'])]

def wavg(x, df = totals, w = 'Amount spent') :
    """Weighted average function to handle exception raised when 'Amount spent' equals 0"""
    try : return np.average(x, weights = df.loc[x.index, w])
    except : return np.nan

grouper = ['Campaign ID', 'Campaign name', 'Ad set ID', 'Ad set name', 'Ad ID', 'Ad name']

agg_dict = {
    'Impressions': 'sum',
    'Frequency': lambda x: wavg(x),
    'Results': 'sum',
    'Cost per result': lambda x: wavg(x),
    'Amount spent': 'sum',
    'Result rate': lambda x: wavg(x),
    'Relevance score': lambda x: wavg(x),
    'Positive feedback': lambda x: x.unique()[0],
    'Negative feedback': lambda x: x.unique()[0],
    'Page likes': 'sum',
    'Post comments': 'sum',
    'Post shares': 'sum',
    'Cost per post share': lambda x: wavg(x),
    'Cost per post comment': lambda x: wavg(x),
    'Cost per Page like': lambda x: wavg(x),
    'New messaging conversations': 'sum',
    'Video watches at 25%': 'sum',
    'Video watches at 50%': 'sum',
    'Video watches at 75%': 'sum',
    'Video watches at 95%': 'sum',
    'Video watches at 100%': 'sum',
    '3-second video views': 'sum',
    'Video percentage watched': lambda x: wavg(x),
    'Video average watch time': lambda x: wavg(x),
    'Link clicks': 'sum',
    'Button clicks': 'sum',
    'Month': lambda x: x.unique()[0],
    'Length': lambda x: wavg(x),
    'Length_max': lambda x: wavg(x),
    'Audience type': lambda x: x.unique()[0],
    'Audience category': lambda x: x.unique()[0],
    'Audience size': 'mean',
    'Ad category': lambda x: x.unique()[0]
}

totals_ads = totals.loc[(totals['Ad name'] != 'All') & (totals['Ad set name'] != 'All')].groupby(['Campaign ID', 'Campaign name', 'Ad set ID', 'Ad set name', 'Ad ID', 'Ad name']).agg(agg_dict).reset_index()
totals_ad_sets = totals.loc[(totals['Ad name'] == 'All') & (totals['Ad set name'] != 'All')].groupby(['Campaign ID', 'Campaign name', 'Ad set ID', 'Ad set name']).agg(agg_dict).reset_index()
totals_campaigns = totals.loc[(totals['Ad name'] == 'All') & (totals['Ad set name'] == 'All')].groupby(['Campaign ID', 'Campaign name']).agg(agg_dict).reset_index()
totals_merged_ad_sets = totals_ad_sets.copy()
totals_merged_ad_sets['Ad set name'] = totals_merged_ad_sets['Ad set name'].str.upper()
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'PRO-PALESTINE ORGS – BID CAP') | (totals_merged_ad_sets['Ad set name'] == 'PRO-PALESTINE ORGS – ARAB') | (totals_merged_ad_sets['Ad set name'] == 'PRO-PALESTINE ORGS (ALL)') | (totals_merged_ad_sets['Ad set name'] == 'PRO-PAL ORGS (ALL)'), 'Ad set name'] = 'PRO-PALESTINE ORGS'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'FR / BRU / GEN') | (totals_merged_ad_sets['Ad set name'] == 'FRENCH (FR / BE / GE)'), 'Ad set name'] = 'FR / BE / CH'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'PIPD ENGAGEMENT (LOOKALIKE US)') | (totals_merged_ad_sets['Ad set name'] == 'PIPD ENGAGEMENT LOOKALIKE') | (totals_merged_ad_sets['Ad set name'] == 'PIPD LOOKALIKE – BID CAP') | (totals_merged_ad_sets['Ad set name'] == 'PIPD LOOKALIKE (7%)_PHOTO'), 'Ad set name'] = 'PIPD LOOKALIKE'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'INCARCERATION / SOCIAL JUSTICE') | (totals_merged_ad_sets['Ad set name'] == 'SOCIAL JUSTICE / HUMAN RIGHTS'), 'Ad set name'] = 'SOCIAL JUSTICE'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'SOCIAL JUSTICE (LOOKALIKE)') | (totals_merged_ad_sets['Ad set name'] == 'SOCIAL JUSTICE (INDIGENOUS RIGHTS) - LOOKALIKE'), 'Ad set name'] = 'SOCIAL JUSTICE LOOKALIKE'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'PIPD ENGAGEMENT_PHOTO'), 'Ad set name'] = 'PIPD ENGAGEMENT'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'FRANCE') | (totals_merged_ad_sets['Ad set name'] == 'FRANCE - CHRISTIANS') | (totals_merged_ad_sets['Ad set name'] == 'FRANCE (SPORTS)'), 'Ad set name'] = 'FRANCE (GENERAL)'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'SPAIN') | (totals_merged_ad_sets['Ad set name'] == 'SPAIN - CHRISTIANS') | (totals_merged_ad_sets['Ad set name'] == 'SPAIN (SPORTS)'), 'Ad set name'] = 'SPAIN (GENERAL)'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'UK') | (totals_merged_ad_sets['Ad set name'] == 'UK - CHRISTIANS') | (totals_merged_ad_sets['Ad set name'] == 'UK (SPORTS)'), 'Ad set name'] = 'UK (GENERAL)'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'GERMANY') | (totals_merged_ad_sets['Ad set name'] == 'GERMANY - CHRISTIANS') | (totals_merged_ad_sets['Ad set name'] == 'GERMANY (SPORTS)'), 'Ad set name'] = 'GERMANY (GENERAL)'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'TOP DISTRICTS LOOKALIKE – BID CAP'), 'Ad set name'] = 'TOP DISTRICTS LOOKALIKE'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'NY / DC (LIB)') | (totals_merged_ad_sets['Ad set name'] == 'NY / DC (MOD)') | (totals_merged_ad_sets['Ad set name'] == 'NY / DC (CON)') | (totals_merged_ad_sets['Ad set name'] == 'WOMEN / LIBERAL') | (totals_merged_ad_sets['Ad set name'] == 'ENV / AGRI - LIBERAL') | (totals_merged_ad_sets['Ad set name'] == 'CHRISTIAN AID ORGS (US)') | (totals_merged_ad_sets['Ad set name'] == 'TOP 15 DISTRICTS-CHRISTIAN') | (totals_merged_ad_sets['Ad set name'] == 'CHRISTIANS-OLD (US)') | (totals_merged_ad_sets['Ad set name'] == 'SPORTS (GENERAL -- US)') | (totals_merged_ad_sets['Ad set name'] == 'CHRISTIANS-YOUNG (US)') | (totals_merged_ad_sets['Ad set name'] == 'SPORTS (BASKETBALL)') | (totals_merged_ad_sets['Ad set name'] == 'WOMEN / GIRLS SPORTS (US)'), 'Ad set name'] = 'US (GENERAL)'
totals_merged_ad_sets.loc[(totals_merged_ad_sets['Ad set name'] == 'IL-1') | (totals_merged_ad_sets['Ad set name'] == 'IL-4') | (totals_merged_ad_sets['Ad set name'] == 'IL-7') | (totals_merged_ad_sets['Ad set name'] == 'MA-2') | (totals_merged_ad_sets['Ad set name'] == 'ME-1') | (totals_merged_ad_sets['Ad set name'] == 'MN-5') | (totals_merged_ad_sets['Ad set name'] == 'IN-7') | (totals_merged_ad_sets['Ad set name'] == 'MN-4') | (totals_merged_ad_sets['Ad set name'] == 'NJ') | (totals_merged_ad_sets['Ad set name'] == 'NY-9') | (totals_merged_ad_sets['Ad set name'] == 'NC-4') | (totals_merged_ad_sets['Ad set name'] == 'OH-9') | (totals_merged_ad_sets['Ad set name'] == 'TX-30') | (totals_merged_ad_sets['Ad set name'] == 'OR-4') | (totals_merged_ad_sets['Ad set name'] == 'OR-3') | (totals_merged_ad_sets['Ad set name'] == 'VA-8') | (totals_merged_ad_sets['Ad set name'] == 'VT') | (totals_merged_ad_sets['Ad set name'] == 'DC') | (totals_merged_ad_sets['Ad set name'] == 'WI-4') | (totals_merged_ad_sets['Ad set name'] == 'WA-7') | (totals_merged_ad_sets['Ad set name'] == 'WI-2') | (totals_merged_ad_sets['Ad set name'] == 'CT') | (totals_merged_ad_sets['Ad set name'] == 'DE') | (totals_merged_ad_sets['Ad set name'] == 'GA-4') | (totals_merged_ad_sets['Ad set name'] == 'CA-2') | (totals_merged_ad_sets['Ad set name'] == 'CA-24') | (totals_merged_ad_sets['Ad set name'] == 'CA-47') | (totals_merged_ad_sets['Ad set name'] == 'CA-37') | (totals_merged_ad_sets['Ad set name'] == 'CA-17') | (totals_merged_ad_sets['Ad set name'] == 'CA-18') | (totals_merged_ad_sets['Ad set name'] == 'CA-16') | (totals_merged_ad_sets['Ad set name'] == 'CA-14') | (totals_merged_ad_sets['Ad set name'] == 'CA-13') | (totals_merged_ad_sets['Ad set name'] == 'AZ-3') | (totals_merged_ad_sets['Ad set name'] == 'ARAB COUNTIES') | (totals_merged_ad_sets['Ad set name'] == 'US 18-45'), 'Ad set name'] = 'US (GEOGRAPHY)'

def wavg2(x, df = totals_merged_ad_sets, w = 'Amount spent') :
    """Weighted average function to handle exception raised when 'Amount spent' equals 0"""
    try : return np.average(x, weights = df.loc[x.index, w])
    except : return np.nan

agg_dict = {
    'Impressions': 'sum',
    'Frequency': lambda x: wavg2(x),
    'Results': 'sum',
    'Cost per result': lambda x: wavg2(x),
    'Amount spent': 'sum',
    'Result rate': lambda x: wavg2(x),
    'Relevance score': lambda x: wavg2(x),
    'Positive feedback': lambda x: x.unique()[0],
    'Negative feedback': lambda x: x.unique()[0],
    'Page likes': 'sum',
    'Post comments': 'sum',
    'Post shares': 'sum',
    'Cost per post share': lambda x: wavg2(x),
    'Cost per post comment': lambda x: wavg2(x),
    'Cost per Page like': lambda x: wavg2(x),
    'New messaging conversations': 'sum',
    'Video watches at 25%': 'sum',
    'Video watches at 50%': 'sum',
    'Video watches at 75%': 'sum',
    'Video watches at 95%': 'sum',
    'Video watches at 100%': 'sum',
    '3-second video views': 'sum',
    'Video percentage watched': lambda x: wavg2(x),
    'Video average watch time': lambda x: wavg2(x),
    'Link clicks': 'sum',
    'Button clicks': 'sum',
    'Month': lambda x: x.unique()[0],
    'Length': lambda x: wavg2(x),
    'Length_max': lambda x: wavg2(x),
    'Audience type': lambda x: x.unique()[0],
    'Audience category': lambda x: x.unique()[0],
    'Audience size': 'mean',
    'Ad category': lambda x: x.unique()[0]
}

totals_merged_ad_sets = totals_merged_ad_sets.groupby(['Ad set name']).agg(agg_dict).reset_index()

def get_dummies(df, grouper) :
    grouper = grouper
    df = pd.get_dummies(df.set_index(grouper))
    return df.reset_index()

daily_dummies = get_dummies(daily, grouper = ['Campaign ID', 'Campaign name', 'Ad set ID', 'Ad set name', 'Ad ID', 'Ad name'])
totals_ads_dummies = get_dummies(totals_ads, grouper = ['Campaign ID', 'Campaign name', 'Ad set ID', 'Ad set name', 'Ad ID', 'Ad name'])
totals_ad_sets_dummies = get_dummies(totals_ad_sets, grouper = ['Campaign ID', 'Campaign name', 'Ad set ID', 'Ad set name'])
totals_campaigns_dummies = get_dummies(totals_campaigns, grouper = ['Campaign ID', 'Campaign name'])
totals_merged_ad_sets_dummies = get_dummies(totals_merged_ad_sets, grouper = ['Ad set name'])

# daily.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Daily ad data_1June18.csv')
# totals_ads.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Total ad data_1June18.csv')
# totals_ad_sets.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Total ad set data_1June18.csv')
# totals_campaigns.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Total campaign data_1June18.csv')
# totals_merged_ad_sets.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Total merged ad sets data_1June18.csv')
#
# daily_dummies.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Daily ad data_1June18_dummies.csv')
# totals_ads_dummies.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Total ad data_1June18_dummies.csv')
# totals_ad_sets_dummies.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Total ad set data_1June18_dummies.csv')
# totals_campaigns_dummies.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Total campaign data_1June18_dummies.csv')
# totals_merged_ad_sets_dummies.to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Lifetime monthly data/PIPD_Total merged ad sets data_1June18_dummies.csv')


print ('Done')
