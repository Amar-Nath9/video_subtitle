# video_subtitle

## Description

The `video_subtitle` project is a Django application that allows users to upload videos and extract subtitles using FFmpeg. The application supports searching for phrases in videos and retrieving timestamps for those phrases.

## Requirements

- Python 3.x
- Django
- PostgreSQL
- FFmpeg
- Docker (optional)

## Setting Up the Database

1. **Create a PostgreSQL Database with UTF8 Encoding:**

   Before running the Django application, create a PostgreSQL database with UTF8 encoding using the following SQL command:

   <pre>
   <code>
   CREATE DATABASE your_database_name ENCODING 'UTF8';
   </code>
   <button onclick="navigator.clipboard.writeText('CREATE DATABASE your_database_name ENCODING \'UTF8\';')"></button>
   </pre>

2. **Update Django Settings:**

   In your `settings.py` file, configure the database settings as follows:

   <pre>
   <code>
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   </code>
   <button onclick="navigator.clipboard.writeText('DATABASES = {\\n    \'default\': {\\n        \'ENGINE\': \'django.db.backends.postgresql\',\\n        \'NAME\': \'your_database_name\',\\n        \'USER\': \'your_user\',\\n        \'PASSWORD\': \'your_password\',\\n        \'HOST\': \'localhost\',\\n        \'PORT\': \'5432\',\\n    }\\n}')"></button>
   </pre>

## Installing Requirements

3. **Install Dependencies:**

   Before running the application, install the required Python packages using the following command:

   <pre>
   <code>
   pip install -r requirements.txt
   </code>
   <button onclick="navigator.clipboard.writeText('pip install -r requirements.txt')"></button>
   </pre>

## Setting Up the Database

4. **Run Migrations:**

   After setting up the database, create the necessary database tables by running:

   <pre>
   <code>
   python manage.py makemigrations
   python manage.py migrate
   </code>
   <button onclick="navigator.clipboard.writeText('python manage.py makemigrations\npython manage.py migrate')"></button>
   </pre>

## Running the Server

5. **Start the Django Development Server:**

   Once everything is set up, start the Django development server with:

   <pre>
   <code>
   python manage.py runserver
   </code>
   <button onclick="navigator.clipboard.writeText('python manage.py runserver')"></button>
   </pre>

## Additional Requirements

- **While checking the closed captions (CC), try toggling the CC off and on.**
- **While running the server, if the subtitles are not visible, try changing the language and check again.**

- Ensure you have PostgreSQL installed and running on your machine.
- If using Docker, make sure your containers are properly configured and running.
- Set up environment variables for sensitive information like database credentials if needed.
