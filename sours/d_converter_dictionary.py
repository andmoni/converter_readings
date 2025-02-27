#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 14 фев. 2024 г.

@author: Следователь (Andmoni@yandex.ru)
@last_editing: 19.02.2025

Окдно диалога вывода и изменения списка слов в словаре автозамены
"""

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QApplication
from sours.UI.d_converter_dictionary import Ui_DialogConverterEditDictionary
from sours.d_converter_edit_words import DialogEditWords
from datetime import datetime

# data/replacement_words.dict

def load_replacement_words(words_file: str = r'data/replacement_words.dict'):
    """Загрузка словаря конвертера с диска"""
    words_dict = {}
    try:
        with open(words_file, encoding='utf-8') as f:
            line_words = f.readlines()
            version = line_words[0].split("::")[1].strip()
            # пропускаем первые две строки файла
            for line_word in line_words[2:]:
                # вдруг пустая строка или
                # в строке нет разделителя - пропускаем
                if "::" not in line_word.strip():
                    continue
                _words = line_word.split("::")
                # добавление данных в словарь с удалением пробельных символов
                words_dict[_words[0].strip()] = [_words[1].strip(),
                                                 _words[2].strip(),
                                                 _words[3].strip(),
                                                 _words[4].strip()]
    except IOError:
        print('Ошибка чтения словаря конвертера из файла: {}'.format(words_file))
        # при невозможности загрузить словарь, берем словарь по умолчанию
        # words_dict = _orig_words_dict
        version = '0'
    return words_dict, version


def save_replacement_words(replacement_words_dict: dict,
                           file_replacement_dictionary: str = r'data/replacement_words.dict') -> int:
    """Сохранение словаря конвертера на диск"""
    version = datetime.today().strftime("%Y%m%d")
    lns = ['{}::{}\n'.format(
        "version".ljust(30),
        version.ljust(30)
    ),
        '{}::{}::{}::{}::{}\n'.format(
        "неопределенная форма".center(30),
        "ед.ч. 1 лицо".center(30),
        "ед.ч. 3 лицо".center(30),
        "мн.ч. 1 лицо".center(30),
        "мн.ч. 3 лицо".center(30)
    ), ]
    keys = list(replacement_words_dict.keys())
    keys.sort()
    for key in keys:
        words = replacement_words_dict.get(key)
        lns.append("{}::{}::{}::{}::{}\n".format(
            key.ljust(30),
            words[0].ljust(30),
            words[1].ljust(30),
            words[2].ljust(30),
            words[3].ljust(30),
        ))
    try:
        with open(file_replacement_dictionary, 'w', encoding='utf-8') as f:
            f.writelines(lns)
            return 1
    except Exception as e:
        print('Какая-то ошибка::{}'.format(e))
        return 0


def convert_dictionary_for_conversion(replacement_words_dict: dict):
    """Преобразование словаря конвертера из 5 элементного в 2"""
    converted_dictionary = {}
    keys = list(replacement_words_dict.keys())
    keys.sort()
    for key in keys:
        words = replacement_words_dict.get(key)
        converted_dictionary[words[0]] = words[1]
        converted_dictionary[words[2]] = words[3]
    return converted_dictionary


class DialogConverterEditDictionary(QDialog, Ui_DialogConverterEditDictionary):
    """Виджет редактирования списка слов"""

    def __init__(self, replacement_words_dict: dict, parent=None):
        """Конструктор окна"""
        print('DialogConverterWordsList.__init__')
        super().__init__(parent)
        self.setupUi(self)

        self.replacement_words_dict = replacement_words_dict
        # отображение
        self.reviewData()
        self._switchSignals()
        # подключение сигналов
        self.tw_replacement_dictionary.currentItemChanged.connect(self._switchSignals)
        
    def _switchSignals(self):
        """Включение-отключение кнопок"""
        self.tbtn_delete.setEnabled(False)
        self.tbtn_edit.setEnabled(False)
        row = self.tw_replacement_dictionary.currentRow()
        if row != -1 and row is not None:
            self.tbtn_edit.setEnabled(True)
            self.tbtn_delete.setEnabled(True)

    def saveWordsDictionary(self):
        """Сохранение слов из таблицы в файл по умолчанию по пути 'data/replacement_words.dict'"""
        print('DialogConverterWordsList.saveWordsDictionary')
        save_replacement_words(self.replacement_words_dict)
        self.accept()

    def reviewData(self, data: dict = None):
        """Обновление данных таблицы"""
        print('DialogConverterWordsList.reviewData')
        if data is None:
            _words_dict = self.replacement_words_dict
            self.l_sum_info.setText(
                'Всего в словаре {} слов для замены. '.format(len(self.replacement_words_dict)) +
                'Отображены все.' if len(
                    self.replacement_words_dict) else 'Словарь пуст. Нечего показывать.'
            )
        else:
            _words_dict = data
            self.l_sum_info.setText(
                'Всего в словаре {} слов для замены. '.format(len(self.replacement_words_dict)) +
                'Отображено {} слов'.format(len(_words_dict)) if len(
                    self.replacement_words_dict) else 'Слов с заданными условиями нет. Нечего показывать.')
        keys = list(_words_dict.keys())
        keys.sort()
        self.tw_replacement_dictionary.clearContents()
        self.tw_replacement_dictionary.setRowCount(0)
        row = 0
        for key in keys:
            self.tw_replacement_dictionary.insertRow(self.tw_replacement_dictionary.rowCount())
            self.tw_replacement_dictionary.setItem(row, 4, QTableWidgetItem(key))
            self.tw_replacement_dictionary.item(row, 4).setTextAlignment(8 | 128)
            self.tw_replacement_dictionary.setItem(row, 0, QTableWidgetItem(_words_dict[key][0]))
            self.tw_replacement_dictionary.item(row, 0).setTextAlignment(8 | 128)
            self.tw_replacement_dictionary.setItem(row, 1, QTableWidgetItem(_words_dict[key][1]))
            self.tw_replacement_dictionary.item(row, 1).setTextAlignment(8 | 128)
            self.tw_replacement_dictionary.setItem(row, 2, QTableWidgetItem(_words_dict[key][2]))
            self.tw_replacement_dictionary.item(row, 2).setTextAlignment(8 | 128)
            self.tw_replacement_dictionary.setItem(row, 3, QTableWidgetItem(_words_dict[key][3]))
            self.tw_replacement_dictionary.item(row, 3).setTextAlignment(8 | 128)
            row += 1
        self.tw_replacement_dictionary.resizeRowsToContents()
        # выбор последнего документа в описи
        self.tw_replacement_dictionary.selectRow(0)

    def addWords(self):
        """Добавление слова в таблицу и список"""
        print('DialogConverterWordsList.addWord')
        wid = DialogEditWords(parent=self)
        result = wid.exec_()
        if result:
            words = wid.getWords()
            self.replacement_words_dict[words[0]] = [words[1], words[2], words[3], words[4]]
            # обновление данных в таблице
            self.reviewData()

    def editWords(self):
        """Изменение слова"""
        print('DialogConverterWordsList.editWords')
        # определение выбранной строки
        row = self.tw_replacement_dictionary.currentRow()
        key = self.tw_replacement_dictionary.item(row, 4).text()
        words = [*self.replacement_words_dict.pop(key)]
        words = [key, words[0],words[1], words[2], words[3]]
        wid = DialogEditWords(words, self)
        res = wid.exec_()
        if res:
            words = wid.getWords()
        self.replacement_words_dict[words[0]] = [words[1], words[2], words[3], words[4]]
        self.reviewData()

    def deleteWords(self) -> None:
        """Удаление слова из таблицы.
        :rtype: None
        """
        print('DialogConverterWordsList.deleteWords')
        row = self.tw_replacement_dictionary.currentRow()
        key = self.tw_replacement_dictionary.item(row, 0).text()
        self.replacement_words_dict.pop(key)
        self.reviewData()

    def filterWords(self):
        """Фильтр-поиск при изменении строки фильтра"""
        print('DialogConverterWordsList.filterWords')
        # текст в поле поиска
        f_key = self.le_filter.text()
        if f_key.strip():
            self.tbtn_clear_filter.setEnabled(True)
            # как вариант кнопку очистки можно скрывать
            f_data = {}
            keys = list(self.replacement_words_dict.keys())
            for key in keys:
                if f_key in self.replacement_words_dict.get(key)[3]:
                    f_data.update({key: self.replacement_words_dict.get(key)})
                if f_key in key:
                    f_data.update({key: self.replacement_words_dict.get(key)})
            # отображение отфильтрованного словаря
            self.reviewData(f_data)
        else:
            self.tbtn_clear_filter.setEnabled(False)
            self.reviewData()


def test():
    """Тестовый пуск"""
    import sys
    app = QApplication(sys.argv)
    rwd = load_replacement_words()
    wid = DialogConverterEditDictionary(rwd[0])
    wid.exec_()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
