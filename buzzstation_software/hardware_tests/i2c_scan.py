import smbus
import time


def scan_i2c_bus(bus_number=1):
    bus = smbus.SMBus(bus_number)
    print(f"Scanning I2C bus {bus_number}...\n")

    devices = []
    for address in range(0x03, 0x77):
        try:
            # SMBus2 wersja 0 jest kompatybilna z większością urządzeń
            bus.write_quick(address)
            devices.append(hex(address))
        except OSError:
            # Jeśli urządzenie nie odpowiada, kontynuuj
            continue

    if devices:
        print("Found I2C device(s) at address(es):")
        print(", ".join(devices))
    else:
        print("No I2C devices found.")

if __name__ == "__main__":
    scan_i2c_bus()

