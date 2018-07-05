from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_columns', 20)

def create_full_set(fname_camp, fname_adset, fname_ad) :
    all = list()
    cols_keep = ['Campaign name', 'Ad set name', 'Ad name', 'Link clicks', 'Reporting starts', 'Amount spent (USD)', 'Post comments', 'Page likes', 'Result rate', 'Video percentage watched', 'Post shares', 'Results', 'Frequency', 'Video average watch time', 'Level', 'Impressions', 'Post engagement', 'Length', 'Positive feedback', 'Relevance score']
    for a, b, c in zip(fname_camp, fname_adset, fname_ad) :
        camp = pd.read_csv(a, parse_dates = ['Reporting starts', 'Reporting ends'])
        camp = camp[(camp['Campaign name'] == 'Ireland campaign_post engagement') | (camp['Campaign name'] == 'Ireland campaign_traffic')]
        camp['Level'] = 'Campaign'
        camp['Ad set name'] = np.nan
        camp['Ad name'] = np.nan
        camp['Positive feedback'] = np.nan
        camp['Relevance score'] = np.nan
        camp['Length'] = (camp['Reporting ends'].sub(camp['Reporting starts']) / np.timedelta64(1, 'D') + 1)
        adset = pd.read_csv(b, parse_dates = ['Reporting starts', 'Reporting ends'])
        adset = adset[(adset['Campaign name'] == 'Ireland campaign_post engagement') | (adset['Campaign name'] == 'Ireland campaign_traffic')]
        adset['Level'] = 'Ad set'
        adset['Ad name'] = np.nan
        adset['Positive feedback'] = np.nan
        adset['Relevance score'] = np.nan
        adset['Length'] = (adset['Reporting ends'].sub(adset['Reporting starts']) / np.timedelta64(1, 'D') + 1)
        ad = pd.read_csv(c, parse_dates = ['Reporting starts', 'Reporting ends'])
        ad = ad[(ad['Campaign name'] == 'Ireland campaign_post engagement') | (ad['Campaign name'] == 'Ireland campaign_traffic')]
        ad['Level'] = 'Ad'
        ad['Length'] = (ad['Reporting ends'].sub(ad['Reporting starts']) / np.timedelta64(1, 'D') + 1)
        all.extend((camp[cols_keep], adset[cols_keep], ad[cols_keep]))
    reporting = pd.concat(all, ignore_index = True)
    reporting['Cost per link click'] = reporting['Amount spent (USD)'] / reporting['Link clicks']
    reporting['Cost per post engagement'] = reporting['Amount spent (USD)'] / reporting['Post engagement']
    reporting['Cost per post comment'] = reporting['Amount spent (USD)'] / reporting['Post comments']
    reporting['Cost per post share'] = reporting['Amount spent (USD)'] / reporting['Post shares']
    reporting['Cost per result'] = reporting['Amount spent (USD)'] / reporting['Results']
    return reporting

camp_daily_fnames = sorted(glob('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Ireland/Daily/PIPD-Campaigns*.csv'))
adset_daily_fnames = sorted(glob('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Ireland/Daily/PIPD-Ad-sets*.csv'))
ad_daily_fnames = sorted(glob('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Ireland/Daily/PIPD-Ads*.csv'))
daily_reporting = create_full_set(camp_daily_fnames, adset_daily_fnames, ad_daily_fnames)

camp_cumulative_fnames = sorted(glob('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Ireland/Cumulative/PIPD-Campaigns*.csv'))
adset_cumulative_fnames = sorted(glob('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Ireland/Cumulative/PIPD-Ad-sets*.csv'))
ad_cumulative_fnames = sorted(glob('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Ad data/Ireland/Cumulative/PIPD-Ads*.csv'))
cumulative_reporting = create_full_set(camp_cumulative_fnames, adset_cumulative_fnames, ad_cumulative_fnames)
