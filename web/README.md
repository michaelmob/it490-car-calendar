# Car Calendar Frontend

## Stack
The web frontend uses [Flask](https://flask.palletsprojects.com/en/1.1.x/).

## Vagrant Development
1. Spin up the web virtual machine.
```bash
vagrant up web
```

2. SSH into the virtual machine.
```bash
vagrant ssh web
```

3. Run flask development server.
```bash
cd /srv/car-calendar
./run_webserver
```

## REST (Unfinished)
| Method | Endpoint            | Fields | Description                |
| --     | --                  | --     | --                         |
| POST   | /auth/login         | ...    | Log user in.               |
| POST   | /auth/register      | ...    | Register.                  |
| GET    | /events             |        | List all events.           |
| POST   | /events             | ...    | Create a new event.        |
| GET    | /events/{id}        |        | Retrieve event by `id`.    |
| DELETE | /events/{id}        |        | Delete event by `id`.      |
| PUT    | /events/{id}        | ...    | Update event by `id`.      |
| GET    | /reminders          |        | List all reminders.        |
| POST   | /reminders          | ...    | Create a new reminder.     |
| GET    | /reminders/{id}     |        | Retrieve reminder by `id`. |
| DELETE | /reminders/{id}     |        | Delete reminder by `id`.   |
| PUT    | /reminders/{id}     | ...    | Update reminder by `id`.   |
| GET    | /notifications      |        | List all notifications.    |
| POST   | /notifications      | ...    | Create a new reminder.     |
| GET    | /notifications/{id} |        | Retrieve reminder by `id`. |
| DELETE | /notifications/{id} |        | Delete reminder by `id`.   |
| PUT    | /notifications/{id} | ...    | Update reminder by `id`.   |


#testing changes
