import os
import sqlite3

from flask import (Flask, flash, g, jsonify, redirect, render_template,
                   request, url_for)

from algoritmos import busca_por_nome, ordenar_por_nome

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "vacinafacil.db")


# ---------------------------------------------------------------------------
# Banco de dados (UC32)
# ---------------------------------------------------------------------------
def get_db():
    """Abre (uma vez por requisição) a conexão com o SQLite."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def fechar_db(erro=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria as tabelas (se não existirem) e insere vacinas de exemplo."""
    db = sqlite3.connect(DATABASE)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            telefone TEXT
        );

        CREATE TABLE IF NOT EXISTS vacinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            fabricante TEXT,
            doses_total INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS aplicacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            vacina_id INTEGER NOT NULL,
            data_aplicacao TEXT NOT NULL,
            dose TEXT NOT NULL,
            lote TEXT,
            observacoes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
            FOREIGN KEY (vacina_id) REFERENCES vacinas (id) ON DELETE CASCADE
        );
        """
    )
    if db.execute("SELECT COUNT(*) FROM vacinas").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO vacinas (nome, fabricante, doses_total) VALUES (?, ?, ?)",
            [
                ("Hepatite B", "Butantan", 3),
                ("Influenza (Gripe)", "Butantan", 1),
                ("Tríplice Viral", "Bio-Manguinhos", 2),
                ("Dupla Adulto (dT)", "Serum Institute", 3),
            ],
        )
    db.commit()
    db.close()


# Roda ao importar o módulo, assim funciona também no gunicorn (Render)
init_db()


# ---------------------------------------------------------------------------
# Página inicial
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    db = get_db()
    totais = {
        "pacientes": db.execute("SELECT COUNT(*) FROM pacientes").fetchone()[0],
        "vacinas": db.execute("SELECT COUNT(*) FROM vacinas").fetchone()[0],
        "aplicacoes": db.execute("SELECT COUNT(*) FROM aplicacoes").fetchone()[0],
    }
    # JOIN + ORDER BY: últimas 5 aplicações
    recentes = db.execute(
        """
        SELECT a.data_aplicacao, a.dose, p.nome AS paciente, v.nome AS vacina
        FROM aplicacoes a
        JOIN pacientes p ON p.id = a.paciente_id
        JOIN vacinas v ON v.id = a.vacina_id
        ORDER BY a.data_aplicacao DESC, a.id DESC
        LIMIT 5
        """
    ).fetchall()
    return render_template("index.html", totais=totais, recentes=recentes)


# ---------------------------------------------------------------------------
# Pacientes (CRUD)
# ---------------------------------------------------------------------------
def ler_paciente_do_form():
    return {
        "nome": request.form.get("nome", "").strip(),
        "data_nascimento": request.form.get("data_nascimento", "").strip(),
        "telefone": request.form.get("telefone", "").strip(),
    }


@app.route("/pacientes")
def listar_pacientes():
    busca = request.args.get("busca", "").strip()
    linhas = get_db().execute("SELECT * FROM pacientes").fetchall()
    pacientes = [dict(l) for l in linhas]
    if busca:
        pacientes = busca_por_nome(pacientes, busca)  # busca sequencial (UC30)
    pacientes = ordenar_por_nome(pacientes)  # insertion sort (UC30)
    return render_template("pacientes.html", pacientes=pacientes, busca=busca)


@app.route("/pacientes/novo", methods=["GET", "POST"])
def novo_paciente():
    if request.method == "POST":
        dados = ler_paciente_do_form()
        if not dados["nome"] or not dados["data_nascimento"]:
            flash("Nome e data de nascimento são obrigatórios.", "erro")
            return render_template("paciente_form.html", paciente=dados)
        db = get_db()
        db.execute(
            "INSERT INTO pacientes (nome, data_nascimento, telefone) VALUES (?, ?, ?)",
            (dados["nome"], dados["data_nascimento"], dados["telefone"]),
        )
        db.commit()
        flash("Paciente cadastrado com sucesso!", "ok")
        return redirect(url_for("listar_pacientes"))
    return render_template("paciente_form.html", paciente=None)


@app.route("/pacientes/<int:id>/editar", methods=["GET", "POST"])
def editar_paciente(id):
    db = get_db()
    paciente = db.execute("SELECT * FROM pacientes WHERE id = ?", (id,)).fetchone()
    if paciente is None:
        flash("Paciente não encontrado.", "erro")
        return redirect(url_for("listar_pacientes"))
    if request.method == "POST":
        dados = ler_paciente_do_form()
        if not dados["nome"] or not dados["data_nascimento"]:
            flash("Nome e data de nascimento são obrigatórios.", "erro")
            dados["id"] = id
            return render_template("paciente_form.html", paciente=dados)
        db.execute(
            "UPDATE pacientes SET nome = ?, data_nascimento = ?, telefone = ? WHERE id = ?",
            (dados["nome"], dados["data_nascimento"], dados["telefone"], id),
        )
        db.commit()
        flash("Paciente atualizado!", "ok")
        return redirect(url_for("listar_pacientes"))
    return render_template("paciente_form.html", paciente=paciente)


@app.route("/pacientes/<int:id>/excluir", methods=["POST"])
def excluir_paciente(id):
    db = get_db()
    db.execute("DELETE FROM pacientes WHERE id = ?", (id,))
    db.commit()
    flash("Paciente excluído (e suas aplicações também).", "ok")
    return redirect(url_for("listar_pacientes"))


# ---------------------------------------------------------------------------
# Vacinas (CRUD)
# ---------------------------------------------------------------------------
def ler_vacina_do_form():
    try:
        doses = int(request.form.get("doses_total", "1"))
    except ValueError:
        doses = 0
    return {
        "nome": request.form.get("nome", "").strip(),
        "fabricante": request.form.get("fabricante", "").strip(),
        "doses_total": doses,
    }


@app.route("/vacinas")
def listar_vacinas():
    vacinas = get_db().execute("SELECT * FROM vacinas ORDER BY nome").fetchall()
    return render_template("vacinas.html", vacinas=vacinas)


@app.route("/vacinas/nova", methods=["GET", "POST"])
def nova_vacina():
    if request.method == "POST":
        dados = ler_vacina_do_form()
        if not dados["nome"] or dados["doses_total"] < 1:
            flash("Informe o nome e um número de doses maior que zero.", "erro")
            return render_template("vacina_form.html", vacina=dados)
        db = get_db()
        db.execute(
            "INSERT INTO vacinas (nome, fabricante, doses_total) VALUES (?, ?, ?)",
            (dados["nome"], dados["fabricante"], dados["doses_total"]),
        )
        db.commit()
        flash("Vacina cadastrada!", "ok")
        return redirect(url_for("listar_vacinas"))
    return render_template("vacina_form.html", vacina=None)


@app.route("/vacinas/<int:id>/editar", methods=["GET", "POST"])
def editar_vacina(id):
    db = get_db()
    vacina = db.execute("SELECT * FROM vacinas WHERE id = ?", (id,)).fetchone()
    if vacina is None:
        flash("Vacina não encontrada.", "erro")
        return redirect(url_for("listar_vacinas"))
    if request.method == "POST":
        dados = ler_vacina_do_form()
        if not dados["nome"] or dados["doses_total"] < 1:
            flash("Informe o nome e um número de doses maior que zero.", "erro")
            dados["id"] = id
            return render_template("vacina_form.html", vacina=dados)
        db.execute(
            "UPDATE vacinas SET nome = ?, fabricante = ?, doses_total = ? WHERE id = ?",
            (dados["nome"], dados["fabricante"], dados["doses_total"], id),
        )
        db.commit()
        flash("Vacina atualizada!", "ok")
        return redirect(url_for("listar_vacinas"))
    return render_template("vacina_form.html", vacina=vacina)


@app.route("/vacinas/<int:id>/excluir", methods=["POST"])
def excluir_vacina(id):
    db = get_db()
    db.execute("DELETE FROM vacinas WHERE id = ?", (id,))
    db.commit()
    flash("Vacina excluída (e suas aplicações também).", "ok")
    return redirect(url_for("listar_vacinas"))


# ---------------------------------------------------------------------------
# Aplicações (CRUD com JOIN, WHERE e ORDER BY)
# ---------------------------------------------------------------------------
def ler_aplicacao_do_form():
    return {
        "paciente_id": request.form.get("paciente_id", "").strip(),
        "vacina_id": request.form.get("vacina_id", "").strip(),
        "data_aplicacao": request.form.get("data_aplicacao", "").strip(),
        "dose": request.form.get("dose", "").strip(),
        "lote": request.form.get("lote", "").strip(),
        "observacoes": request.form.get("observacoes", "").strip(),
    }


def opcoes_formulario():
    db = get_db()
    pacientes = db.execute("SELECT id, nome FROM pacientes ORDER BY nome").fetchall()
    vacinas = db.execute("SELECT id, nome FROM vacinas ORDER BY nome").fetchall()
    return pacientes, vacinas


@app.route("/aplicacoes")
def listar_aplicacoes():
    vacina_id = request.args.get("vacina_id", "").strip()
    db = get_db()

    sql = """
        SELECT a.id, a.data_aplicacao, a.dose, a.lote, a.observacoes,
               p.nome AS paciente, v.nome AS vacina
        FROM aplicacoes a
        JOIN pacientes p ON p.id = a.paciente_id
        JOIN vacinas v ON v.id = a.vacina_id
    """
    parametros = []
    if vacina_id.isdigit():
        sql += " WHERE a.vacina_id = ?"
        parametros.append(int(vacina_id))
    sql += " ORDER BY a.data_aplicacao DESC, a.id DESC"

    aplicacoes = db.execute(sql, parametros).fetchall()
    vacinas = db.execute("SELECT id, nome FROM vacinas ORDER BY nome").fetchall()
    return render_template(
        "aplicacoes.html",
        aplicacoes=aplicacoes,
        vacinas=vacinas,
        vacina_id=vacina_id,
    )


@app.route("/aplicacoes/nova", methods=["GET", "POST"])
def nova_aplicacao():
    pacientes, vacinas = opcoes_formulario()
    if request.method == "POST":
        dados = ler_aplicacao_do_form()
        if not (dados["paciente_id"] and dados["vacina_id"]
                and dados["data_aplicacao"] and dados["dose"]):
            flash("Preencha paciente, vacina, data e dose.", "erro")
            return render_template("aplicacao_form.html", aplicacao=dados,
                                   pacientes=pacientes, vacinas=vacinas)
        db = get_db()
        db.execute(
            """INSERT INTO aplicacoes
               (paciente_id, vacina_id, data_aplicacao, dose, lote, observacoes)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (dados["paciente_id"], dados["vacina_id"], dados["data_aplicacao"],
             dados["dose"], dados["lote"], dados["observacoes"]),
        )
        db.commit()
        flash("Aplicação registrada!", "ok")
        return redirect(url_for("listar_aplicacoes"))
    return render_template("aplicacao_form.html", aplicacao=None,
                           pacientes=pacientes, vacinas=vacinas)


@app.route("/aplicacoes/<int:id>/editar", methods=["GET", "POST"])
def editar_aplicacao(id):
    db = get_db()
    aplicacao = db.execute("SELECT * FROM aplicacoes WHERE id = ?", (id,)).fetchone()
    if aplicacao is None:
        flash("Aplicação não encontrada.", "erro")
        return redirect(url_for("listar_aplicacoes"))
    pacientes, vacinas = opcoes_formulario()
    if request.method == "POST":
        dados = ler_aplicacao_do_form()
        if not (dados["paciente_id"] and dados["vacina_id"]
                and dados["data_aplicacao"] and dados["dose"]):
            flash("Preencha paciente, vacina, data e dose.", "erro")
            dados["id"] = id
            return render_template("aplicacao_form.html", aplicacao=dados,
                                   pacientes=pacientes, vacinas=vacinas)
        db.execute(
            """UPDATE aplicacoes
               SET paciente_id = ?, vacina_id = ?, data_aplicacao = ?,
                   dose = ?, lote = ?, observacoes = ?
               WHERE id = ?""",
            (dados["paciente_id"], dados["vacina_id"], dados["data_aplicacao"],
             dados["dose"], dados["lote"], dados["observacoes"], id),
        )
        db.commit()
        flash("Aplicação atualizada!", "ok")
        return redirect(url_for("listar_aplicacoes"))
    return render_template("aplicacao_form.html", aplicacao=aplicacao,
                           pacientes=pacientes, vacinas=vacinas)


@app.route("/aplicacoes/<int:id>/excluir", methods=["POST"])
def excluir_aplicacao(id):
    db = get_db()
    db.execute("DELETE FROM aplicacoes WHERE id = ?", (id,))
    db.commit()
    flash("Aplicação excluída.", "ok")
    return redirect(url_for("listar_aplicacoes"))


# ---------------------------------------------------------------------------
# API JSON (UC33)
# ---------------------------------------------------------------------------
@app.route("/api/pacientes")
def api_pacientes():
    linhas = get_db().execute("SELECT * FROM pacientes").fetchall()
    pacientes = ordenar_por_nome([dict(l) for l in linhas])
    return jsonify(pacientes)


@app.route("/api/aplicacoes")
def api_aplicacoes():
    linhas = get_db().execute(
        """
        SELECT a.id, a.data_aplicacao, a.dose, a.lote,
               p.nome AS paciente, v.nome AS vacina
        FROM aplicacoes a
        JOIN pacientes p ON p.id = a.paciente_id
        JOIN vacinas v ON v.id = a.vacina_id
        ORDER BY a.data_aplicacao DESC
        """
    ).fetchall()
    return jsonify([dict(l) for l in linhas])


if __name__ == "__main__":
    app.run(debug=True)
