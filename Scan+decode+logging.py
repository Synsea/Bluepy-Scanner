from bluepy.btle import Scanner
import logging
from datetime import datetime

scanner=Scanner()

CAPTEURS={
"d6:1c:bf:b7:76:62":"DEMO1",
"d6:c6:c7:39:a2:e8":"DEMO2",
"d7:ef:13:27:15:29":"DEMO3",
"d1:bf:9d:01:3e:11":"DEMO4"
}

logging.basicConfig(
    filename="bluetooth.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
logging.info("Démarrage du scan Bluetooth")

try:
    while True:
        try:
            devices=scanner.scan(timeout=3.0)
        except Exception as e:
            print("Erreur scan :",e)
            logging.error(f"Erreur scan : {e}")
            continue

        for device in devices:
            addr=device.addr.lower()

            if addr in CAPTEURS:
                for adtype,description,value in device.getScanData():
                    if description=="16b Service Data":
                        batterie,temp,hum=decode_data(value)
                        nom=CAPTEURS[addr]

                        print("\n"+nom)
                        print("Adresse :",addr)
                        print("RSSI :",device.rssi,"dB")
                        print("Batterie :",batterie,"%")
                        print("Température :",f"{temp:.2f}","°C")
                        print("Humidité :",f"{hum:.2f}","%")
                        print("Trame :",value)

                        logging.info(f"{nom} {addr} RSSI={device.rssi} Batterie={batterie}% Temp={temp:.2f}C Hum={hum:.2f}% Trame={value}")

except KeyboardInterrupt:
    print("\nScan arrêté proprement.")
    logging.info("Arrêt du scan Bluetooth")
