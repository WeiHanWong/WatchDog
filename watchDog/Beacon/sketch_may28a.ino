#include "sys/time.h"
#include "BLEDevice.h"
#include "BLEUtils.h"
#include "BLEServer.h"
#include "BLEBeacon.h"
#include "esp_sleep.h"

#define GPIO_DEEP_SLEEP_DURATION     1 
#define BEACON_UUID "5a4bcfce-174e-4bac-a814-092e77f6b7e5"

RTC_DATA_ATTR static time_t last;      
RTC_DATA_ATTR static uint32_t bootcount;
BLEAdvertising *pAdvertising;  

void setBeacon() {

  BLEBeacon oBeacon = BLEBeacon();

  oBeacon.setManufacturerId(0x4C00);
  BLEUUID bleUUID = BLEUUID(BEACON_UUID) ;
  bleUUID = bleUUID.to128();
  oBeacon.setProximityUUID(BLEUUID( bleUUID.getNative()->uuid.uuid128, 16, true ));
  oBeacon.setMajor(0);
  oBeacon.setMinor(0);

  BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();
  BLEAdvertisementData oScanResponseData = BLEAdvertisementData();
  oAdvertisementData.setFlags(0x04); 
  
  std::string strServiceData = "";
  strServiceData += (char)26; 
  strServiceData += (char)0xFF; 
  strServiceData += oBeacon.getData();
  oAdvertisementData.addData(strServiceData);
  pAdvertising->setAdvertisementData(oAdvertisementData);
  pAdvertising->setScanResponseData(oScanResponseData);

}

void setup() {
  BLEDevice::init("WatchDog Beacon");

  //BLE Server
  BLEServer *pServer = BLEDevice::createServer();
  pAdvertising = BLEDevice::getAdvertising();
  BLEDevice::startAdvertising();

  setBeacon();

  pAdvertising->start();
  delay(100);
  pAdvertising->stop();
  esp_deep_sleep(1000000LL * GPIO_DEEP_SLEEP_DURATION);

}

void loop() {

}

