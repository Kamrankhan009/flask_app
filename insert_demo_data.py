import sqlite3
import datetime
dt_now = datetime.datetime.now()
from werkzeug.security import generate_password_hash
import random
import secrets
import uuid
import string

connection = sqlite3.connect('app/database.sqlite')
cur = connection.cursor()


def generate_email():
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for i in range(8))
    domain = ''.join(random.choice(letters) for i in range(5))
    extension = ''.join(random.choice(letters) for i in range(3))
    return f"{username}@{domain}.{extension}"

def generate_username():
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for i in range(8))
    return f"{username}"




products = []

for i in range(1, 11):
    product = {
        'title': f'Product {i}',
        'description': f'This is the description of Product {i}',
        'price': 9.99 * i,
        'image': f'image_{i}.jpg'
    }
    products.append(product)

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

jobs = []
for _ in range(10):
    job = {
        "title": generate_random_string(10),
        "description": generate_random_string(50)
    }
    jobs.append(job)

# Insert 10 of users to the user table
for i in range(1,20):
    email = generate_email()
    username = generate_username()
    if i <=3:
        cur.execute("INSERT OR IGNORE INTO 'user' (username,email,password,is_active,is_admin,duration, image, banner) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (f"{username}",f"{email}",'123456', True, True, random.randint(30,200), 'actor.png', 'white.png')
                )
        
    else:
        cur.execute("INSERT OR IGNORE INTO 'user' (username,email,password,is_active,is_admin,duration, image, banner) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (f"{username}",f"{email}",'123456', True, False, random.randint(30,200), 'actor.png', 'white.png')
                )
    if i <=10:
        cur.execute("INSERT OR IGNORE INTO 'leaderboard_list' (user_id,username,email,rank) VALUES (?, ?, ?, ?)",
                (i,f"{username}",f"{email}", i)
                )





# insert 10 product
for i in range(0,10):
    cur.execute("INSERT OR IGNORE INTO product (title,description, price, image) VALUES (?, ?, ?, ?)",
            (products[i]['title'],products[i]['description'], products[i]['price'],products[i]['image'] )
            )  


# insert 10 jobs
for i in range(0,10):
    cur.execute("INSERT OR IGNORE INTO job (title,description,from_salary,to_salary) VALUES (?, ?, ?, ?)",
            (jobs[i]['title'],jobs[i]['description'], random.randint(0,200), random.randint(200,400) )
            )




connection.commit()
connection.close()

