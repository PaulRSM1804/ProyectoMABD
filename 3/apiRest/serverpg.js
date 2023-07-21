const express = require('express');
const { Pool } = require('pg');
const app = express();
const port = 4000;

const getData = async (conn, page = 1, limit = 100) => {
  const client = await conn.connect();
  const offset = (page - 1) * limit;
  try {
    const res = await client.query('SELECT * FROM Dataframe OFFSET $1 LIMIT $2', [offset, limit]); // Suponiendo que tu tabla se llama 'Dataframe'
    return res.rows;
  } finally {
    client.release();
  }
};

app.get('/data1', async (req, res) => {
  try {
    const conn = new Pool({
      host: 'localhost',
      port: 5440, 
      database: 'data',
      user: 'postgres', 
      password: 'admin', 
    });
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 100;
    const data = await getData(conn, page, limit);
    res.send(data);
  } catch (error) {
    res.status(500).send({ message: error.message });
  }
});

app.get('/data2', async (req, res) => {
  try {
    const conn = new Pool({
      host: 'localhost',
      port: 5441, 
      database: 'data',
      user: 'postgres', 
      password: 'admin', 
    });
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 100;
    const data = await getData(conn, page, limit);
    res.send(data);
  } catch (error) {
    res.status(500).send({ message: error.message });
  }
});

app.get('/data3', async (req, res) => {
  try {
    const conn = new Pool({
      host: 'localhost',
      port: 5442, 
      database: 'data',
      user: 'postgres', 
      password: 'admin', 
    });
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 100;
    const data = await getData(conn, page, limit);
    res.send(data);
  } catch (error) {
    res.status(500).send({ message: error.message });
  }
});

app.listen(port, () => {
  console.log(`El servidor esta ejecutado en el puerto: ${port}`);
});
