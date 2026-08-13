# Проведено моделирование системы управления колебаниями трубок кориолисова расходомера.
# Используемая частота дискретизации - 1,0 кГц. С помощью скалярного метода матричных пучков
# получены оценки амплитуды и частоты сигналов с сенсора расходомера.

# Построить графики сигналов с драйвера и сенсора

# Обработать переходные процессы по амплитуде и частоте сигнала с сенсора. С помощью отдельной
# функции получить данные о времени регулирования и перерегулировании по амплитуде и частоте

import pandas as pd # библиотека для работы с таблицами (в том числе с файлами .csv)
import numpy as np # библиотека для математических операций со списками
import matplotlib.pyplot as plt # библиотека для построения
# графиков (https://metanit.com/python/matplotlib/), (https://habr.com/ru/articles/1028868/)


def get_quality_indicators(transient_process, delta, time): # функция, рассчитывающая время регулирования и перерегулирование
    # transient_process - список с элементами, описывающий переходный процесс
    # delta - процент от установившегося значения для расчета границ коридора для времени регулирования
    
    steady_state_value = transient_process[len(transient_process)-1]; # установившееся значение
    max_value = max(transient_process); # максимальное значение
    
    # Границы коридора для расчета времени регулирования
    up = steady_state_value + delta*steady_state_value; # верхняя граница коридора
    down = steady_state_value - delta*steady_state_value; # нижняя граница коридора
    
    # Расчет времени регулирования
    flag = 0; # индикатор того, что величина transient_process вошла в коридор
    # при flag = 0 величина transient_process еще не вошла в коридор
    for i in range(len(transient_process)):
        if (transient_process[i] > down and transient_process[i] < up): # если величина вошла в коридор,
            if(flag==0): # и flag равен 0,
                settling_time = round(time[i],2); # то время регулирования равно текущему значению времени
            flag +=  1; # отсчет итераций, в которые величина transient_process внутри коридора
        # Если величина transient_process вышла из коридора:
        if (((flag != 0) and (transient_process[i] < down)) or (flag != 0) and (transient_process[i] > up)):
            flag = 0; # то flag возвращаем в 0

    # Расчет перерегулирования
    overshoot = round(((max_value - steady_state_value)/steady_state_value)*100,2);
    
    return settling_time, overshoot # settling_time - время регулирования; overshoot - перерегулирование

#------------------------------------------------------------------------------------------------------------------

# Считывание данных из файлов и запись их в списки

Coil_path = '1_Control system\cs_data\Coil.csv'; # путь к файлу_1
Driver_path = '1_Control system\cs_data\Driver.csv'; # путь к файлу_2
est_A_path = '1_Control system\cs_data\est_A.csv'; # путь к файлу_3
est_f_path = '1_Control system\cs_data\est_f.csv'; # путь к файлу_3

Coil_df = pd.read_csv(Coil_path, header=None); # считать данные из csv-файла, расположенного по заданному пути
Driver_df = pd.read_csv(Driver_path, header=None); # считать данные из csv-файла, расположенного по заданному пути
est_A_df = pd.read_csv(est_A_path, header=None); # считать данные из csv-файла, расположенного по заданному пути
est_f_df = pd.read_csv(est_f_path, header=None); # считать данные из csv-файла, расположенного по заданному пути

Coil = Coil_df[0].tolist(); # перенести данные из первого столбца (нумерация с 0) в список под названием Coil
Driver = Driver_df[0].tolist(); # перенести данные из первого столбца (нумерация с 0) в список под названием Driver
est_A = est_A_df[0].tolist(); # перенести данные из первого столбца (нумерация с 0) в список под названием est_A
est_f = est_f_df[0].tolist(); # перенести данные из первого столбца (нумерация с 0) в список под названием est_A

#------------------------------------------------------------------------------------------------------------------

# Временной диапазон для построения графиков
t0 = 0; # начало записи
dt = 1e-3; # период дискретизации
t_stop = dt*len(Coil); # окончание записи

window_size = 50; # длина блочного окна метода матричных пучков
dt_est = dt*window_size; # период обновления оценок

t = np.arange(t0,t_stop,dt); # временной диапазон для наблюдения (range() подходит только для типа int)
t_est = np.arange(t0,t_stop-dt_est,dt_est); # время получения оценок

#------------------------------------------------------------------------------------------------------------------

# Получение показателей качества

delta_A = 0.05; # процент от установившегося значения для расчета границ коридора (5 %)
delta_f = 0.05; # процент от установившегося значения для расчета границ коридора (5 %)

[settling_time_A, overshoot_A] = get_quality_indicators(est_A, delta_A, t_est);
[settling_time_f, overshoot_f] = get_quality_indicators(est_f, delta_f, t_est);

print(f'Амплитуда: время регулирования - {settling_time_A} с, перерегулирование - {overshoot_A} %');
print(f'Частота: время регулирования - {settling_time_f} с, перерегулирование - {overshoot_f} %');

#------------------------------------------------------------------------------------------------------------------

# Построение графиков

# Сигналы с драйвера и сенсора

fig1,ax1 = plt.subplots() # создание фигуры и графика

# Внешний вид линий и label для легенды
ax1.plot(t, Driver, color='green', label='Драйвер')
ax1.plot(t, Coil, color='red', label='Сенсор')

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

#------------------------------------------------------------------------------------------------------------------

# Оценки амплитуды

fig2,ax2 = plt.subplots() # создание фигуры и графика

# Внешний вид линий
ax2.plot(t_est, est_A, marker='o', color='red')

# Заголовок и подписи осей графика
ax2.set_title('Оценки амплитуды', fontsize='14', fontweight='bold')
ax2.set_xlabel('Время, с', fontsize='12')
ax2.set_ylabel('Напряжение, В', fontsize='12')

# Задание сетки на графике
ax2.grid(True, alpha=0.6) # alpha - толщина линий сетки

#------------------------------------------------------------------------------------------------------------------

# Оценки частоты

fig3,ax3 = plt.subplots() # создание фигуры и графика

# Внешний вид линий
ax3.plot(t_est, est_f, marker='o', color='green')

# Заголовок и подписи осей графика
ax3.set_title('Оценки частоты', fontsize='14', fontweight='bold')
ax3.set_xlabel('Время, с', fontsize='12')
ax3.set_ylabel('Частота, Гц', fontsize='12')

# Задание сетки на графике
ax3.grid(True, alpha=0.6) # alpha - толщина линий сетки

# Показать все графики на экране
plt.show()