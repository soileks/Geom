
from math import sqrt
import random as rand
from functools import cmp_to_key
import time
from matplotlib import pyplot as plt



# Генерирует n псевдослучайных вещественных точек с заданными настройками
def get_list_of_random_points(
        n,
        minX=1.0, minY=1.0,
        maxX=10.0, maxY=10.0) -> list[tuple[float, float]]:    #то есть должен вернуться список кортежей
    points_set = set()  #в множестве объекты неизменяемые, поэтому используются кортежи

    i = 0
    while i < n:
        oldLen = len(points_set)
        points_set.add((rand.uniform(minX, maxX), rand.uniform(minY, maxY))) #добавляем набор из координат точки
        newLen = len(points_set)
        if newLen != oldLen:    #исключаем добавление одинаковых точек(при добавлении в множество одинаковых наборов, оно не меняется)
            i += 1

    return list(points_set)

def drawResult(N, V, title, scale=6.0):  #V - точки оболочки, N - это множество всех точек
    fig, ax = plt.subplots() #обЪекты: фигура(рамка) и оси 
    fig.set_size_inches(scale, scale) #задаем размер рамки
    # Нарисуем все точки множества N
    ax.plot([p[0] for p in N], [p[1] for p in N], "o",
            color="b", markersize=3.5, zorder=0)
    # Нарисуем все точки множества V
    ax.plot([p[0] for p in V] + [V[0][0], V[-1][0]], #для соединения первой и последней точек
            [p[1] for p in V] + [V[0][1], V[-1][1]], "o-",
            color="r", markersize=3.5, zorder=1)
 # Отобразим окно
    plt.title(title)
    plt.xlabel("ось X")
    plt.ylabel("ось Y")
    plt.axis('equal')
    plt.show()


def rotate(p1, p2, p3): #даны 3 точки
    return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0]) #вычисляем det векторов (если положительно, то p3 слева от вектора p2p1, если отрицательно, то справа)


def graham(N): #ищем выпуклую оболочку
    if len(N) <= 2:
        return N

    # t - самая левая нижняя точка
    t = min(N, key=lambda point: (point[0], point[1]))# ищем минимум по координатам
    N.remove(t)#удаляем точку t из множества(она уже точно войдет)

    def compare(p1, p2): # сравнение векторов
        # Координаты вектора v1(из координат точек)
        v1x = p1[0] - t[0]
        v1y = p1[1] - t[1]
        # Координаты вектора v2
        v2x = p2[0] - t[0]
        v2y = p2[1] - t[1]

        # Сравнение по знаку определителя
        det = v1x * v2y - v1y * v2x

        if det > 0:
            # v1 < v2 по определителю
            return -1
        elif det == 0:
            # v1 == v2 по определителю. Сравним векторы по длине
            len_v1 = sqrt(v1x ** 2 + v1y ** 2)
            len_v2 = sqrt(v2x ** 2 + v2y ** 2)

            if len_v1 < len_v2:
                return -1
            elif len_v1 == len_v2:
                return 0
            else:
                return 1
        else:
            # v1 > v2 по определителю
            return 1

    # Отсортируем все точки в N по углу относительно t с помощью compare 
    N.sort(key=cmp_to_key(compare))

    # V - итоговое множество точек выпуклой оболочки - будущий результат алгоритма
    V = [t, N[0]]

    for i in range(1, len(N)):
        p1 = V[-2] #предпоследняя
        p2 = V[-1] #последняя
        p3 = N[i] #текущая

        rot = rotate(p1, p2, p3)

        # p1, p2, p3 на одной прямой - заменим p2 на p3
        if rot == 0:
            V[-1] = p3
        elif rot < 0:
            # Пока p1, p2, p3 образуют правый поворот или прямую - исключаем p2  (кратчайший поворот -  правый)(против часовой стрелки, если смотреть сверху)
            #Если угол между векторами больше чем 180, то векторное произведение положительно -> нужно удалить точку
            while rotate(V[-2], V[-1], p3) <= 0:
                V.pop() #выкидываем неподходящие точки из оболочки(предыдущего уровня)
            V.append(p3)
        else:
            # Левые повороты нас устраивают - просто добавляем p3 к результату (кратчайший поворот - левый)(по часовой стрелке)
            V.append(p3)

    return V


def readF(): #читаем точки из файла
    
    f = open('C:\\Users\\User\\Desktop\\result.txt')
    _size = int(f.readline())
    _set = set()
    for i in range(0, _size, 1):
        
        p = f.readline()
        w = p.split()
        a = float(w[1])    
        b = float(w[3])
        tup=(a, b)
        _set.add(tup)
        

    return list(_set)
    
##############################################################################

def main():

    in1 = int(input("Доступные команды:\n"
                    "1. Случайные точки\n"
                    "2. Ввести точки из файла\n"
                    "Ваш выбор: "))
    if in1 == 1:
        in2 = int(input("Введите число точек: "))
        N = get_list_of_random_points(in2)
    elif in1 == 2:
        N=readF()

    V = graham(N)
   
    drawResult(N, V, title="Нахождение выпуклой оболочки:\nАлгоритм Грехэма")
    t_ = [0]
    xaxis = [0]
    for i in range(10, 10**3 + 2, 10):
        xaxis.append(i)
        start = time.perf_counter()*1000000
        N = get_list_of_random_points(i)
        V = graham(N)
        t_.append(time.perf_counter()*1000000 - start)
    plt.title("Время работы алгоритма Грехэма")
    plt.xlabel("количество точек")
    plt.ylabel("время работы(микросекунды)")
    plt.plot(xaxis, t_, linestyle = '-', color = 'red', label = "Алгоритм Грехэма")
    plt.legend()  
    plt.show()

main()

