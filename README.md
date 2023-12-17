# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/KseniaLysikova/DjangoChat.git
    $ cd DjangoChat/MyApp
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate

And start redis server:

    $ sudo docker run -p 6379:6379 -d redis:5


You can now run the development server:

    $  daphne -b 0.0.0.0 -p 8001 app.asgi:application
