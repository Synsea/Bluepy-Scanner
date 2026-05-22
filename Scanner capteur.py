from bluepy.btle import Scanner
import time

scanner=Scanner()

CAPTEURS={
"MAC":"NAME1",

}

print("Scan capteurs... Ctrl+C pour arrêter")

try:
    while True:
        devices=scanner.scan(timeout=5.0)

        for device in devices:
            addr=device.addr.lower()

            if addr in CAPTEURS:
                print("\n"+CAPTEURS[addr])
                print("Adresse :",addr)
                print("Type :",device.addrType)
                print("RSSI :",device.rssi,"dB")

                for adtype,description,value in device.getScanData():
                    print(description,"=",value)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nScan arrêté")
