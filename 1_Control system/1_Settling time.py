# Работа с csv-файлами. Чтение данных из файла и обработка этих данных

import pandas as pd # библиотека для работы с таблицами (в том числе с файлами .csv)
import numpy as np # библиотека для математических операций со списками
import matplotlib.pyplot as plt # библиотека для построения
# графиков (https://metanit.com/python/matplotlib/), (https://habr.com/ru/articles/1028868/)

file_path1 = '1_Control system\cs_data\Coil.csv'; # путь к файлу_1
file_path2 = '1_Control system\cs_data\Driver.csv'; # путь к файлу_2
file_path3 = '1_Control system\cs_data\est_A.csv'; # путь к файлу_3

Coil_df = pd.read_csv(file_path1, header=None); # считать данные из csv-файла, расположенного по заданному пути
Driver_df = pd.read_csv(file_path2, header=None); # считать данные из csv-файла, расположенного по заданному пути
est_A_df = pd.read_csv(file_path3, header=None); # считать данные из csv-файла, расположенного по заданному пути

Coil = Coil_df[0].tolist(); # перенести данные из первого столбца (нумерация с 0) в список под названием Coil
Driver = Driver_df[0].tolist(); # перенести данные из первого столбца (нумерация с 0) в список под названием Driver
est_A = est_A_df[0].tolist(); # перенести данные из первого столбца (нумерация с 0) в список под названием est_A

# Временной диапазон для построения графиков
t0 = 0; # начало записи
dt = 1e-3; # период дискретизации
t_stop = dt*len(Coil);

window_size = 50; # длина блочного окна метода матричных пучков
dt_est = dt*window_size; # период обновления оценок

t = np.arange(t0,t_stop,dt); # временной диапазон для наблюдения (range() подходит только для типа int)
t_est = np.arange(t0,t_stop-dt_est,dt_est);

# Построение графиков

fig1,ax1 = plt.subplots() # создание фигуры и графика

# Внешний вид линий и label для легенды
ax1.plot(t, Coil, color='red', label='Сенсор')
ax1.plot(t, Driver, color='green', label='Драйвер')

# Заголовок и подписи осей графика
ax1.set_title('Сигналы с расходомера', fontsize='14', fontweight='bold')
ax1.set_xlabel('Время, с', fontsize='12')
ax1.set_ylabel('Напряжение, В', fontsize='12')

# Задание сетки на графике
ax1.grid(True, alpha=0.6) # alpha - толщина линий сетки

# Задание пределов видимости осей на графике
ax1.set_xlim([0,t_stop]);

# Задание легенды
ax1.legend()

fig2,ax2 = plt.subplots() # создание фигуры и графика

# Внешний вид линий и label для легенды
ax2.plot(t_est, est_A, marker='o', color='red')

# Заголовок и подписи осей графика
ax2.set_title('Оценки амплитуды', fontsize='14', fontweight='bold')
ax2.set_xlabel('Время, с', fontsize='12')
ax2.set_ylabel('Напряжение, В', fontsize='12')

# Задание сетки на графике
ax2.grid(True, alpha=0.6) # alpha - толщина линий сетки

# Показать все графики на экране
plt.show()