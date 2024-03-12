A python-django project.

1. Clonar o projeto
2. Instalar poetry
   ```cmd
   pip install poetry
   ```
3. Instalar dependencias do projeto utilizando o poetry
   ```cmd
   poetry install
   ```
4. Criar db MySQL
5. editar variaveis de ambiente do projeto, para isso, criar arquivo .secrets.toml, copiar o que está em settings e alterar com os dados para conectar no banco, não subir o secrets no git.
6. Rodar migrations para criar tabelas no banco
   ```cmd
   poetry run python manage.py migrate
   ```
7. rodar servidor e verificar se o django está funcionando
   ```cmd
   poetry run python manage.py runserver
   ```
