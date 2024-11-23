import sys
import numpy as np
import typing as tp

def read_properties(path : str) -> dict[str, str]:
    '''
      Функция для чтения параметров из xml файла.

      Принимаемые параметры:
      path - строка с путём к файлу с параметрами.

      Возвращаемые значения:
      properties - словарь с параметрами из файла.
    '''
    file = open(path, 'r')
    property_lines = file.readlines()
    file.close()
    properties = {}
    for line in property_lines:
        line = line.strip()
        if line.startswith("<") and line.endswith(">"):
            tag_start = line.find("<") + 1
            tag_end = line.find(">")
            tag_name = line[tag_start:tag_end]

            value_start = tag_end + 1
            value_end = line.find("</")
            value = line[value_start:value_end]

            properties[tag_name] = value
    return properties



def func_calculate(x : np.ndarray,a : float,b : float,c : float) -> tp.Iterable[float]:
    '''
      Функция для вычисления результатов

      Принимаемые параметры:
      x - значение для которого вычисляется функция
      a, b, c - параметры функции из варианта.п

      Возвращаемое значение:
      Значение функции для точки x.
    '''
    sin_x = a * np.sin(x)
    cos_x = b * np.cos(x)
    absolute_value = np.abs(sin_x - cos_x)
    y = sin_x + cos_x + absolute_value + c
    return y

def write_results(path: str, arr: tp.Iterable[float]) -> None:
    '''
      Функция для записи резулятатов вычислений в файл.

      Принимаемые параметры:
      path - строка с путём к файлу для записи.
      arr - итератор по множеству результата.
      '''
    file = open(path, 'w')
    for elem in arr:
        file.write(str(elem) + '\n')
    file.close()

def calculate_and_write(n0 : float, h : float, nk : float, a : float, b : float, c : float) -> None:
    '''
       Функция для вычисления результа и записи в файл results.txt.

       Принимаемые значения:
       n0, h, nk, a, b, c - параметры для вычисления значений функции.
    '''
    n = int((nk - n0)/h)
    lst_y = func_calculate(np.arange(n0, nk, h), a, b, c)
    write_results("results.txt", lst_y)

def config_properties() -> tuple[float, ...]:
    '''
    Функция для получения параметров из файла config.xml

    Возвращаемое значение:
    Кортеж из параметров n0, h, nk, a, b, c
    '''
    properties = read_properties("config.xml")
    n0 = float(properties['n0'])
    h = float(properties['h'])
    nk = float(properties['nk'])
    a = float(properties['a'])
    b = float(properties['b'])
    c = float(properties['c'])
    return (n0, h, nk, a, b, c)

def params_properties(params : list[str]) -> tuple[float, ...]:
    '''
        Функция для получения параметров из массива строк.

        Принимаемые значения:
        params - cписок параметров в виде строки.

        Возвращаемое значение:
        Кортеж из параметров n0, h, nk, a, b, c.
    '''
    n0 = float(params[0])
    h = float(params[1])
    nk = float(params[2])
    a = float(params[3])
    b = float(params[4])
    c = float(params[5])
    return (n0, h, nk, a, b, c)

def run_with_config() -> None:
    '''
        Функция для запуска программы с параметрами из файла конфигурации.
    '''
    properties = config_properties()
    calculate_and_write(*properties)

def run_with_params(params : list[str]) -> None:
    '''
       Функция для запуска программы с параметрами из консоли.

       Принимаемые значения:
       params - cписок параметрок в виде строк.
    '''
    properties = params_properties(params)
    print(*properties)
    calculate_and_write(*properties)

# Точка входа в программу
if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_with_config()
    elif len(sys.argv) == 7:
        run_with_params(sys.argv[1:])
