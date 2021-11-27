import math
import statistics
import numpy as np
import threading
from tkinter import Button, Label, Toplevel, Tk, OptionMenu, StringVar, IntVar
import random
from Cell import Cell
from NatureForce import LandType, Altitude, WindDirection, Clouds, Rain, Pollution
import matplotlib.pyplot as plt

temperature_in_cities_list = []
temperature_list = []
pollution_list = []

root = Tk()
root.title('Earth Simulation')

N = 10
cellArray = [[0] * N for i in range(N)]  # The matrix of arrays
btnArray = [[0] * N for i in range(N)]  # The matrix of Buttons


def updateCellArray():
    for i in range(0, N):
        for k in range(0, N):
            cell = cellArray[i][k]
            button = StringVar()
            button.set(cell.landType.name)
            btnArray[i][k].config(text=button.get(), bg=cell.getStatus())


def updateLand(c, x, s):
    newTemp = s.get()
    c.temperature = newTemp
    c.landType = LandType[f'{x[0]}']
    c.evaluateTemperature(c.landType)
    updateCellArray()


def updateAltitude(c, x):
    c.altitude = Altitude[f'{x[0]}']
    updateCellArray()


def updateWindDirection(c, x):
    c.windDirection = WindDirection[f'{x[0]}']
    updateCellArray()


def updateClouds(c, x):
    c.clouds = Clouds[f'{x[0]}']
    updateCellArray()


def updateRain(c, x):
    c.rain = Rain[f'{x[0]}']
    updateCellArray()


def updatePollution(c, x):
    c.pollution = Pollution[f'{x[0]}']
    updateCellArray()


def isLegit(i, j):
    if 0 <= i < N and 0 <= j < N:
        return True
    else:
        return False


# TODO: Put into Cell class
def changeHealth(cell, temp=0):
    if cell.temperature < 65:
        cell.temperature += temp


generation_counter = IntVar()
generation_counter.set(0)
generation_text = StringVar()
generation_text.set(f'generation: {generation_counter.get()}')


# Rule set
# Pollution raises the temperature
# Temperature melts ice into water
def checkTemperatureRuleSet(cell, l, k):
    rightNeighbour = cellArray[l + 1][k] if isLegit(l + 1, k) else cellArray[0][k]
    leftNeighbour = cellArray[l - 1][k] if isLegit(l - 1, k) else cellArray[N - 1][k]
    upperNeighbour = cellArray[l][k - 1] if isLegit(l, k - 1) else cellArray[l][N - 1]
    lowerNeighbour = cellArray[l][k + 1] if isLegit(l, k + 1) else cellArray[l][0]

    if cell.pollution is Pollution.NONE and cell.temperature > 20:
        changeHealth(cell, temp=-0.5)
    # If the cell is polluted, it will increase in temperature
    if cell.pollution is Pollution.POLLUTED:
        changeHealth(cell, temp=2)
    # If the neighbour is polluted the temperature will increase but not by much
    elif rightNeighbour.pollution is Pollution.POLLUTED and cell.temperature < 31:
        changeHealth(cell, temp=1)
    elif leftNeighbour.pollution is Pollution.POLLUTED and cell.temperature < 31:
        changeHealth(cell, temp=1)
    elif upperNeighbour.pollution is Pollution.POLLUTED and cell.temperature < 31:
        changeHealth(cell, temp=1)
    elif lowerNeighbour.pollution is Pollution.POLLUTED and cell.temperature < 31:
        changeHealth(cell, temp=1)
    if cell.altitude is Altitude.HIGH and cell.temperature > 15:
        changeHealth(cell, temp=-0.5)
    elif cell.altitude is Altitude.HIGH and cell.temperature > 15:
        changeHealth(cell, temp=-1)

    cell.evaluateLandType()


def checkWindRuleSet(cell, l, k):
    rightNeighbour = cellArray[l + 1][k] if isLegit(l + 1, k) else cellArray[0][k]
    leftNeighbour = cellArray[l - 1][k] if isLegit(l - 1, k) else cellArray[N - 1][k]
    upperNeighbour = cellArray[l][k - 1] if isLegit(l, k - 1) else cellArray[l][N - 1]
    lowerNeighbour = cellArray[l][k + 1] if isLegit(l, k + 1) else cellArray[l][0]

    # Pollution can be light, noise, waste etc.
    if rightNeighbour.pollution is Pollution.POLLUTED and rightNeighbour.windDirection is WindDirection.WEST:
        cell.pollution = Pollution.POLLUTED
        if cell.landType is not LandType.SEA:
            cell.windDirection = WindDirection.WEST
    if leftNeighbour.pollution is Pollution.POLLUTED and leftNeighbour.windDirection is WindDirection.EAST:
        cell.pollution = Pollution.POLLUTED
        if cell.landType is not LandType.SEA:
            cell.windDirection = WindDirection.EAST
    if upperNeighbour.pollution is Pollution.POLLUTED and upperNeighbour.windDirection is WindDirection.SOUTH:
        cell.pollution = Pollution.POLLUTED
        if cell.landType is not LandType.SEA:
            cell.windDirection = WindDirection.SOUTH
    if lowerNeighbour.pollution is Pollution.POLLUTED and lowerNeighbour.windDirection is WindDirection.NORTH:
        cell.pollution = Pollution.POLLUTED
        if cell.landType is not LandType.SEA:
            cell.windDirection = WindDirection.NORTH

    cell.evaluateLandType()


def checkCloudsRuleSet(cell, l, k):
    rightNeighbour = cellArray[l + 1][k] if isLegit(l + 1, k) else cellArray[0][k]
    leftNeighbour = cellArray[l - 1][k] if isLegit(l - 1, k) else cellArray[N - 1][k]
    upperNeighbour = cellArray[l][k - 1] if isLegit(l, k - 1) else cellArray[l][N - 1]
    lowerNeighbour = cellArray[l][k + 1] if isLegit(l, k + 1) else cellArray[l][0]

    if rightNeighbour.clouds is Clouds.YES and rightNeighbour.windDirection is WindDirection.WEST:
        cell.clouds = Clouds.YES
    if leftNeighbour.clouds is Clouds.YES and leftNeighbour.windDirection is WindDirection.EAST:
        cell.clouds = Clouds.YES
    if upperNeighbour.clouds is Clouds.YES and upperNeighbour.windDirection is WindDirection.SOUTH:
        cell.clouds = Clouds.YES
    if lowerNeighbour.clouds is Clouds.YES and lowerNeighbour.windDirection is WindDirection.NORTH:
        cell.clouds = Clouds.YES

    # If all 4 neighbours have clouds, the cell will have rain
    if rightNeighbour.clouds is Clouds.YES and leftNeighbour.clouds is Clouds.YES and upperNeighbour.clouds is Clouds.YES and lowerNeighbour.clouds is Clouds.YES:
        cell.clouds = Clouds.YES
        cell.rain = Rain.YES


def checkPollutionRuleSet(cell, l, k):
    rightNeighbour = cellArray[l + 1][k] if isLegit(l + 1, k) else cellArray[0][k]
    leftNeighbour = cellArray[l - 1][k] if isLegit(l - 1, k) else cellArray[N - 1][k]
    upperNeighbour = cellArray[l][k - 1] if isLegit(l, k - 1) else cellArray[l][N - 1]
    lowerNeighbour = cellArray[l][k + 1] if isLegit(l, k + 1) else cellArray[l][0]

    if rightNeighbour.altitude is Altitude.HIGH and rightNeighbour.pollution is Pollution.POLLUTED:
        cell.pollution = Pollution.POLLUTED
        rightNeighbour.pollution = Pollution.NONE
    if leftNeighbour.altitude is Altitude.HIGH and leftNeighbour.pollution is Pollution.POLLUTED:
        cell.pollution = Pollution.POLLUTED
        leftNeighbour.pollution = Pollution.NONE
    if upperNeighbour.altitude is Altitude.HIGH and upperNeighbour.pollution is Pollution.POLLUTED:
        cell.pollution = Pollution.POLLUTED
        upperNeighbour.pollution = Pollution.NONE
    if lowerNeighbour.altitude is Altitude.HIGH and lowerNeighbour.pollution is Pollution.POLLUTED:
        cell.pollution = Pollution.POLLUTED
        lowerNeighbour.pollution = Pollution.NONE
    cell.evaluateLandType()


# We operate in Von Neuman neighbourhood

def nextGen():
    global avg_temp
    global generation_counter
    global generation_text
    global pollution_counter
    global avg_temp_in_cities
    global cityCounter

    pollution_counter = 0
    avg_temp = 0
    avg_temp_in_cities = 0
    # Test to see affect of city on a nearby forest
    for l in range(0, N):
        for k in range(0, N):
            current_cell = cellArray[l][k]
            checkTemperatureRuleSet(current_cell, l, k)
            checkWindRuleSet(current_cell, l, k)
            checkCloudsRuleSet(current_cell, l, k)
            checkPollutionRuleSet(current_cell, l, k)

            cellArray[l][k].evaluateTemperature(current_cell.temperature)
            avg_temp += abs(current_cell.temperature)
            if current_cell.pollution is Pollution.POLLUTED:
                pollution_counter += 1
            if current_cell.landType is LandType.CITY:
                avg_temp_in_cities += current_cell.temperature

    generation_counter.set(generation_counter.get() + 1)
    generation_text.set(str(f'generation: {generation_counter.get()}'))
    print('current generation:', generation_counter.get())
    temperature_list.append(avg_temp / (N ** 2))
    pollution_list.append((pollution_counter / N ** 2) * 100)
    temperature_in_cities_list.append(avg_temp_in_cities/cityCounter)
    updateCellArray()


# Experimental
def loopForever():
    counter = 0
    while counter < 10:
        nextGen()
        counter += 1
        # time.sleep(0.2)


def nextGenLoop():
    thread = threading.Thread(target=loopForever)
    thread.daemon = True
    thread.start()


def getCellInfo(cell):
    infoLayer = Toplevel()
    infoLayer.title('Cell Info')
    landLabel = Label(infoLayer, text='temperature:')
    landLabel.grid(column=0, row=0)
    altitudeLabel = Label(infoLayer, text='landType:')
    altitudeLabel.grid(column=0, row=1)
    tempLabel = Label(infoLayer, text='altitude:')
    tempLabel.grid(column=0, row=2)
    windDirLabel = Label(infoLayer, text='windDirection:')
    windDirLabel.grid(column=0, row=4)
    cloudsLabel = Label(infoLayer, text='clouds:')
    cloudsLabel.grid(column=0, row=5)
    rainLabel = Label(infoLayer, text='rain:')
    rainLabel.grid(column=0, row=6)
    pollutionLabel = Label(infoLayer, text='pollution:')
    pollutionLabel.grid(column=0, row=7)

    scaleVar = IntVar()
    scaleVar.set(cell.temperature)
    tempValue = Label(infoLayer, textvariable=scaleVar)
    tempValue.grid(column=1, row=0)

    clickedLand = StringVar()
    clickedLand.set(cell.landType.name)
    dropListLand = [[i.name] for i in list(LandType)]
    landValue = OptionMenu(infoLayer, clickedLand, *dropListLand,
                           command=lambda x=clickedLand.get(), c=cell, s=scaleVar: updateLand(c, x, s))
    landValue.grid(column=1, row=1)

    clickedAltitude = StringVar()
    clickedAltitude.set(cell.altitude.name)
    dropListAltitude = [[i.name] for i in list(Altitude)]
    altitudeValue = OptionMenu(infoLayer, clickedAltitude, *dropListAltitude,
                               command=lambda x=clickedAltitude.get(), c=cell: updateAltitude(c, x))
    altitudeValue.grid(column=1, row=2)

    clickedWindDirection = StringVar()
    clickedWindDirection.set(cell.windDirection.name)
    dropListWindDirection = [[i.name] for i in list(WindDirection)]
    windDirectionValue = OptionMenu(infoLayer, clickedWindDirection, *dropListWindDirection,
                                    command=lambda x=clickedWindDirection.get(), c=cell: updateWindDirection(c, x))
    windDirectionValue.grid(column=1, row=4)

    clickedClouds = StringVar()
    clickedClouds.set(cell.clouds.name)
    dropListClouds = [[i.name] for i in list(Clouds)]
    cloudsValue = OptionMenu(infoLayer, clickedClouds, *dropListClouds,
                             command=lambda x=clickedClouds.get(), c=cell: updateClouds(c, x))
    cloudsValue.grid(column=1, row=5)

    clickedRain = StringVar()
    clickedRain.set(cell.rain.name)
    dropListRain = [[i.name] for i in list(Rain)]
    rainValue = OptionMenu(infoLayer, clickedRain, *dropListRain,
                           command=lambda x=clickedRain.get(), c=cell: updateRain(c, x))
    rainValue.grid(column=1, row=6)

    clickedPollution = StringVar()
    clickedPollution.set(cell.pollution.name)
    dropListPollution = [[i.name] for i in list(Pollution)]
    pollutionValue = OptionMenu(infoLayer, clickedPollution, *dropListPollution,
                                command=lambda x=clickedPollution.get(), c=cell: updatePollution(c, x))
    pollutionValue.grid(column=1, row=7)

    infoLayer.mainloop()


cityCounter = 0
land = None
avg_temp = 0
avg_temp_in_cities = 0
pollution_counter = 0
for i in range(0, N):
    for j in range(0, N):
        # Parameters
        # Colder as the equator closer
        if j < 1 or j > 8:
            # temperature = random.randint(-40, 0)
            land = LandType.ICE
        if j == 1 or j == 8:
            land = LandType.SEA
        if 2 <= j < 6:
            # temperature = random.randint(20, 40)
            tempList = list(LandType)
            tempList.remove(LandType.ICE)
            if random.randint(0, 100) > 20:
                tempList.remove(LandType.SEA)
            if cityCounter > 4:
                tempList.remove(LandType.CITY)
            land = random.choice(tempList)
            if land == LandType.CITY:
                cityCounter += 1

        print(cityCounter)

        newCell = Cell(landType=land)
        btn_text = StringVar()
        btn_text.set(newCell.landType.name)
        newBtn = Button(root, width=5, text=btn_text.get(),
                        command=lambda cell=newCell, txt=btn_text: getCellInfo(cell),
                        bg=newCell.getStatus())
        newBtn.grid(column=i, row=j)
        cellArray[i][j] = newCell
        btnArray[i][j] = newBtn
        print(cellArray[i][j])
        avg_temp += abs(newCell.temperature)
        if newCell.pollution is Pollution.POLLUTED:
            pollution_counter += 1
        if newCell.landType is LandType.CITY:
            avg_temp_in_cities += newCell.temperature

temperature_list.append(avg_temp / (N ** 2))
pollution_list.append((pollution_counter / N ** 2) * 100)
temperature_in_cities_list.append((avg_temp_in_cities / cityCounter))

Label(root, textvariable=generation_text).grid(column=6, row=N, columnspan=6)
btn_next = Button(root, text='next generation', command=nextGen).grid(column=2, row=N, columnspan=6)
Button(root, text='auto', command=nextGenLoop).grid(column=0, row=N, columnspan=4)

root.mainloop()

# Here we write the data to graph logic
# For data normalization I used z = (x-min(x))/(max(x)-min(x)) to get a scatter between 0 and 1

# Average Temperature in cities
avgTemperatureInCities = round(sum(temperature_in_cities_list) / len(temperature_in_cities_list), ndigits=3)
temperatureInCitiesDeviation = round(statistics.stdev(temperature_list), ndigits=3)
print(f'avg temperature in cities overall was {avgTemperatureInCities}')
print(f'the temperature in cities overall is between {min(temperature_in_cities_list)} and {max(temperature_in_cities_list)}')
print(f'deviation is {avgTemperatureInCities}')
normalized_temperature_cities_list = [
    (x - min(temperature_in_cities_list)) / (max(temperature_in_cities_list) - min(temperature_in_cities_list)) for x in
    temperature_in_cities_list]
plt.scatter(x=list(range(0, generation_counter.get() + 1)), y=normalized_temperature_cities_list)
plt.title('normalized temperature in cities')
plt.show()

# Temperature Data
avgTemperatureThisRun = round(sum(temperature_list) / len(temperature_list), ndigits=3)
temperatureDeviation = round(statistics.stdev(temperature_list), ndigits=3)
print(f'avg temperature was {avgTemperatureThisRun}')
print(f'the temperature is between {min(temperature_list)} and {max(temperature_list)}')
print(f'deviation is {temperatureDeviation}')
normalized_temperature_list = [(x - min(temperature_list)) / (max(temperature_list) - min(temperature_list)) for x in
                               temperature_list]
plt.scatter(x=list(range(0, generation_counter.get() + 1)), y=normalized_temperature_list)
plt.title('normalized temperature')
plt.show()

# Pollution Data
print(f'polluted cells {pollution_counter} and pollution is {round(pollution_counter / N ** 2, ndigits=3) * 100}%')
avgPollutionThisRun = round(sum(pollution_list) / len(pollution_list), ndigits=3)
pollutionDeviation = round(statistics.stdev(pollution_list), ndigits=3)
print(f'avg pollution was {avgPollutionThisRun}')
print(f'the pollution percentage is between {min(pollution_list)} and {max(pollution_list)}')
print(f'deviation is {pollutionDeviation}')
normalized_pollution_list = []
try:
    normalized_pollution_list = [(x - min(pollution_list)) / (max(pollution_list) - min(pollution_list)) for x in
                                 pollution_list]
except ZeroDivisionError:
    normalized_pollution_list = [x / len(pollution_list) for x in pollution_list]
plt.scatter(x=list(range(0, generation_counter.get() + 1)), y=normalized_pollution_list)
plt.title('normalized pollution')
plt.show()
