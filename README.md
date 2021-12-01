# Tussel
Tussel is a game developed using Python and the PyGame library. It is a Turn-Based Strategy game where each player takes their turns simultaneously. Players can connect across a Local Area Network to play against one another. 

The game features a wide variety of content and units including soldiers, tanks, robots, jeeps, mechanics, and much more. 

![Alt text](screenshots/tussel_screenshot_3.PNG?raw=true "Screenshot")

## How to use

1. Download the repository from GitHub
2. Install the required modules listed below
3. Run client.py
4. Either start a server (using the given menu button), or enter the local IP address of another device with a running server
5. Click either Solo or Multiplayer, and the game will start

Clicking the in-game "Start Server" button will run server.py in the background, so running it yourself will produce the same results. 

server.py can also be run on a seperate device altogehter, and each client can connect it. For ease of use though, it is simplist to use the in-game menu to run server.py 

## Required Software
 - Python 3 (https://python.org/download/)
 - pygame (https://www.pygame.org/download.shtml)
 - Pillow (https://pypi.org/project/Pillow/#files)

 pygame and Pillow can be installed using pip with the following commands:

```
pip install pygame
pip install Pillow
```

The project was made and tested using Windows 10 and Python 3.7, pygame 1.9+ and Pillow  6.2. I can't make any guratees it will work on any other operating systems. 

## Gameplay

The game occurs in turns, with each player commanding their respective units simultaneously. Once each player has indicated that they are done ordering their units, every unit carries out their commands at once. A unit can only recieve certain orders depending on the unit type. Possible orders include moving to a new square, generating resources, constructing new units, and attacking enemy units. 

To give a unit an order, simply click on it. This will not only show all posible orders this unit can carry out, but also display the units stats. You may select any of these options to choose an order to give. To select certain orders faster, you may select icons nearby the unit, or a select from one of the options at the bottom of the screen to construct a new unit. 

To indicate you are done ordering units, click the done button in the lower-right corner, or you can also right click anywhere on screen. If you are the only player that hasn't finished the round, the button will begin flashing. 

The objective of the game is to completely eliminate your opponent.