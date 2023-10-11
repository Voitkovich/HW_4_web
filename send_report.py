import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import yaml
import datetime as DT

with open("/Users/portable/Desktop/For leaning/HW_4_api/testdata.yaml") as f:
    testdata = yaml.safe_load(f)

now = DT.datetime.now(DT.timezone.utc).astimezone()
time_format = "%Y-%m-%d %H:%M:%S"
reportname = f"report {now:{time_format}}.xml"

# Данные для отправки письма
sender_email = testdata['fromaddr_report']
print(sender_email, "sender_email")
recipient_email = testdata['toaddr_report']
print(recipient_email, "recipient_email")
subject = f"report {now:{time_format}}.xml"
message_body = 'Это тестовый отчет по ДЗ.'
filename = "log.txt"


# Создание объекта MIMEMultipart
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject

# Добавление текста сообщения
msg.attach(MIMEText(message_body, 'plain'))

# Добавляем файл во вложение
with open(filename, 'rb') as f:
    attach = MIMEBase('application', 'octet-stream')
    attach.set_payload(f.read())
    encoders.encode_base64(attach)
    attach.add_header('Content-Disposition', f'attachment; filename= {filename}')
    msg.attach(attach)

# Ввод пароля для почты отправителя
password = testdata['mail_password']

# Настройка SMTP-сервера Mail.ru
smtp_server = 'smtp.mail.ru'
smtp_port = 587  # Порт для шифрованного соединения (TLS)

try:
    # Создание объекта SMTP и установка соединения
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Включение шифрованного соединения

    # Вход в почтовый аккаунт
    server.login(sender_email, password)

    # Отправка письма
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print('Отчет успешно отправлен!')
except Exception as e:
    print(f'Ошибка: {str(e)}')
finally:
    server.quit()