import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def ecdf(d) :
    x = np.sort(d)
    y = np.arange(1, len(d) + 1) / len(d)
    return x, y

def diff_of_means(data1, data2) :
    return np.mean(data1) - np.mean(data2)

def draw_bs_reps(data, fcn = np.mean, size = 1, keep_dict = False):
        bs_reps = np.empty(size)
        bs_dict = {}
        for i in range(size):
            bs_sample = np.random.choice(data, len(data))
            bs_reps[i] = fcn(bs_sample)
            if keep_dict == True :
                bs_dict[i] = bs_sample
        if keep_dict == True :
            return bs_reps, bs_dict
        else :
            return bs_reps

def draw_perm_reps(data1, data2, fcn = diff_of_means, size = 1):
    data = np.concatenate((data1, data2))
    perm_reps = np.empty(size)
    for i in range(size) :
        permuted = np.random.permutation(data)
        perm_sample_1 = permuted[:len(data1)]
        perm_sample_2 = permuted[len(data1):]
        perm_reps[i] = fcn(perm_sample_1, perm_sample_2)
    return perm_reps

income = pd.read_excel('/Users/jbachlombardo/Desktop/Hubway travel data/15zp22ma.xls', header = 3, skiprows = 2, usecols = [0, 17, 18], names = ['zipcode', 'returns', 'income'], converters = {0: lambda x: '0' + str(x), 2: lambda x: pd.to_numeric(x * 1000)})
income = income.dropna().drop_duplicates(subset = 'zipcode', keep = 'first')
income['avg_income'] = income['income'] / income['returns']

avgs = income['avg_income']

mask = (avgs < np.percentile(avgs, 41)) & (avgs > np.percentile(avgs, 30))
mask2 = (avgs < np.percentile(avgs, 40)) & (avgs > np.percentile(avgs, 29))

top_quartile = avgs[mask].values
bottom_ten = avgs[mask2].values

perm_reps = draw_perm_reps(top_quartile, bottom_ten, size = 1000)

diff = diff_of_means(top_quartile, bottom_ten)

p = np.sum(perm_reps > diff) / len(perm_reps)

print ('p:', p)

avg = income['avg_income'].mean()
size = 1000
reps, reps_dict = draw_bs_reps(income['avg_income'], size = size, keep_dict = True)

p = np.sum(reps > avg) / len(reps)

print ('p:', p)

plt.figure()
plt.xscale('log')
x, y = ecdf(avgs)
plt.plot(x, y, marker = '.', linestyle = 'none', ms = 1, c = 'green', alpha = 0.65)
plt.plot([avg, avg], [0, 1], c = 'green')
for i in range(1, 101) :
    xi, yi = ecdf(reps_dict[i])
    plt.plot(xi, yi, marker = '.', linestyle = 'none', ms = 1, c = 'purple', alpha = 0.01)
    plt.plot([reps[i], reps[i]], [0, 1], c = 'purple', alpha = 0.05)
plt.plot([reps.mean(), reps.mean()], [0, 1], c = 'purple', alpha = 0.5, linestyle = '-')
plt.show()
