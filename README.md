# restaurant_voting
API for a restaurant with voting system

### Instructions on running

Clone repository, the go to the directory of the project.

#### Build Docker Images

```docker-compose build```

#### Run Database Migrations

```docker-compose run --rm app sh -c "python manage.py makemigrations"```
```docker-compose run --rm app sh -c "python manage.py migrate"```

#### Start the Docker Containers

```docker-compose up```

To view the admin page, go to [http://localhost:8000/admin.](http://127.0.0.1:8000/admin/login/?next=/admin/).

To view API's, go to [[http://localhost:8000/api/docs](http://127.0.0.1:8000/api/docs/#/)](http://127.0.0.1:8000/api/docs/).
