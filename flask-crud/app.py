import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-in-production'
# In-memory DB for runtime-only storage
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pessoa(db.Model):
    __tablename__ = 'pessoas'
    nomeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), nullable=False, unique=True)

    def __repr__(self):
        return f"<Pessoa {self.nomeId} - {self.nome}>"


@app.route('/')
def index():
    q = request.args.get('q', '').strip()
    if q:
        like = f"%{q.lower()}%"
        pessoas = Pessoa.query.filter(
            func.lower(Pessoa.nome).like(like) | func.lower(Pessoa.email).like(like)
        ).order_by(Pessoa.nome.asc()).all()
    else:
        pessoas = Pessoa.query.order_by(Pessoa.nome.asc()).all()
    return render_template('index.html', pessoas=pessoas, q=q)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        if not nome or not email:
            flash('Nome e e-mail são obrigatórios.', 'danger')
            return redirect(url_for('create'))
        # Check duplicate email
        if Pessoa.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'warning')
            return redirect(url_for('create'))
        p = Pessoa(nome=nome, email=email)
        db.session.add(p)
        db.session.commit()
        flash('Registro criado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('form.html', action='create', pessoa=None)

@app.route('/edit/<int:nomeId>', methods=['GET', 'POST'])
def edit(nomeId):
    p = Pessoa.query.get_or_404(nomeId)
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        if not nome or not email:
            flash('Nome e e-mail são obrigatórios.', 'danger')
            return redirect(url_for('edit', nomeId=nomeId))
        # Enforce unique email except self
        existing = Pessoa.query.filter(Pessoa.email==email, Pessoa.nomeId!=nomeId).first()
        if existing:
            flash('E-mail já cadastrado para outro registro.', 'warning')
            return redirect(url_for('edit', nomeId=nomeId))
        p.nome = nome
        p.email = email
        db.session.commit()
        flash('Registro atualizado!', 'success')
        return redirect(url_for('index'))
    return render_template('form.html', action='edit', pessoa=p)

@app.route('/delete/<int:nomeId>', methods=['POST'])
def delete(nomeId):
    p = Pessoa.query.get_or_404(nomeId)
    db.session.delete(p)
    db.session.commit()
    flash('Registro removido!', 'info')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Host 0.0.0.0 for Docker access, port from env or default 5000
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
