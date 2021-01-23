import values_to_rules
import voltage_measure
import voltage_change
import stability_measure


def witch_qc_append(aveliable_qc=[]):
    voltage_start = voltage_measure.main()
    voltage_change.up()
    voltage_difrence = voltage_measure.main() - voltage_start
    if (voltage_difrence > values_to_rules.qc_3_change_minimal) and (voltage_difrence < values_to_rules.qc_3_change_max):
        aveliable_qc.append(3)
    elif (voltage_difrence > values_to_rules.qc_2_change_minimal) and (voltage_difrence < values_to_rules.qc_2_change_max):
        aveliable_qc.append(2)
    return aveliable_qc


def check_voltage_corretly(desired_voltage, accepted_delta=values_to_rules.voltage_correctly_delta):
    actual_voltage = voltage_measure.main()
    actual_delta = actual_voltage - desired_voltage
    if abs(actual_delta) <= accepted_delta:
        return "voltage_correct"
    else:
        if actual_delta < 0:
            result = "up"
        if actual_delta > 0:
            result = "down"

    return result


def parametre_to_energy_test(measure_v_a, what_proc_max_power=0.5):
    max_voltage = max(measure_v_a.keys())
    max_power = max([power[2] for power in measure_v_a[max_voltage]])
    test_power = what_proc_max_power * max_power
    test_resistance = (max_voltage*max_voltage/test_power)
    return test_resistance, max_voltage


def check_voltage_stability():
    fast_detect_measure = stability_measure.main()
    teoretic_voltage = list(fast_detect_measure.keys())[0]
    average_voltage = sum(fast_detect_measure[teoretic_voltage])/len(fast_detect_measure[teoretic_voltage])
    difrence_voltage = abs(teoretic_voltage - average_voltage)
    if difrence_voltage > teoretic_voltage * 0.01:
        return "False - to big difference between theoretical and practice voltage"
    sig3 = [measure for measure in fast_detect_measure[teoretic_voltage] if abs(teoretic_voltage-measure) > values_to_rules.sig3_lvl]
    if len(sig3) > values_to_rules.sig3_limit:
        return f"False - to many measure in sig3: {len(sig3)}"

    sig2 = [measure for measure in fast_detect_measure[teoretic_voltage] if abs(teoretic_voltage-measure) > values_to_rules.sig2_lvl]
    if len(sig2) > values_to_rules.sig2_limit:
        return f"False - to many measure in sig2: {len(sig2)}"

    sig1 = [measure for measure in fast_detect_measure[teoretic_voltage] if abs(teoretic_voltage-measure) > values_to_rules.sig1_lvl]
    if len(sig2) > values_to_rules.sig1_limit:
        return f"False - to many measure in sig1: {len(sig1)}"

    return "True - correct voltage stability"


if __name__ == '__main__':
    print(check_voltage_stability())