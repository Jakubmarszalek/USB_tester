import json
import math


def main(test_value=5):
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)
    if (data["base_voltage"]*data["base_voltage"])/data["resistor_value"] > data["base_power"][str(data["base_voltage"])]:
        return math.sqrt(data["base_power"][str(data["base_voltage"])]*data["resistor_value"])
    return data["base_voltage"]


if __name__ == '__main__':
    print(main())