import random
import time

def intro():
    print('The zombie waves won\'t stop, one dies, ten are on the way.',
    '\nYou tried to get out from your house, but a zombie is right in front of it.',
    '\nYou have no choice but to escape using the window.',
    '\nYou ran, and ran, and found an old house with no zombies nearby.',
    '\nThere is enough food, but they will be here, prepare yourself.')
    proceed = input('\nStart the game?')

def rules():
    print('\nw/a/s/d - choose direction',
    '\nm - motion tracker (accurate and covers large range, but cost battery)',
    '\nn - charge motion tracker/check charging progress (tracker will be unuseable until full charge)',
    '\nl - flashlight (inaccurate and covers smaller range, but doesn\'t cost battery)',
    '\nt - throw object (if you throw too far, zombies might not notice/if you throw too close, zombie will be even closer)',
    '\nq - quit the game (requires confirmation)'
    )
    proceed = input('Proceed?')

def throwing(danger_level):
    thinking = True
    while thinking:
        try:
            how_far = int(input('\nHow far do you want to throw? 1/5: '))
            if 0 < how_far < 6:
                distance = 5 - how_far
                thinking = False
            else:
                print('Invalid')
        except ValueError:
            print('Invalid')
    if 0 < (danger_level - distance) < 3:
        danger_level = distance
    elif 0 > (danger_level - distance) > -3:
        danger_level = distance
    else:
        pass
    return danger_level

def flashing(danger_level):
    inaccuracy = random.randint(-1,2)
    observation = danger_level + inaccuracy
    if observation < 0:
        observation = 0
    elif observation > 5:
        observation = 5
    else:
        pass
    return flashlight[observation]

choice = input('Controls - 1/Skip - any other key: ')
panel = ['m','n','l','t','q']
controls = ['1','2','3','4','5','6','7','8']
flashlight = [
    'You saw nothing, and heard nothing, silence made you fear',
    'You saw nothing, but heard groans',
    'You saw shadows far away',
    'You saw the zombies, but they are far away',
    'The zombies are still not close',
    'They are getting closer'
]
if choice == '1':
    rules()

while True:
    choosing = True
    while choosing:
        try:
            choice = int(input('Choose difficulty 1 to 3: '))
            if 0 < choice < 4:
                difficulty = 7 - choice
                choosing = False
            else:
                continue
        except ValueError:
            continue
    intro()
    danger = [0,0,0,0,0,0,0,0]
    battery = 6
    main_game_loop = True
    count = True
    charging = False
    print('Loading new game...')
    time.sleep(0.7)
    timer = 0
    hall = []
    seen= {}
    while main_game_loop:
        if 6 in danger:
            print('\nYou died, gg')
            for i in range(len(danger)):
                if danger[i] > 5:
                    hall.append(controls[i])
            print('You are attacked by zombies from hallway(s):', *hall)
            break
        if count == True:
            for i in range(8):
                closing = random.randint(1, difficulty)
                if closing == 1:
                    danger[i] += 1
                else:
                    pass
            if charging == True:
                battery += 1
        if battery > 6:
            battery = 6
            charging = False
            print('Tracker fully charged')
        choosing = True
        while choosing:
            choice = input('\nchoose action: ')
            choice.lower
            if choice in panel:
                choosing = False
            else:
                print('invalid')
        if choice == 'm':
            if charging == False:
                if battery > 0:
                    print('\nScanning motion on all eight directions... ///')
                    time.sleep(0.7)
                    for i in range(8):
                        if danger[i] > 4:
                            print('Heavy motion detected, direction: '+ controls[i])
                        elif danger[i] > 2:
                            print('Motion detected, coming from direction: '+ controls[i])
                        elif danger[i] > 0:
                            print('Light motion detected')
                        elif danger[i] < 1:
                            print('No motion detected')
                    battery -= 1
                    count = True
                else:
                    print('Not enough battery')
                    count = False
            else:
                percentage = str(battery*20-20)+'%'
                print('Charging... '+ percentage)
                count = False
        elif choice == 'q':
            quiting = input('\nARE YOU SURE YOU WANT TO QUIT THE CURRENT GAME? (y for yes /any other key for no)')
            if quiting == 'y' or quiting == 'Y':
                break
            else:
                count = False
                continue 
        elif choice == 'n':
            if charging == False:
                if battery > 5:
                    print('You have full battery')
                    count = False
                else:
                    print('You are now charging your battery, you cannot use this tracker until it was fully charged')
                    count = True 
                    charging = True
            else:
                percentage = str(battery*20-20)+'%'
                print('Charging... '+ percentage)
                count = False
        else:
            choosing = True
            count = True
        while choosing:
            direction = input('Which direction?')
            direction.lower
            if direction in controls:
                for i in range(8):
                    if controls[i] == direction:
                        if choice == 'l':
                            print(flashing(danger[i]))
                        elif choice == 't':
                            danger[i] = throwing(danger[i])
                        break
                    else:
                        continue
                choosing = False
            else:
                print('invalid')
        timer+=1
    print('You survived '+str(timer)+' rounds')
    playagain = input('play again? (y/n)')
    playagain.lower
    if playagain == 'y' or playagain == 'yes':
        continue
    elif playagain == 'n' or playagain == 'no':
        print('OK byeee')
        break
    else:
        print('I take that as a no')
        break