#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <BLEBeacon.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "";
const char* password = "";
const char* serverName = "http://X/api/urssi";
const char* ntpName = "http://X/api/gettime";
const String probeid = "1";

int scanTime = 5; //In seconds
BLEScan *pBLEScan;

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
    void onResult(BLEAdvertisedDevice advertisedDevice)
    {
      if (advertisedDevice.haveServiceUUID())
      {
        BLEUUID devUUID = advertisedDevice.getServiceUUID();
      }
      
      if (advertisedDevice.haveManufacturerData() == true)
      {
        std::string strManufacturerData = advertisedDevice.getManufacturerData();

        uint8_t cManufacturerData[100];
        strManufacturerData.copy((char *)cManufacturerData, strManufacturerData.length(), 0);

        if (strManufacturerData.length() == 25 && cManufacturerData[0] == 0x4C && cManufacturerData[1] == 0x00)
        {
          BLEBeacon oBeacon = BLEBeacon();
          oBeacon.setData(strManufacturerData);
          if(WiFi.status()== WL_CONNECTED){
            WiFiClient client;
            HTTPClient http;

            http.begin(client, ntpName);
            http.addHeader("Content-Type", "application/x-www-form-urlencoded");
            String httpRequestData = "";           
            int httpResponseCode = http.POST(httpRequestData);
            String payload = "";
            if (httpResponseCode==200) {
              payload = http.getString();
            }
            http.end();

            http.begin(client, serverName);
            http.addHeader("Content-Type", "application/x-www-form-urlencoded");
            httpRequestData = "probe=" + probeid + "&uuid=" + oBeacon.getProximityUUID().toString().c_str() + "&urssi=" + oBeacon.getSignalPower() + "&time=" + payload;           
            httpResponseCode = http.POST(httpRequestData);
            http.end();
          }
        }
      }
    }
};

void setup()
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);
}

void loop()
{
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  pBLEScan->clearResults();
  delay(1);
}