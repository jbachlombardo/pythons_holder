
# coding: utf-8

# In[246]:


from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import statsmodels.api as sm
import statsmodels.formula.api as smf
import seaborn as sns
from statsmodels.stats.proportion import proportion_confint, proportions_ztest, proportions_chisquare
from pandas_datareader import DataReader


# In[10]:


def dot_plot(data) :
    """Make a R-type dotplot for integer results"""
    if data.dtype != 'int' :
        raise ValueError('Data is not all integers.')
    else :
        x = np.arange(np.min(data), np.max(data) + 1)
        y = np.bincount(data)[np.min(data):]
        
        plot_x = []
        plot_y = []
        
        for a, b in zip(x, y) :
            count = b
            while b >= 1 :
                plot_x.append(a)
                plot_y.append(b)
                b -= 1
                if b == 1 :
                    plot_x.append(a)
                    plot_y.append(1)
                    break
        
        plt.figure(figsize = (12, 5))
        plt.plot(plot_x, plot_y, linestyle = 'None', marker = 'o', markerfacecolor = 'white', markeredgecolor = 'firebrick')
        plt.xticks([int(x_x) for x_x in np.arange(np.min(x), np.max(x) + 1)])
        if np.max(y) > 25 :
            plt.yticks([int(y_y) for y_y in np.arange(1, np.max(y) + 5) if y_y % 5 == 0])
        else :
            plt.yticks([int(y_y) for y_y in np.arange(1, np.max(y) + 1)])
        plt.show()


# In[11]:


def ecdf_plot(data) :
    x = np.sort(data)
    y = np.arange(1, len(x) + 1) / len(x)
    plt.figure(figsize = (8, 5))
    plt.plot(x, y)
    plt.show()


# In[12]:


def outliers_by_IQR(data) :
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    data_no_outliers = data[(data > (q1 - (1.5 * (q3-q1)))) & (data < (q3 + (1.5 * (q3-q1))))]
    print ('Lower:', q1 - (1.5 * (q3-q1)))
    print ('Upper:', q3 + (1.5 * (q3-q1)))
    return data_no_outliers


# In[13]:


df = pd.read_csv("http://www.datadescant.com/stat104/survey.csv")


# In[14]:


stats.describe(df['height'])


# In[15]:


df['height'].quantile([0, 0.25, 0.5, 0.75, 1])


# In[16]:


dot_plot(df['height'])


# In[17]:


ecdf_plot(df['height'])


# In[18]:


height_no_outliers = outliers_by_IQR(df['height'])


# In[23]:


#Discrete
print ('dbinom (density) =', stats.binom.pmf(7, 10, .5))
print ('pbinom (probability) =', stats.binom.cdf(5, 20, .1))


# In[24]:


#Continuous
print ('pnorm =', stats.norm.cdf(38000,35000,4000))
print ('qnorm =', stats.norm.ppf(0.02, 5100, 200))


# In[25]:


#Student's t test -- tsum.test
def get_conf_interval_from_sample(n, mean, sigma, alpha = 0.95) :
    """Get confidence interval from sample data with sample of n, mean, sigma, where df = n-1
    Equivalent to getting confidence interval using t.test / tsum.test in R"""
    df = n-1
    scale = sigma / np.sqrt(n)
    return stats.t.interval(alpha=alpha, df=df, loc=mean, scale=scale)

get_conf_interval_from_sample(121, 65, 22)


# In[26]:


#equivalent to binom.confint in R
print ('asymptotic / Wald CI:', proportion_confint(40, 100))
#count = # of p, nobs = # of trials
#defaults: alpha = 0.05, method = 'normal' (asymptotic / Wald)
#Agresti-Coull CI: method = 'agresti_coull'
print ('Agresti-Coull CI:', proportion_confint(40, 100, method = 'agresti_coull'))


# In[16]:


accord = pd.read_csv('http://people.fas.harvard.edu/~mparzen/stat104/accordprices.csv')


# In[17]:


results_f = smf.ols('Price ~ Odometer', data = accord).fit()


# In[18]:


results_f.summary()


# In[168]:


#b0 and b1
results_f.params


# In[167]:


#Residual standard error
np.sqrt(results_f.scale)


# In[191]:


#Standard errors for each variable
results_f.bse


# In[217]:


ci_x = tuple(results_f.conf_int().iloc[1])
tuple(round(x, 3) for x in ci_x)


# In[283]:


def ols_fit_results_onevar(data, dep, ind, params = 'key', rounded = True, print_results = True) :
    lm = smf.ols('{} ~ {}'.format(dep, ind), data = data).fit()
    if params == 'key' :
        b0 = lm.params[0]
        b1 = lm.params[1]
        rsq = lm.rsquared
        rse = np.sqrt(lm.scale)
        ci_y = tuple(lm.conf_int().iloc[0])
        ci_x = tuple(lm.conf_int().iloc[1])
        if print_results == True :
            if rounded == True :
                b0, b1, rsq, rse, ci_y, ci_x = round(b0, 3), round(b1, 3), round(rsq, 3), round(rse, 3), tuple(round(y, 3) for y in ci_y), tuple(round(x, 3) for x in ci_x)
                print ('b0: {}\nb1: {}\nRSQ: {}\nRSE: {}\nci_y: {}\nci_x: {}'.format(b0, b1, rsq, rse, ci_y, ci_x))
            else :
                print ('b0: {}\nb1: {}\nRSQ: {}\nRSE: {}\nci_y: {}\nci_x: {}'.format(b0, b1, rsq, rse, ci_y, ci_x))
        else :
            if rounded == 'Yes' :
                b0, b1, rsq, rse, ci_y, ci_x = round(b0, 3), round(b1, 3), round(rsq, 3), round(rse, 3), tuple(round(y, 3) for y in ci_y), tuple(round(x, 3) for x in ci_x)
                return b0, b1, rsq, rse, ci_y, ci_x
            else :
                return b0, b1, rsq, rse, ci_y, ci_x
    else :
        results = lm.summary()
        if print_results == True :
            print (results)
        else :
            return results


# In[282]:


# b0, b1, rse, ci_y, ci_x = ols_fit_results(accord, 'Price', 'Odometer', print_results = False)
ols_fit_results_onevar(accord, 'Price', 'Odometer')


# In[243]:


#Hypothesis test on regression (b1)
hypothesis = 'Odometer = -0.07'
results_f.t_test(hypothesis)


# In[242]:


sns.lmplot(x = 'Odometer', y = 'Price', data = accord, ci = None)


# In[261]:


#Chi-square goodness of fit
stats.chisquare([32, 28, 16, 14, 10], [20, 20, 20, 20, 20])


# In[277]:


#Chi-square test of independence (contingency table)
table = np.array([[31, 13, 16],
                 [8, 16, 7],
                 [12, 10, 17],
                 [10, 5, 7]])
x2, p, df, e_table = stats.chi2_contingency(table)
print ('chi^2: {}\np-value: {}\nddof: {}\nexpected values:\n{}'.format(x2, p, df, e_table))

