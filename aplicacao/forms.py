from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, PasswordField, SubmitField, SelectField, DecimalField, BooleanField, DateField, TextAreaField, IntegerField, RadioField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Regexp
from aplicacao.models import Funcionario
from datetime import datetime


class FormCriarConta(FlaskForm):
    nome = StringField('Nome: ', validators=[DataRequired(), Length(max=75)])
    email = StringField("Email", validators=[DataRequired(), Length(max=250), Regexp(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message="E-mail inválido")])
    telefone = StringField('Telefone: ',  validators=[DataRequired()])
    senha = PasswordField('Senha: ', validators=[DataRequired()])
    confirmacao_senha = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo("senha", message="Senhas não coincidem!")])
    botao_enviar = SubmitField('Criar Conta')

    def validate_email(self, email): 
        email = Usuario.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Erro! E-mail já utilizado!")
        
    def validate_senha(self, senha):
        if len(senha.data) < 8:
            raise ValidationError("A senha deve ter mais de 8 caracteres")
        
    def validate_senha(self, telefone):
        telefone = Usuario.query.filter_by(telefone=telefone.data).first()
        if telefone:
            raise ValidationError("Erro! Número de telefone já cadastrado")

funcionarios = Funcionario.query.all()

class FormBuscarHorarios(FlaskForm):
    funcionarios_disponiveis = RadioField('Com quem deseja marcar?', choices=[(funcionario.id, funcionario.nome) for funcionario in funcionarios], validators=[DataRequired()])
    data = DateField('Selecione a data', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now().date())
    botao_enviar = SubmitField('Buscar Horários')

    def validate_data(self, data):
        if data.data < datetime.now().date():
            flash('Data inválida!')
            raise ValidationError('Data inválida!')

class FormConfirmarHorario(FlaskForm):
    botao_confirmar = SubmitField('Confirmar horário')

class FormConfirmarAgendamento(FlaskForm):
    botao_agendar = SubmitField('Confirmar Agendamento')