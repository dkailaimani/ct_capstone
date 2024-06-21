from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error
from password import my_password

from flask_cors import CORS



app = Flask(__name__)
CORS(app)
ma = Marshmallow(app)

class chosen_car_schema(ma.Schema):
    id = fields.Integer(required=True)
    type_of_car = fields.String(required=True)
    car_model = fields.String(required=True)
    car_name = fields.String(required=True)
    car_year = fields.Integer(required=True)
    car_cost = fields.Float(required=True)
    num_of_wheel_drive = fields.Integer(required=True)
    car_mileage = fields.Integer(required=True)
    car_color = fields.String(required=True)
    interior_material = fields.String(required=True)
    engine_type = fields.String(required=True)

    class Meta:
        fields = ("id", "type_of_car","car_model","car_name","car_year","car_cost","num_of_wheel_drive","car_mileage","car_color","interior_material","engine_type")
chosen_schema = chosen_car_schema()
chosens_schema = chosen_car_schema(many=True)

class car_build_schema(ma.Schema):
    id = fields.Integer(required=True)
    type_of_car = fields.String(required=True)
    num_of_doors = fields.Integer(required=True)

    class Meta:
        fields = ("id", "type_of_car", "num_of_doors")

car_schema = car_build_schema()
cars_schema = car_build_schema(many=True)

def get_db_connection():
    """Connect to the MySQL database and return the connection object"""
    db_name = "cardax_db"
    user = "root"
    password = my_password
    host = "localhost"

    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )
        print("Connected to MySQL database successfully")
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route("/chosen_car", methods=["GET"])
def get_chosen_car():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM chosen_car"
        cursor.execute(query)
        chosen_car = cursor.fetchall()

        return jsonify(chosens_schema.dump(chosen_car))
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/chosen_car", methods=["POST"])
def add_chosen_car():
    try:
        chosen_car_data = chosen_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_chosen_car = (
            chosen_car_data["id"],
            chosen_car_data["type_of_car"], chosen_car_data["car_model"], chosen_car_data["car_name"],
            chosen_car_data["car_year"], chosen_car_data["car_cost"], chosen_car_data["num_of_wheel_drive"],
            chosen_car_data["car_mileage"], chosen_car_data["car_color"],
            chosen_car_data["interior_material"], chosen_car_data["engine_type"]
        )

        query = "INSERT INTO chosen_car (id, type_of_car, car_model, car_name, car_year, car_cost, num_of_wheel_drive, car_mileage, car_color, interior_material, engine_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, new_chosen_car)
        conn.commit()

        return jsonify({"message": "New car added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/car_build", methods=["GET"])
def get_car_build():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM car_build"
        cursor.execute(query)
        car_build = cursor.fetchall()

        return jsonify(cars_schema.dump(car_build))
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/car_build", methods=["POST"])
def add_car_build():
    try:
        car_build_data = car_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_car_build = (
            car_build_data["id"], car_build_data["type_of_car"], car_build_data["num_of_doors"]
        )

        query = "INSERT INTO car_build (id, type_of_car, num_of_doors) VALUES (%s, %s, %s)"
        cursor.execute(query, new_car_build)
        conn.commit()

        return jsonify({"message": "New car build added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/chosen_car/<int:id>", methods=["PUT"])
def update_chosen_car(id):
    try:
        chosen_car_data = chosen_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_chosen_car = (
            chosen_car_data["type_of_car"],
            chosen_car_data["car_model"],
            chosen_car_data["car_name"],
            chosen_car_data["car_year"],
            chosen_car_data["car_cost"],
            chosen_car_data["num_of_wheel_drive"],
            chosen_car_data["car_mileage"],
            chosen_car_data["car_color"],
            chosen_car_data["interior_material"],
            chosen_car_data["engine_type"],
            id  
        )
        query = 'UPDATE chosen_car SET type_of_car = %s, car_model = %s, car_name = %s, car_year = %s, car_cost = %s, num_of_wheel_drive = %s, car_mileage = %s, car_color = %s, interior_material = %s, engine_type = %s WHERE id = %s'
        
        cursor.execute(query, updated_chosen_car)
        conn.commit()

        return jsonify({"message": "Car updated successfully"}), 200
        
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/chosen_car/<int:id>", methods=["DELETE"])
def delete_chosen_car(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        chosen_car_to_remove = (id,)

        cursor.execute("SELECT * FROM chosen_car WHERE id = %s", chosen_car_to_remove)
        chosen_car = cursor.fetchone()
        if not chosen_car:
            return jsonify({"error": "Car not found!"}), 404

        query = "DELETE FROM chosen_car WHERE id = %s"
        cursor.execute(query, chosen_car_to_remove)
        conn.commit()

        return jsonify({"message": "Car removed successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
