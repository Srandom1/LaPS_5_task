from abc import ABC, abstractmethod

from PyQt5.QtWidgets import *

class CustomView(ABC, QWidget):
    
    
    def __init__(self):
        super().__init__()
        self.child = []
    
    def paint(self):
        pass

