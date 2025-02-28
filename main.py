#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 19.02.2024 г.

@author: Следователь.

Основной модуль для запуска программы конвертера показаний.
"""
import sys
from PyQt5.QtWidgets import QApplication
from sours.mw_converter import MainWindowConverter

print ('''
Если Вы не хотите видеть это окно консоли, 
запустите программу файлом run.bat в папке с программой.
''')


def main():
    import sys
    app = QApplication(sys.argv)
    main_win = MainWindowConverter()
    main_win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # перехватываем системный вывод для лога
    tmp_std_out = sys.stdout
    # создаем лог-файл для записи системного вывода
    file_log = open("system.log", 'w', encoding='utf-8')
    # записываем системный вывод в файл
    sys.stdout = file_log
    try:
        main()
    except Exception as e:
        print('Ошибка при работе программы: {}'.format(str(e)))
    # возврат вывода в консоль
    sys.stdout = tmp_std_out
    file_log.close()
    input('Работа программы закончена, спасибо, что воспользовались ей.\n\
        Теперь это окно можно закрыть, для выхода нажмите любую кнопку.')