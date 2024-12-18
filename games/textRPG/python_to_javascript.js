let quests = [
    {"name": "Reise nach Beutelsend", "completed": false, "condition": "travel_to_beutelsend"}
];

let classtypes = ["Magier/in", "Barbar/in", "Bogenschütze/in"];
let statnames = ["Attacke", "Geschwindigkeit", "Verteidigung", "SpezialPower", "Gesundheit"];
let classStats = [
    [4, 5, 5, 10, 100],
    [10, 7, 3, 3, 100],
    [8, 10, 5, 1, 100]
];
let pName = "";
let pStats = [0, 0, 0, 0, 0];
let statAdjustment = [0, 0, 0, 0, 0];
let pClass = -1;
let pMoney = 500;
let pStatus = "Gut";
let pLevel = 0;
let pExp = 0;
let currentLocation = "Höhle";
let placestotravel = [["Beutelsend", "Stardew Valley", "Daytons Wetlands", "Höhle"], [200, 300, 75, 0]];
let distanceFromHome = 0;
let activityMenu = ["Statistiken anzeigen", "Reisen", "Laden", "Inventar", "Quests anzeigen", "Item benutzen"];
let itemsToBuy = [["Trank", "Feuerheilung", "Eisheilung", "Statistikboost"], [75, 50, 50, 100]];
let itemsToFind = [["Trank", "Feuerheilung", "Eisheilung", "Statistikboost", "Billige Vase", "Teure Vase", "Müll"], [100, 50, 50, 200, 25, 300, 0]];
let monsterTypes = [["Feuerdämon", "Eisbandit", "Baka the Duck", "Schwacher Gegner", "MEGA BOSS"], [10, 8, 3, 1, 15], [8, 5, 3, 3, 9], [5, 7, 3, 1, 7], [10, 10, 3, 2, 5], [120, 120, 75, 30, 100]];
let inventory = ["Trank"];
let escapeAttempt = [false, false];

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function indexInList(item, myList) {
    return myList.indexOf(item);
}

function listToText(myList) {
    let combinedText = "\n";
    for (let i = 0; i < myList.length; i++) {
        combinedText += `${i}) ${myList[i]}\n`;
    }
    return combinedText + "\n";
}

function checkMenuRange(question, listName, isCancable = false) {
    let index = parseInt(prompt(question + listToText(listName)));
    while (true) {
        if (isCancable && index === -1) {
            return index;
        } else if (index < 0 || index >= listName.length) {
            index = parseInt(prompt("Ungültige Auswahl, bitte versuchen Sie es erneut\n"));
        } else {
            return index;
        }
    }
}

function checkQuestCompletion() {
    for (let quest of quests) {
        if (quest.condition === "travel_to_beutelsend" && !quest.completed) {
            if (currentLocation === "Beutelsend") {
                quest.completed = true;
                console.log(`Quest '${quest.name}' abgeschlossen!`);
                break;
            }
        }
    }
}

function showQuests() {
    console.log("Aktuelle Quests:");
    for (let quest of quests) {
        let status = quest.completed ? "Abgeschlossen" : "Offen";
        console.log(`${quest.name} - ${status}`);
    }
}

function print_ascii_image() {
    console.log(`
                o\\
   _________/__\\__________
  |                  - (  |
 ,'-.                 . \`-|
(____".       ,-.    '   ||
  |          /\\,-\\   ,-.  |
  |      ,-./     \\ /'.-\\ |
  |     /-.,\\      /     \\|
  |    /     \\    ,-.     \\
  |___/_______\\__/___\\_____\\ 
`);
    prompt("Drücke Enter, um weiterzumachen...");
    console.log("Du befindest dich in einer ramponierten und zerstörten Höhle...");
}

function start_game() {
    console.log("Willkommen zu meinem Text-Adventure!");
    prompt("Drücke Enter, um zu starten...");
    print_ascii_image();
}

function starLine(numRows, numSleep) {
    let sLine = "*".repeat(10);
    for (let i = 0; i < numRows; i++) {
        console.log(sLine);
    }
    sleep(numSleep * 1000);
}

async function useItemMenu() {
    showInventory(inventory);
    let uniqueInventoryList = [...new Set(inventory)];
    if (inventory.length < 1) {
        return;
    }
    let chosenItem = await checkMenuRange("Welches Item möchtest du benutzen?", uniqueInventoryList, true);
    if (chosenItem === -1) {
        return;
    }
    let itemToUse = indexInList(uniqueInventoryList[chosenItem], itemsToFind[0]);
    if (itemToUse === 0) {
        pStats[4] += 20;
        console.log("Du wurdest geheilt!");
    } else if (itemToUse === 1) {
        if (pStatus === "Gut" || pStatus === "erfrieren") {
            console.log("Feuerheilung hatte keinen Effekt");
        } else {
            console.log(`${pName} verbrennen wurde geheilt`);
            pStatus = "Gut";
        }
    } else if (itemToUse === 2) {
        if (pStatus === "Gut" || pStatus === "verbrennen") {
            console.log("Eisheilung hatte keinen Effekt");
        } else {
            console.log(`${pName} erfrieren wurde geheilt`);
            pStatus = "Gut";
        }
    } else if (itemToUse === 3) {
        let checkStatBoost = await checkMenuRange("Welchen Status möchtest du vorübergehend erhöhen?", ["Attacke", "Geschwindigkeit", "Verteidigung", "SpezialPowerPower"]);
        let numBoost = Math.ceil(pStats[checkStatBoost] * 0.1);
        pStats[checkStatBoost] += numBoost;
        statAdjustment[checkStatBoost] += numBoost;
        console.log("Status geboostet!");
    } else {
        console.log("");
    }

    if (itemToUse > 3) {
        console.log("Es gibt eine Zeit und einen Ort für jeden Gegenstand!");
        starLine(1, 2);
    } else {
        console.log("Aktuelle Statistiken");
        for (let i = 0; i < statnames.length; i++) {
            console.log(`${statnames[i]}: ${pStats[i]}`);
        }
        inventory.splice(inventory.indexOf(itemsToFind[0][itemToUse]), 1);
    }
}

function showInventory(InventoryList) {
    if (InventoryList.length < 1) {
        console.log("Dein Inventar ist leer...");
        return;
    }
    let uniqueInventoryList = [...new Set(InventoryList)];
    for (let i = 0; i < uniqueInventoryList.length; i++) {
        console.log(`${i}) ${uniqueInventoryList[i]} (${InventoryList.filter(item => item === uniqueInventoryList[i]).length})`);
    }
}

function PlayerAttack() {
    let runStat = Math.floor(Math.random() * 101);

    let fightChoice = checkMenuRange("Was möchtest du machen?", ["Kämpfen", "Item", "Flüchten"]);

    if (fightChoice === 0) {
        let attackType = checkMenuRange("Wähle eine Attacke aus!", ["Faust", "Magie", "Ausweichen"]);
        let monDefPercentage = 1 - monsterStats[2] / 12;
        let damage = 0;
        if (attackType === 0) {
            console.log("BOINK BOINK BOINK BA");
            damage = pStats[0] * monDefPercentage;
            console.log(`Schaden: ${damage}`);
            monsterStats[4] -= damage;
        } else if (attackType === 1) {
            console.log("Wooosh WOOOOSCH Woosch");
            let critChance = Math.floor(Math.random() * 101);
            let critBonus = 1;
            if (critChance > 70) {
                console.log("KRITISCHER TREFFER!");
                critBonus = 1.4;
            }
            damage = pStats[3] * monDefPercentage * critBonus;
            console.log(`Schaden: ${damage}`);
            monsterStats[4] -= damage;
        } else {
            escapeAttempt[0] = true;
        }
        console.log(`Monster Gesundheit: ${monsterStats[4]}`);
        starLine(1, 2);
    } else if (fightChoice === 1) {
        await useItemMenu();
    }
    else {
        console.log("Flucht war erfolgreich!");
        currentLocation = "Höhle";
        monsterStats[4] = 100;
    }
}

start_game();
