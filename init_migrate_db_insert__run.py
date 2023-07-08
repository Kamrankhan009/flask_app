import os
import shutil
from time import sleep
import sys
import platform

# Delete 'migrations' directory
if os.path.exists("migrations"):
    shutil.rmtree("migrations")

# Delete 'app/database.sqlite' file
if os.path.exists("app/database.sqlite"):
    os.remove("app/database.sqlite")

sleep(1)


if platform.system() == "Windows":
    os.system("venv\\Scripts\\activate.bat")
else:
    os.system("source venv/bin/activate")


sleep(1)

# Initialize the database
os.system("flask db init")
sleep(1)

# Generate migration script
os.system("flask db migrate")
sleep(1)

# Apply database migrations
os.system("flask db upgrade")
sleep(1)

# Run the script to insert demo data
os.system("python insert_demo_data.py")
sleep(1)

# Run the main script
os.system("python main.py")
