# IT 491 - Car Calendar

A car maintenance calendar.

## Quickstart

The easiest way to run these services is through vagrant.
A `Vagrantfile` convenientally exists.

### Setup

**1. Set up your environment variables files.**
There are two env files (`.env`) that must be created, one in `./db` and one in
`./web`. It is easiest to simply
copy the contents of the `_env` files into `.env` files.
```
# Make sure you are inside the root directory of the project before running any
# command.

# Duplicate _env files to .env
cp db/src/_env db/src/.env
cp web/src/_env web/src/.env

# Configure .env files (Read towards the bottom of the page to see an example.)
nano db/src/.env
nano web/src/.env
```

**2. Create the virtual machines for the services.**
```
# This will take a while.
vagrant up
```

**3. Do something else for 10 minutes.**

[Click here to learn more about Vagrant commands.](https://vagrantup.com/docs/cli/)


## Development
Connecting to a VM is as easy as SSHing into it, because it is.

SSH into your desired virtual machine.
```
vagrant ssh db      # access db vm shell
vagrant ssh web     # access web vm shell
vagrant ssh dmz     # access dmz vm shell
vagrant ssh broker  # access broker vm shell
```

### Useful Information
READ THE MOTD (`/etc/motd`) AS SOON AS YOU SSH IN.

#### Common Directories
These directories should all be the same no matter which VM you are in.
Some may not have specific directories.

- Log Directory: `/var/log/car-calendar`
- Project Directory: `/srv/car-calendar`

#### Common URLs (FOR TESTING PURPOSES ONLY!!!)
- RabbitMQ admin: http://localhost:15672
- Adminer: http://localhost:3380
- Gunicorn/Flask: http://localhost:5000
- Nginx: http://localhost:8080

#### Example `.env` files (FOR TESTING PURPOSES ONLY!!!)
##### File: `db/src/.env`
```bash
#!/usr/bin/env bash
export RABBITMQ_HOST=12.12.0.2
export RABBITMQ_PORT=5672
export RABBITMQ_AUTH_USER=admin
export RABBITMQ_AUTH_PASS=adminpass
export RABBITMQ_LOG_USER=admin
export RABBITMQ_LOG_PASS=adminpass
export RABBITMQ_DATA_USER=admin
export RABBITMQ_DATA_PASS=adminpass

export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_DB=carcalendar
export MYSQL_USER=db
export MYSQL_PASS=dbpass
```

##### File: `web/src/.env`
```bash
#!/usr/bin/env bash
export FLASK_APP=main.py
export FLASK_ENV=development

export RABBITMQ_HOST=12.12.0.2
export RABBITMQ_PORT=5672
export RABBITMQ_VHOST='/'
export RABBITMQ_AUTH_USER=admin
export RABBITMQ_AUTH_PASS=adminpass
export RABBITMQ_LOG_USER=admin
export RABBITMQ_LOG_PASS=adminpass
export RABBITMQ_DATA_USER=admin
export RABBITMQ_DATA_PASS=adminpass
```

Because the variables are exported, we can source them if needed.
```bash
source db/src/.env
source web/src/.env
```
