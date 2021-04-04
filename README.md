# flask-trackerproductivity
Basic RESTApi for tracking productivity. Project could be extended with more methods and statistics
that would impact on user's productivity. 


## Install
```
pip install -r requirements.txt
```

## Migrations

First create database 
```
sudo -u name_of_user createdb name_of_database
```

You can access created database with created user by,
```
psql -U name_of_user -d name_of_database
```

export 
```
export APP_SETTINGS="config.DevelopmentConfig"
```
and your database 
```
export DATABASE_URL="postgresql://USERNAME:PASSWORD@localhost:PORT/NAME_OF_YOUR_DATABASE"
```

Starting migration
```
python manage.py db init
```

Run
```
python manage.py db migrate
```

Apply migrations to the database
```
python manage.py db upgrade
```

## API TASK

POST USER
'/user'
```
{
    "username": "Mateusz",
    "email": "howtogetajobasaprogrammer@gmail.com"
}
```

POST TASK
/task
```
{
    "task_id": 10,
    "task_name": "Learning Flask",
    "username": "Mateusz"
}
```

GET TASK
'/task'
```
{
    "task_id": 10
}
```
And its response 
```
{
    "success": true,
    "task": {
        "date_created": "2021-04-04T16:13:37.694996",
        "description": null,
        "duration": 0.0,
        "is_active": true,
        "task_id": 10,
        "task_name": "Learning Flask",
        "username": "Mateusz"
    }
}
```

Delete task
'/task'
```
{
    "message": "Tak has been deleted.",
    "success": true,
    "task": {
        "date_created": "2021-04-04T16:13:37.694996",
        "description": null,
        "duration": 0.0,
        "is_active": true,
        "task_id": 10,
        "task_name": "Learning Flask",
        "username": "Mateusz"
    }
}
```

Finish task
'/task/finish'
```
{
    "success": true,
    "task": {
        "date_created": "2021-04-04T16:16:04.287866",
        "description": null,
        "duration": 0.0,
        "is_active": false,
        "task_id": 10,
        "task_name": "Learning Flask",
        "username": "Mateusz"
    }
}
```

GET ALL TASKS
'/task/get/all'

GET ALL TASKS FROM LAST WEEK FOR USER
'/task/user/week'

## API USER
GET USER
'/user'
```
{
    "success": true,
    "user": {
        "email": "howtogetajobasaprogrammer@gmail.com",
        "registered": "2021-04-04T16:12:43.604617",
        "tasks": [
            {
                "date_created": "2021-04-04T16:16:04.287866",
                "description": null,
                "duration": 0.0,
                "is_active": false,
                "task_id": 10,
                "task_name": "Learning Flask",
                "username": "Mateusz"
            }
        ],
        "username": "Mateusz"
    }
}
```

GET TASKS FOR USER
'/user/tasks'
```
{
    "message": [
        {
            "date_created": "2021-04-04T16:16:04.287866",
            "description": null,
            "duration": 0.0,
            "is_active": false,
            "task_id": 10,
            "task_name": "Learning Flask",
            "username": "Mateusz"
        }
    ],
    "success": true
}
```

GET ACTIVE TASKS FOR USER
'/user/tasks/active'
```
{
    "success": true,
    "tasks": [
        {
            "date_created": "2021-03-29T12:54:56.534634",
            "description": "korki marek",
            "duration": null,
            "is_active": true,
            "task_id": 8,
            "task_name": "Korki",
            "username": "Radzi"
        },
        {
            "date_created": "2021-03-29T12:56:00.749178",
            "description": "korki marek",
            "duration": null,
            "is_active": true,
            "task_id": 9,
            "task_name": "Korki",
            "username": "Radzi"
        },
        {
            "date_created": "2021-04-01T23:08:21.104053",
            "description": null,
            "duration": 0.0,
            "is_active": true,
            "task_id": 100,
            "task_name": "test_task",
            "username": "Radzi"
        }
    ]
}
```

CALCULATING PRODUCTIVITY FOR USER
'/user/tasks/productivity'
```
{
    "productive_time": 71.86666666666666,
    "success": true,
    "user": {
        "email": "abc",
        "registered": "2021-03-28T14:34:38.138443",
        "tasks": [
            {
                "date_created": "2021-03-29T12:54:56.534634",
                "description": "korki marek",
                "duration": null,
                "is_active": true,
                "task_id": 8,
                "task_name": "Korki",
                "username": "Radzi"
            },
            {
                "date_created": "2021-03-29T12:56:00.749178",
                "description": "korki marek",
                "duration": null,
                "is_active": true,
                "task_id": 9,
                "task_name": "Korki",
                "username": "Radzi"
            },
            {
                "date_created": "2021-03-29T12:14:12.070333",
                "description": "korki marek",
                "duration": 22.566666666666666,
                "is_active": false,
                "task_id": 6,
                "task_name": "Korki",
                "username": "Radzi"
            },
            {
                "date_created": "2021-03-29T12:20:05.606415",
                "description": "korki marek",
                "duration": 22.5,
                "is_active": false,
                "task_id": 7,
                "task_name": "Korki",
                "username": "Radzi"
            },
            {
                "date_created": "2021-03-29T21:51:57.045535",
                "description": null,
                "duration": 13.15,
                "is_active": false,
                "task_id": 1,
                "task_name": "Korki",
                "username": "Radzi"
            },
            {
                "date_created": "2021-03-29T21:52:56.337449",
                "description": null,
                "duration": 13.65,
                "is_active": false,
                "task_id": 2,
                "task_name": "Korki",
                "username": "Radzi"
            },
            {
                "date_created": "2021-04-01T23:08:21.104053",
                "description": null,
                "duration": 0.0,
                "is_active": true,
                "task_id": 100,
                "task_name": "test_task",
                "username": "Radzi"
            }
        ],
        "username": "Radzi"
    }
}
```

GET ALL USERS
'/user/get/all'


##TODO
- [] create unit tests for setup and methods
- [] deploy restapi using docker/heroku
- [] write more methods for statistics