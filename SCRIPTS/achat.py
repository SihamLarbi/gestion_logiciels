import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
from SCRIPTS.utilisateur import Utilisateur
from PyQt5.QtGui import QColor
from datetime import datetime
from SCRIPTS.connexion import Connexion


from SCRIPTS.DataBaseManager import DataBaseManager

from SCRIPTS.EventFilter import EventFilter




class Achats(QMainWindow):
    """
    Cette classe gère l'interface utilisateur et les fonctionnalités liées aux achats.
    """

    def __init__(self, stacked_widget):
        super(Achats, self).__init__()

        try:
            loadUi('INTERFACES/achats.ui', self)  # Chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1)
        # créer un objet dbb (base de donnes) de la classe DataBaseManger
        self.dbb = DataBaseManager()
        self.dbb.connect()

        self.stacked_widget = stacked_widget
        self.navigation_ui()
        self.listWidget.hide()
        self.list_btn.clicked.connect(self.show_list)
        #self.menu_widget_1.hide()
        self.menu_btn_1.clicked.connect(self.show_menu_widget)
        self.info_widget.hide()
        self.info_btn.clicked.connect(self.show_info_widget)
        self.user_btn.clicked.connect(self.load_utilisateur)

        # connecter le signal clicked du bouton 'Ajouter' a a ma methode
        self.AddButtonA.clicked.connect(self.ajouter_achat)

        # connecter l'événement de clic sur notre QTableWdiget a une fonction pour charger les données dans les LineEdits
        self.tableWidget.cellClicked.connect(self.charger_donnees_ligne_selectionnee4)

        # connecter le signal clicked du bouton 'Modifier' a ma methode
        self.ModifierButtonA.clicked.connect(self.enregistrer_modifications4)

        # connecter le signal clicked du bouton'Supprimer'a la methode
        self.SupprimerButtonA.clicked.connect(self.supprimer_ligne4)

        self.AnnulerButtonA.clicked.connect(self.reinitialiser_champs4)

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
        if self.menu_widget_1.isHidden():
            self.menu_widget_1.show()
        elif not self.menu_btn_1.isChecked():  # Vérifie si le bouton menu_btn n'est pas enfoncé
            self.menu_widget_1.hide()


        else:
            self.menu_widget_1.hide()

    def show_list(self):
        # Affiche ou masque le widget listWidget en fonction de son état actuel
        if self.listWidget.isHidden():
            self.listWidget.show()
        else:
            self.listWidget.hide()

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


    def mettre_a_jour_liste_achats(self):

        self.listWidget.clear()  # Effacer le contenu actuel de la listWidget

        # Parcourir les lignes de la tableWidget et ajouter les informations des produits à la listWidget
        for row in range(self.tableWidget.rowCount()):
            nom_produit = str(self.tableWidget.item(row, 2).text())  # Nom du produit
            qte_produit = str(self.tableWidget.item(row, 3).text())  # Quantité du produit
            prix_unitaire = str(self.tableWidget.item(row, 4).text())  # Prix unitaire du produit
            date_achat = str(self.tableWidget.item(row, 1).text())  # Date de l'achat

            # Créer une chaîne formatée avec les informations du produit
            produit_info = f"{nom_produit} - Qté: {qte_produit}, Prix unitaire: {prix_unitaire} , Date achat: {date_achat}"

            # Ajouter la chaîne à la listWidget
            self.listWidget.addItem(produit_info)

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


    def ajouter_achat(self):
        # récupérer les valeurs saisies dans les LineEdits
        try:
            nomProduit = str(self.nomProduit.text())
            Qte_produit = float(self.Qte_produit.text())
            montant = float(self.montant.text())
            prix_unitaire = float(self.prix.text())
            fournisseur = int(self.fournisseur.text())
            date = datetime.now().date()  # date actuelle

            # Vérifier si l'ID du fournisseur existe
            if not self.verifier_fournisseur_existe(fournisseur):
                QMessageBox.warning(self, "ID Fournisseur non trouvé",
                                    "L'ID du fournisseur saisi n'existe pas dans la base de données.")
                return

            # insertion des donnees dans la bdd

            self.dbb.cursor.execute("""
                              INSERT INTO achat (Date, Nom_produit, Qte_produit, Prix_unitaire, Montant_total,Fournisseur)
                              VALUES (%s, %s, %s, %s, %s, %s)
                              """, (date, nomProduit, Qte_produit, prix_unitaire, montant, fournisseur))
            self.dbb.conn.commit()

            QMessageBox.information(self, "Succès", "Entrée ajoutée avec succès à la base de données.")
            self.reinitialiser_champs4()
        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout de l'entrée:{err}")

        # apres avoir inséré les données avec succes, vider la tableWidget
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        # # récupérer les données de la base de données après l'ajout
        self.dbb.cursor.execute("SELECT * FROM achat ")
        result4 = self.dbb.cursor.fetchall()  # recuperer toutes les lignes

        # Ajouter les données a la tableWidget
        for row_number, row_data in enumerate(result4):
            # Insérer une nouvelle ligne dans le QTableWidget
            self.tableWidget.insertRow(row_number)
            for column, value in enumerate(row_data):
                # Créer un QTableWidgetItem pour chaque valeur et l'insérer dans le QTableWidget
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_number, column, item)

        self.mettre_a_jour_liste_achats()



    def verifier_fournisseur_existe(self, fournisseur_id):
        self.dbb.cursor.execute("SELECT COUNT(*) FROM fournisseur WHERE idfournisseur = %s", (fournisseur_id,))
        result = self.dbb.cursor.fetchone()
        return result[0] > 0

    def charger_donnees_ligne_selectionnee4(self, row, column):
        # Réinitialiser la couleur de fond de toutes les lignes à leur couleur par défaut (blanc)
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    item.setBackground(QColor("white"))

        # Color les lignes séléctionée
        self.colorier_ligne(row)


        # Récupérer les données de la ligne sélectionnée
        id_achat = self.tableWidget.item(row, 0).text()
        date =self.tableWidget.item(row, 1).text()
        nomP = self.tableWidget.item(row, 2).text()
        Qte_produit = self.tableWidget.item(row, 3).text()
        Prix_unitaire = self.tableWidget.item(row, 4).text()
        montant =self.tableWidget.item(row, 5).text()
        fournisseur = self.tableWidget.item(row, 6).text()


        # afficher les données dans les LineEdits
        self.nomProduit.setText(nomP)
        self.Qte_produit.setText(Qte_produit)
        self.montant.setText(montant)
        self.fournisseur.setText(fournisseur)
        self.prix.setText(Prix_unitaire)

        # focntion pour enregistrer les modification dans la bdd

    def enregistrer_modifications4(self):
        try:
            # Récupérer les valeurs modifiées à partir des LineEdits
            nomP = str(self.nomProduit.text())
            qte_produit = float(self.Qte_produit.text())
            montant = float(self.montant.text())
            fournisseur = int(self.fournisseur.text())
            prix_unitaire = float(self.prix.text())

            # Vérifier si une ligne est sélectionnée dans la tableWidget
            if self.tableWidget.currentRow() == -1:
                QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à modifier.")
                return

            # Vérifier si l'ID du fournisseur existe
            if not self.verifier_fournisseur_existe(fournisseur):
                QMessageBox.warning(self, "ID Fournisseur non trouvé",
                                    "L'ID du fournisseur saisi n'existe pas dans la base de données.")
                return

            # Récupérer l'ID de l'achat
            selected_row = self.tableWidget.currentRow()
            id_achat = self.tableWidget.item(selected_row, 0).text()

            # Mettre à jour les données dans la base de données
            self.dbb.cursor.execute("""
                             UPDATE achat
                             SET Nom_produit=%s, Qte_produit=%s , Prix_unitaire =%s,Montant_total =%s,Fournisseur=%s
                             WHERE ID_achat=%s
                         """, (nomP, qte_produit, prix_unitaire, montant, fournisseur, id_achat))
            self.dbb.conn.commit()

            # Mettre à jour les cellules correspondantes dans le QTableWidget
            self.tableWidget.setItem(selected_row, 2, QTableWidgetItem(nomP))
            self.tableWidget.setItem(selected_row, 3, QTableWidgetItem(str(qte_produit)))
            self.tableWidget.setItem(selected_row, 4, QTableWidgetItem(str(prix_unitaire)))
            self.tableWidget.setItem(selected_row, 5, QTableWidgetItem(str(montant)))
            self.tableWidget.setItem(selected_row, 6, QTableWidgetItem(str(fournisseur)))

            self.reinitialiser_champs4()

            QMessageBox.information(self, "Succès", "Modifications enregistrées avec succès.")

            self.mettre_a_jour_liste_achats()

        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")



    def supprimer_ligne4(self):
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
                id_achat = self.tableWidget.item(selected_row, 0).text()

                # Supprimer la ligne de la base de données
                self.dbb.cursor.execute("DELETE FROM achat WHERE ID_achat = %s", (id_achat,))
                self.dbb.conn.commit()

                # Supprimer la ligne de la tableWidget
                self.tableWidget.removeRow(selected_row)
                self.reinitialiser_champs4()

                # Réinitialiser la couleur de fond de la ligne supprimée
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(selected_row, j)
                    if item is not None:
                        item.setBackground(QColor("white"))

                #  si toutes les lignes sont supprimées , reinitialiser l'auto-incrémentation de l'id
                if self.tableWidget.rowCount() == 0:
                    self.reinitialiser_id()

                self.mettre_a_jour_liste_achats()
            else:
                pass
        else:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à supprimer.")



    def reinitialiser_champs4(self):
        # Réinitialiser les champs QLineEdit
        self.nomProduit.clear()
        self.Qte_produit.clear()
        self.montant.clear()
        self.fournisseur.clear()
        self.prix.clear()

    def colorier_ligne(self, row):
        # Colorier la ligne sélectionnée en vert
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(row, col)
            if item is not None:
                item.setBackground(QColor("#c0c2e8"))  # Choisir la couleur de fond souhaitée

    def reinitialiser_id(self):
        # Réinitialiser l'auto-incrémentation de l'ID dans la base de données
        self.dbb.cursor.execute("ALTER TABLE achat AUTO_INCREMENT = 1")
        self.dbb.conn.commit()



    def closeEvent(self, event):
        self.dbb.close()





