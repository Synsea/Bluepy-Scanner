from bluepy.btle import Scanner
import csv,os,time
from datetime import datetime

scanner=Scanner()
CSV="scan_bluetooth.csv"

if not os.path.exists(CSV):
    with open(CSV,"w",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["Date","Heure","Adresse","Type","RSSI","Description","Valeur"])

print("Scan Bluetooth + CSV... Ctrl+C pour arrêter")

try:
    while True:
        devices=scanner.scan(timeout=5.0)

        for device in devices:
            now=datetime.now()
            date=now.strftime("%d/%m/%Y")
            heure=now.strftime("%H:%M:%S")

            print(device.addr,"|",device.addrType,"| RSSI=",device.rssi,"dB")

            for adtype,description,value in device.getScanData():
                with open(CSV,"a",newline="") as f:
                    writer=csv.writer(f)
                    writer.writerow([date,heure,device.addr,device.addrType,device.rssi,description,value])

        time.sleep(1)

except KeyboardInterrupt:
    print("\nScan arrêté")
