
""" Тест 3 Домашнее Задание 
Добавить в тестовый проект шаг добавления
поста после входа. Должна выполняться
проверка на наличие названия поста на странице
сразу после его создания."""


from testpage import OperationsHelper, get, get_post, post
from conftest import login
import logging
import yaml
import time

with open("/Users/portable/Desktop/For leaning/HW_4_api/testdata.yaml") as f:
    testdata = yaml.safe_load(f)

def test_step1(browser):
    logging.info("Test 1 started")
    testpage = OperationsHelper(browser) #делаем страницу экземпляром класса и передаем браузер, так как он нужен для BasePage
    testpage.go_to_site() #открывваем страницу
    testpage.enter_login('test') #вводим логин
    testpage.enter_pass("test")
    testpage.click_login_button()
    assert testpage.get_error_text() == "401"


def test_step2(browser):
    logging.info("Test2 Starting")
    test_page = OperationsHelper(browser)
    test_page.go_to_site()
    test_page.enter_login(testdata["login"])
    test_page.enter_pass(testdata["password"])
    test_page.click_login_button()
    test_page.get_blog()
    assert test_page.get_blog() == "Blog"


def test_step3(browser):
    logging.info("Test 3 Starting")
    test_page = OperationsHelper(browser)
    test_page.go_to_site()
    test_page.enter_login(testdata["login"])
    test_page.enter_pass(testdata["password"])
    test_page.click_login_button()
    test_page.click_button_create_post()
    test_page.input_title_post(testdata['title'])
    test_page.click_button_save_post()
    time.sleep(5)
    test_page.new_post()
    assert test_page.new_post() == "Check Text Post"


#Добавить в проект тест (test_step4) по проверке механики
#работы формы Contact Us. Должно проверятся
#открытие формы, ввод данных в поля, клик
#по кнопке и появление всплывающего alert.
#Совет:
#Переключиться на alert можно
#командой alert = self.driver.switch_to.alert
#Вывести текст alert.text


def test_step4(browser):
    logging.info("Test 4 Starting")
    test_page = OperationsHelper(browser)
    test_page.go_to_site()
    test_page.enter_login(testdata["login"])
    test_page.enter_pass(testdata["password"])
    test_page.click_login_button()

    test_page.click_contact()
    test_page.input_name(testdata["name"])
    test_page.input_email(testdata["email"])
    test_page.input_content(testdata["content"])
    time.sleep(3)
    test_page.click_button_contact_us()
    time.sleep(3)
    test_page.alert()

    assert test_page.alert() == "Form successfully submitted"

# Добавить в проект тесты API, доработать тесты в едином стиле с тестами UI, добавив
# логирование и обработку ошибок.


def test_step5(login):
    logging.info("Test 5 Starting")
    res = get(login)
    lst = res['data']
    lst_id = [el["id"] for el in lst]

    assert 81104 in lst_id, 'тест провален'

def test_step6(login):
    logging.info("Test 6 Starting")
    my_post = post(login)
    all_posts = get_post(login)
    lst = all_posts['data']
    lst_description = [el["description"] for el in lst]

    assert "Мое первое автотестирование" in lst_description, 'тест провален'