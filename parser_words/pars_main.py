# -*- coding: utf-8 -*-

"""
Парсер слов с сайта https://inflectonline.ru/

На входе получает ссылки на XML-файлы схема страниц сайта слов.
Маппинг скопировал с сайта ручками.
Хранится в файлах sitemap-words(, -2, -3).xml в одной папке с этим файлом.

После парсинга слов с сайта надо просмотреть полученную таблицу на ошибки переименовать ее и переместить в папку data
"""

import sys
import urllib
from datetime import datetime
from urllib.parse import quote, urlsplit, urlunsplit
from urllib.request import Request
from lxml import etree as ET
import lxml.html as html


def iri_to_uri(iri):
    '''Функция преобразования кириллицы в строке адреса страницы сайта'''
    parts = urlsplit(iri)
    uri = urlunsplit((
        parts.scheme,
        parts.netloc.encode('idna').decode('ascii'),
        quote(parts.path),
        quote(parts.query, '='),
        quote(parts.fragment),
    ))
    return uri


def find_urls(words_dic_xmls):
    print('Начал поиск адресов слов')
    '''Функция поиска url адресов страниц в схеме сайта'''
    # список всех адресов из схемы сайта
    urls = []
    # список всех слов
    words_dict = []
    for dic_xml in words_dic_xmls:
        tree = ET.parse(dic_xml)
        root = tree.getroot()
        #print(len(root.findall('url')))
        for childs in root:
            #print(child, child.tag, child.text)
            for child in childs.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                urls.append(str(child.text))
                words_dict.append(str(child.text)[25:])

    # сохраняем обнаруженный список ссылок на страницы слов
    with open('urls_site.txt', 'w', encoding='utf-8') as f:
        f.writelines([f'{url}\n' for url in urls])
        print('Сохранил словарь обнаруженных адресов слов')

    # сохраняем обнаруженные на сайте слова в словарь (без склонений и спряжений)
    with (open('all_words.txt', 'w', encoding='utf-8') as f):
        f.write("Всего обработано {} слов. \n".format(len(words_dict)))
        f.write('Словарь:\n')
        f.writelines([f'{ln}\n' for ln in words_dict])
        print('Сохранил словарь обнаруженных слов')
    print('Закончил поиск адресов слов')
    return urls


def pars(urls: list, s: int = 0):
    """
    :param urls: список url-адресов сайта для парсинга
    :param s: начальный номер адреса для парсинга (задает значение счетчика)
    :return: возвращает словарь со словами которые нашел на сайте
    """
    print('Начал парсинг найденных страниц')
    # список значений при достижении которых счетчиком необходимо сохранять работу
    save_ars = [a * 200 for a in range(280)]
    # словарь глаголов - ключ(неопределенная форма):список (спряжения глагола)
    words_dict_gl = {}
    # итоговое количество всех ссылок
    i = len(urls)
    # перебираем ссылки
    for url in urls[s:i]:
        # увеличиваем счетчик на 1
        s += 1
        # выводим в консоль информацию о сделанной работе
        #print(f'Обработано {s} из {i} страниц.')
        # проверяем надо ли сохранять работу
        if s in save_ars:
            # выводим информацию о сохранении словаря
            print(f'Сохраняю. Обработано {s} из {i} страниц.')
            # сохранение словаря по шаблону
            save_to_file(words_dict_gl)
            # сохранение всего словаря в базу
            save_dict(s, words_dict_gl)

        # формируем запрос на страницу сайта https://inflectonline.ru/{} для скачивания
        req = Request(
            url=iri_to_uri(url),
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        # пробуем скачать страницу
        try:
            f = urllib.request.urlopen(req).read().decode('utf-8')
            # Если на странице нет сведений о глаголе, пропускаем ее.
            # Тем самым ищем глаголы и их спряжения
            if not 'Спряжение глагола' in f:
                #print('Пропущено')
                continue
            # задаем парсер страницы
            parser = ET.HTMLParser()
            # получаем корневой элемент для html страницы
            root = html.fromstring(f, parser=parser)
            # перебираем элементы страницы отыскивая блок "main"
            for child in root:
                if 'body' in child.tag:
                    for body_child in child:
                        if 'main' in body_child.tag:
                            # задаем значение если слово не проверено
                            adm_check = "нет"
                            # задаем пустой словарь для сбора найденных слов
                            tb_wrd = []
                            # перебираем элементы блока main
                            for sub_body_child in body_child:
                                # отыскиваем элемент содержащий сведения о проверке слова админом
                                if 'p' in sub_body_child.tag:
                                    if "class" in sub_body_child.attrib:
                                        if "text-success" in sub_body_child.get('class'):
                                            if 'Слово проверено администратором.' in sub_body_child.text:
                                                # меняем значение проверки на положительное
                                                adm_check = "да"
                                # отыскиваем элемент с таблицей
                                if "div" in sub_body_child.tag:
                                    #print('e_main_div: ', sub_body_child.attrib)
                                    if "class" in sub_body_child.attrib:
                                        #print(sub_body_child.get('class'))
                                        for el in sub_body_child:
                                            if 'Изъявительное наклонение' in el.text:
                                                pass
                                            if 'div' in el.tag:
                                                if 'table-responsive' in el.get('class'):
                                                    for table in el:
                                                        if 'table' in table.tag:
                                                            for tb_el in table:
                                                                if 'tbody' in tb_el.tag:
                                                                    for trow in tb_el:
                                                                        if 'tr' in trow.tag:
                                                                            for cell in trow:
                                                                                if 'td' in cell.tag:
                                                                                    #print(cell.text.strip())
                                                                                    # добавляем значение из ячейки
                                                                                    # обрезав пробелы
                                                                                    tb_wrd.append(cell.text.strip())
                            # добавляем в список к найденым словам сведения о проверке слов админом
                            tb_wrd.append(adm_check)
                            # добавляем слово и его спряжения в словарь глаголов
                            words_dict_gl[url[25:]]=tb_wrd
                            #print('insert: {}'.format(url[25:]))
        except Exception as e:
            # если произошла ошибка при обращении к странице, выводим ее в консоль
            print(f"Ошибка при обращении к {url}: {e}")
    # возвращаем получившийся словарь значений
    print('Закончил поиск слов по страницам из списка')
    return words_dict_gl


def save_dict(i: int, di: dict):
    '''
    Сохранение словаря не форматированного в файл
    :param i: номер страницы при сохранении
    :param di: словарь со словами и их спряжениями
    '''
    with open('replacement_dict.txt', 'w', encoding='utf-8') as f:
        f.write(f'{str(i)}\n')
        f.write(',\n'.join(f'"{str(x)}":{str(di.get(x))}' for x in di.keys()))
        print('Сохранил словарь всего')


def save_to_file(words_dict_gl: dict):
    '''
    Сохранение словаря в форматированной таблице в текстовый файл
    :param words_dict_gl: словарь со словами и их спряжениями
    '''
    # генерим версию словаря
    version = datetime.today().strftime("%Y%m%d")
    # формируем шапку таблицы
    lns = ['{}::{}\n'.format(
            "version".ljust(30),
            version.ljust(30)
        ),
            '{}::{}::{}::{}::{}::{}\n'.format(
            "неопределенная форма".center(30),
            "ед.ч. 1 лицо".center(30),
            "ед.ч. 3 лицо".center(30),
            "мн.ч. 1 лицо".center(30),
            "мн.ч. 3 лицо".center(30),
            'проверено'.center(30)
        ), ]
    # сортируем ключи словаря и формируем строки для записи в таблицу
    keys = list(words_dict_gl.keys())
    keys.sort()
    # формируем тело таблицы
    for key in keys:
        # получаем спряжения слов
        words = words_dict_gl.get(key)
        # print(key, words)
        # ловим странные символы в словаре
        if "?" in words[0]:
            # пропускаем слово если есть странный символ
            # мы добавили не то слово
            continue
        # пытаемся записать строку в таблицу
        try:
            lns.append("{}::{}::{}::{}::{}::{}\n".format(
                key.ljust(30),
                words[0].ljust(30),
                words[4].ljust(30),
                words[1].ljust(30),
                words[5].ljust(30),
                words[-1].ljust(30),
            ))
        # если в таблице по ключу не было словаря значений прописываем ошибку над таблицей
        except Exception as e:
            print(f'Ошибка при парсинге слова {key}: {e}')
            lns.insert(1,f'key:{key},words:{words}\n')
            continue
    # сохраняем полученную данные и таблицу в файл
    with open('replacement_word_pars.dict', 'w', encoding='utf-8') as f:
        f.writelines(lns)
        print('Сохранил таблицу глаголов replacement_dictionary для программы')



def main():
    '''Основная функция'''
    # схема страниц сайта со словами
    # тут не мешало бы добавить скачивание схемы с сайта иее разбор, но пока оставим так
    words_dic_xmls = [
    'parser_words/sitemap-words.xml',
    'parser_words/sitemap-words-2.xml',
    'parser_words/sitemap-words-3.xml'
    ]
    # перехватываем системный вывод для лога
    tmp_std_out = sys.stdout
    # создаем лог-файл для записи системного вывода
    file_log = open("../system.log", 'w', encoding='utf-8')
    # записываем системный вывод в файл
    #sys.stdout = file_log
    # ищем ссылки на страницы в схеме сайта
    urls = find_urls(words_dic_xmls)
    # проводим парсинг найденых страниц, с генерацией словаря глаголов
    wdg = pars(urls)
    # сохраняем найденные глаголы
    save_to_file(wdg)
    # возврат вывода в консоль
    sys.stdout = tmp_std_out
    file_log.close()
    # сообщение, что закончили работу
    print('ЗАКОНЧИЛ РАБОТУ')


if __name__ == '__main__':
    main()