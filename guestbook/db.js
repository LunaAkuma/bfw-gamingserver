const entriesDiv = document.getElementById("entryContainer");
const authorInput = document.getElementById("name");
const messageInput = document.getElementById("message");
const STORAGE_KEY = "guestbookEntries";

let guestbookEntries = [];

function loadEntries() {
  const storedEntries = localStorage.getItem(STORAGE_KEY);
  if (storedEntries) {
    guestbookEntries = JSON.parse(storedEntries);
  }
  displayEntries();
}

function saveEntries() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(guestbookEntries));
}

function displayEntries() {
  entriesDiv.innerHTML = ""; // Clear existing entries

  guestbookEntries.forEach((entry) => {
    const entryDiv = document.createElement("div");
    entryDiv.classList.add("entry"); // Add a class for styling (optional)
    entryDiv.innerHTML = `
        <h3>${entry.author}</h3>
        <p>${entry.message}</p>
        <small>${entry.creationDate}</small>
      `;
    entriesDiv.appendChild(entryDiv);
  });
}

function addEntry() {
  const author = authorInput.value.trim();
  const message = messageInput.value.trim();

  if (author === "" || message === "") {
    alert("Please enter both your name and a message.");
    return;
  }

  const newEntry = {
    author: author,
    message: message,
    creationDate: new Date().toLocaleString(),
  };

  guestbookEntries.push(newEntry);
  saveEntries();
  displayEntries();

  // Clear input fields
  authorInput.value = "";
  messageInput.value = "";
}

// Load entries when the page loads
window.onload = loadEntries;
