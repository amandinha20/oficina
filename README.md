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

Link de uma documentação mais completa: 
https://doc-14-as-apps-viewer.googleusercontent.com/viewer/secure/pdf/r26994evrlsplog6jlrnpb0klubdfvo7/ui4qkts6k9o4b9t82p1nuq651bg9f8h3/1762352100000/drive/00435045251240229807/ACFrOgCn_EnVL-KiVKH_09DTbz7d-XSHfLzf-CEYKQ49RyUshJP_E4PEnSk8-0qaOrI3b_QeMvHyaC-mGz7dUDKzKoPbVQ4gpR4Uuub6krl6x70NOwYYFcvn0mXTWbVevmto6KahBg-4MBG2K0GWCOMzSSz88gZu5RZaJfmPPWV9pJ0ciJLff9zxal2KHfqMNjsV_v1G5qX_Q2_TiqUQGUU4Z3YKc3-bUxrJmRIUtYleiTsI6pq4mSD-oW9O1jAQ2zOd_SuWfoRHTnrrtS5D?print=true&nonce=philo3nmgob7m&user=00435045251240229807&hash=6npkk6v86o6scksh044j0t2rq8dda9md

Imagens do projeto funcionando: 
<img width="1875" height="864" alt="image" src="https://github.com/user-attachments/assets/39ef3ae1-44e3-4d17-9b1f-69f4f14d26c2" />
<img width="1708" height="829" alt="image" src="https://github.com/user-attachments/assets/c6811ebe-e781-4aca-8010-7386e963b970" />
<img width="1607" height="680" alt="image" src="https://github.com/user-attachments/assets/27a0567b-9da9-4209-986a-71094c4a00b8" />
<img width="1251" height="864" alt="image" src="https://github.com/user-attachments/assets/0bd49cfc-aa6d-4839-a199-d23cf3229810" />

