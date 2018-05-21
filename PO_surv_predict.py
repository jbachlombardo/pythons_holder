import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import neighbors, preprocessing
from sklearn.metrics import accuracy_score
from collections import defaultdict

def pred_from_cntry(df, *qs) :
    d = defaultdict(preprocessing.LabelEncoder)
    questions = list(qs)
    df[questions] = df[questions].apply(lambda x: d[x.name].fit_transform(x))
    df_train = df[df['From country'] != 'None provided']
    df_predict = df[df['From country'] == 'None provided']
    X, y = df_train[questions], df_train['From country']
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    knn = neighbors.KNeighborsClassifier(n_neighbors = 9).fit(X_train, y_train)
    score = knn.score(X_test, y_test)
    predicts = knn.predict(df_predict[questions])
    df_predict['From country'] = predicts
    new_predicts = df_predict['From country'].value_counts()
    df_resp_predicted = pd.concat([df_train, df_predict])
    df_resp_predicted[questions] = df_resp_predicted[questions].apply(lambda x: d[x.name].inverse_transform(x))
    return df_resp_predicted, new_predicts, score

def pred_loc_cntry(df, *qs) :
    d = defaultdict(preprocessing.LabelEncoder)
    questions = list(qs)
    df[questions] = df[questions].apply(lambda x: d[x.name].fit_transform(x))
    df_train = df[df['Location country'] != 'None provided']
    df_predict = df[df['Location country'] == 'None provided']
    X, y = df_train[questions], df_train['Location country']
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    knn = neighbors.KNeighborsClassifier(n_neighbors = 5).fit(X_train, y_train)
    score = knn.score(X_test, y_test)
    predicts = knn.predict(df_predict[questions])
    df_predict['Location country'] = predicts
    new_predicts = df_predict['Location country'].value_counts()
    df_resp_predicted = pd.concat([df_train, df_predict])
    df_resp_predicted[questions] = df_resp_predicted[questions].apply(lambda x: d[x.name].inverse_transform(x))
    return df_resp_predicted, new_predicts, score
