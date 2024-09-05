from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import random
import string

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://url-shortener-abdulmateens-projects.vercel.app"]}})

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
    url = data.get('value')  #Gets the url

    code = generate_code(length=6)
    shortUrl = 'shorturl/' + code

    conn = psycopg2.connect(database="postgres",
                        host="aws-0-eu-central-1.pooler.supabase.com",
                        user="postgres.zbcxlqlgrhlncpuipnli",
                        password="123Abdul.mateen",
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
                (url, shortUrl))

    conn.commit()
    print("Created sucessfull!")

    cur.close()
    conn.close()
    return jsonify({"message": "message received!", "longUrl": url, "shortUrl": shortUrl}), 200
