import json


def up():
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)
    if data["resistor_value"] >= 25:
        return False
    data["resistor_value"] = round(data["resistor_value"] + 0.1, 1)
    with open('test_data/power_supply.json', "w") as json_file:
        json.dump(data, json_file)
    return True


def down():
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)
    if data["resistor_value"] < 1.1:
        return False
    data["resistor_value"] = round(data["resistor_value"] - 0.1, 1)
    with open('test_data/power_supply.json', "w") as json_file:
        json.dump(data, json_file)
    return True


def set_max():
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)
    data["resistor_value"] = 25
    with open('test_data/power_supply.json', "w") as json_file:
        json.dump(data, json_file)
    return True


def set_value(value):
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)
    data["resistor_value"] = value
    with open('test_data/power_supply.json', "w") as json_file:
        json.dump(data, json_file)
    return True

if __name__ == '__main__':
    set_max()