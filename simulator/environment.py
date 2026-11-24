

import random
import time
import requests
from datetime import datetime, timezone

# AWS API configuration
API_URL = "https://3rqqcfw2va.execute-api.ap-southeast-2.amazonaws.com/readings"

# Server room configuration
device_id = "server_room_001"

# Initial environmental conditions
temperature = 23.0
humidity = 50.0
cooling_level = 60.0

print("Server Room Environmental Simulator Started")
print("Generating environmental readings...")
print("Press Ctrl + C to stop.\n")

try:
    while True:

        # Generate changing server workload
        workload = random.uniform(30, 95)

        # Gradually adjust humidity
        humidity += random.uniform(-0.3, 0.3)
        humidity = max(45.0, min(60.0, humidity))

        # Calculate the target temperature
        target_temperature = (
            20 + (workload * 0.09) - (cooling_level * 0.06)
        )

        # Gradually change temperature
        temperature += (
            (target_temperature - temperature) * 0.25
            + random.uniform(-0.2, 0.2)
        )

        # Automatically adjust cooling
        if temperature >= 27:
            cooling_level += 15

        elif temperature > 24:
            cooling_level += 8

        elif temperature < 22:
            cooling_level -= 5

        # Keep cooling within operating limits
        cooling_level = max(20.0, min(100.0, cooling_level))

        # Prepare environmental reading
        reading = {
            "device_id": device_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "workload": round(workload, 2),
            "cooling_level": round(cooling_level, 2),
            "data_source": "simulated"
        }

        # Send reading to AWS
        try:
            response = requests.post(
                API_URL,
                json=reading,
                timeout=10
            )

            response.raise_for_status()
            result = response.json()

            print(
                f"Temperature: {temperature:.2f} °C | "
                f"Humidity: {humidity:.2f}% | "
                f"Workload: {workload:.2f}% | "
                f"Cooling: {cooling_level:.2f}% | "
                f"Status: {result.get('status', 'Unknown')} | "
                f"Alert: {result.get('alert_sent', False)}"
            )

        except requests.exceptions.RequestException as error:
            print(f"Unable to send reading: {error}")

        # Wait five seconds before next reading
        time.sleep(5)

except KeyboardInterrupt:
    print("\nSimulator stopped.")
