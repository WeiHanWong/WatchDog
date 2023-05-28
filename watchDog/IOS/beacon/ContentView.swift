//
//  ContentView.swift
//  beacon
//
//  Created by Will on 27/5/23.
//
import Combine
import CoreLocation
import SwiftUI

class beacon : NSObject, ObservableObject, CLLocationManagerDelegate{
    var didChange = PassthroughSubject<Void, Never>()
    var locationManager: CLLocationManager?
    var lastDistance = CLProximity.unknown
    
    override init(){
        super.init()
        
        locationManager = CLLocationManager()
        locationManager?.delegate = self
        locationManager?.requestWhenInUseAuthorization()
    }
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if status == .authorizedWhenInUse {
            if CLLocationManager.isMonitoringAvailable(for: CLBeaconRegion.self){
                if CLLocationManager.isRangingAvailable(){
                    startScanning()
                }
            }
        }
    }
    
    func startScanning(){
        let uuid = UUID(uuidString: "5A4BCFCE-174E-4BAC-A814-092E77F6B7E5")!
        let contraint = CLBeaconIdentityConstraint(uuid: uuid, major: 0, minor: 0)
        let beaconRegion = CLBeaconRegion(beaconIdentityConstraint: contraint, identifier: "mybeacon")
        locationManager?.startMonitoring(for: beaconRegion)
        locationManager?.startRangingBeacons(satisfying: contraint)
    }
    
    func locationManager (_ manager: CLLocationManager, didRange beacons: [CLBeacon], satisfying beaconConstraint: CLBeaconIdentityConstraint) {
        if let beacon = beacons.first {
            update(distance: beacon.proximity)
        } else {
            update(distance: .unknown)
        }
    }
    
    func update(distance: CLProximity){
        lastDistance = distance
        didChange.send(())
    }
}
struct BigText: ViewModifier {
    func body (content: Content) -> some View {
        content
            .font (Font.system(size: 72, design: .rounded))
            .frame (minWidth: 0, maxWidth: .infinity)
    }
}
struct ContentView: View {
    @ObservedObject var detector = beacon()
    
    var body: some View {
        if detector.lastDistance == .immediate {
            Text ("RIGHT HERE" )
                .modifier(BigText())
                .background (Color.gray)
                .edgesIgnoringSafeArea(.all)
        } else if detector.lastDistance == .near {
            Text ("NEAR" )
                .modifier(BigText())
                .background (Color.gray)
                .edgesIgnoringSafeArea(.all)
        } else if detector.lastDistance == .far {
            Text ("FAR" )
                .modifier(BigText())
                .background (Color.gray)
                .edgesIgnoringSafeArea(.all)
        } else {
            Text ("UNKNOWN" )
                .modifier(BigText())
                .background (Color.gray)
                .edgesIgnoringSafeArea(.all)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
