import sys

import mysql.connector
from PyQt5.QtGui import QColor

from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtGui import QPainter

from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QDialog, QTableWidgetItem, QComboBox
from PyQt5.uic import loadUi

from SCRIPTS.utilisateur import Utilisateur
from SCRIPTS.DataBaseManager import DataBaseManager

from SCRIPTS.EventFilter import EventFilter
from SCRIPTS.connexion import Connexion

class Bon(QDialog):
    def __init__(self, nom, prenom, m_payement, service, client_id):
        super(Bon, self).__init__()
        try:
            loadUi('INTERFACES/bon.ui', self)
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1)

        self.client_id = client_id

        self.imprimer_btn.clicked.connect(self.imprimer_function)

        self.le2.setText(str(nom))
        self.le3.setText(str(prenom))
        self.le6.setText(str(service))
        self.le9.setText(str(m_payement))

        self.le1.setText(str(client_id)) # affiche l'ID du client comme numéro de bon


        self.g_btn.clicked.connect(self.generate_function)
        self.apercu_btn.clicked.connect(self.preview_function)

    def preview_function(self):
        printer = QPrinter(QPrinter.HighResolution)
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(lambda printer: self.render_preview(printer))  # Utilisation de lambda pour passer l'argument printer
        preview_dialog.exec_()

    def render_preview(self, printer):
        painter = QPainter(printer)
        self.print_widget(painter, printer)  # Ajout de l'argument printer
        painter.end()

    def print_widget(self, painter, printer):
        widget = self.widget_bon  # Remplacez 'widget_bon' par le nom de votre widget à imprimer

        # Déplacer l'origine du QPainter au coin supérieur gauche de la page
        painter.translate(printer.paperRect(QPrinter.DevicePixel).topLeft())

        # Ajuster l'échelle du QPainter pour remplir la page
        painter.scale(printer.pageRect(QPrinter.DevicePixel).width() / widget.width(),
                      printer.pageRect(QPrinter.DevicePixel).height() / widget.height())

        # Peindre le contenu du widget dans le QPainter
        widget.render(painter)
    def generate_function(self):
        sac_text = self.le4.text().strip()
        bidon_text = self.le5.text().strip()
        qte_olive_text = self.le7.text().strip()
        qte_huile_text = self.le8.text().strip()

        # Vérifier que les champs ne sont pas vides
        if sac_text and bidon_text and qte_olive_text and qte_huile_text:
            try:
                sac = int(sac_text)
                bidon = int(bidon_text)
                qte_olive = float(qte_olive_text)
                qte_huile = float(qte_huile_text)

                # Accéder au texte du champ le6 pour obtenir le service
                service = self.le6.text()

                if service == 'Transformation olives' or service == 'Les deux':
                    resultat = (sac * 100) + (bidon * 150) + (qte_huile * 900) + qte_olive
                else:
                    resultat = (sac * 100) + (bidon * 150) + (qte_huile * 900)

                # Effacer le champ le10 avant de mettre à jour son contenu
                self.le10.clear()
                self.le10.setText(str(resultat))
            except ValueError:
                QMessageBox.warning(self, "Erreur de conversion", "Veuillez entrer des valeurs numériques valides.")
        else:
            QMessageBox.warning(self, "Champs vides", "Veuillez remplir tous les champs avant de générer le bon.")

    def imprimer_function(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            self.print_widget(painter)
            painter.end()



class Clients(QMainWindow):
    def __init__(self, stacked_widget):
        super(Clients, self).__init__()
        try:
            loadUi('INTERFACES/clients.ui', self)
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1)
        # créer un objet dbb (base de donnes) de la classe DataBaseManger
        self.dbb = DataBaseManager()
        self.dbb.connect()

        self.servie_box = QComboBox() # initialiser un QComboBox

        self.stacked_widget = stacked_widget
        self.navigation_ui()
        self.menu_btn_3.clicked.connect(self.show_menu_widget)
        self.info_widget.hide()
        self.info_btn.clicked.connect(self.show_info_widget)
        self.user_btn.clicked.connect(self.load_utilisateur)
        self.bon_btn.clicked.connect(self.load_bon)

        # connecter le signal clicked du bouton 'Ajouter' a a ma methode
        self.AddButtonC.clicked.connect(self.ajouter_client)

        # connecter l'événement de clic sur notre QTableWdiget a une fonction pour charger les données dans les LineEdits
        self.tableWidget.cellClicked.connect(self.charger_donnees_ligne_selectionnee2)

        # connecter le signal clicked du bouton 'Modifier' a ma methode
        self.ModifierButtonC.clicked.connect(self.enregistrer_modifications2)

        # connecter le signal clicked du bouton'Supprimer'a la methode
        self.SupprimerButtonC.clicked.connect(self.supprimer_ligne2)

        self.AnnulerButtonC.clicked.connect(self.reinitialiser_champs2)

        # Variable pour stocker l'ID du client sélectionné
        self.selected_client_id = None

        # Créer et installer l'EventFilter
        self.event_filter = EventFilter(self, self.tableWidget)
        self.installEventFilter(self.event_filter)

        self.Recherche.clicked.connect(self.search_by_id)

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
                self.colorier_ligne2(row)
                found = True
                break

        if not found:
            QMessageBox.information(self, "Recherche", "Aucune entrée trouvée pour l'Id spécifiée.")

    def load_bon(self, nom=None, prenom=None, m_payement=None, service=None, client_id=None):
        # Utiliser les valeurs fournies, ou celles des champs de texte si non spécifiées
        if nom is None:
            nom = self.nom_le.text().strip()
        if prenom is None:
            prenom = self.prenom_le.text().strip()
        if m_payement is None:
            m_payement = self.payement_box.currentText().strip()
        if service is None:
            if self.rad_1.isChecked():
                service = self.rad_1.text()
            elif self.rad_2.isChecked():
                service = self.rad_2.text()
            else:
                service = self.rad_3.text()
        if client_id is None:
            client_id = self.selected_client_id

        if not client_id:
            QMessageBox.warning(self, "Erreur", "Aucun client sélectionné.")
            return


        bon = Bon(nom, prenom, m_payement, service, client_id)
        bon.exec_()
    def load_utilisateur(self):
        user = Utilisateur()
        user.exec_()

    def show_info_widget(self):
        if self.info_widget.isHidden():
            self.info_widget.show()
        else:
            self.info_widget.hide()

    def show_menu_widget(self):
        if self.menu_widget_3.isHidden():
            self.menu_widget_3.show()
        elif not self.menu_btn_3.isChecked():
            self.menu_widget_3.hide()

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

    def ajouter_client(self):
        # récupérer les valeurs saisies dans les LineEdits
        try:
            nomC = str(self.nom_le.text())
            prenomC = str(self.prenom_le.text())
            ageC = int(self.age_le.text())
            adresseC = str(self.adresse_le.text())
            Num_telc = int(self.numtel_le.text())
            Service_choisi = []

            # Vérifier si le bouton radio correspondant à chaque service est coché
            if self.rad_1.isChecked():
                Service_choisi.append(self.rad_1.text())

            elif self.rad_2.isChecked():
                Service_choisi.append(self.rad_2.text())

            elif self.rad_3.isChecked():
                Service_choisi.append(self.rad_3.text())

            service_choisi_str = ', '.join(
                Service_choisi)  # on convertit  la liste en une chaine de caracater pour que'elle soit stocké dans la bdd car mysql ne stock pas les listes

            Etat_service = str(self.service_box.currentText())

            # insertion des donnees dans la bdd

            self.dbb.cursor.execute("""
                               INSERT INTO client ( Nom, Prénom ,Age, Adresse,Num_tel, Service_choisi , Etat_service)
                               VALUES ( %s, %s, %s, %s, %s, %s, %s)
                               """, (nomC, prenomC, ageC, adresseC, Num_telc, service_choisi_str, Etat_service))
            self.dbb.conn.commit()

            # récuperer l'ID du client nouvellement ajouté
            client_id = self.dbb.cursor.lastrowid

            QMessageBox.information(self, "Succès", "Entrée ajoutée avec succès à la base de données.")
            self.reinitialiser_champs2()

            self.load_bon(nomC, prenomC, Etat_service, service_choisi_str, client_id)

        except ValueError:
            QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout de l'entrée:{err}")

        # apres avoir inséré les données avec succes, vider la tableWidget
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        # # récupérer les données de la base de données après l'ajout
        self.dbb.cursor.execute("SELECT * FROM client ")
        result2 = self.dbb.cursor.fetchall()  # recuperer toutes les lignes

        # Ajouter les données a la tableWidget
        for row_number, row_data in enumerate(result2):
            # Insérer une nouvelle ligne dans le QTableWidget
            self.tableWidget.insertRow(row_number)
            for column, value in enumerate(row_data):
                # Créer un QTableWidgetItem pour chaque valeur et l'insérer dans le QTableWidget
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_number, column, item)

        # fonction pour charger les données de la ligne sélectionnée dans les lineEdits

    def charger_donnees_ligne_selectionnee2(self, row, column):
        # Réinitialiser la couleur de fond de toutes les lignes à leur couleur par défaut (blanc)
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    item.setBackground(QColor("white"))

        # Color les lignes séléctionée
        self.colorier_ligne2(row)

        # Récupérer les données de la ligne sélectionnée
        id_client = self.tableWidget.item(row, 0).text()
        nom = self.tableWidget.item(row, 1).text()
        prenom = self.tableWidget.item(row, 2).text()
        age = self.tableWidget.item(row, 3).text()
        adresse = self.tableWidget.item(row, 4).text()
        Num_tel = self.tableWidget.item(row, 5).text()
        Service_choisi = self.tableWidget.item(row, 6).text()
        Etat_service = self.tableWidget.item(row, 7).text()



        # afficher les données dans les LineEdits
        self.nom_le.setText(nom)
        self.prenom_le.setText(prenom)
        self.age_le.setText(age)
        self.adresse_le.setText(adresse)
        self.numtel_le.setText(Num_tel)
        self.service_box.setCurrentText(Etat_service)
        # Pour les boutons radio Service_choisi
        if Service_choisi == "Transformation olives":
            self.rad_1.setChecked(True)
        elif Service_choisi == "Achat d'huile":
            self.rad_2.setChecked(True)
        elif Service_choisi == "Les deux":
            self.rad_3.setChecked(True)

        # Stocker l'ID du client sélectionné
        self.selected_client_id = id_client



    # fonction pour enregistrer les modifications dans la bdd

    def enregistrer_modifications2(self):
            try:
                # Récupérer les valeurs modifiées à partir des LineEdits
                nom = str(self.nom_le.text())
                prenom = str(self.prenom_le.text())
                age = int(self.age_le.text())
                adresse = str(self.adresse_le.text())
                Num_tel = int(self.numtel_le.text())
                Service_choisi = []
                if self.rad_1.isChecked():
                    Service_choisi.append("Transformation olives")
                if self.rad_2.isChecked():
                    Service_choisi.append("Achat d'huile")
                if self.rad_3.isChecked():
                    Service_choisi.append("Les Deux")
                service_str = ', '.join(
                    Service_choisi)  # est une méthode pour créer une seule chaîne de caractères à partir des éléments d'une liste.
                Etat_service = self.servie_box.currentText()

                # Vérifier si une ligne est sélectionnée dans la tableWidget
                if self.tableWidget.currentRow() == -1:
                    QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à modifier.")
                    return

                # Mettre à jour les données dans la base de données

                selected_row = self.tableWidget.currentRow()
                id_client = self.tableWidget.item(self.tableWidget.currentRow(),
                                                  0).text()  # Récupérer l'ID de la ligne sélectionnée
                self.dbb.cursor.execute("""
                                  UPDATE client
                                  SET Nom=%s, Prénom=%s , Age =%s, Adresse=%s,Num_tel=%s,Service_choisi=%s ,Etat_service = %s
                                  WHERE ID_client=%s
                              """, (nom, prenom, age, adresse, Num_tel, service_str, Etat_service, id_client))
                self.dbb.conn.commit()

                # mettre a jour les cellules correspondantes dans le QTablewidget
                self.tableWidget.setItem(selected_row, 1, QTableWidgetItem(nom))
                self.tableWidget.setItem(selected_row, 2, QTableWidgetItem(prenom))
                self.tableWidget.setItem(selected_row, 3, QTableWidgetItem(str(age)))
                self.tableWidget.setItem(selected_row, 4, QTableWidgetItem(adresse))
                self.tableWidget.setItem(selected_row, 5, QTableWidgetItem(str(Num_tel)))
                self.tableWidget.setItem(selected_row, 6, QTableWidgetItem(service_str))
                self.tableWidget.setItem(selected_row, 7, QTableWidgetItem(Etat_service))

                self.reinitialiser_champs2()

                QMessageBox.information(self, "Succès", "Modifications enregistrées avec succès.")
            except ValueError:
                QMessageBox.critical(self, "Erreur de saisie", "Veuillez saisir des valeurs numériques valides")

        # fonction de suppression


    def supprimer_ligne2(self):
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
                id_client = self.tableWidget.item(selected_row, 0).text()

                # Supprimer la ligne de la base de données
                self.dbb.cursor.execute("DELETE FROM client WHERE ID_client = %s", (id_client,))
                self.dbb.conn.commit()

                # Supprimer la ligne de la tableWidget
                self.tableWidget.removeRow(selected_row)
                self.reinitialiser_champs2()

                # Réinitialiser la couleur de fond de la ligne supprimée
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(selected_row, j)
                    if item is not None:
                        item.setBackground(QColor("white"))

                #  si toutes les lignes sont supprimées , reinitialiser l'auto-incrémentation de l'id
                if self.tableWidget.rowCount() == 0:
                    self.reinitialiser_id2()



        else:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une ligne à supprimer.")

    def reinitialiser_champs2(self):
        # Réinitialiser les champs QLineEdit
        self.nom_le.clear()
        self.prenom_le.clear()
        self.age_le.clear()
        self.adresse_le.clear()
        self.numtel_le.clear()

        # Décocher tous les boutons radio
        self.rad_1.setAutoExclusive(False)
        self.rad_2.setAutoExclusive(False)
        self.rad_3.setAutoExclusive(False)
        self.rad_1.setChecked(False)
        self.rad_2.setChecked(False)
        self.rad_3.setChecked(False)

        # définir mon qcombox par defaut 'Servi'
        self.service_box.setCurrentText("Servi")

    def colorier_ligne2(self, row):
        # Colorier la ligne sélectionnée en vert
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(row, col)
            if item is not None:
                item.setBackground(QColor("#c0c2e8"))  # Choisir la couleur de fond souhaitée


    def reinitialiser_id2(self):
        # Réinitialiser l'auto-incrémentation de l'ID dans la base de données
        self.dbb.cursor.execute("ALTER TABLE client AUTO_INCREMENT = 1")
        self.dbb.conn.commit()







