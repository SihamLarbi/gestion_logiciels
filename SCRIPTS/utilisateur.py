import sys
from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from SCRIPTS.DataBaseManager import DataBaseManager
import mysql.connector
from mysql.connector import Error
from PyQt5 import QtGui

class Utilisateur(QDialog):
    def __init__(self):
        super(Utilisateur, self).__init__()
        try:
            loadUi('INTERFACES/utilisateur.ui', self)
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'Fichier UI introuvable')
            QApplication.instance().quit()

        # créer un objet dbb (base de donnes) de la classe DataBaseManger
        self.dbb = DataBaseManager()
        self.dbb.connect()

        self.ajouterButton.clicked.connect(self.ajout_function)
        self.annuler_btn_2.clicked.connect(self.reinitialiser_champs)
        self.supprimerButton.clicked.connect(self.supprimer_ligne)

        self.mdp.setEchoMode(QtWidgets.QLineEdit.Password)
        self.mdpc.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setFixedSize(640, 411)  # Fixe la taille de la première interface Connexion


        # Charger les utilisateurs depuis la base de données lors de l'initialisation
        self.charger_utilisateurs()

    def charger_utilisateurs(self):
        try:
            self.dbb.cursor.execute("SELECT Nom, Prénom, role FROM utilisateurs")
            utilisateurs = self.dbb.cursor.fetchall()
            for utilisateur in utilisateurs:
                nom, prenom, role = utilisateur
                self.user_list_widget.addItem(f"{nom} {prenom} - {role}")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement des utilisateurs: {err}")

    def ajout_function(self):
        try:
            nom = str(self.nom.text())
            prenom = str(self.prenom.text())
            password = str(self.mdp.text())
            confirm_password = str(self.mdpc.text())
            role = self.role_box.currentText()

            if password != confirm_password :
                QMessageBox.critical(self,'Erreur','les mots de passe ne correspondent pas')
                return
            if not nom or not prenom or not password:
                QMessageBox.critical(self,'Erreur', 'Veuillez remplir tous les champs')
                return

            self.dbb.cursor.execute(
            "INSERT INTO utilisateurs (Nom, Prénom, MotDePasse, role) VALUES (%s, %s, %s, %s)",
            (nom, prenom, password, role))
            self.dbb.conn.commit()

            self.user_list_widget.addItem(f"{nom} {prenom} - {role}")

            QMessageBox.information(self, "Succès", "Entrée ajoutée avec succès à la base de données.")
            self.reinitialiser_champs()
        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout de l'entrée:{err}")

    def supprimer_ligne(self):
        selected_item = self.user_list_widget.currentItem()

        if selected_item is None:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un utilisateur à supprimer.")
            return

        try:
            nom_prenom_role = selected_item.text()
            # Vérifier si le format de la chaîne est correct
            if " - " in nom_prenom_role:
                nom_prenom, role = nom_prenom_role.split(" - ")
                nom_prenom_parts = nom_prenom.split(" ")

                if len(nom_prenom_parts) == 2:
                    nom, prenom = nom_prenom_parts
                else:
                    raise ValueError("Format de nom et prénom incorrect")
            else:
                raise ValueError("Format de chaîne incorrect")

            # Créer une boîte de dialogue pour confirmation
            reply = QMessageBox.question(
                self,
                'Confirmation de suppression',
                'Voulez-vous vraiment supprimer cet utilisateur ?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                try:
                    # Supprimer l'utilisateur de la base de données
                    self.dbb.cursor.execute("DELETE FROM utilisateurs WHERE Nom = %s AND Prénom = %s AND role = %s",
                                            (nom, prenom, role))
                    self.dbb.conn.commit()

                    # Supprimer l'élément sélectionné de QListWidget
                    self.user_list_widget.takeItem(self.user_list_widget.row(selected_item))

                    QMessageBox.information(self, "Succès", "Utilisateur supprimé avec succès.")
                except Error as e:
                    QMessageBox.critical(self, 'Erreur', f"Erreur lors de la suppression de l'utilisateur: {e}")
        except ValueError as ve:
            QMessageBox.critical(self, 'Erreur', f"Erreur lors de la suppression de l'utilisateur: {ve}")

    def reinitialiser_champs(self):
        self.nom.clear()
        self.prenom.clear()
        self.mdp.clear()
        self.mdpc.clear()
        self.role_box.setCurrentText("Facturier")


    def closeEvent(self, event):
        self.dbb.close()







