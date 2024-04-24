from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'optional_default_secret_key')

def get_db_cursor():
    """Create and return a database connection and cursor."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",  
            database="health_db"
        )
        return connection, connection.cursor()
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None, None

@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@app.route('/admin')
def admin_dashboard():
    """Render the admin dashboard page."""
    return render_template('admin.html')

@app.route('/register', methods=['POST'])
def register_admin():
    """Register a new admin."""
    connection, cursor = get_db_cursor()
    if connection and cursor:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            cursor.execute("INSERT INTO Admin (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            connection.commit()
            return redirect('/admin')  # Redirect to admin dashboard after successful registration
        except mysql.connector.Error as e:
            print(f"Error registering admin: {e}")
            return "Failed to register admin"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Failed to connect to the database"

@app.route('/login', methods=['POST'])
def login_admin():
    """Login an admin."""
    connection, cursor = get_db_cursor()
    if connection and cursor:
        username = request.form['username']
        password = request.form['password']
        try:
            cursor.execute("SELECT * FROM Admin WHERE username = %s AND password = %s", (username, password))
            admin = cursor.fetchone()
            if admin:
                session['admin_id'] = admin[0]  # Store admin ID in session for authentication
                return redirect('/admin')  # Redirect to admin dashboard after successful login
            else:
                return "Invalid username or password"
        except mysql.connector.Error as e:
            print(f"Error logging in admin: {e}")
            return "Failed to login"
        finally:
            cursor.close()
            connection.close()
    else:
        return "Failed to connect to the database"
    
    
# Add this route to your Flask application
@app.route('/doctor')
def doctor():
    """Render the doctor information page."""
    return render_template('doctor.html')

# Add this route to your Flask application
@app.route('/patient')
def patient():
    """Render the patient information page."""
    return render_template('patient.html')

# Add this route to your Flask application
@app.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
