# import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from aplicacao import sg

def sendgrid_mail(email_para, mensagem, titulo):
    message = Mail(
        from_email = 'smaniottocaetano@gmail.com', # remetente -> sender configurado no site da api (sendgrid)
        to_emails = email_para,
        subject = mensagem,
        html_content = titulo)
    
    # copia = "itsupport@email.com"
    # message.add_cc(copia)
    
    try:
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)