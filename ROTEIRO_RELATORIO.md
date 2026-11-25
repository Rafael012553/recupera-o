# Roteiro do Relatório Técnico (Parte 2)

A prova exige texto com as **suas palavras**. Por isso este arquivo não traz o relatório pronto: traz o roteiro, os fatos do sistema para você consultar e perguntas para guiar sua escrita.
Escreva no Google Docs ou Word, com 2 a 5 páginas, e exporte em PDF.

---

## 1. Identificação

- Nome completo: PREENCHER
- Data de entrega: PREENCHER
- Nome do sistema: VacinaFácil
- Descrição (1 ou 2 frases): PREENCHER. Dica: "Sistema web para controle de vacinação de pacientes de uma clínica fictícia."

## 2. Descrição do Sistema (10 a 15 linhas)

Responda com suas palavras:
- O que o usuário consegue fazer no sistema? (cadastrar pacientes e vacinas, registrar aplicações, buscar, filtrar)
- Quem usaria? (enfermeiros, recepcionistas de posto de saúde ou clínica)
- Que problema resolve? (pense em carteirinha de vacina em papel: perde, rasura, difícil de consultar)

## 3. Decisões Técnicas

**a) Por que esse tema?**
Pense: por que vacinação? Tem a ver com a sua área, com um caso real, com a importância do histórico vacinal? PREENCHER com sua motivação real.

**b) Maiores dificuldades e como resolveu**
Seja honesto, porque a avaliação valoriza autoavaliação sincera. Lembre de erros reais que você teve. Algumas possibilidades que costumam aparecer neste tipo de projeto (use só as que viveu de verdade):
- Entender o JOIN entre três tabelas
- Configurar o deploy no Render (Procfile, requirements, gunicorn)
- Chaves estrangeiras e exclusão em cascata
- Fazer o layout funcionar no celular
- Autenticação do GitHub pelo PowerShell

**c) Organização do banco de dados** (fatos para consultar)
- `pacientes` (id, nome, data_nascimento, telefone)
- `vacinas` (id, nome, fabricante, doses_total)
- `aplicacoes` (id, paciente_id, vacina_id, data_aplicacao, dose, lote, observacoes)
- `aplicacoes` tem duas chaves estrangeiras: um paciente pode receber várias vacinas e uma vacina pode ser aplicada em vários pacientes (relação muitos-para-muitos resolvida pela tabela intermediária).
- `ON DELETE CASCADE`: apagar um paciente apaga as aplicações dele.
Explique com suas palavras por que você precisou de uma tabela só para as aplicações.

**d) Do que mais se orgulha**
Escolha de verdade: o algoritmo de ordenação? O layout no celular? O deploy funcionando? Explique o porquê.

## 4. Conexão com as UCs (1 parágrafo de 3 a 5 linhas por UC)

Fatos do projeto para você relacionar, cada um com suas palavras:

| UC | Onde aparece no projeto |
|---|---|
| UC30 Lógica | `algoritmos.py`: `ordenar_por_nome` (insertion sort, feito sem `sorted()`) e `busca_por_nome` (busca sequencial). Usam `for`, `while`, `if` e funções. São usados na tela de pacientes e na API. |
| UC31 Interface | HTML e CSS em `templates/` e `static/style.css`. 4 áreas com navegação no menu. Layout mobile first com `@media`, tabelas com rolagem lateral no celular. |
| UC32 Banco | SQLite com 3 tabelas e chaves estrangeiras. CRUD completo. `JOIN` (aplicações com paciente e vacina), `WHERE` (filtro por vacina) e `ORDER BY` (data mais recente primeiro). |
| UC33 Web/APIs | Flask com rotas organizadas por assunto, templates Jinja2 (`{% for %}`, `{% if %}`, herança com `base.html`) e endpoints JSON `/api/pacientes` e `/api/aplicacoes`. |
| UC34 Organização | `README.md`, divisão do trabalho em etapas, commits por etapa, guia de entrega. Conte como você se organizou até o prazo. |
| UC35 Integrador | GitHub público com commits, `requirements.txt`, `Procfile`, deploy no Render. Conte como foi colocar no ar. |

## 5. Reflexão Final (5 a 10 linhas)

Perguntas para pensar (responda do seu jeito):
- Se você pudesse recomeçar o ano, o que faria diferente? (estudar mais cedo, entregar em dia, praticar mais, pedir ajuda)
- O que a TI tem a ver com a saúde? Pense em prontuário eletrônico, carteira de vacinação digital, agendamento, exames, segurança de dados do paciente (LGPD).

---

## Dicas finais

- Escreva em primeira pessoa e cite coisas que só quem fez o projeto saberia (erros reais, decisões reais).
- Antes de entregar, abra o sistema e **leia o código** para conseguir explicá-lo se o professor perguntar.
- Releia tudo e ajuste o nome do sistema e dos campos se você mudar alguma coisa.
