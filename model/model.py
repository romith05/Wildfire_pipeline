from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load model (or load on demand)
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    lat = data["lat"]
    lon = data["lon"]
    
    # Dummy weather data for now
    weather = [22.3, 65.0, 14.2]  # [temp, humidity, windspeed]
    
    X = np.array([[lat, lon] + weather])
    prob = model.predict_proba(X)[0][1]  # Assuming binary classification

    return jsonify({"probability": round(prob, 3)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

