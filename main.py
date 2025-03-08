#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 19.02.2024 г.

@author: Следователь.

Основной модуль для запуска программы конвертера показаний.
"""
# import ctypes
import sys
import site

from PyQt5.QtCore import QLocale, QTranslator
from PyQt5.QtWidgets import QApplication
from sours.mw_converter import MainWindowConverter

print ('''
Если Вы не хотите видеть это окно консоли, 
запустите программу файлом run.bat в папке с программой.
''')


def main():
    '''
    Главная функция по запуску приложения "Конвертер показаний"
    :return: None
    '''
    # задаем идентификатор приложения (для удобства отладки)
    #myappid = 'mycompany.myproduct.subproduct.version'
    #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # перехватываем системный вывод для лога
    #tmp_std_out = sys.stdout
    # создаем лог-файл для записи системного вывода
    #file_log = open("system.log", 'w', encoding='utf-8')
    # записываем системный вывод в файл
    #sys.stdout = file_log
    # инициализируем приложение
    app = QApplication(sys.argv)
    # задаем локаль программы
    locale = QLocale.system().name()
    # загружаем стандартные переводы для приложения
    translator = QTranslator(app)
    # определяем место хранения библиотек site-packages
    site_pack = site.getsitepackages()
    # загружаем переводы для PyQt5
    translator.load('{}{}qtbase_{}.qm'.format(
        site_pack[1], '\\PyQt5\\Qt5\\translations\\', locale.split('_')[0]))
    # устанавливаем загруженный переводы для приложения во всю программу
    app.installTranslator(translator)
    # запускаем главное окно приложения и показываем его
    main_win = MainWindowConverter()
    main_win.show()
    # возврат вывода в консоль
    #sys.stdout = tmp_std_out
    #file_log.close()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    input('Работа программы закончена, спасибо, что воспользовались ей.\n\
        Теперь это окно можно закрыть, для выхода нажмите любую кнопку.')
