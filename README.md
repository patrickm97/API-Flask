# Website with a login feature that saves information on a database

The main frameworks and libraries used are **Flask** and **SQLAlchemy**.

The programming language used is __*Python*__.

__*Jinja*__ is used to program specific **HTML** funtions.

## Usage

### Sign-up

Definition
'POST /sign-up'

Response
HTTP | Description
---|---
201 | success
409 | email already used

### Loggin in

Definition
'POST /login'

Response
HTTP | Description
---|---
200 | success
404 | user not found

### See all posts

Definition
'GET /home'

Response
HTTP | Description
---|---
200 | success

### Delete a post

Definition
'POST /home'

Response
HTTP | Description
---|---
204 | success

### Update account

Definition
'POST /update'

Response
HTTP | Description
---|---
200 | success
409 | input error
