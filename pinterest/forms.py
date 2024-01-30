from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from pinterest.models import Usuario
from pinterest import bcrypt

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirm = SubmitField('Fazer Login')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("Usuário inexistente, crie uma conta para continuar")
    
    def validate_senha(self, senha):
        usuario = Usuario.query.filter_by(email=self.email.data).first()
        if usuario and not bcrypt.check_password_hash(usuario.senha, senha.data):
            raise ValidationError('Senha incorreta. Verifique suas credenciais e tente novamente.')

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(7,25)])
    senha_confirm = PasswordField('Confirme sua Senha', validators=[DataRequired(), EqualTo('senha', message="As senhas não coincidem")])
    botao_confirm = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar")
        
    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError("Nome de Usuário já cadastrado, faça login para continuar")
    


class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirm = SubmitField("Enviar Foto")