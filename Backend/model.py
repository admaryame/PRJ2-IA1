import pickle
import warnings
warnings.filterwarnings('ignore')

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.linear_model import LogisticRegression as LR
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.naive_bayes import GaussianNB as NB
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import AdaBoostClassifier as Ada

DOSSIER_MODELS = 'models'

def charger_data():
    try:
        data = pd.read_csv('pollution.csv')
        return data
    except:
        print('Erreur de Lecture')
        return None

def get_models():
    models = []
    models.append(('Dtree', DTC()))
    models.append(('LR', LR(solver='newton-cg', max_iter=1000)))
    models.append(('SVM-C', SVC(probability=True)))
    models.append(('KNN', KNN(n_neighbors=10)))
    models.append(('LDA', LDA()))
    models.append(('NaiveBayes', NB()))
    models.append(('RandomForest', RFC()))
    models.append(('AdaBoost', Ada()))
    return models

def train_selected_models(data, selected_models):
    dataML = data.values
    X = data.drop(columns=['Qualite_air']).values
    Y = data['Qualite_air'].values

    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.3, random_state=11
    )

    resultats = []
    models = get_models()

    for model_name, model in models:
        if model_name in selected_models:
            model.fit(x_train, y_train)
            y_pred = model.predict(x_test)

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average='weighted')
            rec = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            cm = confusion_matrix(y_test, y_pred).tolist()

            model_name_file = f'models/{model_name}.pkl'
            pickle.dump(model, open(model_name_file, 'wb'))

            resultats.append({
                'Model': model_name,
                'Accuracy': round(acc, 4),
                'Precision': round(prec, 4),
                'Recall': round(rec, 4),
                'F1-Score': round(f1, 4),
                'ConfusionMatrix': cm
            })

    df_resultats = pd.DataFrame(resultats)
    return df_resultats

def list_models():
    return ['Dtree', 'LR', 'SVM-C', 'KNN', 'LDA', 'NaiveBayes', 'RandomForest', 'AdaBoost']

def load_model(model_name):
    chemin = f'models/{model_name}.pkl'
    model = pickle.load(open(chemin, 'rb'))
    return model

def pred_prob(data, model_name):
    model = load_model(model_name)
    data = data.values

    pred = int(model.predict(data)[0])

    if hasattr(model, 'predict_proba'):
        prob = model.predict_proba(data)
        prob = prob[0][pred]
    else:
        prob = 0

    return pred, prob

def label_qualite(pred):
    labels = {0: 'Bonne', 1: 'Moderee', 2: 'Mauvaise', 3: 'Dangereuse'}
    return labels.get(pred, str(pred))