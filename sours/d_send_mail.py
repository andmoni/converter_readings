#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 19.02.2024 г.

@author: Следователь (Andmoni@yandex.ru)
@last_editing: 19.02.2025

Окно отправки письма разработчику, включающее поля для ввода адреса и тела письма.
"""

from PyQt5.QtWidgets import QDialog
from sours.UI.d_send_mail import Ui_DialogSendDevMail
from sours.f_show_message import show_message_dialog


class DialogSendDevMail(QDialog, Ui_DialogSendDevMail):
    """
    Окно отправки письма разработчику.
    """

    def __init__(self, version: str, parent=None):
        """конструктор"""
        super().__init__(parent)
        self.setupUi(self)
        self.version = version

    def send_mail(self):
        """Отправка разработчику письма"""
        print('DialogSendMeMail.sendMail')
        with open(r'письмо разработчику.txt', 'w', encoding='utf-8') as f:
            import sysconfig
            f.write(self.textEdit.toPlainText())
            f.write('\nДанные далее нужны для анализа ошибки. ')
            f.write('Они не содержат личной либо конфиденциальной информации.\n')
            f.write('Операционная система :: {}\n'.format(sysconfig.get_platform()))
            f.write('Версия Python :: {}\n'.format(sysconfig.get_python_version()))
            f.write('Версия программы "Конвертер показаний":: {}'.format(self.version))
        show_message_dialog(
            parent=self, ico=2, title=2,
            msg='Отправьте файл "письмо разработчику.txt" ' +
                'из каталога программы на электронную почту andmoni@yandex.ru.',
            btn_a_text='Отправляю')
        self.accept()
