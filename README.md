﻿## Flexio

### Smart. Simple. Flexible

#### Flexio is the open source solution to internal communication in companies. It is made as a portfolio project by Goran Nushkov.

#### It is a web application that can be cloned freely and the code can be used by anyone who finds use of it. The main features that are included in are:

- Blogging system
- Admin dashboard system
- Mailing system
- Logging and middleware
- Password and email change reqest system
- User profile
- Gravatar service for avatars
- Custom error page handlers
- Donation system by Stripe
- User soft deletion (users stay in the database after deletion)
- And much more mini features...

#### When it comes to the technical part, Flexio uses the following technologies:

- Python as the backend language
- Flask as the web framework
- Gunicorn as the WSGI HTTP Server
- Redis and Celery as workers
- PostgreSQL as the database
- Docker and Docker-Compose for building it all
- Jinja2 as the template language
- HTML, CSS and JavaScript as frontend languages
- Bootstrap as the main frontend library
- And many more Flask extensions and Python test packages...

#### How to start the application:

First, I have to say that there might be issues running this with the Docker Toolbox on Windows. I noticed no problems running it on UNIX systems. Let's begin:

- Download and install `docker` and `docker-compose`.
- Clone this repository.
- Go into the 'flexio' foler you just cloned and run `docker-compose up --build` in your terminal and wait for it to finish.
- Check the web app in your browser by typing `localhost:8000` in the search bar.
- After it is done, you have to initialize the database by running the custom CLI script made for that purpose. Just write `docker-compose exec website flexio db reset --with-testdb` and after that you can login on the page with `dev@local.host` as username and `devpassword` as password. If you want to add fake users to see how the admin dashboard operates, run `docker-compose exec website flexio add users` in the terminal window.
- If you want to test the contact page and the stripe donation system, create a `settings.py` file in the `instance` folder and add the following lines, but remember you have to have a stripe account to get the secret key and the publishable key for testing: \
`MAIL_USERNAME = '<yourrealemail>'` \
`MAIL_PASSWORD = '<yourrealpassword>'` \
`STRIPE_SECRET_KEY = '<yourtestingsecretkey>'` \
`STRIPE_PUBLISHABLE_KEY = '<yourtestingpublishablekey>'`
- After all of this, you can use some other custom CLI commands that are made with Click and you can check them in the `cli/commands` folder.

If you have any issues, feel free to raise an issue in the repository.

### License

---

MIT License

**Copyright &copy; 2018 Goran Nushkov**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
