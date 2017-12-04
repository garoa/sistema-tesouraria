# Sistema da Tesouraria do Garoa

Esse sistema serve para que os associados do Garoa se comunicarem oficialmente com a tesouraria.
Nele você pode quitar seus debitos e pedir reembolsos.

Ele pode ser acessado aqui: https://sistema-tesouraria.herokuapp.com/

## Contribuições:

Contribuições são bem vindas.

## Heroku's Quirks and Features
Este sistema está rodando no Heroku.

Devido ao filesystem temporário do Heroku, as imanges são guardadas na base de dados, usando o `django-database-files-3000`.

Como o Heroku Scheduler não pode ser agendado mensalmente (como o Cron), o script `faz_lancamentos.py` é agendado diariamente, ele deve verificar se o lançamento já foi realizado para um determinado usuário. 

Para poder enviar emails, usamos o Plugin do Sendgrid. Foi necessário customizar o form de reset de senhas para podermos usar o backend correto.

## Further Reading

- [Heroku Django Starter Template](https://github.com/heroku/heroku-django-template)
- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)

## Dodgy 3rd Party Software
- https://github.com/chrisspen/django-database-files-3000
