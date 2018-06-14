# cs1830

|         | % Contribution |
|---------|----------------|
| Octavio | 55             |
| Hugh    | 30             |
| Zach    | 10             |
| Nissan  | 2.5            |
| Greg    | 2.5            |

Ideas board: https://docs.google.com/document/d/1_0hMUYIG_HRFGZmB0RdLcXk4QeVVlYxAIiLZAO06mQw/edit?usp=sharing

SETTINGS: located in classes/config

## To Install

Make sure you have the dependencies. Easiest way to do this is to run it and see what errors you get. 

You will need to make sure you are running this on a Linux/Unix system so you can install the cURL binaries. I don't _think_ there are ones compatible with Windows that pycURL can use. 

You will also need Flask.

## To run

`python3 GameLoop.py` 

By default, it will run in single player. To run in multiplayer you need to change the following in the config file: 

- `two_player` = true
- `game_state` = true
- `config_type` = client/server (2 player multiplayer so one device is server one is client)
- `client_ip` = if you are a client, the remote IP of the server (confusingly named)

You can also override whether you are a server/client via an argument on the command line. 

Server needs to be started before the client (obviously).

When it loads, you will get a nice screen telling you you're waiting for player 2. Make sure you hit space before doing so (it fires some JSON). 

If the connection fails the game may continue to run but with no data being sent. 

You can optionally turn on/off logging as you see fit in the config file. Be aware that various logging opions draw debugging artefacts on screen which significantly affect performane, and others log large amounts to the console (ie. you can enable high levels of logging for networking that dumps all the JSON it sends/recieves to console). This can _significantly_ affect performane. 

We benchmark normal running between 18 FPS (on a Thinkpad) to 25 FPS on a better Linux machine. 

## PROJECT STRUCTURE:

```

CS1830/                                                # main project Files
    .gitignore
    GameLoop.py
    lisence
    packages
    readme.md

    CLASSES/
        config.py
        settings.py

       BASE/                                           # Base classes which are used everywhere
            vectors.py/

       MIDDLE/                                         # all Middle classes that are used in Super and inherit Base
            Particle.py

            SPRITECONTROL/
                SpriteAnimator.py
                spriteSheet.py

       SUPER/                                          # all Super classes that inherit Middle and Base
            Camera.py
            Monster.py
            MonsterAi.py
            Player.py
            Weapon.py

    GAMESTATES/
        GameStates.py
        intro.py

    HANDLERS/                                           # event related detection
        ClickHandler.py
        KeyHandler.py
        Mouse.py

    IMG/
        all img assests in named directories

    LOADING/                                            # any generation of objects to in game
        MonsterAi.py
        Objects.py
        RandomGen.py

    TRANSFER/                                           # Network related
        comms.py
        JsonToObject.py

```
