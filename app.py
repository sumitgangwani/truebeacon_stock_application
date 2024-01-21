# Importing required functions
from flask import Flask, render_template, jsonify, request, session, flash, redirect
import sqlite3
import os
import requests

# Flask constructor
app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_db_connection():
    conn = sqlite3.connect('database/truebacon.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to get historical data based on query parameters
def get_historical_data(symbol, from_date, to_date):
    connection = sqlite3.connect("database/truebacon.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT strftime('%Y-%m-%d %H:%M:%S', date) AS formatted_date, price
        FROM nifty
        WHERE instrument_name = ? AND date BETWEEN ? AND ?
    ''', (symbol, from_date, to_date))

    data = cursor.fetchall()
    connection.close()

    return data




# Root endpoint
@app.route('/')
def render_start_page():
    return render_template('start.html')

# User Authentication Logic
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profile WHERE user_id = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user is not None:
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash("Invalid Login")

    return render_template('signin.html')


# User Registration Logic
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['user_id']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO profile (user_id, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        flash("User registered successfully!")
        return redirect('/signin')

    return render_template('signup.html')


# Modify the 'dashboard' route in app.py
@app.route('/dashboard')
def dashboard():
    # Check if the user is authenticated
    if 'username' not in session:
        return redirect('/signin')  # Redirect to signin page if not authenticated

    # Fetch data from the holdings table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM holdings WHERE user_id = ?", (session['username'],))
    holdings_data = cursor.fetchall()

    # Calculate total PNL
    total_pnl = sum(holding['pnl'] for holding in holdings_data)

    conn.close()

    # Render the dashboard template with the fetched data and total PNL
    return render_template('dashboard.html', holdings_data=holdings_data, total_pnl=total_pnl)

@app.route('/profile')
def profile():
    # Check if the user is authenticated
    if 'username' not in session:
        return redirect('/signin')  # Redirect to signin page if not authenticated

    # Fetch data from the profile table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile WHERE user_id = ?", (session['username'],))
    user_profile = cursor.fetchone()
    conn.close()

    # Render the profile template with the fetched data
    return render_template('profile.html', user_profile=user_profile)



@app.route('/chart')
def render_chart_page():
    return render_template('chart.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/order_successful', methods=['POST'])
def place_order():
    if request.method == 'POST':
        symbol = request.form['symbol']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        # Simulate API call to get place_order_response.json
        place_order_response = {
            "status": "success",
            "message": f"Order placed for {quantity} shares of {symbol} at {price} per share."
        }

        # Display the response in JSON format
        return jsonify(place_order_response)


# API endpoint to get historical data
@app.route('/historical-data', methods=['GET'])
def get_historical_api():
    symbol = request.args.get('symbol')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    if not all([symbol, from_date, to_date]):
        return jsonify({"error": "Missing parameters"}), 400

    try:
        data = get_historical_data(symbol, from_date, to_date)
        return render_template('historical-data.html', data={"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# Main Driver Function
if __name__ == '__main__':
    # Run the application on the local development server
    app.run(debug=True)


