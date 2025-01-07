const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('guestbook.db');

db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, name TEXT, message TEXT)");
});

function saveEntry(name, message) {
    return new Promise((resolve, reject) => {
        db.run("INSERT INTO entries (name, message) VALUES (?, ?)", [name, message], function(err) {
            if (err) {
                return reject(err);
            }
            resolve(this.lastID);
        });
    });
}

function getEntries() {
    return new Promise((resolve, reject) => {
        db.all("SELECT * FROM entries", [], (err, rows) => {
            if (err) {
                return reject(err);
            }
            resolve(rows);
        });
    });
}

module.exports = { saveEntry, getEntries };
