@REM python -m PyQt5.uic.pyuic -x loginDialog.ui -o ../generated/loginDialog.py
@REM python -m PyQt5.uic.pyuic -x dungeonManagerDialog.ui -o ../generated/dungeonManagerDialog.py
@REM python -m PyQt5.uic.pyuic -x MainWindow.ui -o ../generated/MainWindow.py
@REM python -m PyQt5.uic.pyuic -x ViewPog.ui -o ../generated/ViewPog.py
@REM python -m PyQt5.uic.pyuic -x ViewNotes.ui -o ../generated/ViewNotes.py
@REM python -m PyQt5.uic.pyuic -x FlagSelector.ui -o ../generated/FlagSelector.py

pyside2-uic loginDialog.ui -o ../generated/loginDialog.py
pyside2-uic dungeonManagerDialog.ui -o ../generated/dungeonManagerDialog.py
pyside2-uic MainWindow.ui -o ../generated/MainWindow.py
pyside2-uic ViewPog.ui -o ../generated/ViewPog.py
pyside2-uic ViewNotes.ui -o ../generated/ViewNotes.py
pyside2-uic FlagSelector.ui -o ../generated/FlagSelector.py
