from flask import render_template, request, url_for, redirect, flash, session, abort
from aplicacao import app, database, bcrypt
from aplicacao.models import Servico, Funcionario, Barbearia, Agenda, Usuario
from datetime import datetime, timedelta
from aplicacao.forms import FormBuscarHorarios, FormConfirmarHorario, FormConfirmarAgendamento, FormCriarConta, FormLogin
from flask_login import login_required, login_user, logout_user, current_user

@app.errorhandler(403)
def access_denied(e):
    return redirect(url_for('home'))

@app.route('/')
def home():
    servicos = Servico.query.all()
    barbearia = Barbearia.query.first()
    nota = int(barbearia.nota)

    return render_template("home.html", servicos=servicos, barbearia=barbearia, nota=nota)

@app.route('/agendamento/<int:servico_id>', methods=['GET', 'POST'])
def agendamento(servico_id):

    if not current_user.is_authenticated:
        return redirect('/acessar')
    
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
            session['servico'] = servico.id

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

            return render_template("agendamento.html", form=form, form_confirmar_horario=form_confirmar_horario, lista_horarios=lista_horarios, servico=servico)

        if form_confirmar_horario.validate_on_submit():

            if 'horario' in request.form:
                data_horario = datetime.strptime(request.form['horario'], "%Y-%m-%d %H:%M:%S")

                if data_horario > datetime.now():
                    session['data'] = data_horario.strftime("%d %B, %Y")
                    session['horario'] = data_horario.strftime("%H:%M:%S")

                    return redirect(url_for('finish'))
                else:
                    flash("Horário inválido!")
                    return redirect(url_for('agendamento', servico_id=servico_id))
            else:
                return redirect(url_for('agendamento', servico_id=servico_id))

    return render_template("agendamento.html", form=form, servico=servico)

@app.route('/finish', methods=['GET', 'POST'])
@login_required
def finish():

    # session.pop('csrf_token', None)
    form = FormConfirmarAgendamento()

    usuario = Usuario.query.filter_by(id=session['usuario']).first()
    servico = Servico.query.filter_by(id=session['servico']).first()
    funcionario = Funcionario.query.filter_by(nome=session['funcionario']).first()

    session['email'] = usuario.email
    session['nome'] = usuario.nome
    session['telefone'] = usuario.telefone

    if form.validate_on_submit():

        horario_inicio = datetime.strptime(session['horario'],'%H:%M:%S')

        hora_termino = horario_inicio + timedelta(hours=servico.tempo.hour, minutes=servico.tempo.minute, seconds=servico.tempo.second)
        data = datetime.strptime(session['data'], '%d %B, %Y')


        novo_horario = Agenda(
                        servico_id=servico.id,
                        funcionario_id=funcionario.id,
                        usuario_id=current_user.id,
                        data=data,
                        hora_inicio=horario_inicio.time(),
                        hora_termino=hora_termino.time()
        )

        database.session.add(novo_horario)
        database.session.commit()

        flash("Seu horário foi agendado com sucesso!")
        return redirect("/")

    return render_template("finish.html", form=form, servico=servico)

@app.route('/acessar', methods=['GET', 'POST'])
def acessar():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == 'POST':

        if 'login' in request.form:
            return redirect('acessar/signin')
        elif 'register' in request.form:
            return redirect('acessar/signup')

    return render_template('sign.html')

@app.route('/acessar/signin', methods=['GET', 'POST'])
def signin():
    form = FormLogin()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            flash("Logado com sucesso")

            session['email'] = usuario.email
            session['nome'] = usuario.nome
            session['telefone'] = usuario.telefone
            session['usuario'] = usuario.id

            return redirect(url_for('home'))
        else:
            flash("Senha incorreta")
            return redirect("/acessar/signin")
    
    return render_template('sign.html', form=form)

@app.route('/acessar/signup', methods=['GET', 'POST'])
def signup():
    form_criar_conta = FormCriarConta()

    if form_criar_conta.validate_on_submit():
        hash = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')
        usuario = Usuario(
                    nome=form_criar_conta.nome.data,
                    email=form_criar_conta.email.data,
                    telefone=form_criar_conta.telefone.data,
                    senha=hash)
        
        database.session.add(usuario)
        database.session.commit()
        return redirect('/')

    return render_template('sign.html', form_criar_conta=form_criar_conta)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    flash("Saiu com sucesso!")
    return redirect(url_for('home'))


@app.route('/tasks')
@login_required
def tasks():

    if current_user.permissao != 1:
        return abort(403)

    hoje, proxima_semana = datas_da_semana()
    horarios_agendados = Agenda.query.filter(Agenda.data.between(hoje, proxima_semana)).order_by(Agenda.data).all()
    return render_template("tasks.html", horarios_agendados=horarios_agendados)

def datas_da_semana():
    hoje = datetime.today().date()
    proxima_semana = hoje + timedelta(days=7)
    return hoje, proxima_semana

@app.route('/dashboard')
@login_required
def dashboard():

    if current_user.permissao != 1:
        return abort(403)
    
    return render_template('dashboard.html')