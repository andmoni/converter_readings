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


class DialogSendDevMail(QDialog, Ui_DialogSendDevMail):
    """Окно отправки письма разработчику
    """

    def __init__(self, parent=None):
        """конструктор"""
        super().__init__(parent)
        self.setupUi(self)

    def send_mail(self):
        """Отправка разработчику письма"""
        print('DialogSendMeMail.sendMail')
        # TODO: сделать метод?
        #  пользователь вручную отправляет письмо генерируемое в папке с программой
        self.accept()