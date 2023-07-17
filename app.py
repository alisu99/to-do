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




if __name__ == '__main__':
	app.app_context().push()
	db.create_all()
	app.run(debug=True)
