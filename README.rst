EEP71: GUI
===================

Dependencies & How to Install Them
----------------------------------
This readme section is written with primarily Linux in mind. For every step there are instructions for Windows and Linux users with the further distinction of Ubuntu and Debian-based users and Arch-based users.


| 1. Python

| **WINDOWS**: Download and run the most recent setup.exe from https://www.python.org/downloads/.
| **LINUX (ARCH-BASED)**: Run ``sudo pacman -S python``. The Arch maintainers **strongly** recommend that you only use Pacman to install software, so to install any Python libraries you should run ``sudo pacman -S python-LIBRARYNAME`` if it exists in the official repositories. Otherwise you'll need to get it from the AUR using the same method, replacing ``pacman`` with your AUR helper of choice (i.e. yay).
| **LINUX (UBUNTU/DEBIAN)**: Run ``sudo apt-get install python3`` and ``sudo apt-get install python3-pip`` to get the Python package manager. You'll need to use pip to install the Python libraries.  


| 1.1 python-opencv
| **WINDOWS & LINUX (UBUNTU/DEBIAN)**: Run ``pip install opencv-python``. Linux users might need to run this as `sudo`.
| **LINUX (ARCH-BASED)**: Use your AUR helper to get the ``python-opencv`` package from the AUR.

| 1.2 PyQt5
| **WINDOWS & LINUX (UBUNTU/DEBIAN)**: Run ``pip install PyQt5`` to install the PyQt5 library. This requires Qt5 (see 2.) and *might* require sudo.
| **LINUX (ARCH-BASED)**: Use your AUR helper to get the ``python-pyqt5`` package from the AUR.

| 2. Qt

| WINDOWS: Download and run the Qt Online Installer from Qt.io: https://www.qt.io/download-open-source#section-2.
| LINUX (UBUNTU/DEBIAN): Run ``sudo apt-get install qt5-default``.
| LINUX (ARCH-BASED): Run ``sudo pacman -S qt5-base``.


How to Run the Project
----------------------
Assuming all dependencies were installed correctly all you have to do is run ``python mainwindow.py`` in your terminal for the primary window, and ``python otherwindow.py`` for the secondary window with distance measurement.





