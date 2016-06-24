# -*- coding: utf-8 -*-
"""
Created on :
import datetime;print datetime.datetime.now()

@author: Yasin_Yousif
"""

import sys

from radiobtn import *


# Paragraph-yy

class MyForm(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent )
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)





# Paragraph-zz
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())


