#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 16 фев. 2025 г.

@author: Следователь (Andmoni@yandex.ru)
@last_editing: 19.02.2025

Виджет для изменения настроек программы конвертера.
(используется как вкладка в общем окне настроек)
"""

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QFont

from sours.UI.t_converter_setting import Ui_TabSettingConverterText
from sours.d_converter_dictionary import DialogConverterEditDictionary

setting_converter = {
    # настройки конвертера
    'setting_converter': {
        'fix_font':False,
        'font_size': '12',
        'font_name': 'Times New Roman',
        'convert_date': False,
        'remove_breaks': False,
        'remove_double_space': False,
        'add_space_symbol': False,
        'remove_space_symbol': False,
        'remove_tabs': False,
        'add_before_text': False,
        'phrase_before': ' о том, что ',
        'add_after_text': False,
        'phrase_after': "(Том № ___ л.д. ___ - ___)",
        'copy_to_clipboard': False,
        'sys_dict_file': 'data/system_words.dic',
        'user_dict_file': 'data/user_words.dic',
    },
}


def editingReplacementWords(replacement_words_dict):
    '''Изменение замены слов'''
    wid = DialogConverterEditDictionary(replacement_words_dict[0])
    res = wid.exec_()
    if res:
        print('словарь обновлен пользователем')

class TabSettingConverterText(QWidget, Ui_TabSettingConverterText):
    """Виджет для настроек конвертера текста"""

    def __init__(self,
                 setting: dict,
                 replacement_words_dict: list,
                 parent = None):
        """Конструктор виджета"""
        print('TabSettingConverterText.__init__')
        super().__init__(parent)
        self.setupUi(self)
        # словарь замены для конвертера
        self.replacement_words_dict = replacement_words_dict
        # настройки (по умолчанию все отключено и пусто)
        setting = setting_converter if setting is None else setting
        self.setting = setting.get('setting_converter')
        self.setSetting()
        self.chb_convert_date.setEnabled(False)

    def _switchElements(self):
        """Переключение работы элементов выбора имени шрифта и размера"""
        ff = self.chb_fix_font.isChecked()
        self.l_font_name.setEnabled(ff)
        self.fcb_font_name.setEnabled(ff)
        self.l_font_size.setEnabled(ff)
        self.cmb_font_size.setEnabled(ff)
        self.lne_phrase_before.setEnabled(self.chb_add_before_text.isChecked())
        self.lne_phrase_after.setEnabled(self.chb_add_after_text.isChecked())

    def setSetting(self):
        """Установка настроек в окно."""
        print('TabSettingConverterText.setSetting')
        self.chb_fix_font.setChecked(self.setting.get('fix_font'))
        self.cmb_font_size.setCurrentText(self.setting.get('font_size'))
        self.fcb_font_name.setCurrentFont(QFont(self.setting.get('font_name')))
        self.chb_convert_date.setChecked(self.setting.get('convert_date'))
        self.chb_rm_breaks.setChecked(self.setting.get('remove_breaks'))
        self.chb_rm_double_space.setChecked(self.setting.get('remove_double_space'))
        self.chb_add_space_after_mark.setChecked(self.setting.get('add_space_symbol'))
        self.chb_rm_space_before_mark.setChecked(self.setting.get('remove_space_symbol'))
        self.chb_rm_tabs.setChecked(self.setting.get('remove_tabs'))
        self.chb_add_before_text.setChecked(self.setting.get('add_before_text'))
        self.lne_phrase_before.setText(self.setting.get('phrase_before'))
        self.chb_add_after_text.setChecked(self.setting.get('add_after_text'))
        self.lne_phrase_after.setText(self.setting.get('phrase_after'))
        self.chb_copy_to_clipboard.setChecked(self.setting.get('copy_to_clipboard'))

    def updateSetting(self):
        """Получение настроек из окна."""
        print('TabSettingConverterText.updateSetting')
        self.setting.update({
            'fix_font':self.chb_fix_font.isChecked(),
            'font_size': self.cmb_font_size.currentText(),
            'font_name': self.fcb_font_name.currentFont().family(),
            'convert_date': self.chb_convert_date.isChecked(),
            'remove_breaks': self.chb_rm_breaks.isChecked(),
            'remove_double_space': self.chb_rm_double_space.isChecked(),
            'add_space_symbol': self.chb_add_space_after_mark.isChecked(),
            'remove_space_symbol': self.chb_rm_space_before_mark.isChecked(),
            'remove_tabs': self.chb_rm_tabs.isChecked(),
            'add_before_text': self.chb_add_before_text.isChecked(),
            'phrase_before': self.lne_phrase_before.text(),
            'add_after_text': self.chb_add_after_text.isChecked(),
            'phrase_after': self.lne_phrase_after.text(),
            'copy_to_clipboard': self.chb_copy_to_clipboard.isChecked(),
        })

    def getSetting(self):
        """Получение настроек"""
        print('TabSettingConverterText.getSetting')
        self.updateSetting()
        return {'setting_converter': self.setting}

    def resetSetting(self):
        """Сброс настроек в дефолтные."""
        print('TabSettingConverterText.resetSetting')
        self.chb_fix_font.setChecked(False)
        self.cmb_font_size.setCurrentText(12)
        self.fcb_font_name.setFont('Times New Roman')
        self.chb_convert_date.setChecked(False)
        self.chb_rm_breaks.setChecked(False)
        self.chb_rm_double_space.setChecked(False)
        self.chb_add_space_after_mark.setChecked(False)
        self.chb_rm_space_before_mark.setChecked(False)
        self.chb_rm_tabs.setChecked(False)
        self.chb_add_before_text.setChecked(False)
        self.lne_phrase_before.setText(' о том, что ')
        self.chb_add_after_text.setChecked(False)
        self.lne_phrase_after.setText("(Том № ___ л.д. ___ - ___)")
        self.chb_copy_to_clipboard.setChecked(False)

    def editingReplacementWords(self):
        '''Изменение замены слов'''
        print('TabSettingConverterText.editingReplacementWords')
        editingReplacementWords(self.replacement_words_dict)


def test():
    import sys
    app = QApplication(sys.argv)
    wid = TabSettingConverterText(None, {})
    wid.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
