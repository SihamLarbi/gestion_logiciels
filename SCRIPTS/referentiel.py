import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QVBoxLayout
from PyQt5.uic import loadUi
from SCRIPTS.utilisateur import Utilisateur
from PyQt5.QtCore import QDate
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QTableWidgetItem
from SCRIPTS.achat import Achats

class Referentiel(QMainWindow):
    """
    Cette classe gère l'interface utilisateur et les fonctionnalités liées aux employés.
    """

    def __init__(self, stacked_widget):
        super(Referentiel, self).__init__()
        try:
            loadUi('INTERFACES/referentiel.ui', self)  # Chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1)

        self.stacked_widget = stacked_widget
        self.navigation_ui()
        self.gauche_btn.clicked.connect(self.changer_page_1)
        self.droite_btn.clicked.connect(self.changer_page_2)
        self.gauche_btn_2.clicked.connect(self.changer_page_1)
        self.droite_btn_2.clicked.connect(self.changer_page_2)
        self.menu_btn_6.clicked.connect(self.show_menu_widget)
        self.user_btn.clicked.connect(self.load_utilisateur)


        self.achat_interface = None  # Référence à l'interface Achat
        self.inventaire_interface = None
        self.canvas = None # # Canvas pour les dépenses, canevas est utilisé pour stocker une référence à l'élément qui affiche le graphique, et il est mis à jour chaque fois que le graphique est modifié ou recréé.
        self.canvas_revenue = None  # Canvas pour les revenus


        self.graphicsView.setLayout(QVBoxLayout())  # Ajoute une disposition verticale
        self.graphicsView_2.setLayout(QVBoxLayout())
        self.update_graph()
        self.update_graph2()
    def load_utilisateur(self):
        user = Utilisateur()
        user.exec_()

    def show_menu_widget(self):
        # Affiche ou masque le widget menu_widget en fonction de son état actuel
        if self.menu_widget_6.isHidden():
            self.menu_widget_6.show()
        elif not self.menu_btn_6.isChecked():  # Vérifie si le bouton menu_btn n'est pas enfoncé
            self.menu_widget_6.hide()

    def changer_page_1(self):
        self.stackedWidget.setCurrentIndex(0)  # Index de la première page

    def changer_page_2(self):
        self.stackedWidget.setCurrentIndex(1)  # Index de la deuxième page

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

    def set_achat_interface(self, achat_interface):
        self.achat_interface = achat_interface
        self.achat_interface.tableWidget.itemChanged.connect(self.update_graph) #  Connecte le signal itemChanged de la QTableWidget de l'interface d'achat à la méthode update_graph de l'interface de référentiel. Cela signifie que chaque fois qu'un élément dans la table de l'interface d'achat est modifié, la méthode update_graph de l'interface de référentiel sera appelée pour mettre à jour le graphique affiché. Cela permet d'assurer que le graphique est mis à jour en temps réel en fonction des modifications apportées aux données dans l'interface d'achat.

    def update_graph(self):
        if not self.achat_interface:
            return

        tableWidget = self.achat_interface.tableWidget # Cette ligne récupère la QTableWidget de l'interface d'achat pour accéder aux données.
        rows = tableWidget.rowCount()
        dates = []
        amounts = []

        for row in range(rows):
            date_item = tableWidget.item(row, 1)
            amount_item = tableWidget.item(row, 5)

            if date_item and amount_item:
                date_text = date_item.text()
                amount_text = amount_item.text()

                try:
                    date = QDate.fromString(date_text, "yyyy-MM-dd").toPyDate()
                    amount = float(amount_text)
                    dates.append(date)
                    amounts.append(amount)
                except ValueError:
                    continue

        if not dates or not amounts:
            return



        # Trier les données par date
        data = sorted(zip(dates, amounts), key=lambda x: x[0]) #  La fonction zip combine deux listes (dates et amounts) élément par élément pour former une liste de tuples. Chaque tuple contient une paire de valeurs, où la première valeur est une date et la deuxième est un montant.
        dates, amounts = zip(*data) # Cette ligne sépare les dates et les montants triés en deux listes distinctes.

        # Créer une nouvelle figure
        if self.canvas:
            self.graphicsView.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()
            #Ces lignes suppriment le graphique précédent (s'il existe) de la zone graphique (graphicsView) afin de nettoyer avant d'afficher un nouveau graphique.
        plt.close('all')  # Ferme toutes les figures ouvertes précédemment
        fig, ax = plt.subplots()
        ax.bar(dates, amounts, width=0.2, color="#c0c2e8", label='Dépenses')

        ax.set_xlabel('Date')
        ax.set_ylabel('Montant total')
        ax.set_title('Dépenses en fonction de la date')
        ax.legend()

        self.canvas = FigureCanvas(fig)
        self.graphicsView.layout().addWidget(self.canvas)


# -----------------------------------------------------------------------------------------

    def set_inventaire_interface(self, inventaire_interface):
        self.inventaire_interface = inventaire_interface
        self.inventaire_interface.tableWidget.itemChanged.connect(self.update_graph2)

    def update_graph2(self):
        if not self.inventaire_interface:
            return

        tableWidget = self.inventaire_interface.tableWidget
        rows = tableWidget.rowCount()
        dates = []
        incomes = []

        for row in range(rows):
            date_item = tableWidget.item(row, 1)  # Colonne de la date
            income_item = tableWidget.item(row, 6)  # Colonne des revenus

            if date_item and income_item:
                date_text = date_item.text()
                income_text = income_item.text()


                try:
                    date = QDate.fromString(date_text, "yyyy-MM-dd").toPyDate()
                    income = float(income_text)
                    dates.append(date)
                    incomes.append(income)

                except ValueError as e:
                    print(f"Error parsing row {row}: {e}")  # Debug: Affiche les erreurs de parsing
                    continue

        if not dates or not incomes:
            return

        # Trier les données par date
        data = sorted(zip(dates, incomes), key=lambda x: x[0])
        dates, incomes = zip(*data)

        # Créer une nouvelle figure
        if self.canvas_revenue:
            self.graphicsView_2.layout().removeWidget(self.canvas_revenue)
            self.canvas_revenue.deleteLater()

        plt.close('all')  # Ferme toutes les figures ouvertes précédemment

        fig, ax = plt.subplots()
        ax.plot(dates, incomes, marker='o', linestyle='-', color="#c0c2e8", label='Revenus')

        ax.set_xlabel('Date')
        ax.set_ylabel('Revenu')
        ax.set_title('Revenus en fonction de la date')
        ax.legend()

        # Formater les dates sur l'axe x
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # Faire pivoter les étiquettes des dates pour une meilleure lisibilité
        fig.autofmt_xdate(rotation=45)

        self.canvas_revenue = FigureCanvas(fig)
        self.graphicsView_2.layout().addWidget(self.canvas_revenue)


