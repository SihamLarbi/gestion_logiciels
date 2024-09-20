import sys
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import mysql.connector
from PyQt5 import QtWidgets, QtCore

from SCRIPTS.DataBaseManager import DataBaseManager


class Connexion(QDialog):



    def __init__(self):
        super(Connexion, self).__init__()

        try:
            loadUi('INTERFACES/connexion.ui', self)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Erreur de chargement de UI: {e}')
            sys.exit(1)

        self.dbb = DataBaseManager()
        self.dbb.connect()

        self.connexionbutton.clicked.connect(self.connectfunction) #Signal slot
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)  # Cache le mot de passe
        self.setFixedSize(400, 350)

    def connectfunction(self):
        username = self.username.text()
        password = self.password.text()

        try:
            # Vérification si l'utilisateur est l'administrateur
            if username == 'Idir' and password == '123':
                role = 'admin'
                self.accept()
                return

            # Vérification dans la base de données
            self.dbb.cursor.execute("SELECT role FROM utilisateurs WHERE Nom = %s AND MotDePasse = %s",
                                    (username, password))
            user_role = self.dbb.cursor.fetchone()

            if user_role:
                role = user_role[0]
                self.accept()
            else:
                QMessageBox.warning(self, 'Erreur de connexion', 'Entrez les bons identifiants',
                                    QMessageBox.StandardButton.Ok)



        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Erreur de connexion', f'Erreur de connexion à la base de données: {err}')

