# import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from aplicacao import sg, database
from aplicacao.models import Agenda, Servico
from sqlalchemy import func, extract
from datetime import datetime
from collections import defaultdict

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

def calcular_somas_por_mes(ano):
    # Dicionário para armazenar as somas dos valores dos serviços por mês
    somas_por_mes = {}

    # Loop pelos meses do ano
    for mes in range(1, 13):
        # Consulta para somar os valores dos serviços concluídos para o mês atual
        soma_mes = database.session.query(
            func.sum(Servico.preco_servico)  # Soma os valores dos serviços
        ).join(
            Agenda, Servico.id == Agenda.servico_id
        ).filter(
            Agenda.status == 'Concluído',  # Filtra apenas os registros com status "Concluído"
            extract('year', Agenda.data) == ano,  # Filtra o ano especificado
            extract('month', Agenda.data) == mes  # Filtra o mês atual
        ).scalar() or 0  # Retorna 0 se a soma for None

        # Atribui a soma ao mês correspondente no dicionário
        nome_mes = datetime(ano, mes, 1).strftime('%B').lower().capitalize()  # Obtém o nome do mês em minúsculas
        somas_por_mes[nome_mes] = soma_mes

    return somas_por_mes

def total_clientes_mes(ano):
    total_mes = defaultdict(int)  # Cria um defaultdict com valor padrão 0

    resultados = database.session.query(
        extract('month', Agenda.data).label('mes'),  # Extrai o mês da data
        func.count(Agenda.id).label('total_clientes')  # Conta o número de clientes
    ).filter(
        extract('year', Agenda.data) == ano  # Filtra o ano especificado
    ).group_by(extract('month', Agenda.data)).all()  # Agrupa os resultados por mês

    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    for resultado in resultados:
        nome_mes = meses[resultado.mes]
        total_mes[nome_mes] = resultado.total_clientes

    # Preenche os meses ausentes com o valor 0
    for mes in meses.values():
        if mes not in total_mes:
            total_mes[mes] = 0

    return total_mes
