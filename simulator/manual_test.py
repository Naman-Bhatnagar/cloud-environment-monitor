
from datetime import datetime, timezone

from cooling.controller import adjust_cooling, check_temperature


def manual_test():

    print("\nMANUAL ENVIRONMENTAL TEST")
    print("------------------------------")

    try:
        temperature = float(input("Enter temperature (C): "))
        humidity = float(input("Enter humidity (%): "))
        workload = float(input("Enter server workload (%): "))

        if temperature < -50 or temperature > 100:
            print("Invalid temperature.")
            return

        if humidity < 0 or humidity > 100:
            print("Invalid humidity.")
            return

        if workload < 0 or workload > 100:
            print("Workload must be between 0 and 100.")
            return

        cooling_level = adjust_cooling(temperature, 50)
        status = check_temperature(temperature)

        reading = {
            "device_id": "server_room_001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperature": temperature,
            "humidity": humidity,
            "workload": workload,
            "cooling_level": cooling_level,
            "status": status,
            "data_source": "manual_test"
        }

        print("\nTEST RESULTS")
        print("------------------------------")
        print(f"Temperature: {reading['temperature']} °C")
        print(f"Humidity: {reading['humidity']}%")
        print(f"Workload: {reading['workload']}%")
        print(f"Cooling: {reading['cooling_level']}%")
        print(f"Status: {reading['status']}")
        print("------------------------------")

        if status == "CRITICAL":
            print("CRITICAL CONDITION DETECTED!")

        elif status == "WARNING":
            print("WARNING: Cooling adjustment required.")

        else:
            print("Environmental conditions are normal.")

    except ValueError:
        print("Invalid input. Enter numeric values.")


def run_scenarios():

    scenarios = {
        "1": ("Normal Conditions", 22, 45, 40),
        "2": ("Warning Conditions", 25, 55, 75),
        "3": ("Critical Conditions", 27, 65, 90),
        "4": ("Extreme Overheating", 35, 75, 100),
        "5": ("Recovery Conditions", 22, 45, 15)
    }

    print("\nPREDEFINED TEST SCENARIOS")
    print("------------------------------")

    for key, scenario in scenarios.items():
        print(f"{key}. {scenario[0]}")

    choice = input("\nSelect a scenario: ")

    if choice not in scenarios:
        print("Invalid selection.")
        return

    name, temperature, humidity, workload = scenarios[choice]

    cooling_level = adjust_cooling(temperature, 50)
    status = check_temperature(temperature)

    print(f"\nScenario: {name}")
    print("------------------------------")
    print(f"Temperature: {temperature} °C")
    print(f"Humidity: {humidity}%")
    print(f"Workload: {workload}%")
    print(f"Cooling: {cooling_level}%")
    print(f"Status: {status}")
    print("------------------------------")


def main():

    while True:

        print("\nSERVER ROOM TESTING PANEL")
        print("==============================")
        print("1. Enter manual readings")
        print("2. Run predefined scenario")
        print("3. Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            manual_test()

        elif choice == "2":
            run_scenarios()

        elif choice == "3":
            print("Testing panel closed.")
            break

        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
