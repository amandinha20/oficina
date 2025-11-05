O que o projeto provavelmente faz / fluxo esperado

Cadastro e listagem de clientes e veículos.
Registro de serviços realizados (ordens de serviço), histórico e possivelmente valores/peças.
Interface web (HTML/CSS/JS) para usuário interagir; backend em Python (provavelmente Django) que salva dados no SQLite.
Essas suposições vêm da estrutura de pastas e dos nomes dos arquivos — para confirmar faço uma leitura dos arquivos específicos. 
GitHub

Como rodar localmente (passos sugeridos)
é um projeto Django padrão
Clone: git clone https://github.com/amandinha20/oficina.git
Crie e ative um ambiente virtual:
python -m venv venv
Windows: venv\Scripts\activate | mac/linux: source venv/bin/activate
Instale dependências (se houver requirements.txt): pip install -r requirements.txt
Se não houver, instale Django: pip install django
Caso seja Django e haja manage.py, rode migrações (se quiser usar o SQLite do repo, talvez não precise):
python manage.py migrate
python manage.py runserver
Acesse http://127.0.0.1:8000/ no navegador.


