# Get coins from boxes to win
# Or open it all without dying
# Good luck
import random
import time
import string
life = 3        #lives
z = 0           #amount of boxes opened

print('Welcome to boxes')
ruleknown = input('Press r for rules, or any other key to skip: ')
if ruleknown == 'r' or ruleknown == 'R':
    print('There are 200 boxes, you have to choose one box',
    '\nThere is a total of 11 types of boxes, 6 being buffs and 5 being nerfs',
    '\nFor instance, the bronze box provides you either 50 coins or 1 more life',
    '\nLosing all your lifes ends the game, and getting 1250 coins wins the game, you can also win the game by opening all the boxes without dying',
    '\nYou cannot open same boxes, you can check for any unopened boxes by typing b when choosing a box')
    input('continue? (any key)')
    print('Here is the list for all types of boxes',
    '\n\n23% plain box: +20 coins for every two plain boxes you get, BUFF:NONE',
    '\n15% bronze box: +100 coins/ +1 life BUFF:NONE',
    '\n11% silver box: +150 coins/ +2 life BUFF:NONE',
    '\n7% golden box: +200 coins/ +3 life BUFF:POISON EFFECT LAST 1 SECOND SHORTER',
    '\n0.5% jackpot box: +1000 coins BUFF/NERF:IMMUNE FROM ALL NERFS, DAMAGE INCREASES TO 1.5X',
    '\n4% med kit: +4 life ')
    input('continue? (any key)')
    print('\n15% freeze box: -1 life NERF:ROBBED DIFFICULTY INCREASE FOR NEXT 5 BOXES',
    '\n8% flame box: -2 life NERF:POISON EFFECT LAST 1 SECOND LONGER',
    '\n10% robber in box: defend yourself by typing the correct string of letters (-25% coins if incorrect, -10% coins if correct but inaccurate capitalisation, -0% if completely correct)',
    '\n5% poison box: drains 1 life per second for 3 seconds by default',
    '\n1.5% explosive box: reduces your life to 1, BUFF/NERF: removes every buff/nerf')
    input('start the game? (any key)')
play_again = True

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

def bsg(mineral, money, health): #gold silver bronze box
    global coins, life, z
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
    z+=1

#MAIN GAME LOOP
while play_again:
    print('K, let\'s proceed')
    quited = False              #checks if you quited to prevent showing incorrect score
    life = 3                    #lives
    coins = 0                   #coins - the goal of the game
    getmoneyplain = False       #checks whether or not this plain box is the one with money
    rob_nerf_timer = 5          #the free box nerf timer
    jackpot = False             #checks if you hit the jackpot
    robbedchance = 5            #robber difficulty
    poison_duration = 3         #how many lives you will lose if you get poisoned
    damage3 = 1
    box = list(range(1, 201))
    random.shuffle(box)
    z = 0
    usedbox = []
    unusedbox = []
    not_box = False
    while True:
        #checks if rob nerf is over
        if not_box == False:
            if 0 < rob_nerf_timer < 5:
                rob_nerf_timer = rob_nerf_timer - 1
            elif rob_nerf_timer == 0:
                print('Your ROB DIFFICULTY nerf has been removed')
                robbedchance = 5
                rob_nerf_timer = 5
        else:
            not_box = False
        round(coins)
        print('\nYou have ' + str(int(coins)) + ' coin(s) and ' + str(life) +' life, poison effect duration = ' + str(poison_duration))
        #x is the box you chose
        x = input('choose a box (1-200) (b for unopened boxes) (q to quit)')
        if x == 'b':
            #checking every number if it was chosen before
            not_box = True
            for i in range(200):
                if not i in usedbox:
                    j = i + 1
                    unusedbox.append(j)
                else:
                    continue
            print(*unusedbox, sep = ', ')
            unusedbox.clear()
            continue
        elif x == 'q':
            quiting = input('ARE YOU SURE YOU WANT TO QUIT THE GAME (y for yes /any other key for no)')
            if quiting == 'y' or quiting == 'Y':
                quited = True
                play_again = False
                break
            else:
                not_box = True
                continue
        else:
            if x == 'r':
                pass
                x = random.randint(0,199)
            else:
                try:
                    x = int(x) - 1
                except ValueError:
                    print('Either a number or the letters b and q')
                    not_box = True
                    continue
            if x < 0 or x > 199:
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
            y = box[x]
        #boxes
        if 0 <= y <= 46:
            print ('You got a plain box')
            if getmoneyplain == False:
                getmoneyplain = True
            elif getmoneyplain == True:
                print ('You got 20 coins from the box')
                coins = coins + 20
                getmoneyplain = False
            z+=1
        elif 47 <= y <= 76:
            bsg('bronze', 100, 1)
        elif 77 <= y <= 98:
            bsg('silver', 150, 2)
        elif 99 <= y <= 112:
            bsg('golden', 200, 3)
            if poison_duration > 1:
                print('BUFFED: POISON EFFECT DURATION DECREASES BY 1S')
                poison_duration-=1
            else:
                print('Your poison effect duration is capped at 1 second')
            z+=1
        elif y == 113:
            print('HOLY MOLY YOU JUST HIT THE JACKPOT DUDEEEE')
            print('You got 1000 coins, congrats dude, but don\'t get too excited')
            print('BUFF/NERF: IMMUNE TO ALL NERFS, DAMAGE INCREASES TO 1.5X')
            jackpott()
            z+=1
            coins += 1000
        elif 114 <= y <= 121:
            print('You got a med kit and you gained 4 lives')
            life+=4
            z+=1
        elif 122 <= y <= 151:
            print('You got a freeze box and you lost a life')
            damaged(1, damage3)
            if life < 1:
                die()
                break
            if jackpot == False:
                if rob_nerf_timer == 5:
                    print('NERF:ROBBED DIFFICULTY INCREASE FOR NEXT 5 BOXES')
                    robbedchance = 0
                    rob_nerf_timer-=1
                elif rob_nerf_timer < 5:
                    print('You already have this nerf so no additional nerf')
            else:
                print('You are so excited from the jackpot you ignored the nerf')
            z+=1
        elif 152 <= y <= 167:
            print('Oughh, it\'s a box on fire, you burned yourself and lost 2 lives')
            damaged(2, damage3)
            if life < 1:
                die()
                break
            if jackpot == False:
                if poison_duration < 5:
                    print('NERFED: POISON EFFECT DURATION INCREASES BY 1S')
                    poison_duration+=1
                else:
                    print('Your poison effect duration is capped at 5 seconds')
            else:
                print('You are so excited from the jackpot you ignored the nerf')
            z+=1
        elif 168 <= y <= 187:
            #robberout = random.randint(1,robbedchance)
            #if robbedchance == 1:
                #print('A robber(?) jumped out from the box and stole 25% of your coins')
                #coins = coins/4*3
                #int(round(coins))
            #else:
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
            z+=1
        elif 188 <= y <= 197:
            print('the box released poison gas, ew.')
            for a in range(poison_duration):
                time.sleep(1)
                print("1 life drained")
                damaged(1, damage3)
                if life < 1:
                    die()
                    break
                else:
                    continue
            if life < 1:
                break
            z+=1
        elif 198 <= y <= 200:
            print('HOLY SH- IT\'S A EXPLOSIVE BOX RUNNNN')
            print('Yo, you have 1 more life yet lmao. All your buffs, nerfs and antidotes are removed too')
            life = 1
            rob_nerf_timer = 5
            jackpot = False
            robbedchance = 4
            poison_duration = 3
            damage3 = 1
            antidote = 0
            z+=1
        #triggers when you win
        if coins > 1249:
            boxes_opened = len(usedbox) + 1
            coins = str(int(coins))
            life = str(life)
            print('\nHey, you won.')
            print('STATISTICS')
            print('You won with: '+coins)
            print('Lives remaining: '+life)
            break
        #alternate win
        if z > 199:
            print('Hey you open every single box and you haven\'t died yet, impressive work there')
            break
    boxes_opened = len(usedbox)
    print('Boxes opened:',boxes_opened)
    if quited == True:
        score = 0
    else:
        score = round(int(coins)/boxes_opened*int(life))
    print('Score earned: '+str(score))
    jackpotlocation = str(box.index(113)+1)
    print('The Jackpot box is Box #'+jackpotlocation)
    if play_again == False:
        pass
    else:
        playagain = input('Hey, you wanna play again? (y/n)')
        if playagain == 'y' or playagain == 'Y':
            continue
        if playagain == 'n' or playagain == 'N':
            print('K bye')
            play_again = False
        else:
            print('I don\'t know what are you saying and I am taking it as a no')
            play_again = False
