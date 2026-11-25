# Guia: GitHub + Render (PowerShell)

Tudo que está marcado com `PREENCHER` você troca pelos seus dados.

## 1. Rodar local antes de subir

```powershell
cd PREENCHER: caminho da pasta vacinafacil
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000 e teste: cadastre um paciente, uma aplicação, abra `/api/pacientes`.

Se o PowerShell bloquear o `Activate.ps1`, rode uma vez:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 2. Criar o repositório no GitHub

1. Em github.com, clique em **New repository**.
2. Nome sugerido: `vacinafacil`. Marque **Public**.
3. **Não** marque "Add a README" (o projeto já tem um).
4. Copie a URL, algo como `https://github.com/PREENCHER-usuario/vacinafacil.git`.

## 3. Commits (mínimo 5, com mensagens claras)

Faça um commit por etapa, para o histórico mostrar a evolução do projeto:

```powershell
git init
git branch -M main
git config user.name "PREENCHER: seu nome"
git config user.email "PREENCHER: seu e-mail do GitHub"

git add .gitignore requirements.txt Procfile
git commit -m "Configura projeto: dependencias, Procfile e gitignore"

git add algoritmos.py
git commit -m "Adiciona algoritmos de ordenacao (insertion sort) e busca sequencial"

git add app.py
git commit -m "Cria app Flask com banco SQLite e CRUD de pacientes, vacinas e aplicacoes"

git add templates/base.html templates/index.html templates/pacientes.html templates/paciente_form.html templates/vacinas.html templates/vacina_form.html templates/aplicacoes.html templates/aplicacao_form.html
git commit -m "Adiciona templates Jinja2 com navegacao entre paginas"

git add static/style.css
git commit -m "Adiciona CSS responsivo para celular"

git add README.md GUIA_GITHUB_RENDER.md
git commit -m "Adiciona README explicando o sistema"
```

Depois, envie para o GitHub:

```powershell
git remote add origin https://github.com/PREENCHER-usuario/vacinafacil.git
git push -u origin main
```

Se pedir login, use seu usuário e um **Personal Access Token** no lugar da senha
(GitHub > Settings > Developer settings > Personal access tokens).

Confira com `git log --oneline`: devem aparecer 6 commits.

## 4. Deploy no Render

1. Entre em render.com e faça login com o GitHub.
2. **New +** > **Web Service** > escolha o repositório `vacinafacil`.
3. Preencha:
   - **Language:** Python 3
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
4. Em **Environment Variables**, adicione `SECRET_KEY` com um texto longo qualquer.
5. Clique em **Create Web Service** e aguarde o deploy (alguns minutos).
6. Copie a URL `https://PREENCHER.onrender.com` e abra no navegador.

Observações importantes:
- Compare o `requirements.txt` e o `Procfile` deste projeto com os da Geekie (Projeto Integrador). Se os da Geekie forem diferentes, use os da Geekie.
- No plano gratuito, a primeira visita depois de um tempo parado pode demorar cerca de 1 minuto. **Abra o link uns 10 minutos antes de entregar** e teste.
- O disco gratuito é temporário: os dados podem sumir quando o serviço reinicia. Para a avaliação, cadastre alguns pacientes e aplicações de exemplo pouco antes de entregar.

## 5. Checklist final de entrega

- [ ] Repositório público com 5 ou mais commits
- [ ] Link do Render abre e as páginas funcionam
- [ ] `/api/pacientes` retorna JSON no Render
- [ ] Relatório em PDF (2 a 5 páginas)
- [ ] Nome preenchido no README e no rodapé (`templates/base.html`)
- [ ] Entregar: link do GitHub + link do Render + PDF do relatório, até 23h59
