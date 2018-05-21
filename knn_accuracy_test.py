import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from collections import defaultdict

df_demo = pd.read_csv('/Users/jbachlombardo/Documents/Tere International/Clients/Portland/Only/Network/Survey summaries/Survey data/Syria2028_demographics.csv', dtype = {'Age': str})
df_demo = df_demo.fillna('None provided')
df_demo['Age'] = df_demo['Age'].replace(['23842674135270370', '23842674044440370', '23842674044420370', '23842674044430370', '23842669330650370', '23842669319080370', '23842669330480370', '23842713579780370', '23842669330650370; 23842674135270370'], ['18-24', '25-34', '35-44', '45+', 'None provided', 'None provided', 'None provided', 'None provided', 'None provided'])
df_demo.loc[(df_demo['From country'] == 'None provided') & (df_demo['Location country'] == 'Syria'), ['From country']] = 'Syria'
df_surv_7 = pd.read_csv('/Users/jbachlombardo/Documents/Tere International/Clients/Portland/Only/Network/Survey summaries/Survey data/Syria2028_responses_survey7.csv').drop_duplicates('Name')

df_resp = df_demo.merge(df_surv_7, on = 'Name')
df_resp = df_resp[['From country', 'Survey 7 q1', 'Survey 7 q2', 'Survey 7 q3', 'Survey 7 q4']]
print (df_resp.columns)

d = defaultdict(preprocessing.LabelEncoder)
df_resp[['Survey 7 q1', 'Survey 7 q2', 'Survey 7 q3', 'Survey 7 q4']] = df_resp[['Survey 7 q1', 'Survey 7 q2', 'Survey 7 q3', 'Survey 7 q4']].apply(lambda x: d[x.name].fit_transform(x))
df_train = df_resp[df_resp['From country'] != 'None provided']
counts = df_train['From country'].value_counts()
# more_than_10 = list(counts[counts > 10].keys())
# df_train = df_train[df_train['From country'].isin(more_than_10)]
# target_labels = df_train['From country'].unique()
# values = df_train[['Survey 4 q1', 'Survey 4 q2', 'Survey 4 q3', 'Survey 4 q4']].values

X, y = df_train[['Survey 7 q1', 'Survey 7 q2', 'Survey 7 q3', 'Survey 7 q4']], df_train['From country']
X_train, X_test, y_train, y_test = train_test_split(X, y)

neighbors = np.arange(1, 16)
train_accuracy = np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

for i, k in enumerate(neighbors):
    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(X_train, y_train)
    train_accuracy[i] = knn.score(X_train, y_train)
    test_accuracy[i] = knn.score(X_test, y_test)

plt.title('k-NN: Varying Number of Neighbors')
plt.plot(neighbors, test_accuracy, label = 'Testing Accuracy')
plt.plot(neighbors, train_accuracy, label = 'Training Accuracy')
plt.legend()
plt.xlabel('Number of Neighbors')
plt.ylabel('Accuracy')
plt.show()

#For each i, do score(train) - score(test), put this in a list or dict for each k, then use that k to do analysis
