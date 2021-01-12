import json
import random
import voltage_measure

def main():
    i = 0
    result = []
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)
    while i < 100:
        i += 1
        result.append(random.uniform(data["base_voltage"] * 0.96, data["base_voltage"] * 1.01))
    return {voltage_measure.main(): result}


if __name__ == '__main__':
    print(main())