# PoladApi 


#### By **Daniel Muruthi and Lawrence Otieno**

## Description

PoladApi api endpoints enable  Signup, login, inputing twitter credentials and autoposting on twitter.

# Log In To Admin
Log into the admin panel
Username: Polad, 
Password: asad1234

## Endpoints

- Login - https://poladapi.herokuapp.com/auth/login/
- Register - https://poladapi.herokuapp.com/auth/register/
- Twitter Creds - https://poladapi.herokuapp.com/api/twittercreds/
- Post - https://poladapi.herokuapp.com/api/post/


## Setup Requirements

- Visual Studio Code
- Linux Terminal
- Github
- Heroku
- virtual Environment
- pip
- postgresql

## installations
-Clone The Project
Create a virtual environment and proceed to add the dependancies

- python3 -m venv --without-pip virtual
- curl https://bootstrap.pypa.io/get-pip.py | python
- source virtual/bin/activate
- pip install -r requirements.txt
- pip install django-bootstrap
- python3 -m  pip install gunicorn
- install Heroku cli
- install postgresql and create database


## Running program

- In the Terminal run source virtual/bin/activate
- Run python3 manage.py runserver

## Known Bugs

connection to server at "0.0.0.0", port 5432 failed: Connection refused
	Is the server running on that host and accepting TCP/IP connections?


## Technologies Used

This project has been written in django and uses postgresql database



## Support and contact details

email: adinomuruthi1@gmail.com

## License

MIT Licence Copyright © 2021 Daniel Muruthi

