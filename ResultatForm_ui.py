# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Resultat.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultatForm(object):
    def setupUi(self, ResultatForm):
        ResultatForm.setObjectName("ResultatForm")
        ResultatForm.resize(1580, 536)
        self.verticalLayout = QtWidgets.QVBoxLayout(ResultatForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(ResultatForm)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableView.setFont(font)
        self.tableView.setAutoFillBackground(True)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 6, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.Button_Bud = QtWidgets.QPushButton(ResultatForm)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Button_Bud.setFont(font)
        self.Button_Bud.setObjectName("Button_Bud")
        self.gridLayout.addWidget(self.Button_Bud, 0, 0, 1, 1)
        self.Button_Akk = QtWidgets.QPushButton(ResultatForm)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Button_Akk.setFont(font)
        self.Button_Akk.setObjectName("Button_Akk")
        self.gridLayout.addWidget(self.Button_Akk, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(ResultatForm)
        QtCore.QMetaObject.connectSlotsByName(ResultatForm)

    def retranslateUi(self, ResultatForm):
        _translate = QtCore.QCoreApplication.translate
        ResultatForm.setWindowTitle(_translate("ResultatForm", "Års Resultat"))
        self.Button_Bud.setText(_translate("ResultatForm", "Plot Årsresultat Budsjett"))
        self.Button_Akk.setText(_translate("ResultatForm", "Plot Årsresultat Akkumulert"))
