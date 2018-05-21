import pandas as pd
import numpy as np
from sklearn.metrics import log_loss
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.pipeline import Pipeline

train = pd.read_csv('/Users/jbachlombardo/Desktop/Driven Data/Blood/Train.csv', usecols = [0, 1, 2, 4, 5])

train['Donations per month'] = train['Number of Donations'] / train['Months since First Donation']

X = train[['Months since Last Donation', 'Number of Donations', 'Months since First Donation', 'Donations per month']].values
y = train['Made Donation in March 2007'].values

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = Pipeline(steps = [
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

model = model.fit(X_train, y_train)

y_pred = model.predict_proba(X_test)

logloss = log_loss(y_test, y_pred)
score = model.score(X_test, y_test)

print (logloss)
print (score)

test = pd.read_csv('/Users/jbachlombardo/Desktop/Driven Data/Blood/Test.csv')

ppl = t.iloc[:, 0]

test['Donations per month'] = test['Number of Donations'] / test['Months since First Donation']

test_preds = test[['Months since Last Donation', 'Number of Donations', 'Months since First Donation', 'Donations per month']].values

ppl_preds = model.predict_proba(test_preds)[:, 1]

submission = pd.DataFrame({'': ppl, 'Made Donation in March 2007': ppl_preds}).set_index('')

submission.to_csv('/Users/jbachlombardo/Desktop/Driven Data/Blood/DrivenData_blood.csv')

print ('Done')
