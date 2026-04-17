### Projet 2 – Classification de la qualité de l’air

# Description :

Ce projet a pour objectif de comparer plusieurs algorithmes de classification afin de prédire le niveau de qualité de l’air (Bonne, Modérée, Mauvaise, Dangereuse).

# L’application est divisée en deux parties :

1. Backend avec Flask (gestion des modèles et API)
2. Frontend avec Streamlit (interface utilisateur)

# Fonctionnement général :

- L’utilisateur charge un fichier pollution.csv
- Il choisit les modèles à entraîner
- L’application affiche les performances des modèles
- Les modèles sont sauvegardés
- L’utilisateur peut faire des prédictions en temps réel
- Modèles utilisés : Decision Tree - Logistic Regression - SVM - KNN - Naive Bayes - Random Forest - LDA - AdaBoost - Évaluation des modèles

# Les modèles sont comparés avec :

. Accuracy
. Precision
. Recall
. F1-score
. Matrice de confusion

Les résultats sont affichés sous forme de tableaux et graphiques.

# Structure du projet

Projet 2/
│
├── Backend/
│ ├── serveur.py
│ ├── model.py
│ └── models/
│
├── Frontend/
│ ├── app.py
│ └── user.py
│
└── README.md

# Lancer le projet

1. Backend
   Dans un terminal : cd Backend python serveur.py
2. Frontend
   Dans un autre terminal : cd Frontend streamlit run app.py

# Fonctionnalités principales

Accueil
Charger le fichier CSV
Visualiser les données
Apprentissage
Sélection des modèles
Comparaison des performances
Graphiques + matrices de confusion
Prédiction
Saisie manuelle
Ou chargement d’un CSV
Résultat immédiat
API Flask
/train : entraîner les modèles
/predict : faire une prédiction
/models : afficher les modèles disponibles
Remarque

Les données sont envoyées du frontend vers le backend via JSON.
Les modèles entraînés sont sauvegardés dans le dossier models.

# Conclusion :

Ce projet permet de mettre en pratique :
. les algorithmes de classification
. l’évaluation des modèles
. une architecture client-serveur
. la création d’une API

Projet réalisé dans le cadre du cours IA1
Institut Teccart
