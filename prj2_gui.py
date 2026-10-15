
from fileinput import filename
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv

# EEE309 Project 2 - Digital Voltmeter
# TO RUN DO IN TERMINAL: py prj2_gui.py

MULTIMETER = [
    0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4,
    2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.0
]

ADC_VALUES = [
    0, 83, 165, 247, 327, 410, 490,
    573, 656, 737, 817, 902, 983, 1023
]

PORT = "COM6"
BAUD = 9600

class Voltmeter:
    def __init__(self, root):
        self.root = root
        self.root.title("EEE309 Digital Voltmeter")
        self.root.geometry("520x470")

        self.meter = MULTIMETER.copy()
        self.adc = ADC_VALUES.copy()
        self.arduino = None
        self.mode = tk.StringVar(value="Offline")

        ttk.Label(
            root, text="EEE309 Digital Voltmeter",
            font=("Arial", 21, "bold")
        ).pack(pady=20)

        ttk.Label(
            root, text="Select Mode:"
        ).pack()

        self.mode_box = ttk.Combobox(
            root, textvariable=self.mode,
            values=["Offline", "Online"],
            state="readonly"
        )
        self.mode_box.pack(pady=8)
        self.mode_box.bind(
            "<<ComboboxSelected>>", self.change_mode
        )

        self.voltage_label = tk.Label(
            root, text="0.000 V",
            font=("Arial", 42, "bold"),
            fg="#0066cc"
        )
        self.voltage_label.pack(pady=20)

        self.status = ttk.Label(
            root, text="Offline Mode"
        )
        self.status.pack()

        self.slider = tk.Scale(
            root, from_=0, to=len(self.adc)-1,
            orient="horizontal",
            length=400,
            label="Measurement Number",
            command=self.update_offline
        )
        self.slider.pack(pady=15)

        self.adc_label = ttk.Label(
            root, text="ADC: 0 / 1023",
            font=("Arial", 13)
        )
        self.adc_label.pack(pady=5)

        ttk.Button(
            root, text="Load CSV File",
            command=self.load_csv
        ).pack(pady=10)

        ttk.Label(
            root, text="Online refresh rate: 100 ms"
        ).pack(pady=5)

        self.update_offline(0)
        self.root.after(100, self.update_online)
        self.root.protocol(
            "WM_DELETE_WINDOW", self.close
        )

    def update_offline(self, value):
        if self.mode.get() != "Offline":
            return

        i = int(float(value))
        adc = self.adc[i]
        voltage = adc * 5.0 / 1023.0

        self.voltage_label.config(
            text=f"{voltage:.3f} V"
        )
        self.adc_label.config(
            text=f"ADC: {adc} / 1023"
        )
        self.status.config(
            text=f"Multimeter: {self.meter[i]:.1f} V"
        )

    def change_mode(self, event=None):
        if self.arduino:
            self.arduino.close()
            self.arduino = None

        if self.mode.get() == "Offline":
            self.slider.config(state="normal")
            self.update_offline(self.slider.get())
            return

        self.slider.config(state="disabled")

        try:
            import serial
            self.arduino = serial.Serial(
                PORT, BAUD, timeout=0.05
            )
            self.status.config(
                text="Online | Arduino connected"
            )
        except (ImportError, Exception) as e:
            messagebox.showerror(
                "Connection Error", str(e)
            )
            self.mode.set("Offline")
            self.slider.config(state="normal")
            self.update_offline(self.slider.get())

    def update_online(self):
        if self.mode.get() == "Online" and self.arduino:
            try:
                if self.arduino.in_waiting:
                    raw = self.arduino.readline().decode(
                        errors="ignore"
                    ).strip()

                    adc = int(raw)
                    if 0 <= adc <= 1023:
                        voltage = adc * 5.0 / 1023.0

                        self.voltage_label.config(
                            text=f"{voltage:.3f} V"
                        )
                        self.adc_label.config(
                            text=f"ADC: {adc} / 1023"
                        )
            except ValueError:
                pass
            except Exception as e:
                self.status.config(
                    text=f"Connection lost: {e}"
                )
                self.arduino.close()
                self.arduino = None

        self.root.after(100, self.update_online)

    def load_csv(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f, delimiter=",")
                rows = list(reader)

            meter = [
                float(r["Multimeter_V"]) for r in rows
            ]
            adc = [
                int(float(r["ADC"])) for r in rows
            ]

            if not adc or any(
                x < 0 or x > 1023 for x in adc
            ):
                raise ValueError("Invalid ADC values")

            self.meter = meter
            self.adc = adc
            self.mode.set("Offline")

            if self.arduino:
                self.arduino.close()
                self.arduino = None

            self.slider.config(
                to=len(adc)-1, state="normal"
            )
            self.slider.set(0)
            self.update_offline(0)

            messagebox.showinfo(
                "CSV Loaded",
                f"Successfully loaded {len(adc)} measurements!"
            )

        except Exception as e:
            messagebox.showerror("CSV Error", str(e))

    def close(self):
        if self.arduino:
            self.arduino.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Voltmeter(root)
    root.mainloop()
