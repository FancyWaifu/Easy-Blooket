import requests, json, string, random

PIN_NUM = ""
GAME_NAME = ""
NUM_BOTS = ""

def grab_answers(PIN, NAME):
    name = ''.join(random.choices(string.ascii_letters+string.digits,k=9))

    r = requests.put("https://api.blooket.com/api/firebase/join", data={
    	"id": PIN,
    	"name": NAME
    }, headers={
    	"Referer": "https://www.blooket.com/"
    })

    firstPart = r.text.split('"set":"')[1]
    gameID = firstPart[0:firstPart.index('"')]

    r = requests.delete(f"https://api.blooket.com/api/firebase/client?id={PIN}&name={NAME}", headers={
    	"Referer": "https://www.blooket.com/"
    })

    r = requests.get(f"https://api.blooket.com/api/games?gameId={PIN}")
    questions = json.loads(r.text)["questions"]
    for question in questions:
    	print(f"{question['question']}: {question['correctAnswers'][0]}")

def kick_player(PIN, NAME):
    try:
        r = requests.delete(f"https://api.blooket.com/api/firebase/client?id={PIN}&name={NAME}", headers={
        	"Referer": "https://www.blooket.com/"
        })
        print("[*] Kicked " + NAME + " out of the game!")
    except:
        print("[!] Could not kick " + NAME + "out of the game!")

def mass_kick(PIN, NAME):
    try:
        r = requests.put("https://api.blooket.com/api/firebase/join", data={
        	"id": PIN,
        	"name": "blooketbad"
        }, headers={
        	"Referer": "https://www.blooket.com/"
        })

        joinText = r.text

        r = requests.delete(f"https://api.blooket.com/api/firebase/client?id={PIN}&name=blooketbad", headers={
        	"Referer": "https://www.blooket.com/"
        })

        players = json.loads(joinText)["host"]["c"].keys()
        for playerName in players:
        	r = requests.delete(f"https://api.blooket.com/api/firebase/client?id={PIN}&name={playerName}", headers={
        		"Referer": "https://www.blooket.com/"
        	})
        print("[*] Everyone was kicked from the game")
    except:
        print("[!] Could not kick everyone from the game")

def mass_join(PIN, NAME, NUMBER):
    for x in range(0, NUMBER):
        try:
            r = requests.put("https://api.blooket.com/api/firebase/join", data={'id': PIN, 'name': NAME + str(x+1)},
				headers={
				"Referer": "https://www.blooket.com/",
				"Host": "api.blooket.com",
				"Connection": "keep-alive",
				"Accept": "*/*",
				"Access-Control-Request-Method": "PUT",
				"Access-Control-Request-Headers": "content-type",
				"Origin": "https://www.blooket.com",
				"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0",
				"Sec-Fetch-Mode": "cors",
				"Sec-Fetch-Site": "same-site",
				"Sec-Fetch-Dest": "empty",
				"Referer": "https://www.blooket.com/",
				"Accept-Encoding": "gzip, deflate, br",
				"Accept-Language": "en-US,en;q=0.9"})
            print("[*] " + NAME + str(x+1) + " has joined the game!")
        except:
            print("[!] " + NAME + str(x+1) + " could not join!")

def grab_names(PIN):
    r = requests.put("https://api.blooket.com/api/firebase/join", data={
    	"id": PIN,
    	"name": "blooketbad"
    }, headers={
    	"Referer": "https://www.blooket.com/"
    })

    joinText = r.text

    r = requests.delete(f"https://api.blooket.com/api/firebase/client?id={PIN}&name=blooketbad", headers={
    	"Referer": "https://www.blooket.com/"
    })

    players = json.loads(joinText)["host"]["c"].keys()
    for playerName in players:
    	print(playerName)

def help_menu():
    print("[*] set PIN 123456 - Lets you set the game pin")
    print("[*] set NAME testtesttest - Lets you set the name for your bots or user you want to kick")
    print("[*] set BOT 10 - Set the number of bots to join a game")
    print("[*] use ANSWERS - does not work, will return error")
    print("[*] use MASSJOIN - will use PIN, NAME, and BOT to join a game, make sure there set")
    print("[*] use MASSKICK - will kick everyone from the game")
    print("[*] use NAMES - will return everyone in the game")
    print("[*] use KICK - will kick a single player")

def parse_command(COMMAND):
    global PIN_NUM
    global GAME_NAME
    global NUM_BOTS
    command = COMMAND.split()

    #parse the use commands
    if command[0] == "use":
        if command[1] == "ANSWERS":
            #grab_answers(PIN_NUM, GAME_NAME)
            print("[!] I told you not to use this one, doesn't work")
        if command[1] == "MASSJOIN":
            mass_join(PIN_NUM, GAME_NAME, int(NUM_BOTS))
        if command[1] == "MASSKICK":
            mass_kick(PIN_NUM, GAME_NAME)
        if command[1] == "NAMES":
            grab_names(PIN_NUM)
        if command[1] == "KICK":
            kick_player(PIN_NUM, GAME_NAME)

    #parse the set commands
    if command[0] == "set":
        if command[1] == "PIN":
            PIN_NUM = command[2]
            print("[!] PIN number set to " + PIN_NUM)
        if command[1] == "NAME":
            GAME_NAME = command[2]
            print("[!] Game name set to " + GAME_NAME)
        if command[1] == "BOT":
            NUM_BOTS = command[2]
            print("[!] The number of bots is set to " + NUM_BOTS)

    #print the payload options
    if command[0] == "options":
        print("[*] PIN NUMBER: " + PIN_NUM)
        print("[*] Name: " + GAME_NAME)
        print("[*] Number of bots: " + NUM_BOTS)

print("[*] Easy Blooket Scripts")
print("[*] Version: v1.0")
print('[*] Pull up the help menu by typing "help" and to exit type "exit"')

while True:
    choice = str(input("BlooketScripts> "))
    if choice == "help":
        help_menu()
    elif choice == "exit":
        print("[!] Bye Bye")
        break
    else:
        parse_command(choice)
