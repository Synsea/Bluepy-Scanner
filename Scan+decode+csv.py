from bluepy.btle import Scanner
import csv,os
from datetime import datetime

scanner=Scanner()

CAPTEURS={
"MAC":"NAME",
}

CSV="bluetooth_data.csv"

if not os.path.exists(CSV):
    with open(CSV,"w",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["Date","Heure","Nom","Adresse","RSSI","Batterie","Temperature","Humidite","Trame"])

def decode_data(value):
    data=bytes.fromhex(value)

    batterie=data[10]

    temp_int=int.from_bytes(data[12:14],byteorder="big")
    signe=(temp_int>>14)&1
    temp=(temp_int&0x3FFF)*0.01
    if signe==1:
        temp=-temp

    hum_int=int.from_bytes(data[14:16],byteorder="big")
    hum=(hum_int&0x7FFF)*0.01

    return batterie,temp,hum

print("Scan des capteurs... Ctrl+C pour arrêter")

try:
    while True:
        try:
            devices=scanner.scan(timeout=3.0)
        except Exception as e:
            print("Erreur scan :",e)
            continue

        for device in devices:
            addr=device.addr.lower()

            if addr in CAPTEURS:
                for adtype,description,value in device.getScanData():
                    if description=="16b Service Data":
                        batterie,temp,hum=decode_data(value)
                        now=datetime.now()
                        date=now.strftime("%d/%m/%Y")
                        heure=now.strftime("%H:%M:%S")
                        nom=CAPTEURS[addr]

                        print(nom,addr,device.rssi,batterie,f"{temp:.2f}",f"{hum:.2f}")

                        with open(CSV,"a",newline="") as f:
                            writer=csv.writer(f)
                            writer.writerow([date,heure,nom,addr,device.rssi,batterie,f"{temp:.2f}",f"{hum:.2f}",value])

except KeyboardInterrupt:
    print("\nScan arrêté proprement.")
