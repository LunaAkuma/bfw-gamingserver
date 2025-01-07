const mysql = require('mysql');

// Ersetzen Sie die Platzhalter durch Ihre Datenbankverbindungsdetails
const connection = mysql.createConnection({
    host: '3306', // oder die IP-Adresse des MySQL-Servers
    user: 'mysql',
    password: 'Y75kuZ1x7m7IBnvrKXItmynaxi6wOde9t1GVGfe4IDy68',
    database: 'Database'
});

// Verbindung zur Datenbank herstellen
connection.connect((err) => {
    if (err) {
        console.error('Fehler bei der Verbindung zur Datenbank: ' + err.stack);
        return;
    }
    console.log('Verbunden mit der Datenbank als ID ' + connection.threadId);
});

// Funktion zum Speichern eines Eintrags
function saveEntry(name, message) {
    return new Promise((resolve, reject) => {
        const query = 'INSERT INTO entries (name, message) VALUES (?, ?)';
        connection.query(query, [name, message], (err, results) => {
            if (err) {
                return reject(err);
            }
            resolve(results.insertId);
        });
    });
}

// Funktion zum Abrufen der Einträge
function getEntries() {
    return new Promise((resolve, reject) => {
        connection.query('SELECT * FROM entries', (err, rows) => {
            if (err) {
                return reject(err);
            }
            resolve(rows);
        });
    });
}

module.exports = { saveEntry, getEntries };
