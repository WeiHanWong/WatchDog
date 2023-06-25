//
//  ViewController.swift
//  WatchDogToken
//
//  Created by Will on 24/6/23.
//


import UIKit
import CoreBluetooth
import CoreLocation
import CoreData


class ViewController: UIViewController, CBPeripheralManagerDelegate, UITextFieldDelegate {
    
    @IBOutlet weak var nameBox: UITextField!
    @IBOutlet weak var uuidButton: UIButton!
    @IBOutlet weak var uuidValue: UILabel!
    @IBOutlet weak var identityValue: UILabel!
    @IBOutlet weak var loadingCircle: UIActivityIndicatorView!
    @IBOutlet weak var beaconStatus: UILabel!
    
    @IBOutlet weak var startButton: UIButton!
    @IBOutlet weak var stopButton: UIButton!
    
    // Objects used in the creation of iBeacons
    var localBeacon: CLBeaconRegion!
    var beaconPeripheralData: NSDictionary!
    var peripheralManager: CBPeripheralManager!
    
    var localBeaconUUID = "624fda32-5dd9-4600-bca2-9bd7cf1d6058"
    let localBeaconMajor: CLBeaconMajorValue = 0
    let localBeaconMinor: CLBeaconMinorValue = 0
    let identifier = "John"
    let url = "http://192.168.0.184/api/uuidrequest"
    
    func requestAccessAndRefreshTokens(accessCode: String) {
        // Request Preconfiguration
        let requestHeaders: [String:String] = ["Content-Type" : "application/x-www-form-urlencoded"]
        var requestBodyComponents = URLComponents()
        requestBodyComponents.queryItems = [URLQueryItem(name: "name", value: accessCode)]
        
        // Request Configuration
        var request = URLRequest(url: URL(string: url)!)
        request.httpMethod = "POST"
        request.allHTTPHeaderFields = requestHeaders
        request.httpBody = requestBodyComponents.query?.data(using: .utf8)
        // Performing request
        URLSession.shared.dataTask(with: request) { (data, response, eror) in
            guard let data = data else{
                return
            }
            self.localBeaconUUID = String(decoding: data, as: UTF8.self).replacingOccurrences(of: "\"", with: "", options: NSString.CompareOptions.literal, range: nil)
        }.resume()
        DispatchQueue.global(qos: .userInitiated).async {
            sleep(1)
            DispatchQueue.main.async {
                self.identityValue.text = self.nameBox.text
                self.uuidValue.text = self.localBeaconUUID
                self.loadingCircle.isHidden = true
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        stopButton.isHidden = true
        loadingCircle.isHidden = true
        loadingCircle.startAnimating()
        // UI setup
        uuidValue.text = localBeaconUUID
        identityValue.text = identifier
        beaconStatus.text = "OFF"
        nameBox.delegate = self
        
        let tap = UITapGestureRecognizer(target: self, action: #selector(UIInputViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)
    }
    
    @objc func dismissKeyboard() {
        view.endEditing(true)
        uuidButton.endEditing(true)
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        self.view.endEditing(true)
        return false
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
    
    @IBAction func uuidButton(_ sender: Any) {
        loadingCircle.isHidden = false
        requestAccessAndRefreshTokens(accessCode: nameBox.text!)
    }
    
    func initLocalBeacon() {
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
    
}
