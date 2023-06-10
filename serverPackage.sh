#!/bin/bash

pyinstaller --distpath ./linuxDist BattleMatServer.py
cp -r ./webApp/ ./linuxDist/BattleMatServer/

