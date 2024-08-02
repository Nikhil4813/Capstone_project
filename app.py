from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="demo",
    user="postgres",
    password="root",
    port="5433"
)
cur = conn.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Username :- {username},Password :- {password}")
        # cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        # conn.commit()
        try:
            # Start a new transaction
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()  # Commit the transaction if no errors
        except Exception as e:
            conn.rollback()  # Roll back the transaction if an error occurs
            print(f"An error occurred: {e}")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Username :- {username},Password :- {password}")
        try:
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()
            if user:
                session['username'] = username
                return redirect(url_for('home'))
            else:
                return "Invalid credentials"
        except Exception as e:
            print(f"An error occurred: {e}")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5500)
