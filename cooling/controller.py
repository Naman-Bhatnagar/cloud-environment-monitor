
# cooling configuration
target_temperature = 22.0

increase_threshold = 24.0
decrease_threshold = 22.0
critical_threshold = 27.0

cooling_step = 10


def adjust_cooling(temperature, cooling_level):

    if temperature >= critical_threshold:
        cooling_level = 100

    elif temperature > increase_threshold:
        cooling_level += cooling_step

    elif temperature < decrease_threshold:
        cooling_level -= cooling_step

    # keep cooling between 0% and 100%
    cooling_level = max(0, min(100, cooling_level))

    return cooling_level


def check_temperature(temperature):

    if temperature >= critical_threshold:
        return "CRITICAL"

    elif temperature > increase_threshold:
        return "WARNING"

    else:
        return "NORMAL"
