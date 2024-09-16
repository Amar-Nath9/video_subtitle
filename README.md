# video_subtitle

## Setting Up the Database

1. **Create a PostgreSQL Database with UTF8 Encoding:**

   Before running the Django application, you need to create a PostgreSQL database with UTF8 encoding. Use the following SQL command to create a new database:

   ```sql
   CREATE DATABASE your_database_name ENCODING 'UTF8';

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


#### 2. **Provide a Setup Script:**

Create a setup script that users can run to create a UTF8-encoded database. This script can be included in your project repository.

**`setup_database.sh`**
```bash
#!/bin/bash

# Variables
DB_NAME="your_database_name"
DB_USER="your_user"
DB_PASSWORD="your_password"

# Create database with UTF8 encoding
psql -U "$DB_USER" -c "CREATE DATABASE $DB_NAME ENCODING 'UTF8';"

echo "Database $DB_NAME created with UTF8 encoding."
