//
//  ViewController.swift
//  WatchDog
//
//  Created by Will on 18/6/23.
//

import UIKit
import CoreBluetooth
import CoreLocation

class ViewController: UIViewController, CBPeripheralManagerDelegate {
    
    @IBOutlet weak var uuidValue: UILabel!
    @IBOutlet weak var majorValue: UILabel!
    @IBOutlet weak var minorValue: UILabel!
    @IBOutlet weak var identityValue: UILabel!
    @IBOutlet weak var beaconStatus: UILabel!
    
    @IBOutlet weak var startButton: UIButton!
    @IBOutlet weak var stopButton: UIButton!
    
    // Objects used in the creation of iBeacons
    var localBeacon: CLBeaconRegion!
    var beaconPeripheralData: NSDictionary!
    var peripheralManager: CBPeripheralManager!
    
    var localBeaconUUID = ""
    let localBeaconMajor: CLBeaconMajorValue = 0
    let localBeaconMinor: CLBeaconMinorValue = 0
    let identifier = "John"
//    let url = "http://192.168.0.184/api/uuidrequest"
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        stopButton.isHidden = true
        // UI setup
        uuidValue.text = localBeaconUUID
        majorValue.text = String(localBeaconMajor)
        minorValue.text = String(localBeaconMinor)
        identityValue.text = identifier
        beaconStatus.text = "OFF"
    }

    @IBAction func startButton(_ sender: Any) {
        initLocalBeacon()
        startButton.isHidden = true
        stopButton.isHidden = false
        beaconStatus.text = "ON"
    }
    @IBAction func stopButton(_ sender: Any) {
        stopLocalBeacon()
        startButton.isHidden = false
        stopButton.isHidden = true
        beaconStatus.text = "OFF"
    }
    
    func initLocalBeacon() {
//        let parameters = ["name": identifier]
//        sendPostRequest(urlString: url, parameters: parameters) { result in
//            switch result {
//            case .success(let data):
//                // Handle the response data
//                do {
//                    if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
//                       let BeaconUUID = json["uuid"] as? String {
//                        print("UUID: \(BeaconUUID)")
//                        self.localBeaconUUID = BeaconUUID
//                    } else {
//                        print("Invalid JSON or missing 'name' key")
//                    }
//                } catch {
//                    print("Error parsing JSON: \(error)")
//                }
//
//            case .failure(let error):
//                // Handle the error
//                print("Error: \(error)")
//            }
//        }
        if localBeacon != nil {
            stopLocalBeacon()
        }
        let uuid = UUID(uuidString: localBeaconUUID)!
        localBeacon = CLBeaconRegion(uuid: uuid, major: localBeaconMajor, minor: localBeaconMinor, identifier: identifier)
        beaconPeripheralData = localBeacon.peripheralData(withMeasuredPower: nil)
        peripheralManager = CBPeripheralManager(delegate: self, queue: nil, options: nil)
    }
    
    func stopLocalBeacon() {
        peripheralManager.stopAdvertising()
        peripheralManager = nil
        beaconPeripheralData = nil
        localBeacon = nil
    }
    
    func peripheralManagerDidUpdateState(_ peripheral: CBPeripheralManager) {
        if peripheral.state == .poweredOn {
            peripheralManager.startAdvertising(beaconPeripheralData as? [String: Any])
            
        }
        else if peripheral.state == .poweredOff {
            peripheralManager.stopAdvertising()
        }
    }
    
    func sendPostRequest(urlString: String, parameters: [String: String], completion: @escaping (Result<Data, Error>) -> Void) {
        // Create a URL object from the provided string
        if let url = URL(string: urlString) {
            // Create the request
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            
            // Set the content type header
            request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
            
            // Encode the parameters
            let encodedParams = parameters
                .map { key, value in
                    let encodedKey = key.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? ""
                    let encodedValue = value.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? ""
                    return "\(encodedKey)=\(encodedValue)"
                }
                .joined(separator: "&")
            
            // Set the request body
            request.httpBody = encodedParams.data(using: .utf8)
            
            // Create a URLSession configuration
            let config = URLSessionConfiguration.default
            
            // Create a URLSession object
            let session = URLSession(configuration: config)
            
            // Create a data task with the request
            let task = session.dataTask(with: request) { (data, response, error) in
                // Check for any errors
                if let error = error {
                    completion(.failure(error))
                    return
                }
                
                // Check if the response is an HTTP response
                if let httpResponse = response as? HTTPURLResponse {
                    // Get the status code
                    let statusCode = httpResponse.statusCode
                    
                    // Check if the status code is in the success range (200-299)
                    if 200 ..< 300 ~= statusCode {
                        // Check if there is any response data
                        if let data = data {
                            completion(.success(data))
                        } else {
                            let emptyDataError = NSError(domain: "", code: 0, userInfo: [NSLocalizedDescriptionKey: "Response data is empty"])
                            completion(.failure(emptyDataError))
                        }
                    } else {
                        let statusCodeError = NSError(domain: "", code: statusCode, userInfo: [NSLocalizedDescriptionKey: "Status code: \(statusCode)"])
                        completion(.failure(statusCodeError))
                    }
                }
            }
            
            // Start the data task
            task.resume()
        } else {
            let invalidURLError = NSError(domain: "", code: 0, userInfo: [NSLocalizedDescriptionKey: "Invalid URL"])
            completion(.failure(invalidURLError))
        }
    }
    

}
