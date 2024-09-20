import mysql.connector
from PyQt5.QtWidgets import QMessageBox
import sys

class DataBaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None


    def connect(self):
        # etablir la connexion a la bdd
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="admin",
                password="CORE66@@BEN@@_pedro",
                database="huilerie",
                auth_plugin='mysql_native_password'  # Spécifier le plugin d'authentification 

            )
            self.cursor = self.conn.cursor()  # créer un object curseur a partir de la cnx de bdd, ce cursor nous permettra d'executer des requetes SQL sur la bdd
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur de connexion", f"Erreur lors de la connexion a la base de donnée: {err}")
            sys.exit(1)


        # Fermeture de la connexion à la base de données lors de la fermeture de l'application
    def close(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            #print("Connexion à la base de données fermée.")



