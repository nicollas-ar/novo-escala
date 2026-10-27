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
4. A escala sorteada já é **publicada na hora** no site. Depois de sorteada, o coordenador não
   altera nada: só pode **excluir** a missa (no painel) se for necessário. As funções só podem ser
   personalizadas **antes** do sorteio.

Na página "Cerimoniários" dá para desativar/reativar alguém e ver as contagens do rodízio.

O site é responsivo: funciona no computador e no celular (no celular as tabelas viram cartões).

## Publicar (ex.: Render)

- Comando de início: `gunicorn app:app`
- Variáveis de ambiente recomendadas:
  - `SECRET_KEY` — um texto longo e aleatório
  - `PRODUCAO=1` — cookies só por HTTPS
  - `ADMIN_USER` / `ADMIN_PASSWORD` — valem só na **primeira** execução (quando o banco é criado)
  - `DATA_DIR` — pasta onde ficam o banco e as fotos. **Aponte para um disco persistente**
    (ex.: `/var/data`), senão o banco é apagado a cada novo deploy.

## Segurança

Troque a senha `12345` antes de publicar (defina `ADMIN_PASSWORD` antes da primeira execução
ou apague `instance/escala.db` para recriar). O login bloqueia o IP por 5 minutos após 5 erros
seguidos, e todos os formulários usam token CSRF.

## Arquivos

- `app.py` — rotas e telas
- `database.py` — tabelas, lista inicial de cerimoniários e usuário do coordenador
- `sorteio.py` — lógica do sorteio e das funções
- `templates/`, `static/` — visual (cores do logo) e fotos
