# `cyber-students`

This repository provides some sample code for the Shared Project for
Modern Cryptography and Security Management & Compliance.  The project
requires git, Python 3, and MongoDB.  The following sections briefly
explain how to setup the project on your local machine.

## Get the Sample Code

Create a [GitHub](https://github.com) account.  Download and install
[git](https://git-scm.com).  We will use `git` to manage our source
code.

Verify that `git` is installed correctly:

```sh
git --version
```

[Fork this
repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
and clone your forked repository to your local machine:

```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/cyber-students.git
```

## Setup the Project

Create a Python 3 virtual environment:

```sh
python -m venv project-venv

```

Activate the virtual environment:

```bat
:: ... on Windows:
.\project-venv\Scripts\activate
```

```sh
# ... on macOS/*nix:
source project-venv/bin/activate
```

Install the required packages:

```sh
cd cyber-students
pip install -r requirements.txt
```

Download, install and start [MongoDB Community
Edition](https://www.mongodb.com/docs/manual/installation).  We will
use MongoDB as our database.

Download and install [MongoDB
Shell](https://www.mongodb.com/try/download/shell).  Open a MongoDB
shell:

```sh
mongosh
```

Create two databases with a collection named `users` in each:

```
use cyberStudents;
db.createCollection('users');

use cyberStudentsTest;
db.createCollection('users');
```

The first database will store our 'real' data.  The second database
will be used by our tests.

Download and install [curl](https://curl.se).  `curl` is also shipped
by Microsoft as part of Windows 10 and 11.  `curl` is a command-line
tool for interacting with web servers (and other protocols).

Verify that `curl` is installed correctly:

```sh
curl --version
```

## Start the Project

The server contains functionality for:

* registering new users (`api/handlers/registration.py`)
* logging in (`api/handlers/login.py`)
* logging out (`api/handlers/logout.py`)
* displaying profile (`api/handlers/user.py`)

To start the server:

```sh
python run_server.py
```

The server is available on port 4000 at
http://localhost:4000/students/api.  However, it is not possible to
use all of the functionality offered by the server directly using a
browser.  Instead we will use `curl` to interact with the server.

### Registration

To register a new user:

```sh
curl -X POST http://localhost:4000/students/api/registration -d "{\"email\": \"nigel2@gmail.com\", \"password\": \"strongpassword\", \"displayName\": \"Nigel Douglas\", \"fullName\": \"Nigel Douglas\", \"phoneNumber\": \"02537641\", \"disability\": \"leukemia\"}"
```

If the registration is successful, it will confirm the email address
and the display name of the newly registered user:

```
{"email": "foo@bar.com", "displayName": "Foo Bar"}
```

If the registration is unsuccessful, for example, if you try to
register the same user twice, it will return an error message:

```
{"message": "A user with the given email address already exists!"}
```

### Logging In

To login:

```sh
curl -X POST http://localhost:4000/students/api/login -d "{\"email\": \"foo@bar.com\", \"password\": \"pass\"}"
```

If the login is successful, it will return a token and expiration
timestamp:

```
{"token": "d4a5d8b20fe143b7b92e4fba92d409be", "expiresIn": 1648559677.0}
```

A token expires and is intended to be short-lived.  A token expires
two hours after login, after a logout, or if there is another login
from the same user, generating a new token.

If the login is unsuccessful, for example, if you provide an incorrect
password, it will return an error message:

```
{"message": "The email address and password are invalid!"}
```

### Displaying a Profile

To display a user's profile you need to a token that has not expired.
Then you can use:

```sh
curl -H "X-TOKEN: d4a5d8b20fe143b7b92e4fba92d409be" http://localhost:4000/students/api/user
```

Note that this API call does not require the `-X POST` flag.

If successful, it will return the email address and the display name
for the user:

```
{"email": "foo@bar.com", "displayName": "Foo Bar"}
```

### Logging Out

To logout, you also need a token that has not expired.  Then you can
use:


```sh
curl -X POST -H "X-TOKEN: d4a5d8b20fe143b7b92e4fba92d409be" http://localhost:4000/students/api/logout
```

## Test the Project

You can run the automated tests using:

```sh
python run_test.py
```

This command runs a number of automated tests in the `tests` folder.
The tests read and store data in the `cyberStudentsTest` database
only.  They perform tests such as registering new users
(`tests/registration.py`), logging in (`tests/login.py`), and logging
out (`tests/logout.py`).

The project also includes a program called `run_hacker.py`.  You can
run it using:

```sh
python run_hacker.py list
```

It displays all information stored in the MongoDB database.  It
produces output similar to the following:

```
There are 1 registered users:
{'_id': ObjectId('6242d9c34536b3a16b49aa6b'), 'email': 'foo@bar.com', 'password': 'pass', 'displayName': 'Foo Bar'}
```

As you can see, all of the information is stored in the clear; there
is no encryption or password hashing.  If a hacker was to compromise
the database, they could easily run a similar program to retrieve all
of the users personal information and passwords.

## After encryption is enforced

You can see the original 4 registrations did not enforce encryption. <br/>
The latest test has a new field called ```fullName```. The full name and password are encrypted:


<img width="1406" alt="Screenshot 2023-04-16 at 21 01 13" src="https://user-images.githubusercontent.com/126002808/232339107-fd0f2a67-9788-46ee-8805-6035f46cd6bd.png">

## Using Fernet for Encryption
Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key. <br/>
Fernet is an implementation of symmetric (also known as “secret key”) authenticated cryptography. <br/>
Fernet also has support for implementing key rotation via MultiFernet .

<img width="781" alt="Screenshot 2023-04-16 at 20 23 14" src="https://user-images.githubusercontent.com/126002808/232339118-87385483-fafd-42c8-b3ca-bf56fbd0da12.png">

Before and after the encryption - as seen in ```MongoDB Compass```

<img width="1425" alt="Screenshot 2023-04-17 at 12 45 09" src="https://user-images.githubusercontent.com/126002808/232475005-1668efc0-e877-487b-8e48-a77a3535723c.png">

## Using the git worklflow

```git remote -v``` shows me which repo I'm currently connected to. <br/>
```git remote set-url origin``` sets the desired Github account to push changes to.<br/>
```git push -f``` forcefully pushes the changes to the Github branch - even if there is conflict <br/>
```git status``` ensures I'm on the master branch. I don't want to commit to the wrong branch <br/>
```git pull``` checks that everything is already up-to-date <br/>
```git diff``` shows the differences between the file locally and in github <br/>
```git add``` simply adds the files to the approval process <br/>
```git commit``` commits the changes to GitHub ```-m``` flag is to add a description <br/>
```git push```finally pushes the changes up to my Github master

```
git remote -v
git remote set-url origin git@github.com:nigeldouglas-itcarlow/cyber-students.git
git push - f
git status
git pull
git diff requirements.txt
git add requirements.txt
git commit -m "adding password hasher package"
git push
```


<img width="989" alt="Screenshot 2023-04-17 at 12 57 11" src="https://user-images.githubusercontent.com/126002808/232477451-2ec57205-df6c-4aea-84f4-91e76ce31937.png">

## Creating GDPR fields
I'm able to parse the ```full_name``` field to JSON:
```
curl -X POST http://localhost:4000/students/api/registration -d "{\"email\": \"happier@setu.com\", \"password\": \"happier\", \"displayName\": \"happier\", \"fullName\": \"Mr. Happy\"}"
{"email": "happier@setu.com", "displayName": "happier", "fullName": "Mr. Happy"}%
```

However, I'm unable to parse the ```phone_number``` field to JSON:
```
curl -X POST http://localhost:4000/students/api/registration -d "{\"email\": \"happier@setu.com\", \"password\": \"happier\", \"displayName\": \"happier\", \"fullName\": \"Mr. Happy\", \phoneNumber\": \"02136541\"}"
```

![Screenshot 2023-04-17 at 14 51 12](https://user-images.githubusercontent.com/126002808/232504982-38655cb0-ab72-4d92-b4fd-6bde356e3c8d.png)

Eventually loaded the ```Disabilities``` and ```Phone Numbers``` <br/>
The issue was not with the fields I created, it was with the ```run_server.py``` script <br/>
Between tests, I need to kill the process manually, and then restart it to see the changes.

```
ps aux | grep run
kill -9 55879
python run_server.py 
```
<img width="1319" alt="Screenshot 2023-04-18 at 15 42 59" src="https://user-images.githubusercontent.com/126002808/232796988-fa6675a7-35f6-472a-9b6f-e8fabe1a78db.png">

## Ensuring weak password are not used

Ensuring the character length has to ```exceed 6 characters```:
```
if len(password) < 6:
    self.send_error(400, message='The password must be at least 6 characters long!')
    return
```

<img width="1427" alt="Screenshot 2023-04-18 at 16 31 15" src="https://user-images.githubusercontent.com/126002808/232810108-c62707e9-aeb8-44c0-861b-1800367fb97e.png">

```
import re

password = input("Create a password: ")
password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{6,}$')

while not password_pattern.match(password):
    print("Your password must contain at least one uppercase letter, one lowercase letter, and one digit, and be at least 6 characters long.")
    password = input("Create a password: ")
    
print("Password set successfully!")
```

<img width="1427" alt="Screenshot 2023-04-19 at 09 57 55" src="https://user-images.githubusercontent.com/126002808/233008496-2366670f-89df-49b8-bed1-a623b99ce19a.png">


Using regular expressions, (```password_pattern```) to ensure that the password contains at least: <br/>
- one uppercase letter <br/>
- one lowercase letter <br/>
- one digit <br/>
- at least 14 characters long. <br/>
<br/>
If the user's input does not match this pattern, the program will prompt them to create a new password until the requirements are met.

## Loading the key from a file

It's not okay to hardcode your cryptography ```keys``` in the source code <br/>
Instead, I can load it from a file or to use environmental variables (```recommended```)


<img width="1427" alt="Screenshot 2023-04-18 at 15 54 46" src="https://user-images.githubusercontent.com/126002808/232800060-ad5a1bfd-4e0e-4b1b-8752-6dc8e2e4e5c9.png">

Loading the key from a file is a more common approach to avoid hardcoding sensitive data in the code.<br/>
I created a new file named ```secret.env``` in the same directory as my Python script.<br/>
<br/>
The ```load_dotenv``` function loads environment variables from the .env file, and ```os.getenv('CRYPTO_KEY')``` retrieves the value of the ```CRYPTO_KEY``` environment variable set in the .env file. The ```.encode()``` method converts the string key to bytes, which is needed for the Fernet module to work.
<br/>
I made sure to install the ```python-dotenv``` package by running ```pip install python-dotenv``` in the terminal.

<img width="1427" alt="Screenshot 2023-04-19 at 15 52 32" src="https://user-images.githubusercontent.com/126002808/233096802-c01cb581-66d2-4bbb-beda-bb1d878d7687.png">

### Partially initialized module 'api.app' Error
<img width="1427" alt="Screenshot 2023-04-20 at 08 25 49" src="https://user-images.githubusercontent.com/126002808/233276856-45530e87-f2eb-43d5-91cf-a50fbce890e5.png">

### Cannot import name 'Application' from 'api.app' error

<img width="1427" alt="Screenshot 2023-04-20 at 08 36 57" src="https://user-images.githubusercontent.com/126002808/233279764-d7ff131b-d3ae-4291-a310-684fd1648878.png">


### ImportError: attempted relative import with no known parent package

<img width="1427" alt="Screenshot 2023-04-20 at 08 28 06" src="https://user-images.githubusercontent.com/126002808/233277110-97c990cb-9027-4318-896b-be2781635870.png">

### Commiting changes to Git so progress is tracked

<img width="1223" alt="Screenshot 2023-04-20 at 08 47 23" src="https://user-images.githubusercontent.com/126002808/233283435-33d1e08e-6a43-4c3e-ae5a-752b3a60ef6e.png">

There was a long learning curve when working with git

<img width="1223" alt="Screenshot 2023-04-20 at 09 06 46" src="https://user-images.githubusercontent.com/126002808/233287552-6c5e1ce7-5bec-4885-a61f-b38fe9df9100.png">

