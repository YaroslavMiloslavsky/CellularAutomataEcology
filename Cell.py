from NatureForce import *
import random


class Cell:
    def __init__(self, landType=LandType.LAND, altitude=Altitude.LOW, temperature=25,
                 windDirection=WindDirection.NONE, clouds=Clouds.NO, rain=Rain.NO, pollution=Pollution.NONE):
        self.landType = landType
        self.altitude = altitude
        self.temperature = temperature
        self.windDirection = windDirection
        self.clouds = clouds
        self.rain = rain
        self.pollution = pollution

        if landType is LandType.CITY:
            self.temperature = random.randint(23, 32)
            self.pollution = Pollution.POLLUTED
            self.windDirection = random.choice(list(WindDirection))
            self.altitude = Altitude.FLAT
        elif landType is LandType.FOREST:
            self.temperature = random.randint(15, 25)
            self.pollution = Pollution.NONE
            self.altitude = random.choice(list(Altitude))
            if random.randint(0, 100) > 85:
                self.clouds = Clouds.YES
        elif landType is LandType.ICE:
            self.temperature = -40  # ICE must be the same value otherwise it will melt
            self.pollution = Pollution.NONE
        elif landType is LandType.LAND:
            self.temperature = random.randint(25, 26)
            self.pollution = Pollution.NONE
            self.altitude = random.choice(list(Altitude))
        elif landType is LandType.SEA:
            self.temperature = random.randint(0, 20)
            self.pollution = Pollution.NONE
            self.windDirection = random.choice(list(WindDirection))
        if random.randint(0, 100) > 85:
            self.clouds = Clouds.YES

        self.bg = self.evaluateHealth(self.temperature)

    def getStatus(self):
        return self.bg

    def evaluateTemperature(self, landType):
        if landType is LandType.CITY:
            self.temperature = random.randint(25, 40)
        elif landType is LandType.FOREST:
            self.temperature = random.randint(15, 25)
        elif landType is LandType.ICE:
            self.temperature = random.randint(-40, 0)
        elif landType is LandType.LAND:
            self.temperature = random.randint(25, 30)
        elif landType is LandType.SEA:
            self.temperature = random.randint(0, 20)
        self.bg = self.evaluateHealth(self.temperature)

    def evaluateHealth(self, temp):
        if self.landType is LandType.SEA:
            return cellHealth['water']
        if self.rain is Rain.YES:
            return cellHealth['rain']
        if temp < 0:
            return cellHealth['cold']
        elif 10 <= temp < 30:
            return cellHealth['normal']
        elif 30 <= temp < 35:
            return cellHealth['warm']
        elif temp >= 35:
            return cellHealth['hot']

    def evaluateLandType(self):
        if self.landType is LandType.ICE:
            if self.temperature > 0:
                self.landType = LandType.SEA
        elif self.landType is LandType.SEA:
            if self.temperature > 60:
                self.landType = LandType.LAND
            if self.temperature < 0:
                self.landType = LandType.ICE
        elif self.landType is LandType.LAND or self.landType is LandType.FOREST:
            if self.temperature < 0:
                self.landType = LandType.ICE

    def __str__(self):
        return f'landType: {self.landType}, altitude: {self.altitude},' \
               f'temperature: {self.temperature},' \
               f'windDirection: {self.windDirection}, clouds: {self.clouds},' \
               f'rain: {self.rain}, pollution: {self.pollution}'
