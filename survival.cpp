#include <iostream>
#include <unistd.h>
#include <vector>
#include <algorithm>
#include <string>
#include <cstdlib>
#include <typeinfo>
using namespace std;

char choice, proceed, quiting, direction;

void print(vector<int> const &hall){
    for (int i = 0; i < hall.size(); i++){
        cout << hall[i] - 48 << " ";
    }
}

void intro(){
    cout << "\nThe zombie waves won\'t stop, one dies, ten are on the way.";
    cout << "\nYou tried to get out from your house, but a zombie is right in front of it.";
    cout << "\nYou have no choice but to escape using the window.";
    cout << "\nYou ran, and ran, and found an old house with no zombies nearby.";
    cout << "\nThere is enough food, but they will be here, prepare yourself.";
    cout << "\nStart the game?\n";
    system("pause");
}

void rules(){
    cout << "\nw/a/s/d - choose direction";
    cout << "\nm - motion tracker (accurate and covers large range, but cost battery)";
    cout << "\nn - charge motion tracker/check charging progress (tracker will be unuseable until full charge)";
    cout << "\nl - flashlight (inaccurate and covers smaller range, but doesn\'t cost battery)";
    cout << "\nt - throw object (if you throw too far, zombies might not notice/if you throw too close, zombie will be even closer)";
    cout << "\nq - quit the game (requires confirmation)\n";
    system("pause");
}

int throwing(int danger_level){
    bool thinking = true;
    int further;
    while (thinking){
        cout << "\n\nHow far do you want to throw? 1/5: ";
        int how_far; 
        cin >> how_far;
        if(0 < how_far < 6){
            further = 5 - how_far;
            thinking = false;
        } else{
            cout << "\nInvalid";
            cin.clear();
        }
    }
    if (0 < (danger_level - further) < 3){
        danger_level = further;
    } else if (0 > (danger_level - further) > -3){
        danger_level = further;
    }
    return danger_level;
}

string flashlight[] = {
    "\nYou saw nothing, and heard nothing, silence made you fear",
    "\nYou saw nothing, but heard groans",
    "\nYou saw shadows far away",
    "\nYou saw the zombies, but they are far away",
    "\nThe zombies are still not close",
    "\nThey are getting closer"
};

string flashing(int danger_level){
    int inaccuracy = 1 - (rand() % 4);
    int observation = danger_level + inaccuracy;
    if (observation < 0){
        observation = 0;
    } else if (observation > 5){
        observation = 5;
    }
    return flashlight[observation];
}

int main(){
    cout << "Controls - 1/Skip - any other key: ";
    choice = getchar();
    char panel[] = {'m','n','l','t','q'};
    char controls[] = {'1','2','3','4','5','6','7','8'};
    bool choosing = true;
    if (choice == '1'){
        rules();
    }
    int difficulty;
    int difficulty2;
    bool main_game_loop;
    bool play_again = true;
    while (play_again){
        choosing = true;
        while (choosing){
            cout << "\nChoose difficulty 1 to 3: ";
            while ((!(cin >> difficulty)) || (!(difficulty < 4)) || (!(difficulty > 0))){
                cout << "\nNope, choose again: ";
                cin.clear();
                cin.ignore(1000,'\n');
            }
            difficulty2 = 7 - difficulty;
            choosing = false;
            main_game_loop = true;
            proceed = '1';
        }
        intro();
        int danger[8] = {0,0,0,0,0,0,0,0};
        int battery = 6;
        bool count = true;
        bool charging = false;
        int timer = 0; 
        int quitting = 0;
        cout << "\nLoading new game";
        usleep(700000);
        vector<int> hall;
        while (main_game_loop){
            if (find(begin(danger), end(danger), 6) != end(danger)) {
                cout << "\n\nYou died, gg";
                for (int i = 0; i < 8; i++){
                    if (danger[i] > 5){
                        hall.push_back(controls[i]);
                    } else{
                        continue;
                    }
                }
                break;
            }
            if (count == true){
                //cout << "\n";
                for (int i = 0; i < 8; i++){
                    int closing = 1 + (rand() % difficulty2);
                    if (closing == 1){
                        danger[i]++;
                    }
                    //cout << danger[i];
                }
                if (charging){
                    battery++;
                }
            }
            if (battery > 5){
                battery = 6;
                charging = false;
                cout << "\nTracker fully charged";
            }
            choosing = true;
            while (choosing){
                cout << "\n\nChoose action: ";
                cin >> choice;
                if (find(begin(panel), end(panel), choice) != end(panel)){
                    choosing = false;
                } else{
                    cout << "\nInvalid";
                    cin.clear();
                }
            }
            string percentage;
            switch(choice){
                case 'm':
                    if (charging == false){
                        if (battery > 0){
                            cout << "\nScanning motion on all eight directions\n";
                            usleep(700000);
                            for (int i = 0; i < 8; i++){
                                if (danger[i] > 4){
                                    cout << "Heavy motion detected, direction: " << controls[i] << endl;
                                } else if (danger[i] > 2 && danger[i] < 5){
                                    cout << "Motion detected, coming from direction: " << controls[i] << endl;
                                } else if (danger[i] > 0 && danger[i] < 3){
                                    cout << "Light motion detected" << endl;
                                } else if (danger[i] < 1){
                                    cout << "No motion detected" << endl;
                                }
                            }
                            battery -= 1;
                            count = true;
                        } else{
                            cout << "\nNot enough battery";
                            count = false;
                        }
                    } else{
                        percentage = "\nCharging... " + to_string(battery*20-20) + "%";
                        cout << percentage;
                        count = false;
                    }
                    break;
                case 'q':
                    cout << "\nARE YOU SURE YOU WANT TO QUIT THE CURRENT GAME? (y for yes/ any other key for no)";
                    cin >> quiting;
                    quiting = tolower(quiting);
                    if (quiting == 'y'){
                        quitting = 1;
                    } 
                    break;
                case 'n':
                    if (charging){
                        percentage = "\nCharging... " + to_string(battery*20-20) + "%";
                        cout << percentage;
                        count = false;
                    } else{
                        if (battery > 5){
                            cout << "\nYou have full battery";
                            count = false;
                        } else{
                            cout << "\nYou are currently charging your battery, you cannot use this tracker until it was fully charged";
                            count = true;
                            charging = true;
                        }
                    }
                    break;
                default:
                    choosing = true;
                    count= true;
            }
            if (quitting == 1){
                break;
            }
            while (choosing){
                cout<< "\nWhich direction?";
                cin >> direction;
                direction = tolower(direction);
                if (find(begin(controls), end(controls), direction) != end(controls)) {
                    for (int i = 0; i < 8; i++){
                        if (controls[i] == direction){
                            if (choice == 'l'){
                                cout << flashing(danger[i]);
                            } else if (choice == 't'){
                                danger[i] = throwing(danger[i]);
                            }
                            break;
                        } else{
                            continue;
                        }
                    }
                    choosing = false;
                } else{
                    cout << "\nInvalid";
                    cin.clear();
                }
            }
            timer++;
        }
        if (quitting == 0){
            cout << "\nYou are attacked by zombies from hallway(s): ";
            print(hall);
        }
        string response = "\nYou survived " + to_string(timer)+ " rounds";
        char playagain;
        cout << response;
        cout << "\n\nPlay again? (y/n)";
        cin >> playagain;
        playagain = tolower(playagain);
        switch(playagain){
            case 'y':
                play_again = true;
                break;
            case 'n':
                cout << "OK Byeeee";
                play_again = false;
                break;
            default:
                cout << "I take it as a no";
                play_again = false;
        }
    }
    return 0;
}