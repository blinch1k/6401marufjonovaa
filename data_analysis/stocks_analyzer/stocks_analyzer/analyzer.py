import numpy as np
import pandas as pd
import datetime
from scipy.signal import argrelextrema
from pandas import DataFrame
from typing import Callable

class Analyzer:
	'''
	Класс анализатора данных. Содержит обрабатываемую таблицу и методы для ее обработки
	
	Публичные поля:
		data - таблица с данными, которые необходимо проанализировать.
				В процессе вычислений к ней добавляются обработанные значения
		size - количетсво индексо этой таблицы
	'''
	
	def __init__(self, data : DataFrame):
		'''
		Инициализация класса. Передается таблица, которая будет исследоваться

		Входные параметры:
			data - таблица, над которой производятся все вычисления
		'''

		self.data = data
		self.size = data.shape[0]

	def __str_to_list(func : Callable[[str | list, int], np.ndarray | dict | list]) -> Callable[[list, int], np.ndarray | dict | list]:
		'''
		Декоратор для замены преобразования строки с названиями столбцов в список

		Входные параметры:
			func - функция, в которую в качестве первого аргумента передается строка или список названий столбцов

		Возвращаемое значение:
			func - та же функция, но с преобразованием строки в список в качестве первого аргумента, если он является строкой
		'''

		def wrapper(*args):
			if isinstance(args[1], str):
				cols = args[1].split(',')
				
				return func(args[0], cols, args[2])
			else: 
				return func(*args)
		
		return wrapper
	
	def __add_result(self, name : str, columns : list, data : np.ndarray) -> None:
		'''
		Функция записи промежуточных результатов в таблицу

		Входные параметры:
			name - название операции для обработки данных
			columns - название столбца с данными, которые были обработаны 
			data - обработанные данные
		'''

		for i in range(len(columns)):
			self.data[name + ' ' + columns[i]] = data[i]
		
		return

	@__str_to_list
	def SMA(self, columns : list | str, n : int) -> np.ndarray:
		'''
		Функция вычисления арифметического скользящего среднего (SMA) временного ряда 
		
		Входные параметры:
			columns - список столбцов, по которым проводится вычисление SMA
			n - число предыдущих значений, используемых для вычисления SMA 

		Возвращаемое значение: 
			sma - массив со скользящими средними для каждого указанного столбца
		'''
		
		sma = np.zeros((len(columns), self.size))

		for i in range(len(columns)):
			for j in range(self.size):
				start_index = j - n if j - n > 0 else 0
				sma[i][j] = np.average((self.data[columns[i]].array)[start_index : j + 1])
				
		self.__add_result("SMA", columns, sma)

		return sma

	@__str_to_list
	def diff(self, columns: list | str, n : int = 20) -> np.ndarray:
		'''
		Функция вычисления дифференциала временного ряда по скользящему среднему

		Входные параметры:
			columns - список столбцов, по которым вычисляется дифференциал 
			n - количество элементов для вычисления скользящего среднего

		Возвращаемое значение:
			diffs - массив дифференциалов для каждого столбца
		'''

		data_array = self.SMA(columns, n)
			
		diffs = np.zeros((len(columns), self.size))

		ht = self.data.index[1:] - self.data.index[:self.size - 1]

		for i in range(len(columns)):
			diffs[i][1:] = (data_array[i][1:] - data_array[i][:self.size - 1]) / ht.total_seconds()
			
		self.__add_result("DIFF", columns, diffs)

		return diffs

	@__str_to_list
	def ACF(self, columns : str | list, n : int = 20) -> np.ndarray:
		'''
		Функция поиска автокорреляции для указанных столбцов

		Входные параметры:
			columns - столбцы, для которых ищется автокорреляция
			n - количество элементов для вычисления скользящего среднего

		Возвращаемое значение:
			acf - список с автокорреляциями различных лагов для каждого столбца
		'''

		data_array = self.SMA(columns, n)

		acf = np.zeros((len(columns), self.size))

		for i in range(len(columns)):
			for t in range(self.size - 1):
				y = np.roll(data_array[i], t)

				x_avg = np.average(data_array[i][t:])
				y_avg = np.average(y[t:])
				xy_avg = np.average(data_array[i][t:] * y[t:])

				x_s = np.std(data_array[i][t:])
				y_s = np.std(y[t:])

				if x_s * y_s != 0:
					acf[i][t] = (xy_avg - x_avg * y_avg) / (x_s * y_s)

		self.__add_result("ACF", columns, acf)
		
		return acf

	def extreme_points(self, columns : str | list, n : int = 20) -> dict:
		'''
		Функция поиска экстремумов для указанных столбцов

		Входные параметры:
			columns - столбцы, по которым ищутся точки экстремума
			n - количество элементов для вычисления скользящего среднего

		Возвращаемое значение:
			extreme_points - словарь из двух списков, содержащий индексы локальных минимумов и максимумов
		'''

		extreme_points = {'max': self.max_points(columns, n), 'min': self.min_points(columns, n)}
		
		return extreme_points

	@__str_to_list
	def max_points(self, columns : str | list, n : int = 20) -> list:
		'''
		Функция поиска инденксов локальных максимумов для указанных столбцов

		Входные параметры:
			columns - столбцы, по которым ищутся точки минимума
			n - количество элементов для вычисления скользящего среднего

		Возвращаемое значние:
			maxs - список с индексами локальных максимумов для каждого столбца
		'''
		
		data_array = self.SMA(columns, n)

		g = (data_array[i][maxs[i]] for i in range(len(columns)))
		
		maxs = []
		data = np.full((len(columns), self.size), np.nan)
		
		for i in range(len(columns)):
			maxs.append(argrelextrema(data_array[i], np.greater)[0])

			data[i][maxs[i]] = next(g)

		self.__add_result("MAX", columns, data)
		
		return maxs

	@__str_to_list
	def min_points(self, columns : str | list, n : int = 20) -> list:
		'''
		Функция поиска индексов локальных минимумов для указанных столбцов
		
		Входные параметры:
			columns - столбцы, по которым ищутся точки минимума
			n - количество элементов для вычисления скользящего среднего

		Возвращаемое значение:
			mins - список с индексами локальных минимумов для каждого столбца
		'''
		
		data_array = self.SMA(columns, n)

		mins = []
		data = np.full((len(columns), self.size), np.nan)
		
		for i in range(len(columns)):
			mins.append(argrelextrema(data_array[i], np.less)[0])

			data[i][mins[i]] = data_array[i][mins[i]]

		self.__add_result("MIN", columns, data)
		
		return mins

	def save_data_frame(self, file_name : str) -> None:
		'''
		Функция сохранения таблицы в файл с указанным именем

		Входные параметры:
			file_name - название файла, в который сохраняется таблица
		'''
		
		self.data.to_excel(file_name)
		
		return