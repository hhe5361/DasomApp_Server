from flask import Flask, request, jsonify
import pymysql
app = Flask(__name__)

# app.config['MYSQL_HOST'] = "내 sql 적으라는데"
# app.config['MySQL_USER'] = 'your_mysql_user'
# app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
# app.config['MYSQL_DB'] = 'your_mysql_db'
# mysql = MySQL(app)
host = ''
user = ''
password = ''
db = ''

mydb = pymysql.connect(host = host, user = user, password= password, charset='utf8')

@app.route('/api/calendar', methods=['POST'])
def add_event():
    try:
        title = request.json['title']
        student_id = request.json['student_id']
        date = request.json['date']
        content = request.json['content']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO events (title, student_id, date, content) VALUES (%s, %s, %s, %s)",
                    (title, student_id, date, content))
        mysql.connection.commit()
        cur.close()

        response = {
            "status": 200,
            "message": "Event added successfully."
        }

    except Exception as e:
        response = {
            "status": 500,
            "message": str(e)
        }

    return jsonify(response)

# API to delete an event
@app.route('/api/calendar', methods=['DELETE'])
def delete_event():
    try:
        event_id = request.args.get('id')

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
        mysql.connection.commit()
        cur.close()

        response = {
            "status": 200,
            "message": "Event deleted successfully."
        }

    except Exception as e:
        response = {
            "status": 500,
            "message": str(e)
        }

    return jsonify(response)

# API to get events
@app.route('/api/calendar', methods=['GET'])
def get_events():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, title, date FROM events")
        data = [{"id": row[0], "title": row[1], "date": row[2]} for row in cur.fetchall()]
        cur.close()

        response = {
            "status": 200,
            "data": data
        }

    except Exception as e:
        response = {
            "status": 500,
            "message": str(e)
        }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)