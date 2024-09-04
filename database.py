import psycopg2


conn = psycopg2.connect(database="postgres",
                        host="aws-0-eu-central-1.pooler.supabase.com",
                        user="postgres.zbcxlqlgrhlncpuipnli",
                        password="123Abdul.mateen",
                        port="6543")

cur = conn.cursor()

#Write some queries
cur.execute("""CREATE TABLE IF NOT EXISTS url_shortener(
            id            SERIAL PRIMARY KEY,
            original_url  VARCHAR(255) NOT NULL,
            shortened_url VARCHAR(255),
            createdAt     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

#Inserting into table
cur.execute("""INSERT INTO url_shortener(original_url)
            VALUES(%s);
            """,
            ('https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries',))


conn.commit()

cur.close()
conn.close()