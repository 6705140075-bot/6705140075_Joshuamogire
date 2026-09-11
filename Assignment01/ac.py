class AirConditioner:
    """A room air-conditioner. Reported buggy by the QA team - fix it!"""
    VALID_MODES = ("cool", "fan", "dry", "auto")
    MIN_TEMP = 16
    MAX_TEMP = 30

    def __init__(self, brand, room_name, temperature=25, mode="cool", fan_speed=1):
        self.brand = brand
        self.room_name = room_name
        self.is_on = False
        
        # FIX 1: Validate the temperature immediately in the constructor.
        # We must use the property setter here, not set _temperature directly.
        if not (self.MIN_TEMP <= temperature <= self.MAX_TEMP):
            raise ValueError(f"Temperature must be {self.MIN_TEMP}-{self.MAX_TEMP} C.")
        self._temperature = temperature
        
        self.mode = mode
        self.fan_speed = fan_speed
        
        # FIX 2: Removed the stored '_is_energy_saving' variable. 
        # It will be calculated dynamically in the property below.

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        # FIX 3: Changed 'and' to 'or'. 
        # (Old logic: if value < 16 AND value > 30 -> impossible condition)
        if value < self.MIN_TEMP or value > self.MAX_TEMP:
            raise ValueError(f"Temperature must be {self.MIN_TEMP}-{self.MAX_TEMP} C.")
        
        # FIX 4: Assign to self._temperature (the private variable), not self.temperature.
        # Assigning to self.temperature calls this setter again, causing RecursionError.
        self._temperature = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in self.VALID_MODES:
            raise ValueError(f"Mode must be one of {self.VALID_MODES}.")
        self._mode = value

    @property
    def fan_speed(self):
        return self._fan_speed

    @fan_speed.setter
    def fan_speed(self, value):
        if value not in (1, 2, 3):
            raise ValueError("Fan speed must be 1 (low), 2 (medium) or 3 (high).")
        self._fan_speed = value

    @property
    def is_energy_saving(self):
        # FIX 5: Calculate this dynamically based on the current temperature.
        # The test expects it to be True when temp >= 26 (and False at 22).
        return self._temperature >= 26

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def cooler(self):
        # FIX 6: Prevent temperature from dropping below the minimum.
        if self._temperature > self.MIN_TEMP:
            self._temperature -= 1

    def warmer(self):
        # FIX 7: Prevent temperature from exceeding the maximum (good practice).
        if self._temperature < self.MAX_TEMP:
            self._temperature += 1

    def __str__(self):
        power = "ON" if self.is_on else "OFF"
        # FIX 8: Changed 'self.fan' to 'self.fan_speed' to match the property name.
        return (f"{self.brand} AC in {self.room_name}: {power}, "
                f"{self.temperature}C, mode={self.mode}, fan={self.fan_speed}")