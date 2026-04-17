from flask import Flask, request, jsonify
import pandas as pd

from model import train_selected_models, list_models, pred_prob, label_qualite

app = Flask(__name__)


@app.route('/train', methods=['POST'])
def train():
    data = request.get_json(force=True)
    selected_models = data['models']
    dataset = data['dataset']

    data_pollution = pd.DataFrame(dataset)
    df_resultats = train_selected_models(data_pollution, selected_models)

    return df_resultats.to_json(orient='records')


@app.route('/models', methods=['GET'])
def models():
    models_disponibles = list_models()
    return jsonify(models_disponibles)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    model_name = data['model_name']
    valeurs = data['features']

    new_data = pd.DataFrame(valeurs, index=[0])

    pred, prob = pred_prob(new_data, model_name)

    resultat = {
        'class': pred,
        'label': label_qualite(pred),
        'prob': prob
    }

    return jsonify(resultat)


if __name__ == '__main__':
    app.run(debug=True, port=5000)