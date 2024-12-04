import time 
import math
import random


quests = [
    {"name": "Reise nach Beutelsend", "completed": False, "condition": "travel_to_beutelsend"},
] 

def checkQuestCompletion():
    global quests
   
                
    # Hier fügst du die Überprüfung für "Reise nach Beutelsend" hinzu
    if "travel_to_beutelsend" in [quest["condition"] for quest in quests]:
        for quest in quests:
            if quest["condition"] == "travel_to_beutelsend" and not quest["completed"]:
                # Beispiel: Bedingung "Reise nach Beutelsend" prüfen
                if currentLocation == "Beutelsend":
                    quest["completed"] = True
                    print(f"Quest '{quest['name']}' abgeschlossen!")
                    break
                
def showQuests():
    # Zeigt alle Quests und ihren Status an
    print("Aktuelle Quests:")
    for quest in quests:
        status = "Abgeschlossen" if quest["completed"] else "Offen"
        print(f"{quest['name']} - {status}") 
        
        

classtypes = ["Magier/in","Barbar/in","Bogenschütze/in"]
statnames = ["Attacke","Geschwindigkeit","Verteidigung","SpezialPower","Gesundheit"]
classStats = [[4,5,5,10,100],[10,7,3,3,100],[7,10,5,1,100]]
pName = ""
pStats = [0,0,0,0,0]
statAdjustment = [0,0,0,0,0]
pClass = -1
pMoney = 500
pStatus = "Gut"
pLevel = 0 
pExp = 0 
currentLocation = "Höhle"
placestotravel = [["Beutelsend","Stardew Valley","Daytons Wetlands","Höhle"],[200,300,75,0]]
distanceFromHome = 0 
activityMenu = ["Statistiken anzeigen","Reisen","Laden","Inventar","Quests anzeigen","Item benutzen"]
itemsToBuy = [["Trank","Feuerheilung","Eisheilung","Statistikboost"],[100,50,50,200]]
itemsToFind = [["Trank","Feuerheilung","Eisheilung","Statistikboost","Billige Vase","Teure Vase","Müll"],[100,50,50,200,25,300,0]]
monsterTypes = [["Feuerdämon","Eisbandit","Baka the Duck","Schwacher Gegner","MEGA BOSS"],[10,8,5,1,20],[8,5,7,3,11],[5,7,3,1,15],[10,10,5,2,15],[120,120,75,30,300]]
inventory = ["Trank"]
escapeAttempt =[False,False]




def start_game():
    print("Willkommen zu meinem Text-Adventure!")
    input("Drücke Enter, um zu starten...")

    # Zeige das ASCII-Bild an diesem Punkt
    print_ascii_image()
def print_ascii_image():
    print("""
                o\\
   _________/__\\__________
  |                  - (  |
 ,'-.                 . `-|
(____".       ,-.    '   ||
  |          /\\,-\\   ,-.  |
  |      ,-./     \\ /'.-\\ |
  |     /-.,\\      /     \\|
  |    /     \\    ,-.     \\
  |___/_______\\__/___\\_____\\ 
""")

    input("Drücke Enter, um weiterzumachen...")
    print("Du befindest dich in einer ramponierten und zerstörten Höhle. Man könnte sagen es würde so aussehen, als wäre eine Bombe eingeschlagen. Hier und da sieht man Reste zerstörter Möbel. In einer Ecke steck ein halbkaputtes Bett und in der Mitte der Höhle siehst du eine Feuerstelle, von der große Rußspuren ausgehen. Vermutlich ging von dort eine Explosion aus. Wie du in diese Höhle kamst, weißt du nicht mehr und während du dich so umschaust merkst du auch das du gar nichts mehr außer deinem Namen weißt. All deine Erinnerungen sind wie ausgelöscht. Bevor du die Höhle verlässt schnapst du dir noch ein Trank und eine Karte und machst dich auf den Weg deine Erinnerungen wieder zu finden.")
    
    
    
start_game()

#Hilfsfunktionen
def indexInList(item,myList):
    foundIndex = -1
    for i in range(len(myList)):
        if(item == myList[i]):
            foundIndex = i 
            break 
    return foundIndex 

def listToText(myList):
    combinedText = "\n"
    for i in range(len(myList)):
        combinedText +=str(i) + ") " + myList[i] + "\n"
    return combinedText + "\n" 


def checkMenuRange(question,listName,isCancable = False):
    index = int(input(question + listToText(listName)))
    while(True):
        if(isCancable and index == -1):
            return index 
        elif index < 0 or index > len(listName) -1:
            index = int(input("Ungültige Auswahl, bitte versuchen Sie es erneut\n"))
        else:
            return index 
            


if "travel_to_beutelsend" in [quest["condition"] for quest in quests]:
        for quest in quests:
            if quest["condition"] == "travel_to_beutelsend" and not quest["completed"]:
                # Beispiel: Bedingung "Reise nach Beutelsend" prüfen
                if currentLocation == "Beutelsend":
                    quest["completed"] = True
                    print(f"Quest '{quest['name']}' abgeschlossen!")
                    break

def starLine(numRows,numSleep):
    sLine = "*" * 10 
    for i in range(numRows):
        print(sLine)
    time.sleep(numSleep)
    
def ShowInventory(InventoryList):
    if(len(InventoryList) < 1):
        print("Dein Inventar ist leer...")
        return
    uniqueInventoryList = list(set(InventoryList))
    for i in range(len(uniqueInventoryList)):
        print(str(i)+") " + uniqueInventoryList[i] + "("+str(InventoryList.count(uniqueInventoryList[i]))+")")
 
def useItemMenu():
    global pStatus
    ShowInventory(inventory)
    uniqueInventoryList = list(set(inventory))
    if(len(inventory) < 1):
        return
    chosenItem = checkMenuRange("Welches Item möchtest du benutzen?",uniqueInventoryList,True)
    if chosenItem == -1:
        return
    itemToUse = indexInList(uniqueInventoryList[chosenItem], itemsToFind[0])
    if(itemToUse == 0):
        pStats[4] += 10
        print("Du wurdest geheilt!")
    elif(itemToUse == 1):
        if(pStatus == "Gut" or pStatus == "erfrieren"):
            print("Feuerheilung hatte keinen Effekt")
        else:
            print(pName + " verbrennen wurde geheilt")
            pStatus = "Gut"
    elif(itemToUse == 2):
        if(pStatus == "Gut" or pStatus == "verbrennen"):
            print("Eisheilung hatte keinen Effekt")
        else:
            print(pName + " erfrieren wurde geheilt")
            pStatus = "Gut"
    elif(itemToUse == 3):
        checkStatBoost = checkMenuRange("Welchen Status möchtest du vorübergehend erhöhen?", ["Attacke","Geschwindigkeit","Verteidigung","SpezialPowerPower"])
        numBoost = math.ceil(pStats[checkStatBoost] * .1)
        pStats[checkStatBoost] += numBoost
        statAdjustment[checkStatBoost] += numBoost
        print("Status geboostet!")
    else:
        print("")
        
    if(itemToUse > 3):
        print("Es gibt eine Zeit und einen Ort für jeden Gegenstand!")
        starLine(1,2)
    else:
        print("Aktuelle Statistiken")
        for i in range(len(statnames)):
            print(statnames[i],pStats[i])
        inventory.remove(itemsToFind[0][itemToUse])
                
     
def PlayerAttack():
    global pStatus
    runStat = random.randint(0,100)
    
    fightChoice = checkMenuRange("Was möchtest du machen?",["Kämpfen","Item","Flüchten"])
    
    if(fightChoice == 0):
        attackType = checkMenuRange("Wähle eine Attacke aus!", ["Faust","Magie","Ausweichen"])
        monDefPercentage = 1- monsterStats[2] / 12
        if(attackType == 0):
            print("BOINK BOINK BOINK BA")
            damage = pStats[0] * monDefPercentage
            print("Schaden"+ str(damage))
            monsterStats[4] -= (damage)
        elif(attackType == 1):
            print("Wooosh WOOOOSCH Woosch")
            critChance = random.randint(0,100)
            critBonus = 1 
            if(critChance > 70):
                print("KTITISCHER TREFFER!")
                critBonus = 1.4
            damage = (pStats[3]* monDefPercentage) * critBonus
            print("Schaden"+ str(damage))
            monsterStats[4] -= damage
        else:
            #Attempt to dodge 
            escapeAttempt[0] = True 
        print("Monster Gesundheit" + str(monsterStats[4]))
        starLine(1,2)
    elif(fightChoice == 1):
        useItemMenu()
    else:
        #Try to run 
        if(pStats[1]/20 * 100 <= runStat):
            print("Du entkamst!")
            for i in range(len(statAdjustment)):
                pStats[i] -= statAdjustment[i]
                statAdjustment[i] = 0 
            escapeAttempt[1] = True
            starLine(2,1)
        else:
            print("Du konntest nicht entkommen!")
            
    return escapeAttempt
    

def MonsterAttack():
    global pStatus
    if(pStatus != "Gut"):
        if(pStatus == "verbrennen"):
            pStats[4] -=5 
            print(pName + "hat Schaden durch verbrennen erhalten!")
        else:
            pStats[4] -= 3
            print(pName + "hat Schaden durch erfrieren erhalten!")
        print(pName + " Gesundheit ist jetzt " + str(pStats[4]))
    print("Monster Runde")
    starLine(1,1) 
    attackOptionChance = random.randint(0,100)
    pDefPercentage = (1 - (pStats[2]/20))
    if(monsterChoice == 0):
        #Fire demon 
        if(attackOptionChance < 45):
            print("FEUERATEM!")
            pStats[4] -= monsterStats[3] * pDefPercentage
            burnChance = random.randint(0,100)
            if(burnChance < 30):
                print(pName + " verbrennt nun!")
                pStatus = "verbrennen"
        elif(attackOptionChance < 90):
            print(" KOPFSTOß!")
            pStats[4] -= monsterStats[0] * pDefPercentage
        else:
            tauntChance = random.randint(0,100)
            if (tauntChance < 10):
                print("Selbstheilung!")
                monsterStats[4] *= 1.1
            else:
                print("DU ABSOLUTER NARR!")
    elif(monsterChoice == 1):
        #Ice bandit  
        if(attackOptionChance < 45):
            print("EISATEM!")
            pStats[4] -= monsterStats[3] * pDefPercentage
            burnChance = random.randint(0,100)
            if(burnChance < 30):
                print(pName + " erfriert nun!")
                pStatus = "erfrieren"
        elif(attackOptionChance < 90):
            print("HOCHTRITT!")
            pStats[4] -= monsterStats[0] * pDefPercentage
        else:
            tauntChance = random.randint(0,100)
            if (tauntChance < 10):
                print("Selbstheilung!")
                monsterStats[4] *= 1.1
            else:
                print("LOL, du dachtest du könntest mich besiegen?!")
    elif(monsterChoice == 2):
        #Baka the duck 
        if(attackOptionChance < 50):
            #Taunt 
            print("Hi, Ich heiße Baka")
        else:
            print("HONK HONK HOOOONK SCHNABELATTACKE!")
            pStats[4] -= (monsterStats[0] *pDefPercentage)
    elif(monsterChoice == 3):
        #weak Enemy
        print("Boop auf die Nase!")
        pStats[4] -= (monsterStats[0] * pDefPercentage)
    else:
        #Mega Man Boss 
        megaDemonYells = ["Willkommen in der Höllendimension", "Die Hitze ist EWIG!!","Chugga chugga chugga chugga Höllendimension"]
        print(megaDemonYells[random.randint(0,len(megaDemonYells))])
        if(attackOptionChance < 45):
            print("SCHWARZE FLAMMEN DER HÖLLE!")
            pStats[4] -= monsterStats[3] * pDefPercentage
        elif(attackOptionChance < 90):
            print("KLATSCH,KNACKEN,KNALLEN!")
            pStats[4] -= monsterStats[0] * pDefPercentage
        else:
            tauntChance = random.randint(0,100)
            if(tauntChance < 10):
                print("DOPPELTE SELBSTHEILUNG!!")
                monsterStats[4] *= 1.2
            else:
                print("DU BIST NICHTS ALS EIN INSEKT FÜR EINEN GOTT!")
        
    print(pName + "Gesundheit: " + str(pStats[4]))
    
           
        


pName = input("Wie lautet dein Name?\n")
print("Willkommen in der wunderbaren Welt von Asparus " + pName + "!")
starLine(3,1)
for i in range(len(classtypes)):
    print(classtypes[i]+":")
    for j in range(len(classStats[i])):
        print(statnames[j],classStats[i][j])
    starLine(1,1.5)
pClass = checkMenuRange("Wähle deine Klasse: ",classtypes)
print("Du hast " + classtypes[pClass]+ " ausgesucht!")
pStats = classStats[pClass]
starLine(2,2)
print("Von nun an bist du bekannt als " + pName + " der/die " + classtypes[pClass])
starLine(1,3)
 


#Main loop 

inGameLoop = True
while(inGameLoop and pStats[4] > 0):
    #Stats,travel,inventory 
    actChoice = checkMenuRange("Was möchtest du tun? ",activityMenu)
    
    if(actChoice ==0):
        print("Deine Statistiken: ")
        for i in range(len(statnames)):
            print(statnames[1],pStats[i])
            
    elif(actChoice ==1):
        print("travel")
        travelChoice = checkMenuRange("Wo möchtest du hinreisen? ", placestotravel[0],True)
        if travelChoice == -1:
            isTravel = False
        else:
            isTravel = True
            print("Und so geht "+ pName+ " los um ihre/seine Errinerungen wiederzubekommen, auf nach "+placestotravel[0][travelChoice])
            if(placestotravel[1][travelChoice] == distanceFromHome):
                print("Wow! Das war aber schnell! Du bist ja schon da!")
                currentLocation = placestotravel[0][travelChoice]  # Aktuellen Ort setzen
                checkQuestCompletion()  # Überprüfe Quests, ob sie durch das Reisen abgeschlossen sind
                isTravel = False
            
        #Travel Loop 
        distanceDivider = random.randint(3, 6)
        distanceTraveled = math.ceil(placestotravel[1][travelChoice]/ distanceDivider)
        isTravelNeg = placestotravel[1][travelChoice] < distanceFromHome
        while(isTravel and pStats[4] > 0):
            if(not isTravelNeg):
                distanceFromHome += distanceTraveled
                if(distanceFromHome >= placestotravel[1][travelChoice]):
                    print("Du hast "+ placestotravel[0][travelChoice] + " erreicht!")
                    isTravel = False 
            else:
                distanceFromHome -= distanceTraveled
                if(distanceFromHome <= placestotravel[1][travelChoice]):
                    print("Du hast " + placestotravel[0][travelChoice] + " erreicht!")
                    isTravel = False
            if(not isTravel):
                distanceFromHome = placestotravel[1][travelChoice]
                break 
                    
            
            #random pickup or battle
            if(random.randint(0,100) < 60):
                inFight = True
                monsterPercentage = random.randint(0,100)
                monsterChoice = -1
                # fire, ice, baka, weak, mega boss Man
                if(monsterPercentage <= 25):
                    monsterChoice = 3
                elif(monsterPercentage <= 55):
                    monsterChoice = 0 
                elif(monsterPercentage < 85):
                    monsterChoice = 1 
                elif(monsterPercentage < 99):
                    monsterChoice = 2
                else:
                    monsterChoice = 4 
                    
                starLine(1,2)
                print("Du wurdest zum Kampf herausgefordert von/m " + monsterTypes[0][monsterChoice])
                starLine(1,1)
                monsterStats = [monsterTypes[1][monsterChoice],monsterTypes[2][monsterChoice],monsterTypes[3][monsterChoice],monsterTypes[4][monsterChoice],monsterTypes[5][monsterChoice]]
                chanceAdditional = 0 
                currentTurn = -1
                if(pStats[1]>monsterStats[1]):
                    chanceAdditional = random.randint(25,50)
                turnChance = 50 + chanceAdditional
                
                if(random.randint(0,100) < turnChance):
                    currentTurn *= -1
                
                while(inFight and pStats[4] > 0):
                    if(currentTurn == 1):
                        escapeAttempt = PlayerAttack()
                        if(escapeAttempt[1]):
                            escapeAttempt[1] = False
                            break
                    else:
                        incChance = 0 
                        if(pStats[1] > monsterStats[1]):
                            incChance = random.randint(25,50)
                        dChance = 25 + incChance
                        failChance = random.randint(0,100)
                        if(escapeAttempt[0]):
                            if(failChance < dChance):
                                print(pName + " ist knapp dem Angriff ausgewichen!")
                            else:
                                print("ausweichen ist fehlgeschlagen")
                                MonsterAttack()
                            escapeAttempt[0] = False 
                        else: 
                            MonsterAttack()
                    starLine(1,2)
                    
                    currentTurn *= -1 
                    
                    if(pStats[4] <= 0):
                        print("Die/der mächtige/r " + pName + " wurde besiegt....mögen sie in Ruhe frieden")
                        break
                    if(monsterStats[4] <= 0):
                        print(pName + " hat das Monster besiegt!")
                        for i in range(len(statAdjustment)):
                            pStats[i] -= statAdjustment[i]
                            statAdjustment[i] =0 
                        pExp += 10 
                        print(pName + " hat 10 Exp bekommen!")
                        starLine(1,1)
                        if(pExp % ((pLevel+1)*10) == 0):
                            pExp = 0 
                            if pLevel < 20:
                                pLevel += 1 
                                print(pName + " ist jetzt Level " + str(pLevel))
                                starLine(1,1)
                                print("Sie haben einen Statistikpunkt zur Verfügung, welchen werden Sie verwenden? ")
                                print("aktuelle Statistiken: ")
                                for i in range(len(statnames)):
                                    print(statnames[i],pStats[i])
                                sttIncreasChoice = checkMenuRange("", statnames)
                                pStats[sttIncreasChoice] += 1
                                print(statnames[sttIncreasChoice] + " ist jetzt " + str(pStats[sttIncreasChoice]))
                            
                        break 
                    
                
            else:
                #Random Pickup 
                starLine(1,1)
                print("Am Reisen......")
                starLine(1,1)
                pickUpChance = random.randint(0,100)
                if(pickUpChance < 20):
                    itemFound = itemsToFind[0][0]
                elif(pickUpChance < 30):
                    itemFound = itemsToFind[0][-1]
                elif(pickUpChance < 40):
                    itemFound = itemsToFind[0][2]
                elif(pickUpChance <45):
                    itemFound = itemsToFind[0][3]
                elif(pickUpChance < 65):
                    itemFound = itemsToFind[0][4]
                elif(pickUpChance < 69):
                    itemFound = itemsToFind[0][5]
                else:
                    itemFound = itemsToFind[0][6]
                        
                print(pName + "hat " + itemFound + " gefunden")
                addItemCheck = checkMenuRange("Möchten Sie das Item in Ihr Inventar aufnehmen?",["Ja","Nein"])
                if(addItemCheck == 0):
                    print(itemFound + " wurde deinem Inventar hinzugefügt!")
                    
                else:
                    print(itemFound + " wurde entsorgt")
                        
                starLine(1,1)
                print(pName + " setzt die Reise fort!")
                starLine(1,2)
                
    elif(actChoice ==2):
        while(True):
            print("Derzeitiger Kontostand: $" +str(pMoney))
            shopChoice = checkMenuRange("Willkommen in meinem Shop! Mein Name ist Ezro, wie kann ich Ihnen helfen? Möchten Sie kaufen oder verkaufen?",["Kaufen","Verkaufen","Inventar zeigen","Laden verlassen"],True)
            if(shopChoice == 3):
                break
            elif shopChoice ==0:
                #Buy
                buyChoice = checkMenuRange("Was würden Sie gerne kaufen?", itemsToBuy[0])
                if(pMoney - itemsToBuy[1][buyChoice] >= 0):
                    inventory.append(itemsToBuy[0][buyChoice])
                    pMoney -=itemsToBuy[1][buyChoice]
                else:
                    print("Tut mir leid sie können sich das nicht leisten..." + itemsToBuy[0][buyChoice])
            elif shopChoice ==1:
                if(len(inventory) > 0):
                    itemList = list(set(inventory))
                    ShowInventory(inventory)
                    sellChoice = checkMenuRange("Was würden Sie gerne verkaufen?", itemList)
                    if(sellChoice != -1):
                        itemIndex = indexInList(itemList[sellChoice],itemsToFind[0])
                        sellPrice = math.floor(itemsToFind[1][itemIndex] * .9)
                        ConfirmChoice = checkMenuRange("Sind Sie sicher, dass Sie verkaufen wollen, unser bester Preis ist " + str(sellPrice),["Ja","Nein"])
                        if ConfirmChoice ==0:
                            pMoney += sellPrice
                            inventory.remove(itemsToFind[0][itemIndex])
                            print("Artikel verkauft, aktueller Kontostand ist $"+str(pMoney))
                        else:
                            print("Ihr Pech!")
                else:
                    print("Leider haben Sie nichts zu verkaufen!")
            elif shopChoice ==2:
                ShowInventory(inventory)
                    
    elif(actChoice ==3):
        print("Dies ist Ihr Inventar")
        ShowInventory(inventory)
        
    elif(actChoice == 4):
        showQuests()  # Zeigt die Quests an
        starLine(1, 2)
            
    elif(actChoice == 5):  
        useItemMenu()
        







