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
