#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 14 фев. 2024 г.

@author: Следователь (Andmoni@yandex.ru)
@last_editing: 19.02.2025

Окно диалога редактирования слов из словаря для конвертера показаний
"""

from PyQt5.QtWidgets import QDialog, QMessageBox
from sours.UI.d_converter_edit_words import Ui_DialogConverterEditWords


class DialogEditWords(QDialog, Ui_DialogConverterEditWords):
    """Диалоговое окно добавления(изменения) слов в списках слов."""

    def __init__(self, words=None, parent=None):
        """Конструктор"""
        super().__init__(parent)
        self.setupUi(self)
        if words:
            self.setWindowTitle('Изменение слова в словаре.')
            # Расстановка значений по полям
            self.le_indefinite.setText(words[0])
            self.le_f_person.setText(words[1])
            self.le_t_person.setText(words[2])
            self.le_f_persons.setText(words[3])
            self.le_t_persons.setText(words[4])
        else:
            self.setWindowTitle('Добавление слова в словарь.')

    def saveWords(self):
        """Сохранение слова"""
        # убираем пробельные символы из слов
        self.le_indefinite.setText(self.le_indefinite.text().strip())
        self.le_f_person.setText(self.le_f_person.text().strip())
        self.le_t_person.setText(self.le_t_person.text().strip())
        self.le_f_persons.setText(self.le_f_persons.text().strip())
        self.le_t_persons.setText(self.le_t_persons.text().strip())
        # TODO!: добавить убирание знаков препинания (, . ; : и т.п.)

        # проверка на введение слов в поля
        if not self.le_indefinite.text() and not self.le_f_person.text(
            ) and not self.le_t_person.text() and not self.le_f_persons.text(
            ) and not self.le_f_persons.text():
            QMessageBox.information(
                self, "Внимание",
                'Вы не ввели слова.')
            return
        if not self.le_indefinite.text():
            QMessageBox.information(
                self, "Внимание",
                'Вы не ввели слово от первого лица в единственном числе.')
            return
        if not self.le_f_person.text():
            QMessageBox.information(
                self, "Внимание",
                'Вы не ввели слово от первого лица в единственном числе.')
            return
        if not self.le_t_person.text():
            QMessageBox.information(
                self, "Внимание",
                'Вы не ввели слово от третьего лица в единственном числе.')
            return
        if not self.le_f_persons.text():
            QMessageBox.information(
                self, "Внимание",
                'Вы не ввели слово от первого лица в множественном числе.')
            return
        if not self.le_t_persons.text():
            QMessageBox.information(
                self, "Внимание",
                'Вы не ввели слово от третьего лица в множественном числе.')
            return
        # проверить начинается ли слова с цифры
        if self.le_f_person.text()[0].isdigit():
            # выдать предупреждение, что слово не может начинаться на букву или
            # содержать букву
            QMessageBox.information(
                self, "Внимание",
                'Слово от первого лица не может начинаться на цифру.')
            return
        if self.le_t_person.text()[0].isdigit():
            # выдать предупреждение, что слово не может начинаться на букву или
            # содержать букву
            QMessageBox.information(
                self, "Внимание",
                'Слово от третьего лица не может начинаться на цифру.')
            return
        # сделать слова с маленькими буквами
        self.le_indefinite.setText(self.le_indefinite.text().lower())
        self.le_f_person.setText(self.le_f_person.text().lower())
        self.le_t_person.setText(self.le_t_person.text().lower())
        self.le_f_persons.setText(self.le_f_persons.text().lower())
        self.le_t_persons.setText(self.le_t_persons.text().lower())
        self.accept()

    def getWords(self):
        """Возвращает список из слов: глагол - 1 лицо - 3 лицо"""
        # print ((self.f_person_word.text(), self.t_person_word.text()))
        return [self.le_indefinite.text(),
                self.le_f_person.text(),
                self.le_t_person.text(),
                self.le_f_persons.text(),
                self.le_t_persons.text()]


def test():
    '''
    Тестирование диалогового окна редактирования слов в словаре.
    :return:
    '''
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    wid = DialogEditWords(['a', 'b', 'c', 'd', 'f'])
    wid.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
