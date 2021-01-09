import json
import lcd_screen


def main():
    with open('test_data/power_supply.json') as json_file:
        data = json.load(json_file)
    if data["QC"] == 2:
        data["QC"] = 3
    elif data["QC"] == 3:
        data["QC"] = 2
    with open('test_data/power_supply.json', "w") as json_file:
        json.dump(data, json_file)
    lcd_screen.main("QC change")


if __name__ == '__main__':
    print(main())