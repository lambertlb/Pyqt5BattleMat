pyinstaller BattleMatServer.py
xcopy "./webApp" "./dist/BattleMatServer/webApp/" /s /e /h /F
xcopy "./Server" "./dist/BattleMatServer/Server/" /s /e /h /F
xcopy "./services" "./dist/BattleMatServer/services/" /s /e /h /F
