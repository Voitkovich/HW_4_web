from BaseApp import BasePage
from selenium.webdriver.common.by import By
import logging
import yaml
import requests

with open("/Users/portable/Desktop/For leaning/HW_4_api/testdata.yaml") as f:
    testdata = yaml.safe_load(f)

class TestSearchLocators:
    ids = dict()
    with open("./locators.yaml") as f:
        locators = yaml.safe_load(f)
    for locator in locators["xpath"].keys():
        ids[locator] = (By.XPATH, locators["xpath"][locator])
    for locator in locators["css"].keys():
        ids[locator] = (By.CSS_SELECTOR, locators["css"][locator])


class OperationsHelper(BasePage):
# методы Input text
    def enter_text_into_field(self, locator, word, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        logging.debug(f"Send {word} to element {element_name}")
        field = self.find_element(locator)
        if not field:
            logging.error(f'Element {locator} not found')
            return False
        try:
            field.clear()
            field.send_keys(word)
        except:
            logging.exception(f"Exception while operation with {locator}")
            return False
        return True

    def enter_login(self, word): #ввод логина
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_LOGIN_FIELD'], word,description='login form')

    def enter_pass(self, word): #ввод пароля
        self.enter_text_into_field(TestSearchLocators.ids["LOCATOR_PASS_FIELD"], word, description="password form")

    def input_title_post(self, post_title): #ввод название поста
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_TITLE_POST_CREATE'], post_title,
                                   description="Enter Post Title")

    def enter_description(self, post_description):
        self.enter_text_into_field(TestSearchLocators.ids["LOCATOR_NEW_POST_DESCRIPTION"], post_description,
                                   description="Enter Post Descriptionn")
    def input_name(self, contact_name):  # ввод имени в форму Contact us!
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_INPUT_NAME'], contact_name,
                                   description="Enter Contact Name")

    def input_email(self, contact_email):  # ввод email в форму Contact us!
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_INPUT_EMAIL'], contact_email,
                                   description="Enter Contact Email")

    def input_content(self, post_content):  # ввод content в форму Contact us!
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_INPUT_CONTENT'], post_content,
                                   description="Enter Post Content")



# методы get
    def get_text_from_element(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        field = self.find_element(locator, time=3)
        if not field:
            return None
        try:
            text = field.text
        except:
            logging.exception(f"Exception while get test from {element_name}")
            return None
        logging.debug(f'We find text {text} in field {element_name}')
        return text


       # функция, которая возвращает текст в элементе с ошибкой
    def get_error_text(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_ERROR_FIELD"], description="error")

    def get_blog(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_BLOG"], description="blog")

    def new_post(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_NEW_POST"],
                                          description="post title")


    def get_alert(self):
        logging.info("Get alert text")
        text = self.alert()
        logging.info(text)
        return text

    def get_allert_text(self):
        alert_text = self.switch_to_alert().text
        logging.info(f'We find text {alert_text} in title alert on site "Contact Us"')
        return alert_text

# методы click

    def click_button(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        button = self.find_element(locator)
        if not button:
            return False
        try:
            button.click()
        except:
            logging.exception("Exception with click")
            return False
        logging.debug(f"Clicked {element_name} button")
        return True


    def click_login_button(self):
        self.click_button(TestSearchLocators.ids["LOCATOR_LOGIN_BTN"], description="Click login button")
    def click_button_create_post(self): #нажатие кнопки создания поста странице Блог
        self.click_button(TestSearchLocators.ids["LOCATOR_BUTTON_POST_CREATE"], description="Click create post (+) button")

    def click_button_save_post(self): #нажатие кнопки сохранения поста на странице создания поста
        self.click_button(TestSearchLocators.ids["LOCATOR_BUTTON_SAVE_POST"], description='Click "SAVE" button')

    def click_contact(self): #нажатие Contact Us
        self.click_button(TestSearchLocators.ids["LOCATOR_BUTTON_CONTACT"], description='Click "contact" link')

    def click_button_contact_us(self):
        self.click_button(TestSearchLocators.ids["LOCATOR_BUTTON_CONTACT_US"], description='Click "CONTACT US" button')



#GET PROPERTY
    def get_email_label_color(self):
        email_label_color = self.get_element_property(TestSearchLocators.ids["LOCATOR_CONTACTUS_LABEL_EMAIL"], "color")
        logging.info(f'We find err color label {email_label_color} when entered not valid email')
        return email_label_color



def login():
    try:
        response = requests.post(testdata['url_login'],
                                 data={'username': testdata['login'], 'password': testdata['password']})
        if response.status_code == 200:
            return response.json()['token']
        else:
            logging.error(f"Error with login. Status code: {response.status_code}")
            return None
    except:
        logging.exception(f"Exception with login")
        return None

def get(token):
    try:
        resourсe = requests.get(testdata['url_posts'],
                            headers={'X-Auth-Token': token},
                            params={'owner': 'notMe'})
        if resourсe.status_code == 200:
            return resourсe.json()
        else:
            logging.error(f"Error with retrieving data. Status code: {resourсe.status_code}")
            return None
    except:
        logging.exception(f"Exception with get")
        return None

def post(token):
    try:
        new_post = requests.post(testdata['url_posts'],
                                data={'title': "Новый пост",
                                'description': "Мое первое автотестирование",
                                'content':"Добавить в задание с REST API еще один тест,\
                                        в котором создается новый пост,\
                                        а потом проверяется его наличие\
                                        на сервере по полю “описание"},
                                headers={'X-Auth-Token': token})
        if new_post.status_code == 200:
            return new_post.json()
        else:
            logging.error(f"Error with posting data. Status code: {new_post.status_code}")
            return None
    except:
        logging.exception(f"Exception with post")
        return None

def get_post(token):
    try:
        resourсe = requests.get(testdata['url_posts'],
                            headers={'X-Auth-Token': token})
        if resourсe.status_code == 200:
            return resourсe.json()
        else:
            logging.error(f"Error with retrieving data. Status code: {resourсe.status_code}")
            return None
    except Exception as e:
        logging.exception(f"Exception with get_post")
        return None