const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const fs = require('fs');
const cors = require('cors');
const path = require('path');

const app = express();

// Konfigurasi middleware
app.use(cors({
    origin: ['http://localhost:3002', 'http://localhost:3004']
}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Fungsi untuk memuat data JSON
function loadKafeData() {
    const filePath = path.join(__dirname, 'kafe.json');
    const data = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(data);
}

// Endpoint untuk mendapatkan data kafe
app.get('/api/kafe', (req, res) => {
    try {
        const kafeData = loadKafeData();
        res.json(kafeData);
    } catch (error) {
        res.status(500).send('Error membaca data kafe');
    }
});

// Endpoint untuk mendapatkan semua koleksi
app.get('/api/allCollections', async (req, res) => {
    try {
        const collections = await mongoose.connection.db.listCollections().toArray();
        const result = {};

        for (const collection of collections) {
            const collectionName = collection.name;
            const data = await mongoose.connection.db.collection(collectionName).find({}).toArray();
            result[collectionName] = data;
        }

        res.json(result);
    } catch (error) {
        res.status(500).json({ error: 'Gagal mendapatkan semua koleksi' });
    }
});

// Endpoint untuk mendapatkan data dari koleksi tertentu
app.get('/api/collections/:collectionName', async (req, res) => {
    const { collectionName } = req.params;
    try {
        const collection = mongoose.connection.db.collection(collectionName);
        const data = await collection.find({}).toArray();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: `Gagal mendapatkan data dari koleksi ${collectionName}` });
    }
});

// Endpoint untuk mendapatkan item tertentu berdasarkan ID
app.get('/api/:collectionName/:id', async (req, res) => {
    const { collectionName, id } = req.params;
    try {
        if (!mongoose.Types.ObjectId.isValid(id)) {
            return res.status(400).json({ error: 'ID tidak valid' });
        }

        const collection = mongoose.connection.db.collection(collectionName);
        const item = await collection.findOne({ _id: new mongoose.Types.ObjectId(id) });

        if (!item) {
            return res.status(404).json({ error: 'Item tidak ditemukan' });
        }

        res.json(item);
    } catch (error) {
        console.error('Error fetching item:', error);
        res.status(500).json({ error: 'Gagal mendapatkan data item.' });
    }
});

// Ekspor handler untuk Vercel
module.exports = app;