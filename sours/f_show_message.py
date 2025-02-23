# -*- coding: utf-8 -*-

"""
Created on 18.11.2023 г.

@author: Cледователь.
"""

from PyQt5.QtWidgets import QMessageBox, QApplication


def show_message_dialog(parent=None, ico: int = 0, title: int = 0, msg: str = 'Саечка на испуг.',
                        btn_a_text: str = 'Получил', btn_c_text: str = '', btn_d_text: str = '') -> bool:
    """Отображение окна сообщения
    :param parent: Виджет (окно) инициатор вывода сообщения.
    :param ico: Код иконки в окне сообщения
        0 - без иконки (по умолчанию),1 - Question, 2 - Information,
        3 - Warning, 4 - Critical
    :param title: Код заголовка для окна сообщения. 
        0: 'О! Сообщение.' (по умолчанию), 1: 'Это. Тут вопрос!', 2: 'Слушай, информирую!',
        3: 'Эй, Внимание!', 4: 'Ой, Ошибочка!'
    :param msg: Текст сообщения в окне
    :param btn_a_text: Текст на кнопке принятия (с ролью AcceptRole). По-умолчанию - "Получил"
    :param btn_c_text: Текст на кнопке отмены (с ролью RejectRole) По-умолчанию - None,
        при котором не отображается.
    :param btn_d_text: Текст на кнопке непринятия (с ролью DiscardRole) По умолчанию - None,
        при котором не отображается.
    :return: Возвращает результат исполнения окна сообщения
    """
    icons = {0: QMessageBox.NoIcon,
             1: QMessageBox.Question,
             2: QMessageBox.Information,
             3: QMessageBox.Warning,
             4: QMessageBox.Critical}
    titles = {0: 'Оп! Сообщение.',
              1: 'Это, тут вопрос!',
              2: 'Слушай, информирую!',
              3: 'Эй, Внимание!',
              4: 'Ой-вэй, Ошибочка!'}
    msg = QMessageBox(icons[ico], titles[title], msg, parent=parent)
    if not btn_c_text == '':
        msg.addButton(btn_c_text, QMessageBox.RejectRole)
    msg.addButton(btn_a_text, QMessageBox.AcceptRole)
    if not btn_d_text == '':
        msg.addButton(btn_d_text, QMessageBox.DestructiveRole)
    return msg.exec_()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    result = show_message_dialog(
        None, 1, 1, "Опись изменена.\n\nСохранить изменения?",
        "Давай", "Дай подумать", "Не надо")
    print(result)
    sys.exit(app.exec_())
