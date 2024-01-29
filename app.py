from flask_socketio import SocketIO
from flask import Flask, render_template, jsonify, request, session, flash, redirect
import sqlite3
import os



app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

def get_db_connection():
    conn = sqlite3.connect('database/truebeacon.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_historical_data(symbol, from_date, to_date):
    connection = sqlite3.connect("database/truebeacon.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT strftime('%Y-%m-%d %H:%M:%S', date) AS formatted_date, price
        FROM nifty
        WHERE instrument_name = ? AND date BETWEEN ? AND ?
    ''', (symbol, from_date, to_date))

    data = cursor.fetchall()
    connection.close()

    return data





@app.route('/')
def render_start_page():
    return render_template('index.html')


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



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['user_id']
        name=request.form['user_name']
        email=request.form['email']


        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO profile (user_id, user_name, email, password) VALUES (?, ?, ?, ?)", (username, name, email, password))
        conn.commit()
        conn.close()

        flash("User registered successfully!")
        return redirect('/signin')

    return render_template('signup.html')



@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/signin')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM holdings WHERE user_id = ?", (session['username'],))
    holdings_data = cursor.fetchall()

    total_pnl = sum(holding['pnl'] for holding in holdings_data)

    conn.close()


    holdings_data_dict = [dict(row) for row in holdings_data]


    socketio.emit('update_dashboard', {'holdings_data': holdings_data_dict, 'total_pnl': total_pnl},
                  room=session['username'], namespace='/')

    return render_template('dashboard.html', holdings_data=holdings_data, total_pnl=total_pnl)
@app.route('/profile')
def profile():

    if 'username' not in session:
        return redirect('/signin')


    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile WHERE user_id = ?", (session['username'],))
    user_profile = cursor.fetchone()
    conn.close()


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


        place_order_response = {
            "status": "success",
            "message": f"Order placed for {quantity} shares of {symbol} at {price} per share."
        }


        return jsonify(place_order_response)



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


if __name__ == '__main__':
    socketio.run(app, debug=True)


