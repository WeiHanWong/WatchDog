#include <WiFi.h>
#include <HTTPClient.h>
#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <BLEBeacon.h>

int scanTime = 1;
BLEScan *pBLEScan;
const char* ssid = "";
const char* password = "";
const char* serverName = "http://X/api/urssi";
const char* ntpName = "http://X/api/gettime";
const String probe = "2";
class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
  void onResult(BLEAdvertisedDevice advertisedDevice)
  {
    if (advertisedDevice.haveManufacturerData() == true)
    {
      std::string strManufacturerData = advertisedDevice.getManufacturerData();

      uint8_t cManufacturerData[100];
      strManufacturerData.copy((char *)cManufacturerData, strManufacturerData.length(), 0);

      if (cManufacturerData[0] == 0x4C && cManufacturerData[1] == 0x00)
      {
        BLEBeacon oBeacon = BLEBeacon();
        oBeacon.setData(strManufacturerData);
        if (cManufacturerData[0] == 0x4C && cManufacturerData[1] == 0x00)
        {
          BLEBeacon oBeacon = BLEBeacon();
          oBeacon.setData(strManufacturerData);
          if (oBeacon.getManufacturerId()==0x004c && oBeacon.getMinor() == 0x00 && oBeacon.getMajor() == 0x00)
          {
            if(WiFi.status()== WL_CONNECTED)
            {
              WiFiClient client;
              HTTPClient http;

              http.begin(client, ntpName);
              http.addHeader("Content-Type", "application/x-www-form-urlencoded");      
              int httpResponseCode = http.GET();
              String payload = "";
              if (httpResponseCode==200) 
              {
                payload = http.getString();
                payload.replace("\"", "");
              }
              http.end();

              http.begin(client, serverName);
              http.addHeader("Content-Type", "application/x-www-form-urlencoded");
              String httpRequestData = "probe="+probe+"&uuid="+oBeacon.getProximityUUID().toString().c_str()+"&urssi="+advertisedDevice.getRSSI()+"&time=" + payload;           
              httpResponseCode = http.POST(httpRequestData);
              http.end();

              Serial.printf("UUID: %s\n", oBeacon.getProximityUUID().toString().c_str());
              Serial.println(advertisedDevice.getRSSI());
              Serial.println(payload);
            }
          }
        }
      }
    }
  }
};

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println("Connected to Wifi");
  BLEDevice::init("");
  Serial.println("Scanning as Probe " + probe);
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);
}

void loop() {
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  pBLEScan->clearResults();
  delay(0.1);
}