import argparse

from weconnect import weconnect
from weconnect.elements.route import Address, Destination, GeoCoordinate, Route



def main():
    """ Simple example showing how to send destinations in a vehicle by providing the VIN as a parameter """
    parser = argparse.ArgumentParser(
        prog='destinations',
        description='Example sending destinations')
    parser.add_argument('-u', '--username', help='Username of Volkswagen id', required=True)
    parser.add_argument('-p', '--password', help='Password of Volkswagen id', required=True)
    parser.add_argument('--vin', help='VIN of the vehicle to start destinations', required=True)

    args = parser.parse_args()

    route = Route([
        Destination(
            geoCoordinate=GeoCoordinate(
                latitude=52.4278793,
                longitude=10.8077433,
            ),
            name='VW Museum',
        ),
        Destination(
            address=Address(
                country='Germany',
                street='Stadtbrücke',
                zipCode='38440',
                city='Wolfsburg',
            ),
            name='Autostadt',
        )
    ])


    print('#  Initialize WeConnect')
    weConnect = weconnect.WeConnect(username=args.username, password=args.password, updateAfterLogin=False, loginOnInit=False)
    print('#  Login')
    weConnect.login()
    print('#  update')
    weConnect.update()

    for vin, vehicle in weConnect.vehicles.items():
        if vin == args.vin:
            print('#  send destinations')

            if 'destinations' not in vehicle.capabilities or not vehicle.capabilities['destinations']:
                print('#  destinations is not supported')
                continue

            if not vehicle.controls.sendDestinations:
                print('#  sendDestinations is not available')
                continue

            vehicle.controls.sendDestinations.value = route

    print('#  destinations sent')


if __name__ == '__main__':
    main()
