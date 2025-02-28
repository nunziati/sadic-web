# sadic-web
Web app running the SADIC

per avviare il deployment eseguire 'docker-compose up --build'

eventualmente:
docker exec -it sadicweb python3 manage.py flush --noinput
docker exec -it sadicweb python3 manage.py makemigrations
docker exec -it sadicweb python3 manage.py migrate

sul server di produzione usare 'docker-compose up --build -d'


per controllare i dati sul mysql

docker exec -it sadic_database mariadb -u root -p
USE sadic;
SHOW TABLES;

oppure http://0.0.0.0:8081
