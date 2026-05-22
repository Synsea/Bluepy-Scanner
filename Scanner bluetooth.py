from bluepy.btle import Scanner
import time

scanner=Scanner()

print("Scan Bluetooth... Ctrl+C pour arrêter")

try:
    while True:
        devices=scanner.scan(timeout=5.0)

        print("\n--- Appareils détectés ---")

        for device in devices:
            print(device.addr,"|",device.addrType,"| RSSI=",device.rssi,"dB")

            for adtype,description,value in device.getScanData():
                print(" ",description,"=",value)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nScan arrêté")
