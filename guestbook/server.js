const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const db = require('./db'); // Importieren Sie die db.js-Datei

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public')); // Statische Dateien aus dem public-Ordner bereitstellen

// API-Endpunkt zum Speichern von Gästebucheinträgen
app.post('/api/guestbook', (req, res) => {
    const { name, message } = req.body;
    db.saveEntry(name, message)
        .then(() => res.json({ success: true }))
        .catch(err => res.status(500).json({ success: false, error: err }));
});

// API-Endpunkt zum Abrufen von Gästebucheinträgen
app.get('/api/guestbook', (req, res) => {
    db.getEntries()
        .then(entries => res.json(entries))
        .catch(err => res.status(500).json({ success: false, error: err }));
});

// Server starten
app.listen(PORT, () => {
    console.log(`Server läuft auf http://localhost:${PORT}`);
});
