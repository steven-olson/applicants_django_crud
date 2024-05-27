<h2>Overview</h2>
<p>
Standard django crud app, to run simply build and 
run docker images (through compose):

`docker-compose build`

then

`docker-compose up -d`

You'll likely want to create a super user first to make use
of admin to create normal users:

`docker ps -a` to get id of web docker container, then

`docker exec -i -t <id of web container> bash` and run

`python manage.py createsuperuser` in the container.

Tests aren't dockerized (ran out of time), to run them "easily"
go into manage.py, set `test()` as the method to run in `__main__`
at the bottom and run the file.
</p>