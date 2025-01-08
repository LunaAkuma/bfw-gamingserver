document.getElementById('guestbookForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const message = document.getElementById('message').value;

    // Daten an den Server senden
    fetch('http://strapi-s8k0c8gkc0gs44k0g0o8ocgg.176.6.49.236.sslip.io:1337', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, message })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Zeigen Sie nur den aktuellen Eintrag an
        showCurrentEntry(name, message);
        // Leeren Sie das Formular
        resetForm();
    })
    .catch(error => console.error('Fehler:', error));
});

// Funktion zum Anzeigen des aktuellen Eintrags
function showCurrentEntry(name, message) {
    const entriesDiv = document.getElementById('guestbookEntries');
    entriesDiv.innerHTML = ''; // Vorherige Einträge löschen
    const entryDiv = document.createElement('div');
    entryDiv.textContent = `${name}: ${message}`;
    entriesDiv.appendChild(entryDiv);
}

// Funktion zum Zurücksetzen des Formulars
function resetForm() {
    document.getElementById('name').value = '';
    document.getElementById('message').value = '';
}

// Optionale Funktion zum Löschen des Eintrags bei Tab-Schluss
window.addEventListener('beforeunload', function() {
    resetForm();
});

   