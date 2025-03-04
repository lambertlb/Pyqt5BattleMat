#!/bin/bash

cp BattleMatServer.py ./linuxDist//BattleMatServer
cp -r ./webApp/ ./linuxDist/BattleMatServer/
cp -r ./Server/ ./linuxDist/BattleMatServer/
cp -r ./services/ ./linuxDist/BattleMatServer/

