#first install py prj2_analysis.py
#then run in Terminal: py prj2_analysis.py
import numpy as np
import matplotlib.pyplot as plt

# Measurement values
multimeter = np.array([
    0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4,
    2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.0
])

experiment1 = np.array([
    0, 80, 162, 244, 325, 413, 492,
    572, 655, 739, 820, 909, 990, 1024
])

experiment2 = np.array([
    0, 83, 165, 247, 327, 410, 490,
    573, 656, 737, 817, 902, 983, 1023
])

# Ideal ADC values
ideal_adc = multimeter * 1023 / 5.0

# Figure 8 - Experiment 1
plt.figure(figsize=(8, 5))
plt.plot(multimeter, ideal_adc, "k--", label="Ideal ADC")
plt.plot(multimeter, experiment1, "bo-", label="Experiment 1")
plt.xlabel("Multimeter Voltage (V)")
plt.ylabel("ADC Output")
plt.title("Experiment 1 vs Ideal ADC")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Figure8.png", dpi=300)

# Figure 9 - Experiment 2
plt.figure(figsize=(8, 5))
plt.plot(multimeter, ideal_adc, "k--", label="Ideal ADC")
plt.plot(multimeter, experiment2, "ro-", label="Experiment 2")
plt.xlabel("Multimeter Voltage (V)")
plt.ylabel("ADC Output")
plt.title("Experiment 2 vs Ideal ADC")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Figure9.png", dpi=300)



# Calculate deviations from ideal ADC
error1 = experiment1 - ideal_adc
error2 = experiment2 - ideal_adc

# Figure 10 - Experiment 1 Linearity Error
plt.figure(figsize=(8, 5))
plt.plot(multimeter, error1, "bo-", label="Experiment 1")
plt.axhline(0, color="black", linestyle="--", label="Ideal")
plt.xlabel("Multimeter Voltage (V)")
plt.ylabel("Deviation (LSB)")
plt.title("Experiment 1 - Linearity Error")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Figure10.png", dpi=300)

# Figure 11 - Experiment 2 Linearity Error
plt.figure(figsize=(8, 5))
plt.plot(multimeter, error2, "ro-", label="Experiment 2")
plt.axhline(0, color="black", linestyle="--", label="Ideal")
plt.xlabel("Multimeter Voltage (V)")
plt.ylabel("Deviation (LSB)")
plt.title("Experiment 2 - Linearity Error")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Figure11.png", dpi=300)



# Approximate endpoint INL analysis

# Experiment 1: exclude invalid ADC value 1024
v1 = multimeter[:-1]
adc1 = experiment1[:-1]

# Endpoint reference lines
ref1 = adc1[0] + (
    (adc1[-1] - adc1[0]) /
    (v1[-1] - v1[0])
) * (v1 - v1[0])

ref2 = experiment2[0] + (
    (experiment2[-1] - experiment2[0]) /
    (multimeter[-1] - multimeter[0])
) * (multimeter - multimeter[0])

# Approximate INL at sampled points
inl1 = adc1 - ref1
inl2 = experiment2 - ref2

# Plot estimated endpoint INL
for number, voltage, inl in [
    (1, v1, inl1),
    (2, multimeter, inl2)
]:
    plt.figure(figsize=(8, 5))
    plt.plot(voltage, inl, "o-",
             label=f"Experiment {number}")
    plt.axhline(0, color="black",
                linestyle="--", label="Reference")
    plt.xlabel("Multimeter Voltage (V)")
    plt.ylabel("Endpoint Deviation (LSB)")
    plt.title(
        f"Experiment {number}: "
        "Approximate Endpoint INL"
    )
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        f"Experiment{number}_Endpoint_INL.png",
        dpi=300
    )
    plt.show()

print("Experiment 1 max endpoint deviation:",
      np.max(np.abs(inl1)), "LSB")
print("Experiment 2 max endpoint deviation:",
      np.max(np.abs(inl2)), "LSB")


print("Both diagrams have been saved!")
plt.show()
