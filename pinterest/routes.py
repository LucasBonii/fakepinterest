from flask import render_template, url_for, redirect, flash
from pinterest import app, database, bcrypt
from flask_login import login_required, logout_user, login_user, current_user
from pinterest.forms import FormCriarConta, FormLogin, FormFoto
from pinterest.models import Usuario, Post
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["POST", "GET"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email = formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), formlogin.senha.data):
            bcrypt.check_password_hash(usuario.senha, formlogin.senha.data)
            login_user(usuario)
            return redirect(url_for("pageperfil", id_usuario = usuario.id))
        else:
            formlogin.senha.errors.append("Senha incorreta. Verifique suas credenciais e tente novamente.")
    return render_template("homepage.html", form=formlogin)


@app.route("/criar-conta", methods=["POST", "GET"])
def criar_conta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha_cryp = bcrypt.generate_password_hash(formcriarconta.senha.data).decode("utf-8")
        usuario = Usuario(username= formcriarconta.username.data , senha= senha_cryp,
                          email = formcriarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("pageperfil", id_usuario = usuario.id))
    return render_template('criar_conta.html', form=formcriarconta)


@app.route('/perfil/<id_usuario>', methods=["GET", "POST"])
@login_required
def pageperfil(id_usuario):
    if int(current_user.id) == int(id_usuario):
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            safe_name = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], safe_name)
            arquivo.save(caminho)
            foto = Post(imagem=safe_name, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            return redirect(url_for('pageperfil', id_usuario=id_usuario))
        return render_template('perfil.html', usuario=current_user, form=formfoto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route('/feed')
@login_required
def feed():
    fotos = Post.query.order_by(Post.data_post.desc()).all()
    return render_template("feed.html", fotos=fotos)