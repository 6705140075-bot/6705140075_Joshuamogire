# rental.py

class Vehicle:
    def __init__(self, make, model, plate):
        self.make = make
        self.model = model
        self.plate = plate
        self.is_rented = False

    def rent(self):
        if not self.is_rented:
            self.is_rented = True
        else:
            raise Exception("Vehicle is already rented")

    def return_vehicle(self):
        if self.is_rented:
            self.is_rented = False
        else:
            raise Exception("Vehicle is already available")

    def __str__(self):
        status = 'rented' if self.is_rented else 'available'
        return f"{self.make} {self.model} ({self.plate}) [{status}]"


class Renter:
    def __init__(self, name, license_no):
        self.name = name
        self.license_no = license_no
        self.rented = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:  # Checks for empty name
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def license_no(self):
        return self._license_no

    @license_no.setter
    def license_no(self, value):
        if value <= 0:  # Checks for positive license number
            raise ValueError("License number must be positive")
        self._license_no = value


class ElectricCar(Vehicle):
    def __init__(self, make, model, plate, battery_kwh):
        super().__init__(make, model, plate)
        self.battery_kwh = battery_kwh

    def __str__(self):
        status = 'rented' if self.is_rented else 'available'
        return f"Electric Car: {self.make} {self.model} ({self.plate}) - Battery: {self.battery_kwh}kWh [{status}]"


class Motorbike(Vehicle):
    def __init__(self, make, model, plate, engine_cc):
        super().__init__(make, model, plate)
        self.engine_cc = engine_cc

    def __str__(self):
        status = 'rented' if self.is_rented else 'available'
        return f"Motorbike: {self.make} {self.model} ({self.plate}) - Engine: {self.engine_cc}cc [{status}]"
