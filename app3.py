'''
static
    css
        style.css
templates




.gitignore
app.py
ipma.py
'''
#----------------------------------------------------------

from flask import Flask, render_template, redirect, url_for, request,flash,render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,PasswordField
from wtforms.validators import DataRequired, NumberRange,EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,LoginManager,login_user,login_required,logout_user,current_user

#----------------------------------------------------------

class JogoForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    plataforma = StringField('Plataforma', validators=[DataRequired()])
    ano = IntegerField('Ano', validators=[NumberRange(min=1500, max=2100)])
    submeter = SubmitField('Gravar')

class LoginForm(FlaskForm):
    username = StringField('Utilizador', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submeter = SubmitField('Entrar')

class RegistoForm(FlaskForm):
    username = StringField('Utilizador', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmar = PasswordField('Confirmar Password', validators=[EqualTo('password')])
    submeter = SubmitField('Registar')

#----------------------------------------------------------

db = SQLAlchemy()

class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)

class Utilizador(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')


    def check_password(self, password):
        # ERRO: faltava passar o self.password_hash como parametro
        return check_password_hash(self.password_hash, password)

#----------------------------------------------------------

def html(t):
    base='''
<!DOCTYPE html>
<html lang="pt">
'''
    base+='''
<style>

.container {
    width: 70%;
    margin: 50px auto;
    /* text-align: center; */
    /* border: 1px dashed black; */
    font-family: Arial, Helvetica, sans-serif;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nav {
    display: flex;
    gap: 20px;
}

.nav a {
    text-decoration: none;
    background-color: cornflowerblue;
    padding: 4px 15px;
    color: white;
    border-radius: 2px;
}

table {
    width: 70%;
    /* margin: 50px; */
    /* text-align: center; */
    /* border: 1px solid black; */
}

td {
    background-color: rgb(246, 246, 246);
    border-left: 5px solid cornflowerblue;
    padding: 10px;
    text-align: left;
    display: flex;
    width: 100%;
    justify-content: space-between;
    margin-bottom: 15px;
}

td a {
    text-decoration: none;

}

i {
    margin-left: 10px;
}

.editar-apagar {
    display: inline-block;
    margin-right: 10px;
}

input[type="text"], 
input[type="number"] {
    width: 300px;
}

.form-adicionar,
.form-editar {
    width: 60%;
}

.form-adicionar label,
.form-editar label {
    display: block;
    text-align: left;
}

.form-adicionar input,
.form-editar input {
    width: 100%;
    border: none;
    border-bottom: 1px solid black;
    outline: none;
}

.form-adicionar input[type="submit"], 
.form-editar input[type="submit"] {
    width: 100px;
    margin-top: 25px;
    background-color: orange;
    color: white;
    padding: 6px 15px;
    border: none;
    font-weight: bold;
    border-radius: 2px;
    font-size: 16px;
}

</style>
'''
    base+='''
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>{% block titulo %} Lista de Jogos {% endblock %}</title>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" integrity="sha512-Evv84Mr4kqVGRNSgIGL/F/aIDqQb7xQ2vcrdIwxfjThSH8CSR7PBEakCr51Ck+w+/U6swU2Im1vVX0SVk9ABhg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Lista de Jogos</h1>
            <div class="nav">
                {% if current_user.is_authenticated %}
                Olá {{ current_user.username }}
                    <a href="{{ url_for('listar')}}">Listar</a>
                    <a href="{{ url_for('adicionar')}}">Adicionar</a>
                    <a href="{{ url_for('logout')}}">Logout</a>
                {% else %}
                    <a href="{{ url_for('login')}}">Login</a>
                    <a href="{{ url_for('registo')}}">Registo</a>
                {% endif %}
            </div>
        </div>
        <hr>
'''

    if t=='adicionar':
        base+='''
        <h2>{% if request.endpoint == 'adicionar' %} Adicionar {% else %} Editar {% endif %} Jogo</h2>
        <form class="form-adicionar" action="" method="post">
            {{form.hidden_tag()}}
            <p>{{ form.titulo.label }} {{ form.titulo() }}</p>
            <p>{{ form.plataforma.label }} {{ form.plataforma() }}</p>
            <p>{{ form.ano.label }}  {{ form.ano() }}</p>
            <p>{{ form.submeter() }}</p>
        </form>
        '''
    if t=='listar':
        base+='''
        <h2>Lista de Jogos</h2>
        <table>
            {% for jogo in jogos %}
            <tr>
                <td>{{ jogo.titulo }} - {{ jogo.plataforma }}  ({{ jogo.ano }}) <span class="editar-apagar"> <a href="{{url_for('editar', id=jogo.id)}}"><i style="color: rgb(2, 77, 2);" class="fa-regular fa-pen-to-square"></i></a>   <a href="{{url_for('apagar', id=jogo.id)}}"><i style="color: darkred;" class="fa-solid fa-trash"></i></a> </span>
                </td>
            </tr>
            {% endfor %}
        </table>
        '''
    if t=='editar':
        base+='''
        <h2>Editar jogo</h2>

        <form class="form-editar" action="" method="POST">
            {{form.hidden_tag()}}

            <p>
                {{ form.titulo.label }} <br>
                {{ form.titulo(size=40) }} <br>

                {% for error in form.titulo.errors %}
                    <span style="color:red;">{{ error }}</span>
                {% endfor %}
            </p>
            <p>
                {{ form.plataforma.label }} <br>
                {{ form.plataforma(size=40) }} <br>

                {% for error in form.plataforma.errors %}
                    <span style="color:red;">{{ error }}</span>
                {% endfor %}
            </p>
            <p>
                {{ form.ano.label }} <br>
                {{ form.ano(size=40) }} <br>

                {% for error in form.ano.errors %}
                    <span style="color:red;">{{ error }}</span>
                {% endfor %}
            </p>

            <p>{{ form.submeter() }}</p>

        </form>
        '''
    if t=='login':
        base+='''
        <form action="" method="POST">
            <h2>Login</h2>
            {{form.hidden_tag()}}
            <p>{{ form.username.label}} {{form.username()}}</p>
            <p>{{ form.password.label}} {{form.password()}}</p>

            {% if form.confirmar %}
                <p>{{ form.confirmar.label}} {{form.confirmar()}}</p>
            {% endif %}

            <p>{{ form.submeter()}}</p>
        </form>
        '''
    if t=='registo':
        base+='''
        <form action="" method="POST">
            {{ form.hidden_tag() }} <!-- o token CSRF é enviado -->
            <h2>Registo</h2>
        
            <p>{{ form.username.label }} <br>
                {{ form.username(size=40) }} <br>
                {% for error in form.username.errors %}
                    <span style="color:red;">{{ error }}</span>
                {% endfor %}
            </p>
            <p>{{ form.password.label }} <br>
                {{ form.password(size=40) }} <br>
                {% for error in form.password.errors %}
                    <span style="color:red;">{{ error }}</span>
                {% endfor %}
            </p>
            <p>{{ form.confirmar.label }} <br>
                {{ form.confirmar(size=40) }} <br>
                {% for error in form.confirmar.errors %}
                    <span style="color:red;">{{ error }}</span>
                {% endfor %}
            </p>
            <p>{{ form.submeter() }}</p>
        </form>
        '''

    base+='''
    </div>
</body>
</html>
'''

    return base

#----------------------------------------------------------

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.secret_key = 'segredomuitobemguardado'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Utilizador.query.get(int(user_id))

@app.before_request
def criar_bd():
    db.create_all()

#----------------------------------------------------------

@app.route('/')
def index():
    return redirect(url_for('listar'))

@app.route('/jogos')
@login_required
def listar():
    jogos = Jogo.query.all()
    return render_template_string(html('listar'), jogos=jogos)

@app.route('/jogos/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():
    form = JogoForm()
    if form.validate_on_submit():
        jogo = Jogo(titulo=form.titulo.data, plataforma=form.plataforma.data, ano=form.ano.data)
        db.session.add(jogo)
        db.session.commit()
        return redirect(url_for('listar'))
    return render_template_string(html('adicionar'), form=form)

@app.route('/jogos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    jogo = Jogo.query.get_or_404(id)
    form = JogoForm(obj=jogo)
    if form.validate_on_submit():
        form.populate_obj(jogo)
        db.session.commit()
        return redirect(url_for('listar'))
    return render_template_string(html('editar'), form=form)

@app.route('/jogos/apagar/<int:id>')
@login_required
def apagar(id):
    jogo = Jogo.query.get_or_404(id)
    db.session.delete(jogo)
    db.session.commit()
    return redirect(url_for('listar'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilizador.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        return "Login inválido. Tente novamente!"
    return render_template_string(html('login'), form=form)


@app.route('/registo', methods=['GET', 'POST'])
def registo():
    form = RegistoForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        if not username or not password:
            flash("Preencha todos os campos corretamente.", "erro")
            return render_template_string(html('registo'), form=form)

        if Utilizador.query.filter_by(username=username).first():
            flash("O utilizador já existe, escolha outro nome.", "erro")
            return render_template_string(html('registo'), form=form)

        novo_utilizador = Utilizador(username=username)
        novo_utilizador.set_password(password)
        db.session.add(novo_utilizador)
        db.session.commit()
        flash("Registo efetuado com sucesso!", "sucesso")
        return redirect(url_for('login'))

    return render_template_string(html('registo'), form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#----------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)

#----------------------------------------------------------
