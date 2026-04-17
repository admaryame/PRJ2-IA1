import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

from user import input_features


URL_TRAIN = 'http://127.0.0.1:5000/train'
URL_PREDICT = 'http://127.0.0.1:5000/predict'
URL_MODELS = 'http://127.0.0.1:5000/models'


def main():
    st.set_page_config(page_title='Qualite de l air', layout='wide')

    st.sidebar.title('Projet 2 - Classification')
    menu = st.sidebar.selectbox(
        'Navigation',
        ['Accueil', 'Apprentissage et comparaison', 'Prediction']
    )


    if menu == 'Accueil':
        st.title('Etude comparative de classification et prediction en temps reel de la qualite de l air')

        st.write("""
        Cette application permet :
        - de charger le dataset pollution.csv
        - d entrainer plusieurs modeles de classification
        - de comparer leurs performances
        - de sauvegarder les modeles
        - de faire une prediction en temps reel
        """)

        fichier = st.file_uploader('Charger le fichier CSV (pollution.csv)', type=['csv'])

        if fichier is not None:
            data = pd.read_csv(fichier)
            st.session_state['data_pollution'] = data
            st.subheader('Apercu du dataset')
            st.dataframe(data.head(10))
            st.write(f'Nombre de lignes : {data.shape[0]}')
            st.write(f'Nombre de colonnes : {data.shape[1]}')
            st.write(data.dtypes)

        else:
            st.write("Veuillez charger le fichier pollution.csv")


    elif menu == 'Apprentissage et comparaison':
        st.title('Apprentissage et comparaison')

        models_disponibles = [
            'Dtree', 'LR', 'SVM-C', 'KNN',
            'LDA', 'NaiveBayes', 'RandomForest', 'AdaBoost'
        ]

        selected_models = st.multiselect(
            'Selection des modeles a entrainer',
            models_disponibles,
            default=models_disponibles
        )

        if st.button('Lancer apprentissage'):
            try:
                if 'data_pollution' not in st.session_state:
                    st.write('Charge d abord le fichier dans Accueil')
                else:
                    data = st.session_state['data_pollution']
                    data = data.fillna(0)
                    payload = {
                        'models': selected_models,
                        'dataset': data.to_dict(orient='records')
                    }

                    req = requests.post(URL_TRAIN, json=payload)
                    resultats = pd.DataFrame(req.json())

                    st.subheader('Tableau comparatif')
                    st.dataframe(resultats[['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score']])


                    for metric in ['Accuracy', 'Precision', 'Recall', 'F1-Score']:
                        st.subheader(f'Graphique {metric}')
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.bar(resultats['Model'], resultats[metric])
                        ax.set_xlabel('Modeles')
                        ax.set_ylabel(metric)
                        st.pyplot(fig)


                    st.subheader('Matrices de confusion')

                    for i in range(len(resultats)):
                        st.write(f"Modele : {resultats.loc[i, 'Model']}")
                        cm = resultats.loc[i, 'ConfusionMatrix']
                        cm_df = pd.DataFrame(cm)

                        fig, ax = plt.subplots(figsize=(5, 4))
                        sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues', ax=ax)
                        ax.set_xlabel('Prediction')
                        ax.set_ylabel('Reel')
                        st.pyplot(fig)

            except Exception as e:
                st.write('Erreur :')
                st.write(e)

    else : 
        st.title('Prediction en temps reel')

        try:
            req_models = requests.get(URL_MODELS)
            models_disponibles = req_models.json()
        except:
            models_disponibles = []

        if len(models_disponibles) == 0:
            st.write('Aucun modele disponible. Lance d abord l apprentissage.')
            return

        model_name = st.selectbox('Choisir un modele', models_disponibles)

        mode_saisie = st.radio('Mode de saisie', ['Saisie manuelle', 'Charger un CSV'])

        if mode_saisie == 'Saisie manuelle':
            st.sidebar.header('Entrer les valeurs des capteurs')

            analyse = input_features()
            st.write(analyse)

            if st.button('Predire'):
                payload = {
                    'model_name': model_name,
                    'features': analyse
                }

                req = requests.post(URL_PREDICT, json=payload)
                res = req.json()

                st.subheader('Resultat')
                st.write(f"Classe : {res['class']}")
                st.write(f"Qualite : {res['label']}")
                st.write(f"Probabilite : {round(res['prob'] * 100, 2)} %")

        else:
            fichier = st.file_uploader('Charger un CSV de nouvelles mesures', type=['csv'])

            if fichier is not None:
                df = pd.read_csv(fichier)
                st.dataframe(df)

                if st.button('Predire fichier'):
                    resultats = []

                    for i in range(len(df)):
                        ligne = df.iloc[i].to_dict()

                        payload = {
                            'model_name': model_name,
                            'features': ligne
                        }

                        req = requests.post(URL_PREDICT, json=payload)
                        res = req.json()

                        resultats.append({
                            'Prediction': res['label'],
                            'Probabilite': round(res['prob'] * 100, 2)
                        })

                    df_res = pd.concat([df, pd.DataFrame(resultats)], axis=1)
                    st.dataframe(df_res)


if __name__ == '__main__':
    main()