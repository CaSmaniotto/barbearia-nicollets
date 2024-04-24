from aplicacao import database, admin, login_manager
from flask_login import UserMixin, current_user
from datetime import datetime
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask import abort

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.filter_by(id=int(id_usuario)).first()

class Funcionario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False, unique=True)
    horario_inicio = database.Column(database.Time, nullable=False)
    horario_saida = database.Column(database.Time, nullable=False)
    almoco_inicio = database.Column(database.Time, nullable=False)
    almoco_saida = database.Column(database.Time, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    agendamentos = database.relationship("Agenda", backref="funcionario", lazy=True)

    def __repr__(self):
        return (self.nome)

class Barbearia(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False, unique=True)
    endereco = database.Column(database.String, nullable=False)
    cep = database.Column(database.String, nullable=False)
    cidade = database.Column(database.String, nullable=False)
    uf = database.Column(database.String, nullable=False)
    nota = database.Column(database.Numeric(precision=10, scale=1), nullable=False)

    def __repr__(self):
        return self.nome

class Agenda(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    servico_id = database.Column(database.Integer, database.ForeignKey('servico.id'))
    funcionario_id = database.Column(database.Integer, database.ForeignKey('funcionario.id'))
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'))
    data = database.Column(database.Date, nullable=False)
    hora_inicio = database.Column(database.Time, nullable=False)
    hora_termino = database.Column(database.Time, nullable=False)
    status = database.Column(database.String, nullable=False, default='Pendente')
    observacao = database.Column(database.String(40))

    def __repr__(self):
        return (str(self.id))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(75), nullable=False)
    email = database.Column(database.String(250), nullable=False, unique=True)
    telefone = database.Column(database.String(11), nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    permissao = database.Column(database.Integer, nullable=False, default=0)
    agendamentos = database.relationship("Agenda", backref="usuario", lazy=True)

    def __repr__(self):
        return (self.nome)

class Servico(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_servico = database.Column(database.String, nullable=False, unique=True)
    preco_servico = database.Column(database.Numeric(precision=10, scale=2), nullable=False)
    tempo = database.Column(database.Time, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    agendamentos = database.relationship("Agenda", backref="servico", lazy=True)

    def __repr__(self):
        return (self.nome_servico)
    

# modelos interface admin
class ControlAll(ModelView):

    def is_accessible(self):
        if not current_user.is_authenticated:
            return abort(403)
        elif current_user.permissao == 1:
            return True
        else: 
            return abort(403)
        
    def not_auth(self):
        return "acess denied!"

class ControlAgenda(ModelView):

    def is_accessible(self):
        if not current_user.is_authenticated:
            return abort(403)
        elif current_user.permissao == 1:
            return True
        else: 
            return abort(403)
        
    def not_auth(self):
        return "acess denied!"

    form_choices = {
        'status': [ ("Pendente","Pendente"), 
                    ("Concluído", "Concluído"),
                    ("Pendente", "Pendente")]
    }
    

#interface admin views
admin.add_view(ControlAll(Barbearia, database.session, name='Barbearia'))
admin.add_view(ControlAll(Funcionario, database.session, name='Funcionarios'))
admin.add_view(ControlAll(Usuario, database.session, name='Usuarios'))
admin.add_view(ControlAll(Servico, database.session, name='Servicos'))
admin.add_view(ControlAgenda(Agenda, database.session, name='Agenda'))
admin.add_link(MenuLink(name='Voltar', url='/'))
admin.add_link(MenuLink(name='Sair', url='/logout'))