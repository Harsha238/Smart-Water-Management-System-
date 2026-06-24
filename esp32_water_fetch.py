import urequests
import time
import con

# === Tank height calibration (cm) ===
# Measure once: distance from sensor to bottom when tank is EMPTY
H_TANK = 100.0  # Example value; replace with your tank’s measured height

# === Variables for usage rate ===
prev_water_level = None
prev_time = None



def get_prediction():
    api_url = "http://10.134.158.152:8080/predict"
    

    data = {"voltage": 230.5, "current": 42.3}

    try:
        response = urequests.post(api_url, json=data)
        result = response.json()
        print("Prediction:", result['power'],result['energy'],result['bill'])
        response.close()

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
while True:
    get_prediction()
    time.sleep(1)

    
    
    