import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi
from SCRIPTS.utilisateur import Utilisateur

from SCRIPTS.DataBaseManager import DataBaseManager

from SCRIPTS.EventFilter import EventFilter

class Fournisseurs(QMainWindow):
    """
    Cette classe gère l'interface utilisateur et les fonctionnalités liées aux employés.
    """

    def __init__(self, stacked_widget):
        super(Fournisseurs, self).__init__()
        try:
            loadUi('INTERFACES/fournisseurs.ui', self)  # Chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1)

         # créer un objet dbb (base de donnes) de la classe DataBaseManger
        self.dbb = DataBaseManager()
        self.dbb.connect()



        self.stacked_widget = stacked_widget
        self.navigation_ui()
        #self.menu_widget_5.hide()
        self.menu_btn_5.clicked.connect(self.show_menu_widget)
        self.info_widget.hide()
        self.info_btn.clicked.connect(self.show_info_widget)
        self.user_btn.clicked.connect(self.load_utilisateur)

        # connecter le signal clicked du bouton 'Ajouter' a a ma methode
        self.AddButtonF.clicked.connect(self.ajouter_fournisseur)

        # connecter le signal clicked du bouton 'Annuler '
        self.AnnulerButtonF.clicked.connect(self.reinitialiser_champs)

        # connecter l'événement de clic sur notre QTableWdiget a une fonction pour charger les données dans les LineEdits
        self.tableWidget.cellClicked.connect(self.charger_donnees_ligne_selectionnee1)

        # connecter le signal clicked du bouton 'Modifier' a ma methode
        self.ModiferButtonF.clicked.connect(self.enregistrer_modifications1)

        # connecter le signal clicked du bouton'Supprimer'a la methode
        self.SupprimerButtonF.clicked.connect(self.supprimer_ligne1)

        # Créer et installer l'EventFilter
        self.event_filter = EventFilter(self, self.tableWidget)
        self.installEventFilter(self.event_filter)

        self.Recherche.clicked.connect(self.search_by_id)

    def load_utilisateur(self):
        user = Utilisateur()
        user.exec_()

    def show_info_widget(self):
        if self.info_widget.isHidden():
            self.info_widget.show()
        else:
            self.info_widget.hide()

    def show_menu_widget(self):
        # Affiche ou masque le widget menu_widget en fonction de son état actuel
        if self.menu_widget_5.isHidden():
            self.menu_widget_5.show()
        elif not self.menu_btn_5.isChecked():  # Vérifie si le bouton menu_btn n'est pas enfoncé
            self.menu_widget_5.hide()

    def navigation_ui(self):
        self.inventaire_btn.clicked.connect(self.load_inventaire)
        self.achats_btn.clicked.connect(self.load_achats)
        self.stock_btn.clicked.connect(self.load_stock)
        self.client_btn.clicked.connect(self.load_clients)
        self.employee_btn.clicked.connect(self.load_employes)
        self.fournisseurs_btn.clicked.connect(self.load_fournisseurs)
        self.referentiel_btn.clicked.connect(self.load_referentiel)

    def load_inventaire(self):
        self.stacked_widget.setCurrentIndex(0)

    def load_achats(self):
        self.stacked_widget.setCurrentIndex(1)

    def load_stock(self):
        self.stacked_widget.setCurrentIndex(2)

    def load_clients(self):
        self.stacked_widget.setCurrentIndex(3)

    def load_employes(self):
        self.stacked_widget.setCurrentIndex(4)

    def load_fournisseurs(self):
        self.stacked_widget.setCurrentIndex(5)

    def load_referentiel(self):
        self.stacked_widget.setCurrentIndex(6)

    def search_by_id(self):
        # Récupérer la date saisie dans la barre de recherche
        search_id = self.Barre.text().strip()

        # Vérifier que la date n'est pas vide
        if not search_id:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un Id.")
            return

        # Chercher la date dans la table
        found = False
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            if item is not None and item.text() == search_id:
                # Mettre en surbrillance la ligne trouvée
                self.colorier_ligne(row)
                found = True
                break

        if not found:
            QMessageBox.information(self, "Recherche", "Aucune entrée trouvée pour l'Id spécifiée.")

    def ajouter_fournisseur(self):
        # récupérer les valeurs saisies dans les LineEdits
        try:
            nom_F = str(self.nomF.text())
            prenom_F = str(self.prenomF.text())
            Produit_fourni = str(self.Produit.text())
            Num_tel = int(self.Numero.text())
            Entreprise = str(self.Entreprise.text())

             # insertion des donnees dans la bdd

            self.dbb.cursor.execute("""
            INSERT INTO fournisseur (Nom, Prénom, Entreprise , Produit_fourni, Num_tel)
            VALUES (%s, %s, %s, %s, %s)
            """, (nom_F, prenom_F, Entreprise,Produit_fourni,Num_tel) )
            self.dbb.conn.commit()

            QMessageBox.information(self, "Succès", "Entrée ajoutée avec succès à la base de données.")
            self.reinitialiser_champs()
        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")
        except mysql.connector.Error as err :
            QMessageBox.critical(self,"Erreur",f"Erreur lors de l'ajout de l'entrée:{err}")

        # apres avoir inséré les données avec succes, vider la tableWidget
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        # récupérer les données de la base de données après l'ajout
        self.dbb.cursor.execute("SELECT * FROM fournisseur ")
        result1 = self.dbb.cursor.fetchall()  # recuperer toutes les lignes

        # Ajouter les données a la tableWidget
        for row_number, row_data in enumerate(result1):
         # Insérer une nouvelle ligne dans le QTableWidget
            self.tableWidget.insertRow(row_number)
            for column, value in enumerate(row_data):
                # Créer un QTableWidgetItem pour chaque valeur et l'insérer dans le QTableWidget
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_number, column, item)

    # fonction pour charger les données de la ligne sélectionnée dans les lineEdits
    def charger_donnees_ligne_selectionnee1(self, row, column):
        # Réinitialiser la couleur de fond de toutes les lignes à leur couleur par défaut (blanc)
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    item.setBackground(QColor("white"))

            # Color les lignes séléctionée
            self.colorier_ligne(row)

            # Récupérer les données de la ligne sélectionnée
            id_fournisseur = self.tableWidget.item(row, 0).text()
            nom = self.tableWidget.item(row, 1).text()
            prenom = self.tableWidget.item(row, 2).text()
            entreprise = self.tableWidget.item(row, 3).text()
            produit_fourni = self.tableWidget.item(row, 4).text()
            Num_tel = self.tableWidget.item(row, 5).text()

            # afficher les données dans les LineEdits
            self.nomF.setText(nom)
            self.prenomF.setText(prenom)
            self.Produit.setText(produit_fourni)
            self.Entreprise.setText(entreprise)
            self.Numero.setText(Num_tel)

        # focntion pour enregistrer les modification dans la bdd

    def enregistrer_modifications1(self):
        try:
            # Récupérer les valeurs modifiées à partir des LineEdits
            nom = str(self.nomF.text())
            prenom = str(self.prenomF.text())
            produit_fourni = str(self.Produit.text())
            entreprise = str(self.Entreprise.text())
            Num_tel = int(self.Numero.text())

            # Vérifier si une ligne est sélectionnée dans la tableWidget
            if self.tableWidget.currentRow() == -1:
                QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à modifier.")
                return

            # Mettre à jour les données dans la base de données

            selected_row = self.tableWidget.currentRow()
            id_fournisseur = self.tableWidget.item(self.tableWidget.currentRow(),
                                                   0).text()  # Récupérer l'ID de la ligne sélectionnée
            self.dbb.cursor.execute("""
                          UPDATE fournisseur
                          SET Nom=%s, Prénom=%s , Entreprise =%s,Produit_fourni =%s,Num_tel=%s
                          WHERE idfournisseur=%s
                   """, (nom, prenom, entreprise, produit_fourni, Num_tel, id_fournisseur))

            self.dbb.conn.commit()  # apporter les modification

            # mettre a jour les cellules correspondantes dans le QTablewidget
            self.tableWidget.setItem(selected_row, 1, QTableWidgetItem(nom))
            self.tableWidget.setItem(selected_row, 2, QTableWidgetItem(prenom))
            self.tableWidget.setItem(selected_row, 3, QTableWidgetItem(entreprise))
            self.tableWidget.setItem(selected_row, 4, QTableWidgetItem(produit_fourni))
            self.tableWidget.setItem(selected_row, 5, QTableWidgetItem(str(Num_tel)))

            self.reinitialiser_champs()

            QMessageBox.information(self, "Succès", "Modifications enregistrées avec succès.")
        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")


    # fonction de suppression
    def supprimer_ligne1(self):
        # Récupérer l'index de la ligne sélectionnée
        selected_row = self.tableWidget.currentRow()


        if selected_row != -1:  # Vérifier si une ligne est sélectionnée
            # Créer une boîte de dialogue pour confirmation
            reply = QMessageBox.question(
                self,
                'Confirmation de suppression',
                'Voulez-vous vraiment supprimer la ligne ?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            # si l'utilisateur choisit 'Oui'
            if reply == QMessageBox.Yes:
            # recuperer l'ID de la ligne séléctionné
                id_fournisseur = self.tableWidget.item(selected_row, 0).text()


                # Supprimer la ligne de la base de données
                self.dbb.cursor.execute("DELETE FROM fournisseur WHERE idfournisseur = %s", (id_fournisseur,))
                self.dbb.conn.commit()

            # Supprimer la ligne de la tableWidget
                self.tableWidget.removeRow(selected_row)
                self.reinitialiser_champs()

            # Réinitialiser la couleur de fond de la ligne supprimée
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(selected_row, j)
                    if item is not None:
                        item.setBackground(QColor("white"))

            #  si toutes les lignes sont supprimées , reinitialiser l'auto-incrémentation de l'id
                if self.tableWidget.rowCount() == 0:
                    self.reinitialiser_id()
            else:
                pass


    def reinitialiser_champs(self):
        # Réinitialiser les champs QLineEdit
        self.nomF.clear()
        self.prenomF.clear()
        self.Produit.clear()
        self.Entreprise.clear()
        self.Numero.clear()
    def reinitialiser_id(self):
        # Réinitialiser l'auto-incrémentation de l'ID dans la base de données
        self.dbb.cursor.execute("ALTER TABLE fournisseur AUTO_INCREMENT = 1")
        self.dbb.conn.commit()


    def colorier_ligne(self, row):
        # Colorier la ligne sélectionnée en vert
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(row, col)
            if item is not None:
                item.setBackground(QColor("#c0c2e8"))  # Choisir la couleur de fond souhaitée


