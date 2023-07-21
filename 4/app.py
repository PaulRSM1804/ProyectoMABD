import bson
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pymongo
from bson import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27050/DataProcesada'


def connect_to_mongo():
    try:
        mongo = PyMongo(app)
        mongo.db.command('ping')  # Check if connection is active
        return mongo
    except pymongo.errors.ConnectionFailure:
        app.config['MONGO_URI'] = 'mongodb://localhost:27051/DataProcesada'
        return PyMongo(app)


mongo = connect_to_mongo()

# Configuración de paginación
DOCUMENTS_PER_PAGE = 12


@app.route('/')
def index():
    # Obtener número total de documentos
    total_documents = mongo.db.Dataframe.count_documents({})

    # Obtener el número de página a mostrar
    page = int(request.args.get('page', 1))

    # Calcular el índice de inicio y fin para la paginación
    start_index = (page - 1) * DOCUMENTS_PER_PAGE
    end_index = start_index + DOCUMENTS_PER_PAGE

    # Obtener los documentos de la colección con paginación
    documents = mongo.db.Dataframe.find().skip(start_index).limit(DOCUMENTS_PER_PAGE)

    return render_template('index.html', documents=documents, page=page, total_documents=total_documents,
                           DOCUMENTS_PER_PAGE=DOCUMENTS_PER_PAGE)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Crear un nuevo documento en la colección
        document = {
            'wm_yr_wk': request.form.get('wm_yr_wk'),
            'wday': request.form.get('wday'),
            'mes': request.form.get('mes'),
            'anio': request.form.get('anio'),
            'snap_CA': request.form.get('snap_CA'),
            'snap_TX': request.form.get('snap_TX'),
            'sell_price': request.form.get('sell_price'),
            'dept_id': request.form.get('dept_id'),
            'week': request.form.get('week'),
            'dia': request.form.get('dia'),
            'pca_component_1': request.form.get('pca_component_1'),
            'pca_component_2': request.form.get('pca_component_2'),
            'pca_component_3': request.form.get('pca_component_3')
        }

        mongo.db.Dataframe.insert_one(document)
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    document = mongo.db.Dataframe.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        # Actualizar el documento existente en la colección
        updated_document = {
            'wm_yr_wk': request.form.get('wm_yr_wk'),
            'wday': request.form.get('wday'),
            'mes': request.form.get('mes'),
            'anio': request.form.get('anio'),
            'snap_CA': request.form.get('snap_CA'),
            'snap_TX': request.form.get('snap_TX'),
            'sell_price': request.form.get('sell_price'),
            'dept_id': request.form.get('dept_id'),
            'week': request.form.get('week'),
            'dia': request.form.get('dia'),
            'pca_component_1': request.form.get('pca_component_1'),
            'pca_component_2': request.form.get('pca_component_2'),
            'pca_component_3': request.form.get('pca_component_3')
        }

        mongo.db.Dataframe.update_one({'_id': ObjectId(id)}, {'$set': updated_document})
        return redirect(url_for('index'))

    return render_template('update.html', document=document)


@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    # Eliminar un documento de la colección
    mongo.db.Dataframe.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))


from bson import ObjectId

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Obtener el parámetro 'query' de la URL

    # Limpiar el valor de la consulta eliminando espacios en blanco adicionales
    query = query.strip()

    try:
        # Intentar crear un ObjectId válido a partir de la consulta
        object_id = ObjectId(query)

        # Realizar la búsqueda en la colección Dataframe utilizando el ObjectId
        documents = mongo.db.Dataframe.find({
            '_id': object_id
        })

        return render_template('search.html', documents=documents, query=query)
    except bson.errors.InvalidId:
        # Manejar el caso en el que la consulta no sea un ObjectId válido
        error_message = f"El valor de búsqueda '{query}' no es un ObjectId válido."
        return render_template('error.html', error_message=error_message)





if __name__ == "__main__":
    app.run(port=8080)  # Ejecutar la aplicación en el puerto 8080
