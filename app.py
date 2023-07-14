from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.sqlite3'
db = SQLAlchemy(app)


class Tarefa(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tarefa = db.Column(db.String(50))
	descricao = db.Column(db.String(150))

	def __init__(self, tarefa, descricao):
		self.tarefa = tarefa
		self.descricao = descricao


@app.route('/')
def listar_tarefas():
	page = request.args.get('page', 1, type=int)
	per_page = 5
	todas_tarefas = Tarefa.query.paginate(page=page, per_page=per_page)
	return render_template("listar_tarefas.html", tarefas=todas_tarefas)


@app.route('/criar_tarefa', methods=["GET", "POST"])
def criar_tarefa():
	tarefa = request.form.get('tarefa')
	descricao = request.form.get('descricao')

	if request.method == 'POST':
		if not tarefa:
			flash('Digite um nome para a tarefa!', 'error')
		else:
			tarefa = Tarefa(tarefa.capitalize(), descricao.capitalize())
			db.session.add(tarefa)
			db.session.commit()
			return redirect(url_for('listar_tarefas'))
	return render_template('nova_tarefa.html')


@app.route('/<int:id>/atualiza_tarefa', methods=["GET", "POST"])
def atualiza_tarefa(id):
	tarefa = Tarefa.query.filter_by(id=id).first()
	if request.method == 'POST':
		tarefa = request.form['tarefa']
		descricao = request.form['descricao']
		Tarefa.query.filter_by(id=id).update({'tarefa': tarefa.capitalize(), 'descricao': descricao.capitalize()})
		db.session.commit()
		return redirect(url_for('listar_tarefas'))
	return render_template("atualiza_tarefa.html", tarefa=tarefa)


@app.route('/<int:id>/remove_tarefa')
def remove_tarefa(id):
	tarefa = Tarefa.query.filter_by(id=id).first()
	db.session.delete(tarefa)
	db.session.commit()
	return redirect(url_for('listar_tarefas'))


if __name__ == '__main__':
	app.app_context().push()
	db.create_all()
	app.run(debug=True)
