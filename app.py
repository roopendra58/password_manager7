from flask import Flask, render_template, request, redirect
import sqlite3
import secrets
import string

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT,
        username TEXT,
        password TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Generate strong password
def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        website = request.form["website"]
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("INSERT INTO passwords (website,username,password) VALUES (?,?,?)",
                  (website, username, password))

        conn.commit()
        conn.close()

        return redirect("/")

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM passwords")
    data = c.fetchall()

    conn.close()

    return render_template("index.html", data=data)


@app.route("/generate")
def generate():
    return generate_password()



# ADD THIS DELETE CODE HERE
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("DELETE FROM passwords WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)