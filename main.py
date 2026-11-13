from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__, template_folder='templates', static_folder='static')

modelPath = 'model/modelDBS-knn.pkl'

try:
    knnModel = joblib.load(modelPath)
    print("Model Knn berhasil dimuat")
except Exception as e:
    print(f"Gagal memuat model: {e}")

labelBalance = {
    'L': 'Left weight (Berat ke Kiri)',
    'R': 'Right weight (Berat ke Kanan)',
    'B': 'Balanced (Seimbang)'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        lw = float(data.get('left_weight'))
        ld = float(data.get('left_distance'))
        rw = float(data.get('right_weight'))
        rd = float(data.get('right_distance'))

        features = [[lw, ld, rw, rd]]

        prediction = knnModel.predict(features)
        hasilPrediksi = str(prediction[0])

        deskripsiHasil = labelBalance.get(hasilPrediksi, str(hasilPrediksi))

        return jsonify({
            'status': 'success',
            'prediction': deskripsiHasil
        })
    except Exception as e:
        return jsonify({f'error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)