// JavaScript-Implementierung des Python-Codes

const quests = [
    { name: "Reise nach Beutelsend", completed: false, condition: "travel_to_beutelsend" }
];

let classtypes = ["Magier/in", "Barbar/in", "Bogenschütze/in"];
let statnames = ["Attacke", "Geschwindigkeit", "Verteidigung", "SpezialPower", "Gesundheit"];
let classStats = [[4, 5, 5, 10, 100], [10, 7, 3, 3, 100], [8, 10, 5, 1, 100]];
let pName = "";
let pStats = [0, 0, 0, 0, 0];
let statAdjustment = [0, 0, 0, 0, 0];
let pClass = -1;
let pMoney = 500;
let pStatus = "Gut";
let pLevel = 0;
let pExp = 0;
let currentLocation = "Höhle";
let placestotravel = [
    ["Beutelsend", "Stardew Valley", "Daytons Wetlands", "Höhle"],
    [200, 300, 75, 0]
];
let distanceFromHome = 0;
let activityMenu = ["Statistiken anzeigen", "Reisen", "Laden", "Inventar", "Quests anzeigen", "Item benutzen"];
let itemsToBuy = [["Trank", "Feuerheilung", "Eisheilung", "Statistikboost"], [75, 50, 50, 100]];
let itemsToFind = [["Trank", "Feuerheilung", "Eisheilung", "Statistikboost", "Billige Vase", "Teure Vase", "Müll"], [100, 50, 50, 200, 25, 300, 0]];
let monsterTypes = [
    ["Feuerdämon", "Eisbandit", "Baka the Duck", "Schwacher Gegner", "MEGA BOSS"],
    [10, 8, 3, 1, 15],
    [8, 5, 3, 3, 9],
    [5, 7, 3, 1, 7],
    [10, 10, 3, 2, 5],
    [120, 120, 75, 30, 100]
];
let inventory = ["Trank"];
let escapeAttempt = [false, false];

function startGame() {
    console.log("Willkommen zu meinem Text-Adventure!");
    prompt("Drücke Enter, um zu starten...");
    printAsciiImage();
}

function printAsciiImage() {
    console.log(`
                o\\
   _________/__\\__________
  |                  - (  |
 ,'-.                 . `-|
(____".       ,-.    '   ||
  |          /\\,-\\   ,-.  |
  |      ,-./     \\/'.-\\ |
  |     /-.,\\      /     \\
  |    /     \\    ,-.     \\
  |___/_______\\__/___\\_____\\ 
`);
    prompt("Drücke Enter, um weiterzumachen...");
    console.log("Du befindest dich in einer ramponierten und zerstörten Höhle...");
}

function showQuests() {
    console.log("Aktuelle Quests:");
    quests.forEach(quest => {
        let status = quest.completed ? "Abgeschlossen" : "Offen";
        console.log(`${quest.name} - ${status}`);
    });
}

function checkQuestCompletion() {
    if (quests.some(quest => quest.condition === "travel_to_beutelsend")) {
        quests.forEach(quest => {
            if (quest.condition === "travel_to_beutelsend" && !quest.completed) {
                if (currentLocation === "Beutelsend") {
                    quest.completed = true;
                    console.log(`Quest '${quest.name}' abgeschlossen!`);
                }
            }
        });
    }
}

function listToText(list) {
    return list.map((item, index) => `${index}) ${item}`).join("\n") + "\n";
}

function checkMenuRange(question, listName, isCancellable = false) {
    let index = parseInt(prompt(`${question}\n${listToText(listName)}`), 10);
    while (true) {
        if (isCancellable && index === -1) return index;
        if (index < 0 || index >= listName.length) {
            index = parseInt(prompt("Ungültige Auswahl, bitte versuchen Sie es erneut\n"), 10);
        } else {
            return index;
        }
    }
}

function starLine(numRows, numSleep) {
    let sLine = "*".repeat(10);
    for (let i = 0; i < numRows; i++) {
        console.log(sLine);
    }
    setTimeout(() => {}, numSleep * 1000);
}

function showInventory(inventoryList) {
    if (inventoryList.length < 1) {
        console.log("Dein Inventar ist leer...");
        return;
    }
    let uniqueInventoryList = [...new Set(inventoryList)];
    uniqueInventoryList.forEach((item, index) => {
        console.log(`${index}) ${item} (${inventoryList.filter(i => i === item).length})`);
    });
}

// Ähnliche Struktur für andere Funktionen erstellen...

// Start des Spiels
startGame();