#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 14 фев. 2024 г .

@author: Следователь (Andmoni@yandex.ru)
@last_editing: 19.02.2025

Модуль изменения показаний в третье лицо.

Ошибки:
если в начале стоит местоимение с маленькой буквы программа его не конвертирует
"""

import uuid, os
from PyQt5.QtGui import QFont, QImage, QTextDocument, QContextMenuEvent
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QDialogButtonBox, QWidget, QMessageBox, QTextEdit, QMenu, QAction, QFrame
)
from PyQt5.QtCore import Qt, QPoint

from sours.UI.w_converter import Ui_WidgetConverterText
from sours.d_converter_dictionary import convert_dictionary_for_conversion
from sours.w_converter_setting import setting_converter

# словари для работы программы
# русский букварь
abc_ru = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ')
# цифры
digits = list('0123456789')

# предлоги для подстановки перед местоимениями и словами
# TODO: сделать доступным из программы для редактирования.
pretexts_l = ['в', 'без', 'до', 'из', 'к', 'на', 'по', 'от', 'перед', 'при', 'через',
            'с', 'у', 'за', 'над', 'об', 'под', 'про', 'для', 'ради', 'сквозь',
            'между', 'из-под', 'из-за', 'по-над', 'по-за', 'вблизи', 'вглубь',
            'вдоль', 'возле', 'около', 'вокруг', 'впереди', 'после', 'в течение',
            'в течении', 'в продолжение', 'в отличи от', 'в заключение', 'в связи с',
            'в целях', 'за счет', 'в виде', 'по причине', 'наподобие', 'вроде',
            'подобно', 'как', 'вследствие', 'в следствии', 'вслед', 'внутри',
            'навстречу', 'посредством', 'в роли', 'в зависимости от', 'путем',
            'насчет', 'по поводу', 'ввиду', 'по случаю', 'вслед за', 'хотя',
            'благодаря', 'несмотря на', 'спустя']
pretexts = []
for pretext in pretexts_l:
    pretexts.append(f' {pretext} ')
    pretexts.append(f'{pretext.capitalize()} ')

# знаки препинания которые могут встречаться в тексте
chars = [
    ' ', '.', ', ', ': ', ';', '!', '?', '(', ')', '-', '–', '»', '«', '"', "'", '“', '‘'
]

# словосочетания с местоимением для мужчины
change_words_men_p = {
    '{}меня{}': '{}него{}',
    # '{}мне{}': '{}ему{}',
    '{}мною{}': '{}ним{}',
}

change_words_men = [
    {' обо мне{}': ' о нём{}', 'Обо мне{}': 'О нём{}',
     ' со мною{}': ' с ним{}', 'Со мною{}': 'С ним{}',
     ' со мной{}': ' с ним{}', 'Со мной{}': 'С ним{}',
     ' ко мне{}': ' к нему{}', 'Ко мне{}': 'К нему{}',
     ' при мне{}': ' при нём{}', 'При мне{}': 'При нём{}',
     ' на мне{}': ' на нём{}', 'На мне{}': 'На нём{}',
     ' в моем{}': ' в его{}', 'В моем{}': 'В его{}',
     ' в моём{}': ' в его{}', 'В моём{}': 'В его{}',
     ' с моих{}': ' с его{}', 'С моих{}': 'С его{}',
     ' у меня{}': ' у него{}', 'У меня{}': 'У него{}',
     },
    {' я{}': ' он{}', 'Я{}': 'Он{}',
     ' меня{}': ' его{}', 'Меня{}': 'Его{}',
     ' мной{}': ' им{}', 'Мной{}': 'Им{}',
     ' мне{}': ' ему{}', 'Мне{}': 'Ему{}',
     ' мои{}': ' его{}', 'Мои{}': 'Его{}',
     ' моих{}': ' его{}', 'Моих{}': 'Его{}',
     ' моё{}': ' его{}', 'Моё{}': 'Его{}',
     ' мое{}': ' его{}', 'Мое{}': 'Его{}',
     # ' мою{}': ' его{}', 'Мою{}': 'Его{}',
     ' мой{}': ' его{}', 'Мой{}': 'Его{}',
     ' моя{}': ' его{}', 'Моя{}': 'Его{}',
     ' моим{}': ' его{}', 'Моим{}': 'Его{}',
     ' моей{}': ' его{}', 'Моей{}': 'Его{}',
     ' моего{}': ' его{}', 'Моего{}': 'Его{}',
     }]

# словосочетания с местоимением для женщины
change_words_women_p = {
    '{}меня{}': '{}неё{}',
    # '{}мне{}': '{}ней{}',
    '{}мною{}': '{}ней{}',  # ('{}нею{}')
    '{}мной{}': '{}ней{}',  # ('{}нею{}')
}

change_words_women = [
    {
        ' обо мне{}': ' о ней{}', 'Обо мне{}': 'О ней{}',
        ' со мною{}': ' с ней{}', 'Со мною{}': 'С ней{}',
        ' со мной{}': ' с ней{}', 'Со мной{}': 'С ней{}',
        ' ко мне{}': ' к ней{}', 'Ко мне{}': 'К ней{}',
        ' при мне{}': ' при ней{}', 'При мне{}': 'При ней{}',
        ' на мне{}': ' на ней{}', 'На мне{}': 'На ней{}',
        ' в моем{}': ' в ее{}', 'В моем{}': 'В ее{}',
        ' в моём{}': ' в ее{}', 'В моём{}': 'В ее{}',
        ' с моих{}': ' с ее{}', 'С моих{}': 'С ее{}',
        ' у меня{}': ' у нее{}', 'У меня{}': 'У нее{}',
    },
    {
        ' я{}': ' она{}', 'Я{}': 'Она{}',
        ' меня{}': ' её{}', 'Меня{}': 'Её{}',
        ' мне{}': ' ей{}', 'Мне{}': 'Ей{}',
        ' мои{}': ' её{}', 'Мои{}': 'Её{}',
        ' моё{}': ' ее{}', 'Моё{}': 'Ее{}',
        ' мое{}': ' ее{}', 'Мое{}': 'Ее{}',
        # ' мою{}': ' ее{}', 'Мою{}': 'Ее{}',
        ' моих{}': ' её{}', 'Моих{}': 'Её{}',
        ' мой{}': ' её{}', 'Мой{}': 'Её{}',
        ' моя{}': ' её{}', 'Моя{}': 'Её{}',
        ' моим{}': ' её{}', 'Моим{}': 'Её{}',
        ' моей{}': ' её{}', 'Моей{}': 'Её{}',
        ' мной{}': ' ей{}', 'Мной{}': 'Ей{}',  # 'Ею{}'
        ' моего{}': ' её{}', 'Моего{}': 'Её{}',
    }]

# словарь для замены в конвертер (не сортируемый)
# TODO: необходима доработка
orig_words_dict = {
    'в нашем': 'в их', 'его': 'того',
    'ее': 'той', 'ей': 'той',
    'ему': 'тому', 'ею': 'тою',
    'её': 'той', 'им': 'тем',
    'ими': 'теми', 'их': 'тех',
    'мною': 'им', 'мы': 'они',
    'нам': 'им', 'нами': 'ими',
    'нас': 'их', 'наш': 'их',
    'наше': 'их', 'нашего': 'их',
    'нашей': 'их', 'нашем': 'их',
    'наши': 'их', 'наших': 'их',
    'нашу': 'их', 'него': 'того',
    'нее': 'той', 'ней': 'той',
    'нему': 'тому', 'нею': 'тою',
    'неё': 'той', 'ним': 'тем',
    'ними': 'теми', 'них': 'тех',
    'о нас': 'о них', 'о ней': 'о той',
    'о них': 'о тех', 'о нём': 'о том',
    'он': 'тот', 'она': 'та',
    'они': 'те', 'оно': 'то',
    'у нас': 'у них'
}

# дополнительные классы, методы и переменные для функционирования текстового поля

IMAGE_EXTENSIONS = ['.jpg','.png','.bmp']
HTML_EXTENSIONS = ['.htm', '.html']


def hexuuid():
    return uuid.uuid4().hex


def splitext(p):
    return os.path.splitext(p)[1].lower()


class TextEdit(QTextEdit):
    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        cursor = self.textCursor()
        document = self.document()
        if source.hasUrls():
            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())
                else:
                    # If we hit a non-image or non-local URL
                    # break the loop and fall out
                    # to the super call & let Qt handle it
                    break
            else:
                # If all were valid images, finish here.
                return
        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return
        super(TextEdit, self).insertFromMimeData(source)

    # Далее контекстное меню и методы для работы с таблицей(надо дорабатывать)
    def context_menus(self, pos):
        """Создание контекстного меню.
        Если курсор на таблице, создается меню для работы с таблицей"""
        # Получаем курсор
        cursor = self.textCursor()
        # Grab the current table, if there is one
        table = cursor.currentTable()
        # Above will return 0 if there is no current table, in which case
        # we call the normal context menu. If there is a table, we create
        # our own context menu specific to table interaction
        if table:
            menu = QMenu(self)
            appendRowAction = QAction("Append row", self)
            appendRowAction.triggered.connect(lambda: table.appendRows(1))
            appendColAction = QAction("Append column", self)
            appendColAction.triggered.connect(lambda: table.appendColumns(1))
            removeRowAction = QAction("Remove row", self)
            removeRowAction.triggered.connect(self.removeRow)
            removeColAction = QAction("Remove column", self)
            removeColAction.triggered.connect(self.removeCol)
            insertRowAction = QAction("Insert row", self)
            insertRowAction.triggered.connect(self.insertRow)
            insertColAction = QAction("Insert column", self)
            insertColAction.triggered.connect(self.insertCol)
            mergeAction = QAction("Merge cells", self)
            mergeAction.triggered.connect(lambda: table.mergeCells(cursor))
            # Only allow merging if there is a selection
            if not cursor.hasSelection():
                mergeAction.setEnabled(False)
            splitAction = QAction("Split cells", self)
            cell = table.cellAt(cursor)
            # Only allow splitting if the current cell is larger
            # than a normal cell
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:
                splitAction.triggered.connect(lambda: table.splitCell(cell.row(), cell.column(), 1, 1))
            else:
                splitAction.setEnabled(False)
            menu.addAction(appendRowAction)
            menu.addAction(appendColAction)
            menu.addSeparator()
            menu.addAction(removeRowAction)
            menu.addAction(removeColAction)
            menu.addSeparator()
            menu.addAction(insertRowAction)
            menu.addAction(insertColAction)
            menu.addSeparator()
            menu.addAction(mergeAction)
            menu.addAction(splitAction)
            # Convert the widget coordinates into global coordinates
            pos = self.mapToGlobal(pos)
            # Add pixels for the tool and formatbars, which are not included
            # in mapToGlobal(), but only if the two are currently visible and
            # not toggled by the user
            #if self.toolbar.isVisible():
            #    pos.setY(pos.y() + 45)
            #if self.formatbar.isVisible():
            #    pos.setY(pos.y() + 45)
            # Move the menu to the new position
            menu.move(pos)
            menu.show()
        else:
            event = QContextMenuEvent(QContextMenuEvent.Mouse, QPoint())
            self.contextMenuEvent(event)

    def removeRow(self):
        # Grab the cursor
        cursor = self.textCursor()
        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()
        # Get the current cell
        cell = table.cellAt(cursor)
        # Delete the cell's row
        table.removeRows(cell.row(), 1)

    def removeCol(self):
        # Grab the cursor
        cursor = self.textCursor()
        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()
        # Get the current cell
        cell = table.cellAt(cursor)
        # Delete the cell's column
        table.removeColumns(cell.column(), 1)

    def insertRow(self):
        # Grab the cursor
        cursor = self.textCursor()
        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()
        # Get the current cell
        cell = table.cellAt(cursor)
        # Insert a new row at the cell's position
        table.insertRows(cell.row(), 1)

    def insertCol(self):
        # Grab the cursor
        cursor = self.textCursor()
        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()
        # Get the current cell
        cell = table.cellAt(cursor)
        # Insert a new row at the cell's position
        table.insertColumns(cell.column(), 1)


class WidgetConverterText(QWidget, Ui_WidgetConverterText):
    """Окно конвертера показаний"""

    def __init__(self, replacement_words: list, setting: dict, parent=None):
        """Конструктор"""
        print('WidgetConverterText.__init__')
        super().__init__(parent)
        self.setupUi(self)
        # создаем текстовое поле для редактора и настраиваем его
        self.te_text_to_convert = TextEdit(self)
        self.te_text_to_convert.setFrameShape(QFrame.Box)
        self.te_text_to_convert.setFrameShadow(QFrame.Plain)
        self.te_text_to_convert.setAcceptRichText(False)
        self.te_text_to_convert.setAutoFormatting(QTextEdit.AutoAll)
        self.te_text_to_convert.setAcceptDrops(True)
        self.te_text_to_convert.setContextMenuPolicy(Qt.CustomContextMenu)
        self.te_text_to_convert.setPlaceholderText('Тут творится магия с показаниями. (вставьте текст показаний)')
        self.te_text_to_convert.customContextMenuRequested.connect(self.te_text_to_convert.context_menus)
        self.te_text_to_convert.textChanged.connect(self.unblocking)
        # Инициализация шрифта по умолчанию.
        font = QFont('Times New Roman', 14)
        self.te_text_to_convert.setFont(font)
        # Необходимо повторно задать размер текста, чтоб не было ошибок.
        self.te_text_to_convert.setFontPointSize(14)
        self.verticalLayout.insertWidget(1, self.te_text_to_convert)
        self.setting = setting.get('setting_converter')
        # локальный буфер обмена
        self.clipboard = QApplication.clipboard()
        self.replacement_words = replacement_words[0]
        version = replacement_words[1]
        self.lbl_status_info.setText('Версия словаря: {}'.format(version))
        self.blocking()

    def setSetting(self, setting):
        """Установка настроек"""
        print('WidgetConverterText.setSetting')
        self.setting = setting

    def _correct_text(self, text):
        """Корректировка текста из окна в соответствии с настройками"""
        print('WidgetConverterText._correct_text')
        # корректировка текста от настроек
        if self.setting.get('convert_date'):
            pass
            # TODO: сделать метод конвертирования даты
        # убираем абзацы, перенос строки и каретки
        if self.setting.get('remove_breaks'):
            text = text.replace('\n', ' ')
            text = text.replace('\r', ' ')
        # и табуляции
        if self.setting.get('remove_tabs'):
            text = text.replace('\t', ' ')
            text = text.replace('\v', ' ')
        # добавляем пробел после символа
        if self.setting.get('add_space_symbol'):
            for i in chars[1:]:
                text = text.replace(i, '{} '.format(i))
        # цикл убирающий двойные пробелы из текста
        if self.setting.get('remove_double_space'):
            while '  ' in text:
                text = text.replace('  ', ' ')
        # убираем пробел перед символом
        if self.setting.get('remove_space_symbol'):
            for i in chars[1:]:
                text = text.replace(' {}'.format(i), i)
        # следующие исправления не требующие настроек:
        # исправляем добавленный пробел после закрывающейся скобки (кавычки)
        # если следом идет знак препинания
        for c in chars[1:]:
            for cc in [')', '"', "'", '»']:
                text = text.replace(
                    '{} {}'.format(cc, c),
                    '{}{}'.format(cc, c))
        # исправляем убранный пробел перед начальной скобкой (кавычкой)
        for c in ['(', '"', "'", '«']:
            for a in abc_ru:
                text = text.replace(
                    '{}{} '.format(a, c),
                    '{} {}'.format(a, c))
                text = text.replace(
                    '{}{} '.format(a.lower(), c),
                    '{} {}'.format(a.lower(), c))
            for a in [')', '"', "'", '»']:
                text = text.replace(
                    '{}{}'.format(a, c),
                    '{} {}'.format(a, c))
            for a in digits:
                text = text.replace(
                    '{}{}'.format(a, c),
                    '{} {}'.format(a, c))
        # исправляем добавленный пробел после некоторых знаков
        for c in ['-', '(', ]:
            text = text.replace('{} '.format(c), '{}'.format(c))
        # Исправляем добавленный пробел в г.р. и др.
        text = text.replace(' г. р.', ' г.р.')
        text = text.replace(' т. к.', ' т.к.')
        text = text.replace(' т. е.', ' т.е.')
        text = text.replace(' т. п.', ' т.п.')
        # цикл убирающий добавленный пробел после точки в записи дат
        for a in digits:
            for b in digits:
                text = text.replace('{}. {}'.format(a, b), '{}.{}'.format(a, b))
        # цикл убирающий добавленный пробел в инициалах
        for a in abc_ru:
            for b in abc_ru:
                text = text.replace('{}. {}.'.format(a.capitalize(), b.capitalize()),
                                    '{}.{}.'.format(a.capitalize(), b.capitalize()))
        # добавление фразы в начало текста
        if self.setting.get('add_before_text'):
            text = text[0].lower() + text[1:]
            text = self.setting['phrase_before'] + text
        # добавление фразы в конец текста
        if self.setting.get('add_after_text'):
            text = text + ' ' + self.setting['phrase_after']
        return text

    def _convert(self, ch, text):
        """Метод отыскивающий словосочетания с символом ch, в тексте и меняющий
         на 3 лицо"""
        print('WidgetConverterText._convert')
        # цикл для общих местоимений и глаголов (системный словарь)
        for words in orig_words_dict.items():
            text = text.replace(' {}{}'.format(words[0], ch),
                                ' {}{}'.format(words[1], ch))
            text = text.replace('{}{}'.format(words[0].capitalize(), ch),
                                '{}{}'.format(words[1].capitalize(), ch))
        dict_words = convert_dictionary_for_conversion(self.replacement_words)
        # цикл для общих местоимений и глаголов (системный словарь)
        for words in dict_words.items():
            text = text.replace(' {}{}'.format(words[0], ch),
                                ' {}{}'.format(words[1], ch))
            text = text.replace('{}{}'.format(words[0].capitalize(), ch),
                                '{}{}'.format(words[1].capitalize(), ch))
        return text

    def correctText(self):
        """Коректировака текста в зависимости от настроек"""
        print('WidgetConverterText.correctText')
        text = self.te_text_to_convert.toPlainText()
        # не работаем если пусто
        if not text:
            return
        text = self._correct_text(text)
        self.te_text_to_convert.setText(text)

    def grammarCheck(self):
        """Проверка грамматики текста"""
        print('WidgetConverterText.grammarCheck')
        # TODO: реализовать грамматический анализатор
        # Получаем текст из поля редактора
        text = self.te_text_to_convert.toPlainText()
        # Вызываем модуль грамматического анализатора и получаем результаты
        # (список ошибок и предупреждений)
        # grammar_errors, grammar_warnings = grammar_analyzer(text)
        # Если есть ошибки или предупреждения, показываем их
        # if grammar_errors or grammar_warnings:
        #     self.showGrammarErrors(grammar_errors, grammar_warnings)

    def copyTextToClipboard(self):
        """Копируем текст в буфер обмена"""
        print('WidgetConverterText.copyTextToClipboard')
        # копируем текст в буфер обмена
        if self.setting.get('copy_to_clipboard'):
            self.clipboard.setText(self.te_text_to_convert.toPlainText())

    def magic(self):
        """Магия конвертирования показаний"""
        print('WidgetConverterText.magic')
        # определяем какая кнопка вызвала метод
        btn_send = QApplication.instance().sender()
        # получаем текст из поля
        text = self.te_text_to_convert.toPlainText()
        # не работаем если пусто
        if not text:
            return
        # исправляем ошибки в тексте
        text = self._correct_text(text)

        for ch in chars:
            # цикл по общему словарю
            text = self._convert(ch, text)
            # цикл для предложных форм
            # в зависимости от выбранного пола отправляем на конвертирование
            if "wo" not in btn_send.objectName():
                # для мужчин
                for pretext in pretexts:
                    for key in change_words_men_p:
                        text = text.replace(
                            key.format(pretext, ch),
                            change_words_men_p[key].format(pretext, ch))
                # цикл для остальных случаев
                for dic in change_words_men:
                    for key in dic:
                        text = text.replace(key.format(ch), dic[key].format(ch))
            else:
                # для женщины
                for pretext in pretexts:
                    for key in change_words_women_p:
                        text = text.replace(
                            key.format(pretext, ch),
                            change_words_women_p[key].format(pretext, ch))
                # цикл для остальных случаев
                for dic in change_words_women:
                    for key in dic:
                        text = text.replace(key.format(ch), dic[key].format(ch))
        self.te_text_to_convert.clear()
        self.te_text_to_convert.setText(text)
        self.setFontTypeSize()
        self.copyTextToClipboard()
        self.lbl_status_info.setText('Текст сконвертирован.')
        self.blocking()

    def setFontTypeSize(self):
        """Применение типа и размера шрифта к тексту по настройкам"""
        print('WidgetConverterText.setFontTypeSize')
        # исправляет написание текста в окне
        if self.setting.get('fix_font'):
            font_size = self.setting.get('font_size', 13)
            font_name = QFont(self.setting.get('font_name', 'Times New Roman'))
            self.te_text_to_convert.setFont(font_name)
            self.te_text_to_convert.setFontPointSize(float(font_size))

    def addWordFromText(self):
        """Добавление слова из текста (выделенное)"""
        print('WidgetConverterText.addWordFromText')
        # TODO: create
        # получаем выделенный фрагмент в тексте,
        # если фрагмент содержит больше 1 слова - не работаем
        # открываем окно добавления слова,
        # вставляем выделенное слово в позицию ключа (от 1 лица)
        # при accept в окне добавляем значения в словарь пользовательский

    def blocking(self):
        """Блокировка кнопок после замены"""
        print('WidgetConverterText.blocking')
        self.pbtn_men.setEnabled(False)
        self.pbtn_women.setEnabled(False)

    def unblocking(self):
        """Разблокировка кнопок."""
        print('WidgetConverterText.unblocking')
        if self.te_text_to_convert.toPlainText().strip():
            self.pbtn_men.setEnabled(True)
            self.pbtn_women.setEnabled(True)
        else:
            self.blocking()


def test():
    import sys
    t_sett = setting_converter
    app = QApplication(sys.argv)
    main_win = WidgetConverterText({}, t_sett)
    main_win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
