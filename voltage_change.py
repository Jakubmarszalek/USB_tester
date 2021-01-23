import lcd_screen
import voltage_measure
import voltage_change
import resistor_change
import rules_module


import json


def check_voltage(desired_voltage, accepted_delta=0.2):
    actual_voltage = voltage_measure.main()
    actual_delta = actual_voltage - desired_voltage
    if abs(actual_delta) <= accepted_delta:
        result = True
    else:
        result = False

    return (result, actual_delta)


def up():
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)

    if data["QC"] == 3:
        if data["base_voltage"] < 11.99:
            data["base_voltage"] = round(data["base_voltage"] + 0.2, 1)
    elif data["QC"] == 2:
        if data["base_voltage"] >= 9:
            data["base_voltage"] = 12.0
        elif data["base_voltage"] >= 5:
            data["base_voltage"] = 9.0

    with open('test_data/power_supply.json', "w") as json_file:
        json.dump(data, json_file)
    lcd_screen.main("Voltage UP")


def down():
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)

    if data["QC"] == 3:
        if data["base_voltage"] > 5:
            data["base_voltage"] = round(data["base_voltage"] - 0.2, 1)
    elif data["QC"] == 2:
        if data["base_voltage"] > 9:
            data["base_voltage"] = 9.0
        elif data["base_voltage"] <= 9:
            data["base_voltage"] = 5.0

    with open('test_data/power_supply.json', "w") as json_file:
        json.dump(data, json_file)
    lcd_screen.main("Voltage DOWN")


def set_voltage(desired_voltage, accepted_delta=0.2):
    resistor_change.set_max()
    while True:
        measure = rules_module.check_voltage_corretly(desired_voltage, accepted_delta)
        if measure == "voltage_correct":
            return True
        elif measure == "up":
            voltage_change.up()
        elif measure == "down":
            voltage_change.down()


if __name__ == '__main__':
    print(up())
