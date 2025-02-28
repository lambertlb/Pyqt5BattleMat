#!/bin/bash

pyinstaller --distpath ./linuxDist BattleMatServer.py
cp -r ./webApp/ ./linuxDist/BattleMatServer/
cp -r ./Server/ ./linuxDist/BattleMatServer/
cp -r ./services/ ./linuxDist/BattleMatServer/

