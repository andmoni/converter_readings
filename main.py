#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 19.02.2024 г.

@author: Следователь.

Основной модуль для запуска программы конвертера показаний.
"""

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
    main()
    input('Работа программы закончена, спасибо, что воспользовались ей.\n\
        Теперь это окно можно закрыть, для выхода нажмите любую кнопку.')