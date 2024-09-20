import sys
import mysql.connector
from datetime import datetime
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDate

from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
from SCRIPTS.utilisateur import Utilisateur

from SCRIPTS.DataBaseManager import DataBaseManager

from SCRIPTS.EventFilter import EventFilter


# cette classe représente la fenetre principale de l'application
class MainWindow(QMainWindow):
    """
    Cette classe gère l'interface utilisateur principale et ses fonctionnalités.
    """

    def __init__(self, stacked_widget):
        super(MainWindow, self).__init__()
        try:
            loadUi('INTERFACES/inventaire.ui', self)  # chargement de l'interface MainWindow
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1) # l'application se termine avec un code d'erreur

        # créer un objet dbb (base de donnes) de la classe DataBaseManger
        self.dbb = DataBaseManager()
        self.dbb.connect()



        self.stacked_widget = stacked_widget

        self.navigation_ui()
        #self.menu_widget.hide()
        self.menu_btn.clicked.connect(self.show_menu_widget)
        self.info_widget.hide()
        self.info_btn.clicked.connect(self.show_info_widget)

        # connecter le signal dateChanged de dateEdit a la methode update_barre

        self.dateEdit.dateChanged.connect(self.update_barre)

        # connecter le signal clicked du bouton 'Ajouter' a a ma methode
        self.AddButton.clicked.connect(self.ajouter_entree)

        # connecter l'événement de clic sur notre QTableWdiget a une fonction pour charger les données dans les LineEdits
        self.tableWidget.cellClicked.connect(self.charger_donnees_ligne_selectionnee)

        # connecter le signal clicked du bouton 'Modifier' a ma methode
        self.ModifierButton.clicked.connect(self.enregistrer_modifications)

        # connecter le signal clicked du bouton'Supprimer'a la methode
        self.SupprimerButton.clicked.connect(self.supprimer_ligne)

        # Créer et installer l'EventFilter
        self.event_filter = EventFilter(self, self.tableWidget)
        self.installEventFilter(self.event_filter)


        self.Recherche.clicked.connect(self.search_by_date)


    def show_info_widget(self):
        if self.info_widget.isHidden():
            self.info_widget.show()
        else :
            self.info_widget.hide()

    def show_menu_widget(self):
        # Affiche ou masque le widget menu_widget en fonction de son état actuel
        if self.menu_widget.isHidden():
            self.menu_widget.show()
        elif not self.menu_btn.isChecked():  # Vérifie si le bouton menu_btn n'est pas enfoncé
            self.menu_widget.hide()


    def navigation_ui(self):
        self.achats_btn.clicked.connect(self.load_achats)
        self.stock_btn.clicked.connect(self.load_stock)
        self.client_btn.clicked.connect(self.load_clients)
        self.employee_btn.clicked.connect(self.load_employes)
        self.fournisseurs_btn.clicked.connect(self.load_fournisseurs)
        self.referentiel_btn.clicked.connect(self.load_referentiel)
        self.user_btn.clicked.connect(self.load_utilisateur)

    def load_utilisateur(self):
        user = Utilisateur()
        user.exec_()



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

    def update_barre(self, new_date: QDate):


        # mettre a jour le texte de la barre de recherche avec la nouvelle date sélectionné
        self.Barre.setText(new_date.toString("yyyy-MM-dd"))

        # si aucune ligne n'est séléctionné le bouton modifié sera desactivé

    def search_by_date(self):
        # Récupérer la date saisie dans la barre de recherche
        search_date = self.Barre.text().strip()

        # Vérifier que la date n'est pas vide
        if not search_date:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une date.")
            return

        # Chercher la date dans la table
        found = False
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 1)
            if item is not None and item.text() == search_date:
                # Mettre en surbrillance la ligne trouvée
                self.colorier_ligne(row)
                found = True
                break

        if not found:
            QMessageBox.information(self, "Recherche", "Aucune entrée trouvée pour la date spécifiée.")


    def ajouter_entree(self):
        # récupérer les valeurs saisies dans les LineEdits
        try:
            depenses = float(self.lineEdit_depense.text())
            qte_huile = int(self.lineEdit_qte_huile.text())
            qte_olive = int(self.lineEdit_qte_olive.text())
            nbr_client = int(self.lineEdit_nbr_client.text())
            stock_huile = int(self.lineEdit_stock_huile.text())
            revenus = float(self.lineEdit_revenus.text())
            date = datetime.now().date() # date actuelle

            # calcul du bénéfice
            benefice = revenus - depenses

             # insertion des donnees dans la bdd

            self.dbb.cursor.execute("""
            INSERT INTO inventaire (date, Qte_huile, qte_olive,  stock_huile,depense, revenu,benefice,Nbr_client)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (date, qte_huile, qte_olive, stock_huile, depenses, revenus, benefice, nbr_client))
            self.dbb.conn.commit() # C POUR ENREGISTRE LES MODIFICATIONS

            QMessageBox.information(self, "Succès", "Entrée ajoutée avec succès à la base de données.")
            self.reinitialiser_champs()
        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")
        except mysql.connector.Error as err :
            QMessageBox.critical(self,"Erreur",f"Erreur lors de l'ajout de l'entrée:{err}")

        # apres avoir inséré les données avec succes, vider la tableWidget
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        #  récupérer les données de la base de données après l'ajout
        self.dbb.cursor.execute("SELECT * FROM inventaire ")
        result = self.dbb.cursor.fetchall() # recuperer toutes les lignes


        #Ajouter les données a la tableWidget
        for row_number, row_data in enumerate(result):
            # Insérer une nouvelle ligne dans le QTableWidget
            self.tableWidget.insertRow(row_number)
            for column, value in enumerate(row_data):
                # Créer un QTableWidgetItem pour chaque valeur et l'insérer dans le QTableWidget
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_number, column, item)



    # fonction pour charger les données de la ligne sélectionnée dans les lineEdits
    def charger_donnees_ligne_selectionnee(self, row, column):
        # Réinitialiser la couleur de fond de toutes les lignes à leur couleur par défaut (blanc)
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    item.setBackground(QColor("white"))

        # Color les lignes séléctionée
        self.colorier_ligne(row)


        # Récupérer les données de la ligne sélectionnée
        id_entree = self.tableWidget.item(row, 0).text()
        date =self.tableWidget.item(row, 1).text()
        qte_huile = self.tableWidget.item(row, 2).text()
        qte_olive = self.tableWidget.item(row, 3).text()
        stock_huile = self.tableWidget.item(row, 4).text()
        depense =self.tableWidget.item(row, 5).text()
        revenu = self.tableWidget.item(row, 6).text()
        benefice =self.tableWidget.item(row, 7).text()
        nbr_client =self.tableWidget.item(row, 8).text()


        # afficher les données dans les LineEdits
        self.lineEdit_depense.setText(depense)
        self.lineEdit_revenus.setText(revenu)
        self.lineEdit_qte_huile.setText(qte_huile)
        self.lineEdit_qte_olive.setText(qte_olive)
        self.lineEdit_nbr_client.setText(nbr_client)
        self.lineEdit_stock_huile.setText(stock_huile)

    # focntion pour enregistrer les modification dans la bdd
    def enregistrer_modifications(self):
        try:
            # Récupérer les valeurs modifiées à partir des LineEdits
            depenses_modif = float(self.lineEdit_depense.text())
            revenu_modif = float(self.lineEdit_revenus.text())
            huile_modif = int(self.lineEdit_qte_huile.text())
            olive_modif = int(self.lineEdit_qte_olive.text())
            nbr_client_modif = int(self.lineEdit_nbr_client.text())
            stock_huile_modif = int(self.lineEdit_stock_huile.text())

            # Vérifier si une ligne est sélectionnée dans la tableWidget
            if self.tableWidget.currentRow() == -1:
                QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à modifier.")
                return

            # Mettre à jour les données dans la base de données

            selected_row = self.tableWidget.currentRow()
            id_entree = self.tableWidget.item(self.tableWidget.currentRow(),
                                              0).text()  # Récupérer l'ID de la ligne sélectionnée
            self.dbb.cursor.execute("""
                        UPDATE inventaire
                        SET Qte_huile=%s, qte_olive=%s , stock_huile =%s,depense =%s,revenu=%s,Nbr_client=%s
                        WHERE id=%s
                    """, (
            huile_modif, olive_modif, stock_huile_modif, depenses_modif, revenu_modif, nbr_client_modif, id_entree))
            self.dbb.conn.commit()

            # calculer benefice
            benefice_modif = float(revenu_modif) - float(depenses_modif)
            # mettre a jour les cellules correspondantes dans le QTablewidget
            self.tableWidget.setItem(selected_row, 2, QTableWidgetItem(str(huile_modif)))
            self.tableWidget.setItem(selected_row, 3, QTableWidgetItem(str(olive_modif)))
            self.tableWidget.setItem(selected_row, 4, QTableWidgetItem(str(stock_huile_modif)))
            self.tableWidget.setItem(selected_row, 5, QTableWidgetItem(str(depenses_modif)))
            self.tableWidget.setItem(selected_row, 6, QTableWidgetItem(str(revenu_modif)))
            self.tableWidget.setItem(selected_row, 7, QTableWidgetItem(str(benefice_modif)))
            self.tableWidget.setItem(selected_row, 8, QTableWidgetItem(str(nbr_client_modif)))

            self.reinitialiser_champs()

            QMessageBox.information(self, "Succès", "Modifications enregistrées avec succès.")

        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")

    # fonction de suppression
    def supprimer_ligne(self):
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
                id_entree = self.tableWidget.item(selected_row, 0).text()

            # Supprimer la ligne de la base de données
                self.dbb.cursor.execute("DELETE FROM inventaire WHERE id = %s", (id_entree,))
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



        else:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à supprimer.")

    def reinitialiser_champs(self):
        # Réinitialiser les champs QLineEdit
        self.lineEdit_depense.clear()
        self.lineEdit_revenus.clear()
        self.lineEdit_qte_huile.clear()
        self.lineEdit_qte_olive.clear()
        self.lineEdit_nbr_client.clear()
        self.lineEdit_stock_huile.clear()

    def reinitialiser_id(self):
        # Réinitialiser l'auto-incrémentation de l'ID dans la base de données
        self.dbb.cursor.execute("ALTER TABLE inventaire AUTO_INCREMENT = 1")
        self.dbb.conn.commit()

    def rechercher_par_date(self):
        text = self.Barre.text()
        # Convertir la date saisie dans le format yyyy/MM/dd
        date_saisie = QDate.fromString(text, "yyyy/MM/dd")

        self.tableWidget.clearSelection()

        for row in range(self.tableWidget.rowCount()):
            date_item = self.tableWidget.item(row, 2)  # La date est dans la colonne 2
            if date_item is not None:
                # Convertir la date de la tableWidget dans le format yyyy/MM/dd
                date_table = QDate.fromString(date_item.text(), "yyyy/MM/dd")
                if date_table == date_saisie:
                    self.tableWidget.selectRow(row)
                    self.colorier_ligne(row)
                    return

        QMessageBox.information(self, "Aucune correspondance", "Aucune entrée ne correspond à la date saisie.")

    def colorier_ligne(self, row):
        # Colorier la ligne sélectionnée en vert
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(row, col)
            if item is not None:
                item.setBackground(QColor("#c0c2e8"))  # Choisir la couleur de fond souhaitée


    def closeEvent(self, event):
        self.dbb.close()