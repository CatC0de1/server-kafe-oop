const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const fs = require('fs');
const cors = require('cors');
const path = require('path');
const { types } = require('util');
const app = express();
const port = 3003;

// app.use(cors());

app.use(cors({
    origin: ['http://localhost:3002', 'http://localhost:3004']
}));

const ItemSchema = new mongoose.Schema({
    name: String,
    price: String,
    availability: Boolean,
    description: String,
    image: String,
    types: Boolean,
    cold: Boolean
});

// const Item = mongoose.model('Item', ItemSchema);

function loadKafeData() {
    const filePath = path.join(__dirname, 'kafe.json');
    const data = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(data);
}

app.get('/api/kafe', (req, res) => {
    try {
        const kafeData = loadKafeData();
        res.json(kafeData);
    } catch (error) {
        res.status(500).send('Error membaca data kafe');
    }
});

mongoose.connect('mongodb+srv://catcode0101:1234admin@cluster0.ojr60.mongodb.net/Kafe?retryWrites=true&w=majority', {
    // useNewUrlParser: true,
    // useUnifiedTopology: true,
}). then(() => {
    console.log('Berhasil terkoneksi ke MongoDB Atlas');
}). catch((err) => {
    console.log('Gagal terkoneksi ke MongoDB Atlas');
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

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

// app.get('/api/collections', async (req, res) => {
//     try {
//         const collections = await mongoose.connection.db.listCollections().toArray();
//         res.json(collections.map(collection => collection.name));
//     } catch (error) {
//         res.status(500).json({ error: 'Gagal mendapatkan koleksi' });
//     }
// });

app.get('/api/collections/:collectionName', async (req, res) => {
    const { collectionName } = req.params;
    try {
        const collection = mongoose.connection.db.collection(collectionName);
        const data = await collection.find({}).toArray();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error:`Gagal mendapatkan data dari koleksi ${collectionName}` });
    }
});

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

app.listen(port, () => {
    console.log(`Server berjalan di http://localhost:${port}`);
});