# A simple text game
# Patch notes:
# 1.3 (14/9/2021)
#   code rewrite: 
#       list -> dictionary for better code editing
#   game balancing:
#       life: unlimited -> 12 max health
#   bug fixes
# 1.2 (12/9/2021)
#   game balancing:
#       gold: 7% -> 6.5% reduced chance
#       jackpot: 0.5% -> 1% increased chance
#       plain: 2 -> 3 boxes to get coins
#   tips
#   cheatsheet
#   bug fix:
#       jackpot 1.5 damage not working
# 1.1 (9/8/2021)
#   game balancing:
#       robber: new mechanic: type random letters
#   random box choice
# 1.0 (19/1/2021)
#   unofficial launch
import random
import time
import string
plainb = 46     #boxes
bronzeb = 30
silverb = 22
goldb = 13
jackpotb = 2
medkitb = 8
freezeb = 30
flameb = 16
robberb = 20
poisonb = 10
explodeb = 3

tips = ['THERE ARE TWO JACKPOT BOXES, BUT ONLY ONE WILL BE ACTIVATED',
    'IT IS RECOMMENDED TO CHOOSE COINS OVER LIVES WHEN OPENING THE GOLD BOX, UNLESS YOU ARE IN DANGER',
    'ANOTHER FREEZE BOX DOES NOT REFRESH YOUR ROB NERF TIMER',
    'THE ROBBER BOX USED TO BE COMPLETELY LUCK BASED (25%)',
    'THERE IS A SECRET CODE YOU CAN TYPE INGAME TO ACCESS THE CHEAT SHEET OF ALL THE BOXES',
    'REMEMBER TO TYPE B WHILE INGAME TO VIEW YOUR REMAINING UNOPENED BOXES',
    'TRY OPENING ALL THE BOXES WITHOUT GETTING KILLED OR GETTING TOO MUCH MONEY TO UNLOCK AN ALTERNATE WIN',
    'YOUR SCORE IS CALCULATED WITH [coins - (boxes opened * 25) + (lives * 30)]',
    'THE POISON BOX USED TO BE EXTREMELY OVERPOWERED (ALTHOUGH IT STILL IS QUITE OP)',
    'EXPLOSIVE BOX RESETS EVERYTHING TO DEFAULT, EXCEPT FOR YOUR LIVES (1)',
    'WHEN FACING THE ROBBER BOX, IF YOU CAN\'T READ WORDS FAST ENOUGH, MEMORIZE THE WORDS AND IGNORE THE CAPITALIZATION TO REDUCE COIN LOSS',
    'GET AS MUCH HEALTH AS POSSIBLE BEFORE START GETTING COINS FROM BRONZE AND SILVER BOXES',
    'TYPE R TO OPEN A RANDOM BOX',
    'MAX HEALTH IS 12'
]

print('Welcome to boxes')
ruleknown = input('Press r for rules, or any other key to skip: ')
if ruleknown == 'r' or ruleknown == 'R':
    print('There are 200 boxes, you have to choose one box',
    '\nThere is a total of 11 types of boxes, 6 being buffs and 5 being debuffs',
    '\nFor instance, the bronze box provides you either 50 coins or 1 more life',
    '\nLosing all your lifes ends the game, and getting 1250 coins wins the game, you can also win the game by opening all the boxes without dying',
    '\nYou cannot open same boxes, you can check for any unopened boxes by typing b when choosing a box')
    input('continue? (any key)')
    print('Here is the list for all types of boxes',
    '\n\n'+str(plainb/2)+'% plain box: +20 coins for every two plain boxes you get, BUFF:NONE',
    '\n'+str(bronzeb/2)+'% bronze box: +100 coins/ +1 life BUFF:NONE',
    '\n'+str(silverb/2)+'% silver box: +150 coins/ +2 life BUFF:NONE',
    '\n'+str(goldb/2)+'% gold box: +200 coins/ +3 life BUFF:POISON EFFECT LAST 1 SECOND SHORTER',
    '\n'+str(jackpotb/2)+'% jackpot box: +1000 coins BUFF/DEBUFF:IMMUNE FROM ALL DEBUFFS, DAMAGE INCREASES TO 1.5X',
    '\n'+str(medkitb/2)+'% med kit: +4 life ',
    '\n% guard box')
    input('continue? (any key)')
    print('\n'+str(freezeb/2)+'% freeze box: -1 life DEBUFF:ROBBED DIFFICULTY INCREASE FOR NEXT 5 BOXES',
    '\n'+str(flameb/2)+'% flame box: -2 life DEBUFF:POISON EFFECT LAST 1 SECOND LONGER',
    '\n'+str(robberb/2)+'% robber in box: defend yourself by typing the correct string of letters (-25% coins if incorrect, -10% coins if correct but inaccurate capitalisation, -0% if completely correct)',
    '\n'+str(poisonb/2)+'% poison box: drains 1 life per second for 3 seconds by default',
    '\n'+str(explodeb/2)+'% explosive box: reduces your life to 1, BUFF/DEBUFF: removes every buff/debuff')
    input('start the game? (any key)')
play_again = True

def add_values_in_dict(sample_dict, key, list_of_values):
    #Append multiple values to a key in the given dictionary
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict

def packing(packingtime, boxname):
    global i, boxdict
    for hjk in range(packingtime):
        boxdict = add_values_in_dict(boxdict, boxname, [box[i]])
        i+=1

def die():  #death
    global life
    print('I\'m afraid you just died, you still have' , str(int(1250 - coins)) , 'coins to go.')
    life = 0

def damaged(damage, damage2):   #triggers when you received damage
    global life
    life = life - damage * damage2

def jackpott(): #you hit the jackpot
    global damage3, jackpot
    damage3 = 1.5
    jackpot = True

def plain(mes):
    global getmoneyplain, coins
    print (mes)
    if getmoneyplain < 1:
        print ('You got 20 coins from the box')
        coins = coins + 20
        getmoneyplain = 2
    else:
        getmoneyplain -= 1

def bsg(mineral, money, health): #gold silver bronze box
    global coins, life
    print('You got a', mineral, 'box')
    response = 'CHOOSE: '+str(money)+' coins/'+str(health)+' life (1/2)'
    repeat = True
    while repeat:
        choose = input(response)
        if choose == '1':
            print('You got', money,'coins')
            coins = coins + money
            repeat = False
        elif choose == '2':
            print('You got', health, 'life')
            life = life + health
            repeat = False
        else:
            response = '1 or 2 only: '

#MAIN GAME LOOP
while play_again:
    print('K, let\'s proceed')
    quited = False              #checks if you quited to prevent showing incorrect score
    life = 3                    #lives
    coins = 0                   #coins - the goal of the game
    getmoneyplain = 2           #checks whether or not this plain box is the one with money
    rob_debuff_timer = 5        #the freeze box debuff timer
    jackpot = False             #checks if you hit the jackpot
    robbedchance = 5            #robber difficulty
    poison_duration = 3         #how many lives you will lose if you get poisoned
    damage3 = 1
    secret = False
    box = list(range(1, 201))
    random.shuffle(box)
    boxdict = {"plain":[], "bronze":[],"silver":[],"gold":[],"jackpot":[],"medkit":[],"freeze":[],"flame":[],"robber":[],"poison":[],"explosive":[]}
    i = 0
    packing(plainb, 'plain')
    packing(bronzeb, 'bronze')
    packing(silverb, 'silver')
    packing(goldb, 'gold')
    packing(jackpotb, 'jackpot')
    packing(medkitb, 'medkit')
    packing(freezeb, 'freeze')
    packing(flameb, 'flame')
    packing(robberb, 'robber')
    packing(poisonb, 'poison')
    packing(explodeb, 'explosive')
    usedbox = []
    unusedbox = []
    not_box = False
    print("TIP: "+random.choice(tips))
    while True:
        #checks if rob debuff is over
        if life > 12:
            life = 12
            print("You reached MAX life (12)")
        if not_box == False:
            if 0 < rob_debuff_timer < 5:
                rob_debuff_timer = rob_debuff_timer - 1
            elif rob_debuff_timer == 0:
                print('Your ROB DIFFICULTY debuff has been removed')
                robbedchance = 5
                rob_debuff_timer = 5
        else:
            not_box = False
        round(coins)
        print('\nYou have ' + str(int(coins)) + ' coin(s) and ' + str(life) +' life, poison effect duration = ' + str(poison_duration))
        #x is the box you chose
        print('opened boxes:',usedbox)
        x = input('choose a box (1-200) (b for unopened boxes) (q to quit)')
        if x == 'b':
            #checking every number if it was chosen before
            not_box = True
            for i in range(1,201):
                if not i in usedbox:
                    unusedbox.append(i)
                else:
                    continue
            print(*unusedbox, sep = ', ')
            unusedbox.clear()
            continue
        elif x == 'q':
            quiting = input('ARE YOU SURE YOU WANT TO QUIT THE GAME (y for yes /any other key for no)')
            if quiting == 'y' or quiting == 'Y':
                quited = True
                break
            else:
                not_box = True
                continue
        elif x == 'cheat':
            #print("Jackpot 1-2, Plain 3-48, Bronze 49-78, Silver 79-100, Golden 101-113, Medkit 114-121",
            #"\nFreeze 122-151, Fire 152-167, Robber 168-187, Poison 188-197, Exploding 198-200\n")
            #for (i, item) in enumerate(box, start=1):
            #    print(str(i)+":"+str(item))
            for keys,values in boxdict.items():
                print(keys, values)
            not_box = True
            continue
        else:
            if x == 'r':
                x = random.randint(1,200)
            else:
                try:
                    x = int(x)
                except ValueError:
                    print('Either a number or the letters b, q, r')
                    not_box = True
                    continue
            if x < 1 or x > 200:
                print('Dude, 1 to 200')
                not_box = True
                continue
            #checks if the box was chosen before
            if x in usedbox:
                print('You opened that box earlier')
                not_box = True
                continue
            else:
                usedbox.append(x)
            #y is a list of the possible outcomes
            for name, number in boxdict.items():
                if x in number:
                    y = name
        #boxes
        if y == 'jackpot':
            if jackpot == False:
                print('HOLY MOLY YOU JUST HIT THE JACKPOT DUDEEEE')
                print('You got 1000 coins, congrats dude, but don\'t get too excited')
                print('BUFF/DEBUFF: IMMUNE TO ALL DEBUFFS, DAMAGE INCREASES TO 1.5X')
                jackpott()
                coins += 1000
            else:
                plain('You got a weirdly decorated plain box')
        elif y == 'plain':
            plain('You got a plain box')
        elif y == 'bronze':
            bsg('bronze', 100, 1)
        elif y == 'silver':
            bsg('silver', 150, 2)
        elif y == 'gold':
            bsg('gold', 200, 3)
            if poison_duration > 1:
                print('BUFF: POISON EFFECT DURATION DECREASES BY 1S')
                poison_duration-=1
            else:
                print('Your poison effect duration is capped at 1 second')
        elif y == 'medkit':
            print('You got a med kit and you gained 4 lives')
            life+=4
        elif y == 'freeze':
            print('You got a freeze box and you lost a life')
            damaged(1, damage3)
            if life < 1:
                die()
                break
            if jackpot == False:
                if rob_debuff_timer == 5:
                    print('DEBUFF:ROBBED DIFFICULTY INCREASE FOR NEXT 5 BOXES')
                    robbedchance = 0
                    rob_debuff_timer-=1
                elif rob_debuff_timer < 5:
                    print('You already have this debuff so no additional debuff')
            else:
                print('You are so excited from the jackpot you ignored the debuff')
                print('However, you lost additional 0.5 life')
        elif y == 'flame':
            print('Oughh, it\'s a box on fire, you burned yourself and lost 2 lives')
            damaged(2, damage3)
            if life < 1:
                die()
                break
            if jackpot == False:
                if poison_duration < 5:
                    print('DEBUFF: POISON EFFECT DURATION INCREASES BY 1S')
                    poison_duration+=1
                else:
                    print('Your poison effect duration is capped at 5 seconds')
            else:
                print('You are so excited from the jackpot you ignored the debuff')
                print('However, you lost additional 1 life')
        elif y == 'robber':
            print('A robber has jumped out from the box and is attempting to rob you!')
            print('type out the following words (5/10 letters, disappears in 1.5/3 seconds)')
            time.sleep(1)
            letters = string.ascii_letters
            difficulty = 10-robbedchance
            word = ''.join(random.choice(letters) for i in range(difficulty))
            print(word,end="\r")
            time.sleep(0.3*difficulty)
            print(("?"*difficulty),end="\r")
            defend = input()
            if defend == word:
                print('You succesfully defended yourself from the robber')
            else:
                if defend.lower() == word.lower():
                    print('The robber stole 10% of your coins')
                    coins = coins/10*9
                else:
                    print('The robber stole 25% of your coins')
                    coins = coins/4*3
                int(round(coins))
        elif y == 'poison':
            print('the box released poison gas, ew.')
            for a in range(poison_duration):
                time.sleep(1)
                if jackpot:
                    print("1.5 life drained")
                else:
                    print("1 life drained")
                damaged(1, damage3)
                if life < 1:
                    die()
                    break
                else:
                    continue
            if life < 1:
                break
        elif y == 'explosive':
            print('HOLY SH- IT\'S A EXPLOSIVE BOX RUNNNN')
            print('Yo, you have 1 more life yet lmao. All your buffs and debuffs are removed too')
            life = 1
            rob_debuff_timer = 5
            jackpot = False
            robbedchance = 4
            poison_duration = 3
            damage3 = 1
        else:
            print('It seems that you have accidentally wandered into a restricted area, please report this error to the dev')
        #triggers when you win
        if coins > 1249:
            coins = str(int(coins))
            life = str(life)
            print('\nHey, you won.')
            print('STATISTICS')
            print('You won with: '+coins)
            print('Lives remaining: '+life)
            break
        #alternate win
        if len(usedbox) > 199:
            print('Hey you open every single box and you haven\'t died yet, impressive work there')
            secret = True
            break
    boxes_opened = len(usedbox)
    print('Boxes opened:',boxes_opened)
    if quited == True:
        score = 0
    elif secret == True:
        score = 2500
    else:
        score = round(int(coins)-boxes_opened*30+float(life)*30)
        if score < 0:
            score = 0
    score_percent = round((score/1250*100), 3)
    print('Score earned: '+str(score)+'/1250 ('+str(score_percent)+'%)')
    if score_percent > 195:
        print('ALTERNATE WIN UNLOCKED')
    elif score_percent > 100:
        print('PERFECT!')
    elif score_percent > 80:
        print('EXCELLENT!')
    elif score_percent > 70:
        print('AMAZING!')
    jackpotlocation = boxdict['jackpot']
    print('The Jackpot boxes are', jackpotlocation)
    if play_again == False:
        pass
    else:
        playagain = input('Play again? (y/n)')
        if playagain == 'y' or playagain == 'Y':
            continue
        if playagain == 'n' or playagain == 'N':
            print('K bye')
            play_again = False
        else:
            print('I don\'t know what are you saying and I am taking it as a no')
            play_again = False
