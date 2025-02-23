#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 16 фев. 2025 г.

@author: Следователь (Andmoni@yandex.ru)
@last_editing: 19.02.2025

Диалог для изменения настроек программы (всех).
Настройки модулей добавляются в QTabWidget в виде вкладок.
TODO: сменить вкладки на список групп настроек слева
"""
import pickle
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from sours.UI.d_setting_app import Ui_DialogSettingAll
from sours.d_converter_dictionary import load_replacement_words
from sours.w_converter_setting import TabSettingConverterText, setting_converter

# настройки программы по умолчанию
SETTING_ORIG = {
    'setting_app': {
        'lang':1,
        'interface':0
    },
}
SETTING_ORIG.update(setting_converter)


def load_setting(setting_file: str = r'data/app.set'):
    """Загрузка настроек с диска"""
    try:
        with open(setting_file, 'rb') as f:
            setting = pickle.load(f)
        print('Настройки программы успешно загружены с диска')
        return setting
    except Exception as e:
        print('Ошибка загрузки настроек программы: {}'.format(e))
        print('Настройки программы на диске не обнаружены.\nИспользованы настройки по умолчанию.')
        return SETTING_ORIG


def write_setting(setting: dict, file_for_setting: str = r'data/app.set') -> int:
    """Сохранение настроек на диск"""
    try:
        with open(file_for_setting, 'wb') as f:
            pickle.dump(setting, f)
        print('Настройки программы успешно сохранены на диск')
        return 1
    except Exception as e:
        print('Ошибка сохранения настроек программы: {}'.format(e))
        return 0


class DialogSettingApp(QDialog, Ui_DialogSettingAll):
    """
    окно настроек программы (по каждому модулю своя вкладка)
    """

    def __init__(self,
                 all_setting: dict,
                 replacement_words_dict: list,
                 parent=None):
        """
        Конструктор сласса.
        :param all_setting: словарь всех настроек
        :param replacement_words_dict: список замены слов из словаря и версии
        """
        super().__init__(parent)
        self.setupUi(self)
        self.all_setting = all_setting
        self.replacement_words_dict = replacement_words_dict
        # добавление вкладок настроек
        self.w_sett_converter = TabSettingConverterText(
            all_setting, replacement_words_dict, parent=self)
        self.tabWidget.addTab(self.w_sett_converter, "Конвертер текста")
        self.setSetting(all_setting)

    def setSetting(self, setting):
        '''Установка значений настроек'''
        self.cmb_language.disconnect()
        for key, value in setting.items():
            if key == 'setting_app':
                self.cmb_language.setCurrentIndex(value.get('lang'))
                self.cmb_interface.setCurrentIndex(value.get('interface'))
        self.cmb_language.currentIndexChanged.connect(self.changeLanguage)

    def resetSetting(self):
        '''Сброс настроек'''
        self.setSetting(SETTING_ORIG)

    def changeLanguage(self):
        '''Изменение языка'''
        print('changeLanguage')
        self.cmb_language.disconnect()
        if self.cmb_language.currentIndex() == 0:
            QMessageBox.information(
                self, "Оно тебе надо?",'Работай на русском языке.')
        self.cmb_language.setCurrentIndex(1)
        self.cmb_language.currentIndexChanged.connect(self.changeLanguage)

    def saveSetting(self):
        '''Сохранение настроек'''
        self.updateSetting()
        write_setting(self.all_setting, 'data/app.set')
        self.accept()

    def updateSetting(self):
        '''Обновление настроек'''
        self.all_setting['setting_app']['lang'] = self.cmb_language.currentIndex()
        self.all_setting['setting_app']['interface'] = self.cmb_interface.currentIndex()
        self.w_sett_converter.updateSetting()


def test():
    import sys
    app = QApplication(sys.argv)
    saa = load_setting()
    rwd = load_replacement_words()[0]
    wid = DialogSettingApp(saa, rwd)
    wid.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
