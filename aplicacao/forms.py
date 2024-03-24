from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, PasswordField, SubmitField, SelectField, DecimalField, BooleanField, DateField, TextAreaField, IntegerField, RadioField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Regexp
from aplicacao.models import Funcionario
from datetime import datetime


funcionarios = Funcionario.query.all()

class FormBuscarHorarios(FlaskForm):
    funcionarios_disponiveis = RadioField('Com quem deseja marcar?', choices=[(funcionario.id, funcionario.nome) for funcionario in funcionarios], validators=[DataRequired()])
    data = DateField('Selecione a data', format='%Y-%m-%d', validators=[DataRequired()])
    botao_enviar = SubmitField('Buscar Horários')

    def validate_data(self, data):
        if data.data < datetime.now().date():
            flash('A data selecionada não pode ser anterior à data atual.')
            raise ValidationError('A data selecionada não pode ser anterior à data atual.')

class FormConfirmarHorario(FlaskForm):
    botao_confirmar = SubmitField('Confirmar horário')

class FormConfirmarAgendamento(FlaskForm):
    botao_agendar = SubmitField('Confirmar Agendamento')