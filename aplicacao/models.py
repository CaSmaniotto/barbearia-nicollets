from aplicacao import database, admin
from flask_login import UserMixin, current_user
from datetime import datetime
from flask_admin.contrib.sqla import ModelView

class Barbearia(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False, unique=True)
    endereço = database.Column(database.String, nullable=False, unique=True)
    cep = database.Column(database.String, nullable=False, unique=True)
    cidade = database.Column(database.String, nullable=False, unique=True)
    uf = database.Column(database.String, nullable=False, unique=True)
    nota = database.Column(database.Numeric(precision=10, scale=1), nullable=False)

class Agenda(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    servico_id = database.Column(database.Integer, database.ForeignKey('servico.id'))
    funcionario_id = database.Column(database.Integer, database.ForeignKey('funcionario.id'))
    data = database.Column(database.Date, nullable=False)
    hora_inicio = database.Column(database.Time, nullable=False)
    hora_termino = database.Column(database.Time, nullable=False)
    nome_cliente = database.Column(database.String, nullable=False)
    contato_cliente = database.Column(database.String, nullable=False)
    status = database.Column(database.String, nullable=False)

class Servico(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_servico = database.Column(database.String, nullable=False, unique=True)
    preco_servico = database.Column(database.Numeric(precision=10, scale=2), nullable=False)
    tempo = database.Column(database.Time, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    agendamentos = database.relationship("Agenda", backref="servico", lazy=True)

    def __repr__(self):
        return (self.nome_servico)
    
class Funcionario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False, unique=True)
    horario_inicio = database.Column(database.Time, nullable=False)
    horario_saida = database.Column(database.Time, nullable=False)
    almoco_inicio = database.Column(database.Time, nullable=False)
    almoco_saida = database.Column(database.Time, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return (self.id)
    
admin.add_view(ModelView(Barbearia, database.session, name='Barbearia'))
admin.add_view(ModelView(Funcionario, database.session, name='Funcionarios'))
admin.add_view(ModelView(Servico, database.session, name='Servicos'))
admin.add_view(ModelView(Agenda, database.session, name='Agenda'))