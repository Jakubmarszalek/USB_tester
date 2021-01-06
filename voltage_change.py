import lcd_screen
import voltage_measure
import voltage_change


def check_voltage(desired_voltage, accepted_delta=0.2):
    actual_voltage = voltage_measure.main()
    actual_delta = actual_voltage - desired_voltage
    if abs(actual_delta) <= accepted_delta:
        result = True
    else:
        result = False

    return (result, actual_delta)


def up():
    lcd_screen(" UP")


def down():
    lcd_screen("Voltage DOWN")


def set_voltage(desired_voltage, accepted_delta=0.2):
    while True:
        measure = check_voltage(desired_voltage, accepted_delta)
        if measure[0]:
            return True
        elif measure[1] < 0:
            voltage_change.up()
        elif measure[1] > 0:
            voltage_change.down()

