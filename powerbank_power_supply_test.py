import current_measure
import lcd_screen
import voltage_measure
import voltage_change
import QC_type_change
import resistor_change
import config
import stability_measure
import rules_module

import time
import datetime
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", "-t", action="store", required=True,
                        choices=["powerbank", "power_supply"],
                        help="What kind of update should be done")
    return parser


def max_current_test(minimal_voltage=None):
    start_time = datetime.datetime.now()
    measure = []
    resistor_change.set_max()
    while voltage_measure.main() > minimal_voltage:
        actual_current = current_measure.main()
        actual_voltage = voltage_measure.main()
        actual_power = actual_voltage * actual_current
        finish_time = datetime.datetime.now()
        measure.append([actual_current, actual_voltage, actual_power, -actual_power*(start_time-finish_time).total_seconds()])
        start_time = datetime.datetime.now()
        resistor_change.down()

    return measure


def detect_max_power(measure_v_a):
    print(measure_v_a)
    power_list = [measure_v_a[measure][2] for measure in measure_v_a]
    print(power_list)


def qc_detector():
    aveliable_qc = []
    resistor_change.set_max()

    #voltage_start = voltage_measure.main()
    #voltage_change.up()
    #voltage_difrence = voltage_measure.main() - voltage_start
    aveliable_qc = rules_module.witch_qc_append( aveliable_qc)

    QC_type_change.main()

    #voltage_start = voltage_measure.main()
    #voltage_change.up()
    #voltage_difrence = voltage_measure.main() - voltage_start
    aveliable_qc = rules_module.witch_qc_append( aveliable_qc)

    voltage_change.set_voltage(5.0)

    return aveliable_qc


def set_qc_3():
    voltage_change.set_voltage(5.0)
    resistor_change.set_max()

    voltage_change.up()

    if voltage_measure.main() > 5.5:
        QC_type_change.main()

    voltage_change.set_voltage(5.0)


def measure_energy(minimal_voltage):
    measure = []
    start_time = datetime.datetime.now()
    actual_voltage = voltage_measure.main()
    while actual_voltage > minimal_voltage:
        actual_voltage = voltage_measure.main()
        actual_current = current_measure.main()
        actual_power = actual_voltage * actual_current
        finish_time = datetime.datetime.now()
        measure.append(
            [actual_current, actual_voltage, actual_power, -actual_power * (start_time - finish_time).total_seconds()])

        start_time = datetime.datetime.now()
        time.sleep(config.time_beetwen_measure)
        print(measure)
    return measure


def main(type):
    measure_stability = {}
    measure_v_a = {}
    resistor_change.set_max()
    lcd_screen.main("Waiting for", "voltage...")
    while 1:
        if voltage_measure.main() > config.start_voltage_value:
            lcd_screen.main("Detected voltage", "measure start")
            break
        time.sleep(config.start_sleep_perioud)
    voltage_change.set_voltage(5.0)
    measure_v_a[5.0] = max_current_test(minimal_voltage=4.45)
    measure_stability.update(stability_measure.main())
    aveliable_qc = qc_detector()
    if len(aveliable_qc) >= 2:
        set_qc_3()

    while True:
        resistor_change.set_max()
        old_voltage = voltage_measure.main()
        voltage_change.up()
        actual_voltage = voltage_measure.main()
        print(actual_voltage)
        voltage_diffrent = actual_voltage - old_voltage
        if voltage_diffrent < 0.1:
            break
        measure_stability.update(stability_measure.main())
        measure_v_a[actual_voltage] = max_current_test(actual_voltage-0.19)



    for i in measure_v_a:
        print(measure_v_a[i])
    print(aveliable_qc)
    print(measure_stability)
    print(type)


    if type == "powerbank":
        test_resistance, max_voltage = rules_module.parametre_to_energy_test(measure_v_a)
        voltage_change.set_voltage(max_voltage)
        resistor_change.set_value(test_resistance)

        measure_energy(4.0)
    print(detect_max_power(measure_v_a))






if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    print(args.type)
    main(args.type)