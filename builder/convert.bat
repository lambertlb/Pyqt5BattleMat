@REM python -m PyQt5.uic.pyuic -x loginDialog.ui -o ../generated/loginDialog.py
@REM python -m PyQt5.uic.pyuic -x dungeonManagerDialog.ui -o ../generated/dungeonManagerDialog.py
@REM python -m PyQt5.uic.pyuic -x MainWindow.ui -o ../generated/MainWindow.py
@REM python -m PyQt5.uic.pyuic -x ViewPog.ui -o ../generated/ViewPog.py
@REM python -m PyQt5.uic.pyuic -x ViewNotes.ui -o ../generated/ViewNotes.py
@REM python -m PyQt5.uic.pyuic -x FlagSelector.ui -o ../generated/FlagSelector.py

PySide6-uic loginDialog.ui -o ../generated/loginDialog.py
PySide6-uic dungeonManagerDialog.ui -o ../generated/dungeonManagerDialog.py
PySide6-uic MainWindow.ui -o ../generated/MainWindow.py
PySide6-uic ViewPog.ui -o ../generated/ViewPog.py
PySide6-uic ViewNotes.ui -o ../generated/ViewNotes.py
PySide6-uic FlagSelector.ui -o ../generated/FlagSelector.py
