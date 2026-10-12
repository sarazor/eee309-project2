
import serial
import time

# Connect to Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)

time.sleep(2)

print("Arduino connected!")
print("Reading potentiometer voltage...")

try:
    while True:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode(
                'utf-8', errors='ignore'
            ).strip()

            try:
                adc_value = int(data)

                voltage = adc_value * 5.0 / 1023.0

                print(
                    f"ADC: {adc_value} | "
                    f"Voltage: {voltage:.3f} V"
                )

            except ValueError:
                pass

except KeyboardInterrupt:
    print("Stopped.")

finally:
    arduino.close()
