# Файл предназначен для считывания данных о сигналах с системы управления: сигнал с драйвера,
# сигнал с сенсора, оценки амплитуды и оценки частоты. Файл содержит внешнюю функцию, которая
# выполняет расчет времени регулирования и перерегулирования. Время регулирования и
# перерегулирование по амплитуде и частоте выводятся в консоль. Графики в данном файле не
# строятся

import pandas as pd # библиотека для работы с таблицами (в том числе с файлами .csv)
import numpy as np # библиотека для математических операций со списками

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
est_f = est_f_df[0].tolist(); # перенести данные из первого столбца (нумерация с 0) в список под названием est_f

#------------------------------------------------------------------------------------------------------------------

# Временной диапазон наблюдения за сигналами
t0 = 0; # начало записи
dt = 1e-3; # период дискретизации
t_stop = dt*len(Coil); # окончание записи

window_size = 50; # длина блочного окна метода матричных пучков
dt_est = dt*window_size; # период обновления оценок

t_est = np.arange(t0,t_stop-dt_est,dt_est); # время получения оценок

#------------------------------------------------------------------------------------------------------------------

# Получение показателей качества

delta_A = 0.05; # процент от установившегося значения для расчета границ коридора (5 %)
delta_f = 0.05; # процент от установившегося значения для расчета границ коридора (5 %)

[settling_time_A, overshoot_A] = get_quality_indicators(est_A, delta_A, t_est);
[settling_time_f, overshoot_f] = get_quality_indicators(est_f, delta_f, t_est);

print(f'Амплитуда: время регулирования - {settling_time_A} с, перерегулирование - {overshoot_A} %');
print(f'Частота: время регулирования - {settling_time_f} с, перерегулирование - {overshoot_f} %');