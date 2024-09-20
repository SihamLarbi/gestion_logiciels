import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
from SCRIPTS.utilisateur import Utilisateur
from PyQt5.QtGui import QColor

from SCRIPTS.DataBaseManager import DataBaseManager

from SCRIPTS.connexion import Connexion

from SCRIPTS.EventFilter import EventFilter




class Stock(QMainWindow):
    """
    Cette classe gère l'interface utilisateur et les fonctionnalités liées au stock.
    """

    def __init__(self, stacked_widget):
        super(Stock, self).__init__()
        try:
            loadUi('INTERFACES/stock.ui', self)  # Chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1)
        # créer un objet dbb (base de donnes) de la classe DataBaseManger
        self.dbb = DataBaseManager()
        self.dbb.connect()

        self.stacked_widget = stacked_widget
        self.navigation_ui()
        self.listWidget2.hide()
        self.list_btn.clicked.connect(self.show_list)
        #self.menu_widget_2.hide()
        self.menu_btn_2.clicked.connect(self.show_menu_widget)
        self.info_widget.hide()
        self.info_btn.clicked.connect(self.show_info_widget)
        self.user_btn.clicked.connect(self.load_utilisateur)

        # connecter le signal clicked du bouton 'Ajouter' a a ma methode
        self.AddButtonS.clicked.connect(self.ajouter_stock)

        # connecter l'événement de clic sur notre QTableWdiget a une fonction pour charger les données dans les LineEdits
        self.tableWidget.cellClicked.connect(self.charger_donnees_ligne_selectionnee5)

        # connecter le signal clicked du bouton 'Modifier' a ma methode
        self.ModifierButtonS.clicked.connect(self.enregistrer_modifications5)

        # connecter le signal clicked du bouton 'Confirmer' a ma methode
        self.ConfirmerButton.clicked.connect(self.confirmer_stock)

        # connecter le signal clicked du bouton'Supprimer'a la methode
        self.SupprimerButtonS.clicked.connect(self.supprimer_ligne5)

        self.AnnulerButtonS.clicked.connect(self.reinitialiser_champs5)

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
        if self.menu_widget_2.isHidden():
            self.menu_widget_2.show()
        elif not self.menu_btn_2.isChecked():  # Vérifie si le bouton menu_btn n'est pas enfoncé
            self.menu_widget_2.hide()

    def show_list(self):
        # Affiche ou masque le widget listWidget en fonction de son état actuel
        if self.listWidget2.isHidden():
            self.listWidget2.show()
        else:
            self.listWidget2.hide()

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

    def mettre_a_jour_liste_stock(self):

        self.listWidget2.clear()  # Effacer le contenu actuel de la listWidget

        # Parcourir les lignes de la tableWidget et ajouter les informations des produits stock à la listWidget
        for row in range(self.tableWidget.rowCount()):
            nom_produit = str(self.tableWidget.item(row, 1).text())  # Nom du produit
            qte_produit_en_stock = str(self.tableWidget.item(row, 2).text())  # Quantité du produit en stock
            emplacement = str(self.tableWidget.item(row, 3).text())  # emplacement
            seuil = str(self.tableWidget.item(row,4).text()) # le seuil
            # Créer une chaîne formatée avec les informations du produit
            produit_stock = f"{nom_produit} - Qté_en_stock: {qte_produit_en_stock}, Emplacement: {emplacement}"

            # Ajouter la chaîne à la listWidget
            self.listWidget2.addItem(produit_stock)

    def search_by_id(self):
        # Récupérer l'id saisie dans la barre de recherche
        search_id = self.Barre.text().strip()

        # Vérifier que l'ID n'est pas vide
        if not search_id:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un Id.")
            return

        # Chercher l'id dans la table
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

    def ajouter_stock(self):
        # récupérer les valeurs saisies dans les LineEdits
        try:
            nom_produit = str(self.produit.text())
            qte_en_stock = float(self.qtite.text())
            seuil_alerte = float(self.seuil.text())
            emplacement = str(self.emplacement.text())
            qte_a_reduire = str(self.qte_a_reduire.text())

            # insertion des données dans la base de données
            self.dbb.cursor.execute("""
                                INSERT INTO stockk (Nom_produit, Qte_en_stock, seuil_alerte,qte_a_reduire, Emplacement)
                                VALUES (%s, %s, %s, %s, %s)
                                """, (nom_produit, qte_en_stock, seuil_alerte, qte_a_reduire, emplacement))
            self.dbb.conn.commit()

            QMessageBox.information(self, "Succès", "Entrée ajoutée avec succès à la base de données.")
            self.reinitialiser_champs5()
        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout de l'entrée:{err}")

        # apres avoir inséré les données avec succés, vider la tableWidget
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        # récupérer les données de la base de données après l'ajout
        self.dbb.cursor.execute("SELECT * FROM stockk ")
        result5 = self.dbb.cursor.fetchall()  # récupérer toutes les lignes

        # Ajouter les données a la tableWidget
        for row_number, row_data in enumerate(result5):
            # Insérer une nouvelle ligne dans le QTableWidget
            self.tableWidget.insertRow(row_number)
            # Colonnes dans l'ordre : ID_produit, Nom_produit, Qte_en_stock, seuil_alerte, qte_a_reduire, Emplacement
            id_produit = row_data[0]
            nom_produit = row_data[1]
            qte_en_stock = row_data[2]
            emplacement = row_data[5]
            seuil_alerte = row_data[3]

            # Créer un QTableWidgetItem pour chaque valeur et l'insérer dans le QTableWidget
            self.tableWidget.setItem(row_number, 0, QTableWidgetItem(str(id_produit)))
            self.tableWidget.setItem(row_number, 1, QTableWidgetItem(str(nom_produit)))
            self.tableWidget.setItem(row_number, 2, QTableWidgetItem(str(qte_en_stock)))
            self.tableWidget.setItem(row_number, 3, QTableWidgetItem(str(emplacement)))
            self.tableWidget.setItem(row_number, 4, QTableWidgetItem(str(seuil_alerte)))

        self.mettre_a_jour_liste_stock()

    def confirmer_stock(self):
        try:
            # Vérifier si une ligne est sélectionnée dans la tableWidget
            if self.tableWidget.currentRow() == -1:
                QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à modifier.")
                return

            # Récupérer la quantité à réduire saisie dans le LineEdit
            qte_a_reduire = float(self.qte_a_reduire.text())
            if qte_a_reduire <= 0:
                QMessageBox.warning(self, "Quantité invalide", "Veuillez saisir une quantité valide à réduire.")
                return

            # Récupérer l'index de la ligne sélectionnée
            selected_row = self.tableWidget.currentRow()

            # Récupérer la quantité en stock actuelle de la ligne sélectionnée
            qte_en_stock_actuelle = float(self.tableWidget.item(selected_row, 2).text())

            # Calculer la nouvelle quantité en stock
            nouvelle_qte_en_stock = qte_en_stock_actuelle - qte_a_reduire

            # Vérifier si la nouvelle quantité en stock est positive ou nulle
            if nouvelle_qte_en_stock < 0:
                QMessageBox.warning(self, "Stock insuffisant",
                                    "La quantité à réduire est supérieure à la quantité en stock.")
                return

            # Mettre à jour la quantité en stock dans la tableWidget
            self.tableWidget.item(selected_row, 2).setText(str(nouvelle_qte_en_stock))

            # Afficher un message de succès
            QMessageBox.information(self, "Succès",
                                    f"La quantité en stock a été mise à jour avec succès. Nouvelle quantité en stock : {nouvelle_qte_en_stock}")

            self.mettre_a_jour_liste_stock()

        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie",
                                 "Veuillez saisir une quantité à réduire valide (nombre positif).")

    def charger_donnees_ligne_selectionnee5(self, row, column):
        # Réinitialiser la couleur de fond de toutes les lignes à leur couleur par défaut (blanc)
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    item.setBackground(QColor("white"))

        # Color les lignes séléctionée
        self.colorier_ligne(row)


        # Récupérer les données de la ligne sélectionnée
        id_produit = self.tableWidget.item(row, 0).text()
        nom_produit= self.tableWidget.item(row, 1).text()
        qte_en_stock= self.tableWidget.item(row, 2).text()
        emplacement = self.tableWidget.item(row, 3).text()
        seuil_alerte =self.tableWidget.item(row, 4).text()





        # afficher les données dans les LineEdits
        self.produit.setText(nom_produit)
        self.qtite.setText(qte_en_stock)
        self.emplacement.setText(emplacement)
        self.seuil.setText(seuil_alerte)

        # focntion pour enregistrer les modification dans la bdd

    def enregistrer_modifications5(self):
        try:
            # Récupérer les valeurs modifiées à partir des LineEdits
            nomProduit = str(self.produit.text())
            qte_produit = float(self.qtite.text())
            seuil = float(self.seuil.text())
            emplacement = str(self.emplacement.text())

            # Vérifier si une ligne est sélectionnée dans la tableWidget
            if self.tableWidget.currentRow() == -1:
                QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à modifier.")
                return

            # Récupérer l'ID de l'achat
            selected_row = self.tableWidget.currentRow()
            id_p = self.tableWidget.item(selected_row, 0).text()

            # Mettre à jour les données dans la base de données
            self.dbb.cursor.execute("""
                                                  UPDATE stockk
                                                  SET Nom_produit=%s, Qte_en_stock=%s , seuil_alerte =%s, Emplacement=%s 
                                                  WHERE ID_produit=%s
                                              """, (nomProduit, qte_produit, seuil, emplacement, id_p))
            self.dbb.conn.commit()

            # Mettre à jour les cellules correspondantes dans le QTableWidget
            self.tableWidget.setItem(selected_row, 1, QTableWidgetItem(nomProduit))
            self.tableWidget.setItem(selected_row, 2, QTableWidgetItem(str(qte_produit)))
            self.tableWidget.setItem(selected_row, 3, QTableWidgetItem(str(emplacement)))
            self.tableWidget.setItem(selected_row, 4, QTableWidgetItem(str(seuil)))

            self.reinitialiser_champs5()

            QMessageBox.information(self, "Succès", "Modifications enregistrées avec succès.")

            self.mettre_a_jour_liste_stock()

        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")

    def supprimer_ligne5(self):

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

                id_stock = self.tableWidget.item(selected_row, 0).text()

                # Supprimer la ligne de la base de données
                self.dbb.cursor.execute("DELETE FROM stockk WHERE ID_produit = %s", (id_stock,))
                self.dbb.conn.commit()

                # Supprimer la ligne de la tableWidget
                self.tableWidget.removeRow(selected_row)
                self.reinitialiser_champs5()

                # Réinitialiser la couleur de fond de la ligne supprimée
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(selected_row, j)
                    if item is not None:
                        item.setBackground(QColor("white"))

                #  si toutes les lignes sont supprimées , reinitialiser l'auto-incrémentation de l'id
                if self.tableWidget.rowCount() == 0:
                    self.reinitialiser_id()

                self.mettre_a_jour_liste_stock()

        else:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à supprimer.")

    def reinitialiser_champs5(self):
        # Réinitialiser les champs QLineEdit
        self.produit.clear()
        self.qtite.clear()
        self.seuil.clear()
        self.emplacement.clear()
        self.qte_a_reduire.clear()


    def colorier_ligne(self, row):
        # Colorier la ligne sélectionnée en vert
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(row, col)
            if item is not None:
                item.setBackground(QColor("#c0c2e8"))  # Choisir la couleur de fond souhaitée



    def reinitialiser_id(self):
        # Réinitialiser l'auto-incrémentation de l'ID dans la base de données
        self.dbb.cursor.execute("ALTER TABLE stockk AUTO_INCREMENT = 1")
        self.dbb.conn.commit() #pour enregistrer les modifications

    def closeEvent(self, event):
        self.dbb.close()



