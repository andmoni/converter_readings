#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 14 фев. 2024 г.

@author: Следователь (Andmoni@yandex.ru)

Главное окно конвертера показаний.

Описание:
Классический интерфейс - с классическими toolbox menu (скрыть кнопку и меню с вкладками)
современный интерфейс - с меню в виде вкладок (скрываем тулбоксы меню и кнопки
переключающие их отображение)

Errors:
падение при вводе запятой в поле и символов в поле размера теста
QRegExp("[^0-9.]")
"""
VERSION = 3.0

from datetime import datetime
from PyQt5.QtGui import QFont, QDoubleValidator
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QFontDialog, QDialog, qApp, QMenu
)
from PyQt5.QtCore import Qt, QSize, QSettings, QPoint
from sours.UI.mw_converter import Ui_MainWindowConverter
from sours.UI.about_app import Ui_AboutApp
from sours.d_converter_dictionary import load_replacement_words
from sours.d_setting_app import DialogSettingApp, load_setting, write_setting
from sours.w_converter_text import WidgetConverterText
from sours.d_send_mail import DialogSendDevMail
from sours.f_show_message import show_message_dialog
from sours.w_converter_setting import editingReplacementWords


class MainWindowConverter(QMainWindow, Ui_MainWindowConverter):
    """Окно главного приложения."""

    def __init__(self):
        """Конструктор окна."""
        #print('MainWindow.__init__')
        super().__init__()
        self.setupUi(self)
        # чтение настроек для приложения
        self._read_settings()
        # создание текстового редактора и помещение его в центральный виджет
        self.central_widget = WidgetConverterText(self.replacement_words, self._setting_app)
        self.verticalLayout.addWidget(self.central_widget)
        self.central_widget.pbtnbox.hide()
        # связывание элемента главного окна с элементом в виджете для удобства привязки действий
        self.editor = self.central_widget.te_text_to_convert

        # создание действий и меню
        self._createActions()
        self._createToolBars()
        # self._createMenus()
        # связывание кнопок и действий меню с методами окна
        self._connectActs()
        self._createStatusBar()
        self.setInterface()

    def _createActions(self):
        """Создание дополнительных действий для меню, и настройка имеющихся."""
        print('MainWindowInventory._create_actions')
        #format_group = QActionGroup(self)
        #format_group.setExclusive(True)
        #format_group.addAction(self.act_align_left)
        #format_group.addAction(self.act_align_center)
        #format_group.addAction(self.act_align_right)
        #format_group.addAction(self.act_align_justify)

        self._format_acts = [
            self.fcb_font_name,
            self.cb_font_size,
            self.act_bold,
            self.act_italic,
            self.act_underline,
            #self.act_strikethrough,
            #self.act_subscript,
            #self.act_superscript,
            self.tbtn_bold,
            self.tbtn_italic,
            self.tbtn_underline,
            #self.tbtn_strikethrough,
            #self.tbtn_subscript,
            #self.tbtn_superscript,
        ]
        self.status_bar.showMessage('Создал дополнительные действия.', 2000)

    def _createMenus(self):
        """Создание дополнительных меню."""
        print('MainWindowInventory._create_menus')
        self.status_bar.showMessage('Создал дополнительные меню.', 2000)

    def _createToolBars(self):
        """Создание дополнительных тул-баров и настройка тул-баров."""
        print('MainWindowInventory._create_tool_bars')
        self.cb_font_size.setValidator(QDoubleValidator())
        self.status_bar.showMessage('Создал тул-бары.', 2000)

    def _connectActs(self):
        """Создание связей кнопок и действия меню с функциями"""
        print('MainWindowInventory._connect_act')
        # список действий и методы для работы по ним
        _acts = {
            self.act_new: self.editor.clear,
            self.act_undo: self.editor.undo,
            self.act_redo: self.editor.redo,
            self.act_cut: self.editor.cut,
            self.act_copy: self.editor.copy,
            self.act_paste: self.editor.paste,
            self.act_delete: self.editor.clear,
            self.act_select_all: self.editor.selectAll,
            self.act_align_left: lambda: self.editor.setAlignment(Qt.AlignLeft),
            self.act_align_center: lambda: self.editor.setAlignment(Qt.AlignCenter),
            self.act_align_right: lambda: self.editor.setAlignment(Qt.AlignRight),
            self.act_align_justify: lambda: self.editor.setAlignment(Qt.AlignJustify),
            self.act_bold: lambda x: self.editor.setFontWeight(
                QFont.Bold if x else QFont.Normal),
            self.act_italic: self.editor.setFontItalic,
            self.act_underline: self.editor.setFontUnderline,
            # self.act_strikethrough: self.editor.setFontStrikeOut,
            # self.act_subscript: self.editor.setSubscript,
            # self.act_superscript: self.editor.setSuperscript,
            self.act_convert_man_testimony: self.central_widget.magic,
            self.act_convert_woman_testimony: self.central_widget.magic,
            self.act_correct_the_text: self.central_widget.correctText,
            # self.act_upper_case: self.upperCase,
            # self.act_lower_case: self.lowerCase,
            # self.act_proper_case: self.properCase,
            # self.act_sentence_case: self.sentenceCase,
            # self.act_invert_case: self.invertCase,
            self.act_grammar_check: self.central_widget.grammarCheck,
            # self.act_font_color: self.editor.setTextColor,
            # self.act_background_color: self.editor.setTextBackgroundColor,
            # self.act_find: self.findText,
            # self.act_find_next: self.findNextText,
            # self.act_replace: self.replaceText,
            # self.act_replace_all: self.replaceAllText,
            # self.act_select_word: self.selectWord,
            # self.act_select_line: self.selectLine,
            # self.act_select_paragraph: self.selectParagraph,
            # self.act_select_all_text: self.selectAllText,
            # self.act_copy_as_rtf: self.copyTextAsRtf,
            # self.act_copy_as_html: self.copyTextAsHtml,
            # self.act_copy_as_plaintext: self.copyTextAsPlaintext,
            # self.act_export_as_pdf: self.exportAsPdf,
            # self.act_export_as_image: self.exportAsImage,
            # self.act_export_as_word: self.exportAsWord,
            # self.act_export_as_excel: self.exportAsExcel,
            # self.act_export_as_csv: self.exportAsCsv,
            # self.act_export_as_json: self.exportAsJson,
            # self.act_export_as_xml: self.exportAsXml,
            # self.act_export_as_plaintext: self.exportAsPlaintext,
            # self.act_export_as_html: self.exportAsHtml,
            # self.act_export_as_markdown: self.exportAsMarkdown,
            # self.act_export_as_latex: self.exportAsLatex,
            # self.act_export_as_odt: self.exportAsOdt,
            # self.act_export_as_opendocument: self.exportAsOpenDocument,
            # self.act_export_as_epub: self.exportAsEpub,
            # self.act_export_as_mobi: self.exportAsMobi,
            # self.act_export_as_azw3: self.exportAsAzw3,
            # self.act_export_as_text: self.exportAsText,
            # self.act_export_as_rtf: self.exportAsRtf,
            # self.act_export_as_html: self.exportAsHtml,
            # self.act_export_as_markdown: self.exportAsMarkdown,
            # self.act_export_as_latex: self.exportAsLatex,
            # self.act_export_as_odt: self.exportAsOdt,
        }
        # отключение всех сигналов
        for act in _acts.keys():
            act.triggered.disconnect()
        # соединение сигналов
        for act in _acts.keys():
            act.triggered.connect(_acts[act])
        _tbtns = {
            self.tbtn_new: self.editor.clear,
            self.tbtn_undo: self.editor.undo,
            self.tbtn_redo: self.editor.redo,
            self.tbtn_cut: self.editor.cut,
            self.tbtn_copy: self.editor.copy,
            self.tbtn_paste: self.editor.paste,
            self.tbtn_delete: self.editor.clear,
            self.tbtn_select_all: self.editor.selectAll,
            self.tbtn_align_left: lambda: self.editor.setAlignment(Qt.AlignLeft),
            self.tbtn_align_center: lambda: self.editor.setAlignment(Qt.AlignCenter),
            self.tbtn_align_right: lambda: self.editor.setAlignment(Qt.AlignRight),
            self.tbtn_align_justify: lambda: self.editor.setAlignment(Qt.AlignJustify),
            self.tbtn_bold: lambda x: self.editor.setFontWeight(
                QFont.Bold if x else QFont.Normal),
            self.tbtn_italic: self.editor.setFontItalic,
            self.tbtn_underline: self.editor.setFontUnderline,
            # self.tbtn_strikethrough: self.editor.setFontStrikeOut,
            # self.tbtn_subscript: self.editor.setSubscript,
            # self.tbtn_superscript: self.editor.setSuperscript,
            self.tbtn_convert_man_testimony: self.central_widget.magic,
            self.tbtn_convert_woman_testimony: self.central_widget.magic,
            self.tbtn_correct_the_text: self.central_widget.correctText,
            self.tbtn_grammar_check: self.central_widget.grammarCheck,
        }
        # отключение всех сигналов
        for tbtn in _tbtns.keys():
            tbtn.disconnect()
        # соединение сигналов
        for tbtn in _tbtns.keys():
            tbtn.clicked.connect(_tbtns[tbtn])
        # Connect to the signal producing the text of the
        # current selection. Convert the string to float
        # and set as the pointsize. We could also use the
        # index + retrieve from FONT_SIZES.
        self.cb_font_size.currentIndexChanged[str].connect(
            lambda s: self.editor.setFontPointSize(float(s)))
        self.fcb_font_name.currentFontChanged.connect(self.editor.setCurrentFont)
        self.editor.selectionChanged.connect(self.updateFormat)
        self.status_bar.showMessage('Создал соединения.', 2000)

    def _createStatusBar(self):
        """Создание строки состояния."""
        print('MainWindowInventory._createStatusBar')
        self.status_bar.showMessage('Готов к работе.', 3000)

    def updateFontNameSize(self):
        """Обновление текстового поля и выпадающего списка шрифтов и размеров."""
        print('MainWindowInventory.updateFontNameSize')
        font_name = self.fcb_font_name.currentFont()
        font_size = float(self.cb_font_size.currentText())
        self.editor.setFont(font_name)
        self.editor.setFontPointSize(font_size)
        self.editor.update()

    def editFont(self):
        """Изменение шрифта текста."""
        print('MainWindowInventory.editFontName')
        font, ok = QFontDialog.getFont()
        if ok:
            self.editor.setFont(font)
            self.editor.update()
            self.fcb_font_name.setCurrentFont(font)
            self.cb_font_size.setCurrentText(str(font.pointSize()))

    def enlargeFontSize(self):
        """Увеличение размера шрифта текста."""
        #print('MainWindowInventory.enlargeFontSize')
        font_size = self.editor.fontPointSize()
        font_size += 1
        font_name = self.fcb_font_name.currentFont()
        self.editor.setFont(font_name)
        self.editor.setFontPointSize(font_size)
        self.cb_font_size.setCurrentText(str(font_size))

    def reduceFontSize(self):
        """Уменьшение размера шрифта текста."""
        #print('MainWindowInventory.reduceFontSize')
        font_size = self.editor.fontPointSize()
        if font_size > 12:
            font_size -= 1
            font_name = self.fcb_font_name.currentFont()
            self.editor.setFont(font_name)
            self.editor.setFontPointSize(font_size)
            self.cb_font_size.setCurrentText(str(font_size))

    def _blockSignals(self, objects, b):
        """Блокирование сигналов действиям меню и кнопкам."""
        for o in objects:
            o.blockSignals(b, )

    def updateFormat(self):
        """
        Обновление кнопок панели(меню) формат если выбран текст.
        Это необходимо для поддержания кнопок тулбара и меню
        в состоянии актуальном для текста
        """
        # Отключение сигналов для всех виджетов меню формат
        #  значения не переключают формат текста.
        self._blockSignals(self._format_acts, True)

        self.fcb_font_name.setCurrentFont(self.editor.currentFont())
        self.cb_font_size.setCurrentText(
            str(int(self.editor.fontPointSize())))

        self.act_italic.setChecked(self.editor.fontItalic())
        self.act_underline.setChecked(self.editor.fontUnderline())
        self.act_bold.setChecked(
            self.editor.fontWeight() == QFont.Bold)

        self.act_align_left.setChecked(
            self.editor.alignment() == Qt.AlignLeft)
        self.act_align_center.setChecked(
            self.editor.alignment() == Qt.AlignCenter)
        self.act_align_right.setChecked(
            self.editor.alignment() == Qt.AlignRight)
        self.act_align_justify.setChecked(
            self.editor.alignment() == Qt.AlignJustify)

        self.tbtn_italic.setChecked(self.editor.fontItalic())
        self.tbtn_underline.setChecked(self.editor.fontUnderline())
        self.tbtn_bold.setChecked(
            self.editor.fontWeight() == QFont.Bold)

        self.tbtn_align_left.setChecked(
            self.editor.alignment() == Qt.AlignLeft)
        self.tbtn_align_center.setChecked(
            self.editor.alignment() == Qt.AlignCenter)
        self.tbtn_align_right.setChecked(
            self.editor.alignment() == Qt.AlignRight)
        self.tbtn_align_justify.setChecked(
            self.editor.alignment() == Qt.AlignJustify)

        self._blockSignals(self._format_acts, False)

    def sendMailToDev(self):
        """Написать письмо разработчику"""
        print('MainWindowInventory.sendMailToDev')
        wid = DialogSendDevMail(str(VERSION))
        wid.exec_()

    def editSettingApp(self):
        """Изменение настроек программы"""
        print('MainWindowInventory.editSettingApp')
        wid = DialogSettingApp(self._setting_app, self.replacement_words)
        a = wid.exec_()
        if a:
            self.setInterface()
        # TODO: после закрытия обновить если а = ацепт,
        #  проверить язык обновить отображение окон

    def setInterface(self):
        """Применение настроек интерфейса."""
        print('MainWindowInventory.setInterface')
        if self._setting_app['setting_app']['interface']:
            self.act_modern.setChecked(True)
            self.act_classic.setChecked(False)
        else:
            self.act_modern.setChecked(False)
            self.act_classic.setChecked(True)
        self.updateInterface()

    def updateInterface(self):
        """Смена вида интерфейса."""
        print('MainWindowInventory.updateInterface')
        if self.act_classic.isChecked():
            # скрываем вкладки с кнопками и действие меню отображения вкладок
            self.act_v_tabs_menu.setVisible(False)
            self.tw_tabs_menu.setVisible(False)
            # показываем действия включения меню
            self.act_v_main_menu.setVisible(True)
            self.act_v_edit_menu.setVisible(True)
            self.act_v_converter_menu.setVisible(True)
            for key, value in self._setting_app['setting_app'].items():
                if 'tool_bars' in key:
                    self.act_v_main_menu.setChecked(value.get('main'))
                    self.act_v_edit_menu.setChecked(value.get('edit'))
                    self.act_v_converter_menu.setChecked(value.get('convert'))
                    self.tlb_main.setVisible(value.get('main'))
                    self.tlb_edit.setVisible(value.get('edit'))
                    self.tlb_converter.setVisible(value.get('convert'))
            self._setting_app['setting_app']['interface'] = 0
        else:
            self._setting_app['setting_app']['interface'] = 1
            self.act_v_tabs_menu.setVisible(True)
            self.tw_tabs_menu.setVisible(True)
            self.act_v_main_menu.setVisible(False)
            self.act_v_edit_menu.setVisible(False)
            self.act_v_converter_menu.setVisible(False)
            self.tlb_main.setVisible(False)
            self.tlb_edit.setVisible(False)
            self.tlb_converter.setVisible(False)

    def editReplacementWords(self):
        """Изменение словаря замены слов."""
        print('MainWindowInventory.editReplacementWords')
        editingReplacementWords(self.replacement_words)

    def _read_settings(self) -> None:
        """Чтение настроек из реестра."""
        print('MainWindowInventory._read_settings')
        settings = QSettings("Nemec-soft", "Converter testimony")
        # settings.setFallbacksEnabled(True) посмотри что дает, включи если полезно
        size = settings.value("size", QSize(1000, 800))
        self.resize(size)
        pos = settings.value("pos", QPoint(100, 100))
        self.move(pos)
        # загрузка настроек с диска
        self._setting_app = load_setting()
        # загрузка словаря замены слов
        self.replacement_words = load_replacement_words()

    def _save_tool_bars_settings(self):
        """Сохранение настроек на диск."""
        print('MainWindowInventory._save_tool_bars_settings')
        self._setting_app['setting_app']["tool_bars"] = {
            'main': self.tlb_main.isVisible(),
            'edit': self.tlb_edit.isVisible(),
            'convert': self.tlb_converter.isVisible()
        }

    def _write_settings(self):
        """Запись настроек в реестр."""
        print('MainWindowInventory._writeSettings')
        settings = QSettings("Nemec-soft", "Converter testimony")
        # настройка размера окна и положения
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())
        if self.act_classic.isChecked():
            self._save_tool_bars_settings()
            self._setting_app['setting_app']['interface'] = 0
        else:
            self._setting_app['setting_app']['interface'] = 1
        # сохранение настроек в файл
        write_setting(self._setting_app)
        print(self._setting_app)

    def helpFAQ(self):
        """Вывод окна с помощью о приложении."""
        print('MainWindowInventory.helpFAQ')
        show_message_dialog(self, 2, 2,
                            'Простите. Помощь FAQ еще варится в нашем котелке.\nСледите за обновлениями на форуме.',
                            "Придется ждать")

    @staticmethod
    def aboutApp():
        """Вывод окна с информацией о приложении."""
        print('MainWindowInventory.about')
        aa = QDialog()
        ui = Ui_AboutApp()
        ui.setupUi(aa)
        aa.exec_()

    @staticmethod
    def aboutQT():
        """Отображение справки о Qt (на английском)"""
        print('MainWindowInventory.aboutQT')
        # print('ознакомление со справкой о Qt - на английском')
        qApp.aboutQt()

    def closeEvent(self, event):
        """Действия при закрытии программы."""
        print('MainWindowInventory.closeEvent')
        print('{} :: Выход из программы.'.format(datetime.today()))
        self._write_settings()
        event.accept()

    def createPopupMenu(self) -> 'QMenu':
        """Создаем свое контекстное меню для панелей инструментов (док-виджетов)"""
        menu = QMenu('Панели инструментов:', self)
        menu.addAction(self.act_v_main_menu)
        menu.addAction(self.act_v_edit_menu)
        menu.addAction(self.act_v_converter_menu)
        menu.addAction(self.act_v_tabs_menu)
        return menu  # QMainWindow.createPopupMenu(self)


def test():
    print('запуск теста')
    import sys
    app = QApplication(sys.argv)
    wid = MainWindowConverter()
    wid.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
