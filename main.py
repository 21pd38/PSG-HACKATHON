from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Replace with your database connection details
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="VamsKris@987",
    database="hotspots"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    cursor = db_connection.cursor(dictionary=True)

    # Fetch distinct Type and Incident IDs
    cursor.execute("SELECT DISTINCT type_id FROM incident")
    type_ids = cursor.fetchall()

    cursor.execute("SELECT DISTINCT incident_id FROM resolution")
    incident_ids = cursor.fetchall()

    resolutions = []

    # Model to pick the best resolution of all the resolutions by taking the parameters rating, frequency and security level.
    # These are the parameters which were solely defined by us and we use multiple regression.

    """
    def train_model():
    cursor = db_connection.cursor(dictionary=True)

    # Fetch data from the database including ratings, frequency, security level
    cursor.execute("SELECT incident_id, ratings, frequency, security_level FROM resolutions")
    data = cursor.fetchall()

    # Prepare features (X) and target (y)
    X = np.array([[row['ratings'], row['frequency'], row['security_level']] for row in data])
    y = np.array([row['incident_id'] for row in data])

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model"""

#trained_model = train_model()

    if request.method == 'POST':
        selected_type_id = request.form['type_id']
        selected_incident_id = request.form['incident_id']

        # Fetch resolutions for the selected Type and Incident
        cursor.execute("SELECT resolution_text FROM resolution WHERE incident_id = %s", (selected_incident_id,))
        resolutions = cursor.fetchall()

        # Fetch the selected Type and Incident names
        cursor.execute("SELECT type_name FROM type WHERE type_id = %s", (selected_type_id,))
        selected_type_name = cursor.fetchone()['type_name']

        cursor.execute("SELECT incident_name FROM incident WHERE incident_id = %s", (selected_incident_id,))
        selected_incident_name = cursor.fetchone()['incident_name']

        cursor.close()

        return render_template('index.html', type_ids=type_ids, incident_ids=incident_ids, resolutions=resolutions,
                               selected_type_name=selected_type_name, selected_incident_name=selected_incident_name,
                               selected_type_id=selected_type_id, selected_incident_id=selected_incident_id)

    cursor.close()

    return render_template('index.html', type_ids=type_ids, incident_ids=incident_ids, resolutions=resolutions,
                           selected_type_name=None, selected_incident_name=None,
                           selected_type_id=None, selected_incident_id=None)

if __name__ == '__main__':
    app.run(debug=True)