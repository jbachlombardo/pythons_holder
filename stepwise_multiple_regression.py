from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm

def stepwise_by_pval(data, y_col, thresh = 0.05) :
    """Function to perform stepwise regression at removing explanatory variables at p-value threshold of 0.05"""
    dropped_list = list()
    y = data[y_col]
    x_cols = list(data.columns)
    x_cols.remove(y_col)
    X = sm.add_constant(data[x_cols])
    while True :
        lm = sm.OLS(y, X).fit()
        pvals = lm.pvalues
        if pvals.max() > thresh :
            drop_name = pvals.idxmax()
            X = X.drop(drop_name, axis = 1)
            dropped_list.append((drop_name, pvals.loc[drop_name]))
            continue
        else :
            break
    return (lm, lm.params, np.sqrt(lm.scale), dropped_list)

lm_pval, params_pval, se_pval, dropped_pval = stepwise_by_pval(mydata, 'PRICE')

def stepwise_by_aic(data, y_col) :
    """Function to perform stepwise regression by minimizing AIC"""
    y = data[y_col]
    x_cols = list(data.columns)
    x_cols.remove(y_col)
    X = sm.add_constant(data[x_cols])
    lm = sm.OLS(y, X).fit()
    aic = lm.aic
    progress_aic = {}
    progress_aic[lm.aic] = x_cols
    while True :
        new_low_aic_cols = 0
        for i in range(len(x_cols)) :
            mask = np.ones(len(x_cols))
            mask[i] = False
            new_x_cols = [c for c, m in zip(x_cols, mask) if m]
            lm_new = sm.OLS(y, sm.add_constant(data[new_x_cols])).fit()
            if lm_new.aic < aic :
                lm_report = lm_new
                aic = lm_report.aic
                new_low_aic_cols = new_x_cols
        if new_low_aic_cols == 0 :
            break
        else :
            x_cols = new_low_aic_cols
            progress_aic[aic] = new_low_aic_cols
    return lm_report, lm_report.params, np.sqrt(lm_report.scale), progress_aic

lm_aic, params_aic, se_aic, progress_aic = stepwise_by_aic(mydata, 'PRICE')
