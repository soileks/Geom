import math
import random as rand
from functools import cmp_to_key
from time import time
from matplotlib import pyplot as plt

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
def compareVectorsByDet(a, b):
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


def comparePointsByDet(p1, p2): # 
    return compareVectorsByDet((t, p1), (t, p2))


def comparePoints(p1, p2): # для поиска самой правой точки
    return compareVectors((t, p1), (t, p2))


def rotate(p1, p2, p3) -> float:
    return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])


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
    # Инициализируем veerPoints
    #veerPoints = N.copy()
    #veerPoints.remove(t)

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
    # Вернём в N точку v0, чтобы алгоритм был конечен
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
    
    N=readF()
    t1 = time()
    V = Jarvis(N)
    t2 = time()
    print(f"Алгоритм Джарвиса: t = {t2 - t1}")
    drawResult(N, V, customTitle="Нахождение выпуклой оболочки:\nАлгоритм Джарвиса")


main()
