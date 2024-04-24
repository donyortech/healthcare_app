from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'optional_default_secret_key')

def get_db_cursor():
    """Create and return a database cursor."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",  
            database="health_db"
        )
        return connection.cursor()
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None

@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

# # Example route using database cursor
# @app.route('/fetch_data')
# def fetch_data():
#     """Fetch data from the database."""
#     cursor = get_db_cursor()
#     if cursor:
#         cursor.execute("SELECT * FROM your_table_name")
#         data = cursor.fetchall()
#         cursor.close()
#         return render_template('data.html', data=data)
#     else:
#         return "Failed to connect to the database"

# Add this route to your Flask application
@app.route('/admin')
def admin_dashboard():
    """Render the admin dashboard page."""
    return render_template('admin.html')

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
    app.run(host='127.0.0.2', port=5000, debug=True)
