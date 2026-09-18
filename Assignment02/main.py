# main.py

from rental import Vehicle, Renter, ElectricCar, Motorbike

def main():

    car = Vehicle('Toyota', 'Yaris', '1AB234')
    electric_car = ElectricCar('Tesla', 'Model 3', '2CD567', 75)
    motorbike = Motorbike('Yamaha', 'YZF-R3', '3EF890', 321)


    try:
        renter = Renter('John Doe', 12345)

    
        car.rent()
        print(car)


        car.return_vehicle()
        print(car)

    
        invalid_renter = Renter('', -1)  # This should raise ValueError

    except ValueError as ve:
        print("Error:", ve)


    vehicles = [car, electric_car, motorbike]
    for vehicle in vehicles:
        print(vehicle)

if __name__ == "__main__":
    main()
