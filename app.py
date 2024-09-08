from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import psycopg2
import random
import string
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://url-shortener-chi-nine.vercel.app/"]}})

@app.route('/api/data', methods=['GET'])
def get_data():
    return {
        'user': 'Abdulmateen',
        'message': 'Hello World!',
        }

# A fuction that generates codes
def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    short_codes = ''.join(random.choices(characters, k=length))
    return short_codes

@app.route('/create', methods=['POST'])
def create():
    #Getting data from frontend
    data = request.get_json()
    long_url = data.get('value')  #Gets the url

    code = generate_code(length=6)
    short_url = request.url_root + code

    conn = psycopg2.connect(database="postgres",
                        host=os.getenv("DATABASE_HOST"),
                        user=os.getenv("DATABASE_USER"),
                        password=os.getenv("DATABASE_PASSWORD"),
                        port="6543")
    
    cur = conn.cursor()

    #Write some queries to create table if it doesn't exist
    cur.execute("""CREATE TABLE IF NOT EXISTS url_shortener(
                id            SERIAL PRIMARY KEY,
                original_url  VARCHAR(255) NOT NULL,
                shorten_url   VARCHAR(255),
                createdAt     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
    
    cur.execute("""INSERT INTO url_shortener(original_url, shortened_url)
                VALUES(%s, %s);
                """,
                (long_url, short_url))

    conn.commit()
    print("Created sucessfull!")

    cur.close()
    conn.close()
    return jsonify({"message": "message received!", "long_url": long_url, "short_url": short_url}), 200

@app.route('/<short_url>')
def redirect_url(short_url):
    conn = psycopg2.connect(database="postgres",
                        host=os.getenv("DATABASE_HOST"),
                        user=os.getenv("DATABASE_USER"),
                        password=os.getenv("DATABASE_PASSWORD"),
                        port="6543")
    
    cur = conn.cursor()

    cur.execute("""SELECT original_url FROM url_shortener WHERE short_url = %s""", (short_url,))
    #fetch original_url if it exists
    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        original_url = result[0]
        return redirect(original_url)
    return "URL Not Found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)