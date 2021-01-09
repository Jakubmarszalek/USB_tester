import json
import math


def main(test_value=5):
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)

    current = data["base_voltage"]/data["resistor_value"]
    power = current*data["base_voltage"]
    if power > data["base_power"][str(data["base_voltage"])]:
        print("low power")
        current = math.sqrt(data["base_power"][str(data["base_voltage"])]/data["resistor_value"])
    return current


if __name__ == '__main__':
    print(main())