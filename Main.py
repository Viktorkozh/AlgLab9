#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import timeit
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


amount_of_dots = 1000  # Количество точек
aod = (amount_of_dots + 1) * 10
worst_time = {}
median_time = {}
graph_stuff = [i for i in range(10, 10010, 10)]
xlabel = "Количество элементов в массиве"
ylabel = "Среднее время выполнения (секунды)"


def bin_search(search_list, value):
    left = -1
    right = len(search_list)
    while left < right - 1:
        mid = (left + right) // 2
        if search_list[mid] < value:
            left = mid
        else:
            right = mid
    return right


def search(search_list, value):
    for index, item in enumerate(search_list):
        if item == value:
            return index
    return -1


def fill_list(num_of_elements):
    a = [random.randint(0, 1000) for _ in range(num_of_elements)]
    return a


def logarithmic_model(x, a, b):
    return a * np.log(x) + b


def lsm(name, time, graph_num, log):
    plt.figure(graph_num).set_figwidth(8)
    plt.title(
        f"Зависимость времени поиска элемента от размера массива\n({name})")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.grid(False)
    
    x_data = np.array(graph_stuff)
    y_data = np.array(list(time.values()))

    if log:
        params, _ = curve_fit(logarithmic_model, x_data, y_data)

        a_fit, b_fit = params
        print(
            f"Коэффициенты уравнения ({name}): a = {a_fit}, b = {b_fit}")

        x_fit = np.linspace(min(x_data), max(x_data), 100)
        y_fit = logarithmic_model(x_fit, *params)

        plt.plot(x_fit, y_fit, "r-", label="Quadratic Fit")
    else:
        A = np.vstack([graph_stuff, np.ones(len(graph_stuff))]).T
        alpha = np.dot(
            (np.dot(np.linalg.inv(np.dot(A.T, A)), A.T)
             ), np.array(list(time.values()))
        )
        plt.plot(graph_stuff, alpha[0] *
                 np.array(list(graph_stuff)) + alpha[1], "r")

        formatted_alpha = [format(a, ".10f") for a in alpha]
        print(
            f"Коэффициенты прямой {name}: a =",
            formatted_alpha[0],
            "b =",
            formatted_alpha[1],
        )
        print(f"Корреляция {name}:", np.corrcoef(
            graph_stuff, list(time.values()))[0, 1])

    plt.scatter(graph_stuff, time.values(), s=5, c="orange")


if __name__ == '__main__':
    for i in range(10, aod, 10):
        a = fill_list(i)
        worst_time[i] = (timeit.timeit(
            lambda: bin_search(a, 10000000), number=100)) / 100

    lsm("Худший случай", worst_time, 1, True)

    for i in range(10, aod, 10):
        a = fill_list(i)
        t = int(random.randint(1, i - 1))
        median_time[i] = timeit.timeit(
            lambda: bin_search(a, a[t]), number=100) / 100

    lsm("Средний случай", median_time, 2, True)

    for i in range(10, aod, 10):
        a = fill_list(i)
        worst_time[i] = (timeit.timeit(
            lambda: search(a, 10000000), number=100)) / 100

    lsm("Худший случай", worst_time, 3, False)

    for i in range(10, aod, 10):
        a = fill_list(i)
        t = int(random.randint(1, i - 1))
        median_time[i] = timeit.timeit(
            lambda: search(a, a[t]), number=100) / 100

    lsm("Средний случай", median_time, 4, False)

    plt.show()
