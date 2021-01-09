import current_measure
import lcd_screen
import voltage_measure
import voltage_change
import QC_type_change
import resistor_change
import config

import time


def max_current_test(minimal_voltage=None):
    measure = []
    resistor_change.set_max()
    while voltage_measure.main() > minimal_voltage:
        max_current = current_measure.main()
        measure.append([max_current, voltage_measure.main()])
        resistor_change.down()
        print(voltage_measure.main())

    return measure

def main():
    resistor_change.set_max()
    lcd_screen.main("Waiting for", "voltage...")
    while 1:
        if voltage_measure.main() > config.start_voltage_value:
            lcd_screen.main("Detected voltage", "measure start")
            break
        time.sleep(config.start_sleep_perioud)

    measure = max_current_test(minimal_voltage=4.45)
    print(measure)
    resistor_change.set_max()
    voltage_change.up()



if __name__ == '__main__':
    main()