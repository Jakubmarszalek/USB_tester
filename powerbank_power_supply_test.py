import current_measure
import lcd_screen
import voltage_measure
import voltage_change
import QC_type_change
import resistor_change
import config
import stability_measure
import time


def max_current_test(minimal_voltage=None):
    measure = []
    resistor_change.set_max()
    while voltage_measure.main() > minimal_voltage:
        max_current = current_measure.main()
        measure.append([max_current, voltage_measure.main()])
        resistor_change.down()

    return measure


def qc_detector():
    aveliable_qc = []
    resistor_change.set_max()

    voltage_start = voltage_measure.main()
    voltage_change.up()
    voltage_difrence = voltage_measure.main() - voltage_start
    if (voltage_difrence > 0.1) and (voltage_difrence < 0.3):
        aveliable_qc.append(3)
    elif (voltage_difrence > 2) and (voltage_difrence < 5):
        aveliable_qc.append(2)

    QC_type_change.main()

    voltage_start = voltage_measure.main()
    voltage_change.up()
    voltage_difrence = voltage_measure.main() - voltage_start
    if (voltage_difrence > 0.1) and (voltage_difrence < 0.3):
        aveliable_qc.append(3)
    elif (voltage_difrence > 2) and (voltage_difrence < 5):
        aveliable_qc.append(2)

    voltage_change.set_voltage(5.0)

    return aveliable_qc


def set_qc_3():
    voltage_change.set_voltage(5.0)
    resistor_change.set_max()

    voltage_change.up()

    if voltage_measure.main() > 5.5:
        QC_type_change.main()

    voltage_change.set_voltage(5.0)


def main():
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
        measure_v_a[actual_voltage] = max_current_test(actual_voltage-0.19)



    for i in measure_v_a:
        print(measure_v_a[i])
    print(aveliable_qc)



if __name__ == '__main__':
    main()