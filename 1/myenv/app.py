import csv
import uuid
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pymongo
import subprocess
import json

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/MyDatabase'


def connect_to_mongo():
    try:
        mongo = PyMongo(app)
        mongo.db.command('ping')  # Check if connection is active
        return mongo
    except pymongo.errors.ConnectionFailure:
        app.config['MONGO_URI'] = 'mongodb://localhost:27018/MyDatabase'
        return PyMongo(app)


mongo = connect_to_mongo()

# Configuración de paginación
DOCUMENTS_PER_PAGE = 10


@app.route('/')
def index():
    # Obtener número total de documentos
    total_documents = mongo.db.MyCollection.count_documents({})

    # Obtener el número de página a mostrar
    page = int(request.args.get('page', 1))

    # Calcular el índice de inicio y fin para la paginación
    start_index = (page - 1) * DOCUMENTS_PER_PAGE
    end_index = start_index + DOCUMENTS_PER_PAGE

    # Obtener los documentos de la colección con paginación
    documents = mongo.db.MyCollection.find().skip(start_index).limit(DOCUMENTS_PER_PAGE)

    return render_template('index.html', documents=documents, page=page, total_documents=total_documents,
                           DOCUMENTS_PER_PAGE=DOCUMENTS_PER_PAGE)



@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Crear un nuevo documento en la colección
        document = request.form.to_dict()
        document['supplierId'] = str(uuid.uuid4())

        # Convertir los valores de cadena a números
        numeric_fields = ['value', 'wm_yr_wk', 'wday', 'month', 'year', 'snap_CA', 'snap_TX', 'sell_price', 'dept_id',
                          'week', 'day']
        for field in numeric_fields:
            if field in document:
                try:
                    document[field] = int(document[field])
                except ValueError:
                    try:
                        document[field] = float(document[field])
                    except ValueError:
                        document[field] = None

        mongo.db.MyCollection.insert_one(document)
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    document = mongo.db.MyCollection.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        # Actualizar el documento existente en la colección
        updated_document = request.form.to_dict()

        # Convertir los valores de cadena a números
        numeric_fields = ['value', 'wm_yr_wk', 'wday', 'month', 'year', 'snap_CA', 'snap_TX', 'sell_price', 'dept_id',
                          'week', 'day']
        for field in numeric_fields:
            if field in updated_document:
                try:
                    updated_document[field] = int(updated_document[field])
                except ValueError:
                    try:
                        updated_document[field] = float(updated_document[field])
                    except ValueError:
                        updated_document[field] = None

        mongo.db.MyCollection.update_one({'_id': ObjectId(id)}, {'$set': updated_document})
        return redirect(url_for('index'))

    return render_template('update.html', document=document)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    # Eliminar un documento de la colección
    mongo.db.MyCollection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

@app.route("/execute_etl", methods=["GET"])
def execute_etl():
    try:
        # Ejecutar el script ETL
        subprocess.run(["python", "ETL.py"], check=True)
        message = "ETL realizado con éxito"
    except subprocess.CalledProcessError as e:
        message = f"Error al ejecutar el ETL: {e}"

    return jsonify({"message": message})


if __name__ == "__main__":
    app.run()
