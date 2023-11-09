import math
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

# Функция для отображения результатов на экране
def drawResult(N: list[tuple[float, float]],   # точки внутри оболочки
         V: list[tuple[float, float]],   # точки образующие оболочку
         customTitle="Нахождение выпуклой оболочки",
         scale=6.5):
    fig, ax = plt.subplots() #обЪекты: фигура(рамка) и оси 
    fig.set_size_inches(scale, scale)#задаем размер рамки

    # Нарисуем все точки множества N
    ax.plot([p[0] for p in N], [p[1] for p in N], 'o', color='r', markersize=4, zorder=0)

    # Нарисуем все точки множества V
    ax.plot([p[0] for p in V] + [V[0][0], V[-1][0]],
            [p[1] for p in V] + [V[0][1], V[-1][1]], 'o-', color='b',
            markersize=5, zorder=1)

    # Отобразим окно
    plt.title(customTitle)
    plt.xlabel("Ось X")
    plt.ylabel("Ось Y")
    plt.axis('equal')
    plt.show()


# Возвращает -1, если a < b по det
#             0, если a || b
#             1, если a > b по det
def compareVectorsByDet(a, b): #передаются векторы
    a = (a[1][0] - a[0][0], a[1][1] - a[0][1])
    b = (b[1][0] - b[0][0], b[1][1] - b[0][1])

    det = a[0] * b[1] - a[1] * b[0]

    if det > 0:
        return -1
    elif det == 0:
        return 0
    else:
        return 1


# Возвращает -1, если a < b по длине
#             0, если a == b по длине
#             1, если a > b по длине
def compareVectorsByLength(a, b): #если равны по детерминанту, то сравним по длине
    a = (a[1][0] - a[0][0], a[1][1] - a[0][1])
    b = (b[1][0] - b[0][0], b[1][1] - b[0][1])

    len_a = math.sqrt(a[0] ** 2 + a[1] ** 2)
    len_b = math.sqrt(b[0] ** 2 + b[1] ** 2)

    if len_a < len_b:
        return -1
    elif len_a == len_b:
        return 0
    else:
        return 1


# Возвращает -1, если a < b
#             0, если a == b
#             1, если a > b
def compareVectors(a, b): #обобщение сравнения векторов(сборная двух функций)
    detComp = compareVectorsByDet(a, b)

    if detComp != 0:
        return detComp
    else:
        return compareVectorsByLength(a, b)


def comparePoints(p1, p2): # для поиска самой правой точки
    return compareVectors((t, p1), (t, p2))


# Алгоритм Джарвиса поиска выпуклой оболочки
# Трудоёмкость: O(n*h), где h - число вершин выпуклой оболочки
def Jarvis(N):
    global t
    # Примем за t точку с наименьшей абсциссой
    # (если таких точек несколько, то она будет с минимальной ординатой)
    t = min(N, key=lambda p: (p[0], p[1]))

    # V - множество точек, составляющих выпуклую оболочку (результат работы алгоритма)
    V = [t]
    # v0 - первая точка выпуклой оболочки
    v0 = t
    #удалим эту точку, так как она вошла в оболочку
    N.remove(t)
   

    def makeJarvisStep(t: tuple[float, float]) -> tuple[float, float]: #отдельная вспомогательная функция
        # Найдём точку x такую, что вектор tx наименьший (самый правый )
        x = min(N, key=cmp_to_key(comparePoints))

        # Найдём точку v такую, что вектор tv коллинеарен tx, но наибольшей длины
        # (возможно, останется x)
        v = x

        for p in N:
            # Если tp и tv коллинеарны и tp длиннее tv, то v = p
            if compareVectorsByDet((t, p), (t, v)) == 0 and \
                    compareVectorsByLength((t, p), (t, v)) == 1:
                v = p

        return v

    # Произведём первый шаг алгоритма (поиск новой точки v)
    v = makeJarvisStep(t)
    # Вернём в N точку v0, чтобы алгоритм был конечен(просто для соединения оболочки в конце)
    N.append(v0)

    # Продолжим алгоритм
    while v != v0:
        # Добавим в V найденную на предыдущем шаге точку v
        V.append(v)
        # Удалим её из рассмотрения
        N.remove(v)
        # Обновим t
        t = v
        # Произведём новый шаг алгоритма
        v = makeJarvisStep(t)

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

############################################################################
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

    V = Jarvis(N)
   
    drawResult(N, V, customTitle="Нахождение выпуклой оболочки:\nАлгоритм Джарвиса")
    t_ = [0]
    xaxis = [0]
    for i in range(10, 10**3 + 2, 10):
        xaxis.append(i)
        start = time.perf_counter()*1000000
        N = get_list_of_random_points(i)
        V = Jarvis(N)
        t_.append(time.perf_counter()*1000000 - start)
    plt.title("Время работы алгоритма Джарвиса")
    plt.xlabel("количество точек")
    plt.ylabel("время работы(микросекунды)")
    plt.plot(xaxis, t_, linestyle = '-', color = 'red', label = "Алгоритм Джарвиса")
    plt.legend()  
    plt.show()

main()
