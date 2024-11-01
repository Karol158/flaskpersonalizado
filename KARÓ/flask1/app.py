import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "musicadatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Musica(db.Model):
    titulo = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Título: {}>".format(self.titulo)
    
with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            musica = Musica(titulo=request.form.get("title"))
            db.session.add(musica)
            db.session.commit()
        except Exception as e:
            print("Falha ao adicionar a música:", e)

    musicas = Musica.query.all()
    return render_template("index.html", musicas=musicas)

@app.route("/update", methods=["GET", "POST"])
def update():
    musicas = Musica.query.all()
    if request.method == "POST":
        try:
            titulo_antigo = request.form.get("oldtitle")
            novo_titulo = request.form.get("newtitle")
            musica = Musica.query.filter_by(titulo=titulo_antigo).first()
            if musica:
                musica.titulo = novo_titulo
                db.session.commit()
                mensagem = "O título da música foi atualizado com sucesso!"
            else:
                mensagem = "Música não encontrada."
        except Exception as e:
            print("Erro ao atualizar o título da música:", e)
            mensagem = "Erro ao atualizar a música."
        return render_template("update.html", musicas=musicas, mensagem=mensagem)

    return render_template("update.html", musicas=musicas)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    musicas = Musica.query.all()
    if request.method == "POST":
        titulo = request.form.get("title")
        musica = Musica.query.filter_by(titulo=titulo).first()
        
        if musica:
            db.session.delete(musica)
            db.session.commit()
            mensagem = "A música foi deletada com sucesso!"
        else:
            mensagem = "Música não encontrada."
        
        return render_template("delete.html", musicas=musicas, mensagem=mensagem)

    return render_template("delete.html", musicas=musicas)

if __name__ == "__main__":
    app.run(debug=True)
