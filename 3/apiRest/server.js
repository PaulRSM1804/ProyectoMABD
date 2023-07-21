const express = require('express');
const mongoose = require('mongoose');
const app = express();
const port = 3000;

// Definir el esquema para los datos
const DataFrameSchema = new mongoose.Schema({}, { strict: false, collection: 'Dataframe' });

app.get('/data1', async (req, res) => {
    try {
        const conn = mongoose.createConnection('mongodb://localhost:27050/DataProcesada', { useNewUrlParser: true, useUnifiedTopology: true });
        const Dataframe = conn.model('Dataframe', DataFrameSchema);
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 100;
        const skip = (page - 1) * limit;
        const data = await Dataframe.find({}).skip(skip).limit(limit);
        
        // Enviar respuesta como JSON
        res.json(data);
    } catch (error) {
        res.status(500).send({ message: error.message });
    }
});

app.get('/data2', async (req, res) => {
    try {
        const conn = mongoose.createConnection('mongodb://localhost:27051/DataProcesada', { useNewUrlParser: true, useUnifiedTopology: true });
        const Dataframe = conn.model('Dataframe', DataFrameSchema);
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 100;
        const skip = (page - 1) * limit;
        const data = await Dataframe.find({}).skip(skip).limit(limit);
        res.send(data);
    } catch (error) {
        res.status(500).send({ message: error.message });
    }
});

app.get('/data3', async (req, res) => {
    try {
        const conn = mongoose.createConnection('mongodb://localhost:27052/DataProcesada', { useNewUrlParser: true, useUnifiedTopology: true });
        const Dataframe = conn.model('Dataframe', DataFrameSchema);
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 100;
        const skip = (page - 1) * limit;
        const data = await Dataframe.find({}).skip(skip).limit(limit);
        res.send(data);
    } catch (error) {
        res.status(500).send({ message: error.message });
    }
});

app.listen(port, () => {
  console.log(`El servidor esta ejecutado en el puerto: ${port}`);
});
