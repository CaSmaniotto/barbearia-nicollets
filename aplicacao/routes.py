from flask import render_template, request, url_for, redirect, flash, session, abort, jsonify
from aplicacao import app
from aplicacao.models import Servico, Funcionario, Barbearia, Agenda
from datetime import datetime, timedelta
from aplicacao.forms import FormBuscarHorarios, FormConfirmarHorario, FormConfirmarAgendamento

@app.route('/')
def home():
    servicos = Servico.query.all()
    barbearia = Barbearia.query.first()
    nota = int(barbearia.nota)

    return render_template("home.html", servicos=servicos, barbearia=barbearia, nota=nota)

@app.route('/agendamento/<int:servico_id>', methods=['GET', 'POST'])
def agendamento(servico_id):
    servico = Servico.query.filter_by(id=servico_id).first()

    form = FormBuscarHorarios()
    form_confirmar_horario = FormConfirmarHorario()

    lista_horarios = []

    horarios_validos = []
    
    if request.method == 'POST':
        if form.validate_on_submit():

            agenda = Agenda.query.filter_by(data=form.data.data, funcionario_id=int(form.funcionarios_disponiveis.data)).all()
            
            funcionario = Funcionario.query.filter_by(id=int(form.funcionarios_disponiveis.data)).first()

            session['funcionario'] = funcionario.nome
            session['servico'] = servico.nome_servico

            horario_atual = datetime.combine(form.data.data, funcionario.horario_inicio)
            horario_saida = datetime.combine(form.data.data, funcionario.horario_saida)
            almoco_saida = datetime.combine(form.data.data, funcionario.almoco_saida)
            almoco_entrada = datetime.combine(form.data.data, funcionario.almoco_inicio)

            total_minutos = servico.tempo.hour * 60 + servico.tempo.minute
            tempo_servico = timedelta(minutes=total_minutos)

            # Realize o loop enquanto o horário atual for menor que o horário de saída
            while ((horario_atual + tempo_servico) < horario_saida):

                if ((horario_atual + tempo_servico) <= almoco_entrada):
                    lista_horarios.append(horario_atual)
                    horario_atual += tempo_servico
                elif (horario_atual >= almoco_saida):
                    lista_horarios.append(horario_atual)
                    horario_atual += tempo_servico
                else:
                    horario_atual = almoco_saida
                    lista_horarios.append(horario_atual)
                    horario_atual += tempo_servico


            for i in agenda:
                agenda_inicio = datetime.combine(i.data, i.hora_inicio)
                agenda_termino = datetime.combine(i.data, i.hora_termino)
                total_minutos = i.servico.tempo.hour * 60 + i.servico.tempo.minute
                tempo_servico = timedelta(minutes=total_minutos)

                for horario in lista_horarios:
                    if (agenda_inicio == horario):
                        continue
                    elif ((horario >= agenda_inicio) and (horario < agenda_termino)):
                        continue
                    else:
                        horarios_validos.append(horario)
                
                lista_horarios = horarios_validos

            lista_horarios = [(item.strftime("%Y-%m-%d"), item.strftime("%H:%M:%S")) for item in lista_horarios]

            return render_template("agendamento.html", form=form, form_confirmar_horario=form_confirmar_horario, lista_horarios=lista_horarios)

        elif form_confirmar_horario.validate_on_submit():

            if 'horario' in request.form:
                data_horario = datetime.strptime(request.form['horario'], '%Y-%m-%d %H:%M:%S')

                session['data'] = data_horario.strftime("%d %B, %Y")
                session['horario'] = data_horario.strftime("%H:%M")

                return redirect(url_for('finish'))
            else:
                return redirect(url_for('agendamento', servico_id=servico_id))

    return render_template("agendamento.html", form=form)

@app.route('/finish', methods=['GET', 'POST'])
def finish():

    session.pop('csrf_token', None)

    form = FormConfirmarAgendamento()

    if request.method == 'POST':
        session.clear()
        return redirect("/")

    return render_template("finish.html", form=form)