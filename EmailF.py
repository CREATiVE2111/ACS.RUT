import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version

server = 'smtp.mail.ru'
user = 'udachainyou@mail.ru'
password = 'UHpsdBsQ1hN0mwiGQ9S0'
recipients = ['v.alesha_2004@mail.ru']
sender = 'udachainyou@mail.ru'
subject = 'Система контроля пропусков'
# html =  f"<html>" \
#             f"<head>" \
#             f"</head>" \
#             f"<body>" \
#                 f"<p>Здравствуйте, Алексей Василев</p>" \
#                 f"<p>Вы приобрели: {goods[ch]}</p>" \
#                 f"<p>Стоимость: {price[ch]} рублей</p>" \
#                 f"</body" \
#         f"</html>"
def send_message(name, dateS, dateE, purpose):
    html2 = "<html> <head> <style> " \
            ".status {color: black}" \
            ".price {color: red;font-weight: bold;}" \
            ".product {color: black;border-bottom: 1px dashed red;} " \
            "</style> </head>" + f'<body>' \
                    f'<p>Поступила новая заявка<br>{name}<br>Нуждается в пропуске с {dateS} по {dateE}<br>В связи с {purpose}</p>'\
                    f'</body>' \
                    f'</html>'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Pass System <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(html2, 'plain')
    part_html = MIMEText(html2, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()
    print(f"Sent successfully")


if __name__ == '__main__':
    send_message()