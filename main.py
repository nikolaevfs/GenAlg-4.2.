# Начальная популяция - жадный выбор, начиная со случайного груза
# Отбор особей для скрещивания - выбрать только 20% самых приспособленных особей
# Скрещивание (кроссинговер) между выбранными особями - многоточечный с 3мя точками
# Мутация - случайное изменение 3х битов у 5% особей
# Формирование новой популяции - «штраф» за «старость» -10% функции приспособленности, выбор лучших

from random import randint
import copy
import random


# Определяет стоимость набора
def countValue(individual, data):
    weight, volume, price = 0, 0, 0
    for i in range(len(individual)):
        weight += int(data[i][0]) * individual[i]
        volume += float(data[i][1]) * individual[i]
        price += int(data[i][2]) * individual[i]
    if weight > maxWeight or volume > maxVolume:
        return 0
    return price


# Генерируем начальную популяцию
def generatePopulation(numberOfCargo, numberOfIndividuals, data):
    population = []
    for i in range(numberOfIndividuals):
        individual = []
        startWith = randint(0, numberOfCargo - 1)

        for _ in range(startWith):
            individual.append(0)
        individual.append(1)

        for _ in range(numberOfCargo - startWith - 1):
            tryIndividual = copy.deepcopy(individual)
            tryIndividual.append(1)
            if countValue(tryIndividual, data) != 0:
                individual.append(1)
            else:
                for _ in range(numberOfCargo - len(individual)):
                    individual.append(0)
                break
        population.append(individual)
    return population


# Выбор лучших 20%
def selection(myPopulation, data):
    valueOfPopulation = []
    for i in range(len(myPopulation)):
        individualList = []
        individualList.append(countValue(myPopulation[i], data))
        individualList.append(myPopulation[i])
        valueOfPopulation.append(individualList)
    valueOfPopulation.sort(reverse=True)

    numberOfSelected = len(myPopulation) // 5
    selected = []
    for i in range(numberOfSelected):
        selected.append(valueOfPopulation[i][1])

    return selected


# Получает двух новых особей на основе двух родительских
def findChildren(parent1, parent2):
    point1 = random.randint(0, len(parent1) // 3)
    point2 = random.randint(point1, len(parent1) // 3 * 2)
    point3 = random.randint(point2, len(parent1))

    child1 = parent1[0:point1] + parent2[point1:point2] + parent1[point2:point3] + parent2[point3:]
    child2 = parent2[0:point1] + parent1[point1:point2] + parent2[point2:point3] + parent1[point3:]

    return child1, child2


# Скрещивание
def crossing(selectedIndividuals, data):
    parents = sorted(selectedIndividuals, key=lambda *args: random.random())
    numberOfPairs = len(selectedIndividuals) // 2
    crossed = []
    for pairNum in range(numberOfPairs):
        child1, child2 = findChildren(parents[pairNum * 2], parents[pairNum * 2 + 1])

        if countValue(child1, data) != 0:
            crossed.append(child1)
        else:
            crossed.append(parents[pairNum * 2])

        if countValue(child2, data) != 0:
            crossed.append(child2)
        else:
            crossed.append(parents[pairNum * 2 + 1])

    return crossed


# Мутация
def mutating(crossedIndividuals, data, numberOfCargo):
    mutatedIndex = []
    numberOfMutations = len(crossedIndividuals) // 20
    for mutatingNum in range(numberOfMutations):
        tryIndex = random.randint(0, len(crossedIndividuals))
        while tryIndex in mutatedIndex:
            tryIndex = random.randint(0, len(crossedIndividuals))
        mutatedIndex.append(tryIndex)

        bitsIndex = []
        while len(bitsIndex) != 3:
            tryIndex = random.randint(0, numberOfCargo - 1)
            if tryIndex in bitsIndex:
                continue
            else:
                bitsIndex.append(tryIndex)

        # print(crossedIndividuals[tryIndex])
        for i in range(len(bitsIndex)):
            crossedIndividuals[tryIndex][bitsIndex[i]] ^= 1

    return crossedIndividuals


def makeNewPopulation(myPopulation, data, mutatedIndividuals):
    valueOfPopulation = []
    for i in range(len(myPopulation)):
        individualList = []
        individualList.append(int(countValue(myPopulation[i], data) * 0.9))
        individualList.append(myPopulation[i])
        valueOfPopulation.append(individualList)

    for i in range(len(mutatedIndividuals)):
        individualMutatedList = []
        individualMutatedList.append(countValue(mutatedIndividuals[i], data))
        individualMutatedList.append(mutatedIndividuals[i])
        valueOfPopulation.append(individualMutatedList)

    valueOfPopulation.sort(reverse=True)

    while numberOfIndividuals < len(valueOfPopulation):
        valueOfPopulation.pop(numberOfIndividuals)

    return valueOfPopulation


def genAlg(myPopulation, data, lowestCost, circles):
    circles += 1
    forMaxVal = copy.deepcopy(myPopulation)

    valueOfPopulation = []
    for i in range(len(forMaxVal)):
        individualMutatedList = []
        individualMutatedList.append(countValue(forMaxVal[i], data))
        individualMutatedList.append(forMaxVal[i])
        valueOfPopulation.append(individualMutatedList)
    valueOfPopulation.sort(reverse=True)

    maxVal = valueOfPopulation[0][0]

    while circles <= 500:
        # Отбор особей
        selectedIndividuals = selection(myPopulation, data)

        # Скрещивание
        crossedIndividuals = crossing(selectedIndividuals, data)

        # Мутация
        mutatedIndividuals = mutating(crossedIndividuals, data, numberOfCargo)

        # Новая популяция
        newPopulation = makeNewPopulation(myPopulation, data, mutatedIndividuals)

        if abs(maxVal - newPopulation[0][0]) < lowestCost and circles > 100:
            return newPopulation
        maxVal = newPopulation[0][0]
        circles += 1

    return newPopulation


numberOfIndividuals = 200
file = open('20.txt')

line = file.readline()
restrictions = line.split()
maxWeight = int(restrictions[0])
maxVolume = int(restrictions[1])

data = []
line = file.readline()
numberOfCargo = 0
lowestCost = -1
while line:
    data.append(line.split())
    line = file.readline()
    numberOfCargo += 1

for i in range(numberOfCargo):
    price = int(data[i][2])
    if lowestCost == -1 or price < lowestCost:
        lowestCost = price
file.close()

# Генерируем популяцию
myPopulation = generatePopulation(numberOfCargo, numberOfIndividuals, data)

finalPopulation = genAlg(myPopulation, data, lowestCost, 0)

weight, volume = 0, 0

for i in range(numberOfCargo):
    weight += int(data[i][0]) * finalPopulation[0][1][i]
    volume += float(data[i][1]) * finalPopulation[0][1][i]

f = open('result.txt', 'w')
f.write("Value: " + str(finalPopulation[0][0]) + '\n')
f.write("Weight: " + str(weight) + '\n')
f.write("Volume: " + str(volume) + '\n')

print("Value: " + str(finalPopulation[0][0]))
print("Weight: " + str(weight))
print("Volume: " + str(volume))
f.close()
