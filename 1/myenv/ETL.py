import pandas as pd
from pymongo import MongoClient
import psycopg2
from sklearn.decomposition import PCA
from pymongo.errors import PyMongoError

# Establecer la conexión a MongoDB
primary_uri = 'mongodb://localhost:27017/'
secondary_uri = 'mongodb://localhost:27018/'
try:
    mongo_client = MongoClient(primary_uri, serverSelectionTimeoutMS=2000)
    mongo_client.server_info()  # Prueba de conexión
    print(f"Conectado a MongoDB en {primary_uri}")
except PyMongoError:
    print(f"No se pudo conectar a MongoDB en {primary_uri}")

    # Si la conexión falla, intenta la instancia secundaria
    try:
        mongo_client = MongoClient(secondary_uri, serverSelectionTimeoutMS=2000)
        mongo_client.server_info()  # Prueba de conexión
        print(f"Conectado a MongoDB en {secondary_uri}")
    except PyMongoError:
        print(f"No se pudo conectar a MongoDB en {secondary_uri}")
        mongo_client = None


mongo_db = mongo_client['MyDatabase']
mongo_collection = mongo_db['MyCollection']

# Obtener los datos de la colección de MongoDB con proyección y límite
projection = {'_id': 0, 'value': 1, 'wm_yr_wk': 1, 'wday': 1, 'month': 1, 'year': 1, 'snap_CA': 1, 'snap_TX': 1,
              'sell_price': 1, 'dept_id': 1, 'week': 1, 'day': 1}
limit = 100  # Número de documentos a obtener
data = list(mongo_collection.find({}, projection=projection).limit(limit))

# Crear un DataFrame de Pandas a partir de los datos
df = pd.DataFrame(data)

##MINERIA DE DATOS
# Eliminar datos vacíos
df.dropna(inplace=True)

# Eliminar datos duplicados
df.drop_duplicates(inplace=True)

# Cambiar nombres de columnas
df.rename(columns={'day': 'dia', 'month': 'mes', 'year': 'anio'}, inplace=True)

# Exportar el nuevo DataFrame a un archivo CSV
csv_file_path = 'Dataframe.csv'
df.to_csv(csv_file_path, index=False)

# Aplicar PCA para reducir la dimensionalidad
pca = PCA(n_components=3)
df_pca = pca.fit_transform(df.iloc[:, 1:])  # Excluye la columna "value" en la transformación PCA

# Agregar las componentes principales al DataFrame
df['pca_component_1'] = df_pca[:, 0]  
df['pca_component_2'] = df_pca[:, 1]  
df['pca_component_3'] = df_pca[:, 2]  

# Eliminar columnas no importantes o redundantes
df.drop(['value'], axis=1, inplace=True)  # Elimina la columna "value" original

# Exportar el nuevo DataFrame a otros contenedores de Docker de MongoDB
nuevoMongoCliente1 = MongoClient('mongodb://localhost:27050/')
nuevoMongo1 = nuevoMongoCliente1['DataProcesada']
mongoCliente1 = nuevoMongo1['Dataframe']
mongoCliente1.delete_many({})

nuevoMongoCliente2 = MongoClient('mongodb://localhost:27051/')
nuevoMongo2 = nuevoMongoCliente2['DataProcesada']
mongoCliente2 = nuevoMongo2['Dataframe']
mongoCliente1.delete_many({})

nuevoMongoCliente3 = MongoClient('mongodb://localhost:27052/')
nuevoMongo3 = nuevoMongoCliente3['DataProcesada']
mongoCliente3 = nuevoMongo3['Dataframe']
mongoCliente1.delete_many({})
# Convertir el DataFrame a una lista
df_dict_list = df.to_dict(orient='records')

# Insertar los datos en los otros contenedores
mongoCliente1.insert_many(df_dict_list)
mongoCliente2.insert_many(df_dict_list)
mongoCliente3.insert_many(df_dict_list)

# Exportar el nuevo DataFrame a tres bases de datos PostgreSQL en lotes
pg_connection1 = psycopg2.connect(
    host='localhost',
    port=5440,
    user='postgres',
    password='admin',
    database='data'
)

pg_connection2 = psycopg2.connect(
    host='localhost',
    port=5441,
    user='postgres',
    password='admin',
    database='data'
)

pg_connection3 = psycopg2.connect(
    host='localhost',
    port=5442,
    user='postgres',
    password='admin',
    database='data'
)

pg_cursor1 = pg_connection1.cursor()
pg_cursor2 = pg_connection2.cursor()
pg_cursor3 = pg_connection3.cursor()


# Eliminar los datos en la tabla de Dataframe de cada base de datos de PostgreSQL
pg_delete_query = "DELETE FROM Dataframe"
pg_cursor1.execute(pg_delete_query)
pg_cursor2.execute(pg_delete_query)
pg_cursor3.execute(pg_delete_query)

# Confirmar los cambios en las bases de datos PostgreSQL
pg_connection1.commit()
pg_connection2.commit()
pg_connection3.commit()

# Crear una tabla en PostgreSQL para almacenar los datos preprocesados en cada base de datos
pg_create_table_query = "CREATE TABLE IF NOT EXISTS Dataframe (wm_yr_wk INT, wday INT, mes INT, anio INT, snap_CA INT, snap_TX INT, sell_price FLOAT, dept_id INT, week INT, dia INT, pca_component_1 FLOAT, pca_component_2 FLOAT, pca_component_3 FLOAT)"
pg_cursor1.execute(pg_create_table_query)
pg_cursor2.execute(pg_create_table_query)
pg_cursor3.execute(pg_create_table_query)

# Generar los valores para la consulta INSERT INTO
values = ', '.join(['%s'] * len(df.columns))
pg_insert_query = f"INSERT INTO Dataframe ({', '.join(df.columns)}) VALUES ({values})"

# Convertir los datos preprocesados a una lista de tuplas
valoresLote = [tuple(row) for row in df.values]

# Insertar los datos en lotes utilizando executemany en cada base de datos
tamañoLote = 1000
for i in range(0, len(valoresLote), tamañoLote):
    dataLote = valoresLote[i:i+tamañoLote]
    pg_cursor1.executemany(pg_insert_query, dataLote)
    pg_cursor2.executemany(pg_insert_query, dataLote)
    pg_cursor3.executemany(pg_insert_query, dataLote)

# Confirmar los cambios en las bases de datos PostgreSQL
pg_connection1.commit()
pg_connection2.commit()
pg_connection3.commit()

# Cerrar la conexión a las bases de datos PostgreSQL
pg_cursor1.close()
pg_cursor2.close()
pg_cursor3.close()
pg_connection1.close()
pg_connection2.close()
pg_connection3.close()
