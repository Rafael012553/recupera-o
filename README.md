# VacinaFácil

Sistema web para controle de vacinação de uma clínica/posto de saúde fictício. Permite cadastrar pacientes e vacinas e registrar cada dose aplicada, consultando o histórico de forma organizada.

**Autor:** PREENCHER: seu nome completo
**Curso:** MedTec 2026 · Prova de Recuperação (UC30 a UC35)
**Aplicação no Render:** PREENCHER: link do Render
**Repositório:** PREENCHER: link do GitHub

## O que o sistema faz

- **Pacientes:** cadastrar, listar (com busca por nome), editar e excluir.
- **Vacinas:** cadastrar, listar, editar e excluir.
- **Aplicações:** registrar qual paciente recebeu qual vacina, em que data, qual dose e lote. Dá para filtrar por vacina.
- **API JSON:** `/api/pacientes` e `/api/aplicacoes`.

## Tecnologias

- Python 3 + Flask (rotas e templates Jinja2)
- SQLite (módulo `sqlite3`)
- HTML + CSS responsivo (mobile first)
- Gunicorn + Render (deploy)

## Estrutura do projeto

```
vacinafacil/
├── app.py              # rotas Flask, banco de dados e API
├── algoritmos.py       # ordenação e busca feitas à mão (UC30)
├── templates/          # páginas Jinja2
├── static/style.css    # estilos
├── requirements.txt    # dependências
├── Procfile            # comando de inicialização no Render
└── README.md
```

## Banco de dados

Três tabelas, com chaves estrangeiras:

| Tabela | Campos principais |
|---|---|
| `pacientes` | id, nome, data_nascimento, telefone |
| `vacinas` | id, nome, fabricante, doses_total |
| `aplicacoes` | id, paciente_id (FK), vacina_id (FK), data_aplicacao, dose, lote, observacoes |

`aplicacoes` liga pacientes a vacinas (relação muitos-para-muitos). Ao excluir um paciente ou uma vacina, as aplicações ligadas a eles são removidas (`ON DELETE CASCADE`).

As consultas de listagem usam `JOIN`, `WHERE` (filtro por vacina) e `ORDER BY` (mais recentes primeiro).

## Algoritmos (UC30)

- `ordenar_por_nome`: Insertion Sort implementado manualmente.
- `busca_por_nome`: busca sequencial por trecho do nome.

## API

| Rota | Retorno |
|---|---|
| `GET /api/pacientes` | lista de pacientes em JSON, ordenada por nome |
| `GET /api/aplicacoes` | lista de aplicações em JSON, com nome do paciente e da vacina |

## Como rodar localmente (Windows / PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Depois abra http://127.0.0.1:5000 no navegador.

## Deploy no Render

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app` (o mesmo do `Procfile`)

Observação: no plano gratuito do Render o disco é temporário, então os dados do SQLite podem ser apagados quando o serviço reinicia. As vacinas de exemplo são recriadas automaticamente.
