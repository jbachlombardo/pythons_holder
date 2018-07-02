import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
pd.set_option('display.max_columns', 30)

def get_genre(x) :
    """A function to clean the 'genre' column, which reads in as a string of format [{dict 1}, {dict 2}, {dict 3}] and contains several genres. This selects the genre with the highest ID number."""
    try :
        y = ast.literal_eval(x)
        vals_list = list()
        for i in y :
            vals = list(i.values())
            vals_list.append(vals)
        return sorted(vals_list)[-1][1]
    except :
        return 'Error'

df = pd.read_csv('/Users/jbachlombardo/Downloads/tmdb-5000-movie-dataset/tmdb_5000_movies.csv', usecols = [1, 7, 17], converters = {1: lambda x: get_genre(x)})

to_class = df[(df['genres'] == 'Crime') | (df['genres'] == 'Comedy')]

X, X_hold, y, y_hold = train_test_split(to_class[['overview', 'title']], to_class['genres'], test_size = 50 / len(to_class), stratify = to_class['genres'])

titles_hold = X_hold['title']

print ('Training set size:', len(X))
print ('Holdout set size:', len(X_hold))

count_vectorizer = CountVectorizer(stop_words = 'english')
count_X = count_vectorizer.fit_transform(X['overview'])

alphas = np.arange(0.1, 3.1, 0.1)
def train_and_predict(alpha):
    nb_classifier = MultinomialNB(alpha = alpha)
    nb_classifier = nb_classifier.fit(count_X, y)
    scores = cross_val_score(nb_classifier, count_X, y, cv = 5)
    mean_score, plus_std, minus_std = scores.mean(), scores.mean() + scores.std(), scores.mean() - scores.std()
    return mean_score, plus_std, minus_std

mean_scores = np.empty(len(alphas))
plus_stds = np.empty(len(alphas))
minus_stds = np.empty(len(alphas))
i = 0

for alpha in alphas:
    mean_score, plus_std, minus_std = train_and_predict(alpha)
    mean_scores[i] = mean_score
    plus_stds[i] = plus_std
    minus_stds[i] = minus_std
    i += 1

max_alpha = alphas[mean_scores == mean_scores.max()].item(0)
max_score = mean_scores[mean_scores == mean_scores.max()].item(0)

print ('Max alpha:', max_alpha)
print ('Max score:', max_score)

plt.figure()
plt.plot(alphas, mean_scores, color = 'k', marker = '.', label = 'Mean score (cv = 5)')
plt.plot(alphas, plus_stds, color = 'green', alpha = 0.5, label = '+/- 1 std')
plt.plot(alphas, minus_stds, color = 'green', alpha = 0.5)
plt.xticks([x for x in np.arange(0.1, 3.2, 0.5)], rotation = 90)
plt.ylabel('Accuracy score')
plt.xlabel('Alpha')
plt.legend()
plt.tight_layout()
plt.show()

nb_classifier_hold = MultinomialNB(alpha = max_alpha)
nb_classifier_hold = nb_classifier_hold.fit(count_X, y)
count_X_hold = count_vectorizer.transform(X_hold['overview'])
pred = nb_classifier_hold.predict(count_X_hold)
pred_proba = nb_classifier_hold.predict_proba(count_X_hold)
score = metrics.accuracy_score(y_hold, pred)
cm = metrics.confusion_matrix(y_hold, pred)
df_cm = pd.DataFrame(cm, columns = list(to_class['genres'].unique()), index = list(to_class['genres'].unique()))
df_cm.loc['Totals'] = df_cm.sum()
df_cm['Totals'] = df_cm.sum(axis = 1)
list_pred_proba = list()
for a, b, c in zip(titles_hold, pred, pred_proba) :
    list_pred_proba.append((a, b, c.max()))
df_pred_proba = pd.DataFrame(list_pred_proba, columns = ['Film', 'Genre', '% Certain'])
print ('Holdout score:', score)
print (df_cm)
print (df_pred_proba)

# print (pred)
# print (pred_proba)
# for a, b in zip(pred, pred_proba[:, 0]) :
#     if b > 0.5 :
#         print (a, '{0:.2%}'.format(b))
#     else :
#         print (a, '{0:.2%}'.format(1 - b))

# TFIDF
# tfidf_vectorizer = TfidfVectorizer(stop_words = 'english', max_df = 0.7)
# tfidf_train = tfidf_vectorizer.fit_transform(X_train)
# tfidf_test = tfidf_vectorizer.transform(X_test)

# tfidf_df = pd.DataFrame(tfidf_train.A, columns = tfidf_vectorizer.get_feature_names())

# nb_classifier = MultinomialNB()
# nb_classifier = nb_classifier.fit(tfidf_train, y_train)
# pred = nb_classifier.predict(tfidf_test)
# score = metrics.accuracy_score(y_test, pred)
# cm = metrics.confusion_matrix(y_test, pred)
# print(score)
# print(cm)
#

# class_labels = nb_classifier.classes_
# feature_names = tfidf_vectorizer.get_feature_names()
# feat_with_weights = sorted(zip(nb_classifier.coef_[0], feature_names))
# print(class_labels[0], feat_with_weights[:20])
# print(class_labels[1], feat_with_weights[:20])


# #CATEGORICAL VARIABLES -- ORDINAL
# data.salary = data.salary.astype('category')
# data.salary = data.salary.cat.reorder_categories(['low', 'medium', 'high'])
# data.salary = data.salary.cat.codes
# #CATEGORICAL VARIABLES -- NOMINAL
# departments = pd.get_dummies(data.department)
# departments = departments.drop("accounting", axis=1)
# data = data.drop("department", axis=1)
# data = data.join(departments)
