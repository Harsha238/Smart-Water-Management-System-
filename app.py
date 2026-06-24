from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import time

app = Flask(__name__)

# === Load trained AI model ===
model = joblib.load("water_tank_ai_model.pkl")

# === Store latest data ===
latest_data = {
    "distance": None,
    "water_level": None,
    "usage_rate": None,
    "fill_ratio": None,
    "predicted_time_to_empty": None,
    "timestamp": None
}

@app.route('/')
def home():
    return "💧 Smart Water Management System (AI + IoT) Running!"

@app.route('/predict', methods=['POST'])
def predict():
    global latest_data
    data = request.get_json()

    try:
        distance = float(data.get("distance", 0))
        usage_rate = float(data.get("usage_rate", 0))
        fill_ratio = float(data.get("fill_ratio", 0))
        tank_height = float(data.get("tank_height", 100))
        water_level = float(data.get("water_level", 0))
    except Exception as e:
        return jsonify({"error": f"Invalid input: {e}"}), 400

    # Prepare input for AI model
    # (Model trained on normalized data: distance, usage_rate)
    X = np.array([[distance, usage_rate]])

    pred = model.predict(X)[0]  # time to empty in seconds
    pred_minutes = pred / 60

    latest_data = {
        "distance": distance,
        "water_level": water_level,
        "usage_rate": usage_rate,
        "fill_ratio": fill_ratio,
        "predicted_time_to_empty": round(pred_minutes, 2),
        "tank_height": tank_height,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    print(f"[{latest_data['timestamp']}] Water Level: {water_level:.2f} cm | "
          f"Rate: {usage_rate:.3f} cm/s | Empty in {pred_minutes:.2f} min")

    return jsonify(latest_data)

@app.route('/dashboard')
def dashboard():
    return render_template("index.html")

@app.route('/latest_data')
def get_latest_data():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
