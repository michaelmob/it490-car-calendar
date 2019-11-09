# Car Calendar Database

## Vagrant Setup
**IMPORTANT:** Before spinning up your db virtual machine, setting up `.env` files
is required.

1. Inside of the `db/` directory
2. Copy/duplicate `_env` to `.env`
3. Configure newly created `.env` file

**Notice how the `_` (underscore) is changed to a `.` (period).**
These `.env` files can store sensitive data without being commited to version
control.

To spin up a db virtual machine, after the previous setup...
```bash
vagrant up db
```

To completely reset your db virtual machine...
```
vagrant destroy db -f; vagrant up db
```
**WARNING:** Unless `/var/lib/mysql` is a synced folder, the database will be
reset/lost as well.

## Database
| id (AI) | username | password | salt | email               | token  |
| --      | --       | --       | --   | --                  | --     |
| 1       | user     | #hash#   | abcd | example@example.com | abc123 |

### Cars Table
| id (AI) | user_id (FK) | make   | model | year | mileage | date_created        |
| --      | --           | --     | --    | --   | --      | --                  |
| 1       | 1            | Toyota | Camry | 1990 | 100000  | 2019-10-15 12:00:00 |

### Events Table
To be designed.

### Reminders Table
To be designed.

### Notifications Table
To be designed.

## AQMP Exchanges

### Auth Consumer (RPC)

Listening on queue: `auth-queue-rpc`

#### Action: `login`
| Field | Description | Example |
| ---   | ---         | --- |
| `action` | Action to login. `login` | { 'action': 'login' } |
| `username` | Username to login by. | { 'username': 'test' } |
| `email` | Email to login by. (Optional) | { 'email': 'test@test.com' } |
| `password` | Password to authenticate with. | { 'password': '#hash#' } |

**Sent Example:**
The consumer expects a JSON string.
```python
{ 'action': 'login', 'username': 'test', 'password': '#hash#' }
```

**Response Example:**
The response will be a JSON string. The `success` property is always guaranteed
to be present whether its `True` or `False`. A `message` property is also
guaranteed and will offer a message of status.
```python
# On successful login
{ 'success': True, 'token': '#custom user token#', 'message': 'LOGIN_SUCCESS' }

# On failed login
{ 'success': False, 'message': 'LOGIN_FAILED' }
```

#### Action: `register`
| Field | Description | Example |
| ---   | ---         | --- |
| `action` | Action to register. `register` | `{ 'action': 'register' }` |
| `username` | Username for account. | `{ 'username': 'test' }` |
| `email` | Email for account. | `{ 'email': 'test@test.com' }` |
| `password` | Password for account. | `{ 'password': '#hash#' }` |
| `first_name` | First name of account owner. | `{ 'first_name': 'First' }` |
| `last_name` | Last name of account owner. | `{ 'last_name': 'Last' }` |

**Sent Example:**
The consumer expects a JSON string.
```python
{ 'action': 'login', 'username': 'test', 'password': '#hash#' }
```

**Response Example:**
The response will be a JSON string. The `success` property is always guaranteed
to be present whether its `True` or `False`.
```python
# On successful register
{ 'success': True, 'message': 'REGISTER_SUCCESS' }

# On failed register
{ 'success': False, 'message': 'REGISTER_FAILURE' }
```

### Log Consumer

Listening on queue: `log-queue`

