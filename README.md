# Escala cerimoniarios do Limão

Aplicação web (Flask + SQLite) para montar e divulgar a escala de cerimoniários da
Paróquia Santo Antônio do Limão.

## Rodar no computador

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt   # no mínimo: pip install flask
python app.py
```

Abra http://localhost:5000

- **Tela inicial (pública):** próximas missas com a escala de cada uma. Quando o dia da
  missa passa, o quadrado some e a próxima ocupa o destaque.
- **Área do coordenador:** botão "Área do coordenador" no topo.
  Usuário inicial: `juliomalu` — senha inicial: `12345`.

## Como funciona o sorteio

1. O coordenador cadastra a missa (nome, data, hora, quantidade) e marca quem está disponível.
2. O sistema sorteia a quantidade pedida entre os disponíveis. O sorteio é ponderado:
   quem serviu **menos nos últimos 60 dias** (contando também missas já marcadas) tem
   bem mais chance. Ninguém fica com chance zero.
3. As funções (Padre, Missal, Leitor, Gerenciar Coroinha + até 2 personalizadas) são
   distribuídas preferindo quem menos fez aquela função antes. Quem sobrar fica como "Cerimoniário".
4. A escala sorteada fica como **rascunho** (só o coordenador vê). Antes de publicar, o coordenador
   pode **editar as funções** de cada vaga ("Editar funções" no painel) e então clicar em **Publicar**.
   Depois de publicada, nada mais pode ser alterado: só dá para **excluir** a missa se for necessário.

Na página "Cerimoniários" dá para desativar/reativar alguém e ver as contagens do rodízio.

O site é responsivo: funciona no computador e no celular (no celular as tabelas viram cartões).

## Santo do dia

A aba "Santo do dia" mostra o santo da data (calendário em `santo_do_dia.py`) com foto e texto buscados
na Wikipédia em português. Nada disso é gravado no banco: fica só em memória por 24 horas. Nos dias sem
festa no calendário, aparece um santo da lista `POOL`, identificado como "Para conhecer hoje".

## Quiz

A aba "Quiz" tem perguntas em três níveis (fácil, médio e difícil), sorteadas em ordem aleatória, em
rodadas de 10. As perguntas ficam em `quiz_perguntas.py`, uma por linha no formato
`pergunta|resposta certa|errada 1|errada 2|errada 3`. Para acrescentar, basta incluir novas linhas.

## Publicar (ex.: Render)

- Comando de início: `gunicorn app:app`
- Variáveis de ambiente recomendadas:
  - `SECRET_KEY` — um texto longo e aleatório
  - `PRODUCAO=1` — cookies só por HTTPS
  - `ADMIN_USER` / `ADMIN_PASSWORD` — valem só na **primeira** execução (quando o banco é criado)
  - `DATA_DIR` — pasta onde ficam o banco e as fotos. **Aponte para um disco persistente**
    (ex.: `/var/data`), senão o banco é apagado a cada novo deploy.

## Banco gratuito externo (Neon) e site sempre ligado

No plano gratuito do Render o disco é apagado a cada deploy. Para não perder as missas, use um banco
PostgreSQL gratuito do Neon: crie o projeto no Neon, copie a "connection string" e coloque no Render
na variável `DATABASE_URL`. Com ela definida, o app usa o PostgreSQL (as tabelas são criadas sozinhas);
sem ela, usa o arquivo SQLite local.

Variáveis no Render: `DATABASE_URL`, `SECRET_KEY`, `PRODUCAO=1`, `ADMIN_PASSWORD` (vale só na primeira
execução) e, se quiser fixar, `PYTHON_VERSION`. O arquivo `.python-version` já pede o Python 3.12.

Para o site não "dormir" no plano gratuito, cadastre no UptimeRobot (gratuito) um monitor HTTP a cada
5 minutos em `https://SEU-SITE.onrender.com/saude`. Essa rota não consulta o banco de propósito, para o
banco do Neon poder descansar e não gastar as horas gratuitas.

## Backup

No painel há os botões **Baixar backup** (gera um arquivo .json com missas, escalas e cerimoniários) e
**Restaurar backup** (substitui as missas atuais pelas do arquivo). Baixe uma cópia de vez em quando.
Em produção (`PRODUCAO=1`) o app se recusa a iniciar com banco temporário: defina `DATABASE_URL` (Neon)
ou `DATA_DIR` (disco persistente).

## Segurança

Troque a senha `12345` antes de publicar (defina `ADMIN_PASSWORD` antes da primeira execução
ou apague `instance/escala.db` para recriar). O login bloqueia o IP por 5 minutos após 5 erros
seguidos, e todos os formulários usam token CSRF.

## Arquivos

- `app.py` — rotas e telas
- `database.py` — tabelas, lista inicial de cerimoniários e usuário do coordenador
- `sorteio.py` — lógica do sorteio e das funções
- `templates/`, `static/` — visual (cores do logo) e fotos
