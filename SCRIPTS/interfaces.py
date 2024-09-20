import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QStackedWidget, QMainWindow
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

class Achats(QMainWindow):
    def __init__(self,stacked_widget):
        super(Achats, self).__init__()
        try:
            loadUi('INTERFACES/achats.ui', self)  # Chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1)

        self.stacked_widget = stacked_widget
        self.buttonclicked()


    def buttonclicked(self):
        self.inventaire_btn.clicked.connect(self.load_inventaire)
        self.achats_btn.clicked.connect(self.load_achats)
        self.stock_btn.clicked.connect(self.load_stock)
        self.client_btn.clicked.connect(self.load_client)
        self.employee_btn.clicked.connect(self.load_employe)
        self.fournisseurs_btn.clicked.connect(self.load_fournisseurs)
        self.referentiel_btn.clicked.connect(self.load_referentiel)

    def load_inventaire(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.setCurrentIndex()-1)

    def load_achats(self):
        pass

    def load_stock(self):
        print('Stock ui est appélé')
        self.stacked_widget.setCurrentIndex(self.stacked_widget.setCurrentIndex()+1)

    def load_client(self):
        self.stacked_widget.setCurrentIndex(3)

    def load_employe(self):
        self.stacked_widget.setCurrentIndex(4)

    def load_fournisseurs(self):
        self.stacked_widget.setCurrentIndex(5)


    def load_referentiel(self):
        self.stacked_widget.setCurrentIndex(6)


class Stock(QMainWindow):
    def __init__(self,stacked_widget):
        super(Stock, self).__init__()
        try:
            loadUi('INTERFACES/stock.ui', self)  # Chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1)

        self.stacked_widget = stacked_widget
        self.buttonclicked()


    def buttonclicked(self):
        self.inventaire_btn.clicked.connect(self.load_inventaire)
        self.achats_btn.clicked.connect(self.load_achats)
        self.stock_btn.clicked.connect(self.load_stock)
        self.client_btn.clicked.connect(self.load_client)
        self.employee_btn.clicked.connect(self.load_employe)
        self.fournisseurs_btn.clicked.connect(self.load_fournisseurs)
        self.referentiel_btn.clicked.connect(self.load_referentiel)

    def load_inventaire(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.setCurrentIndex()-2)

    def load_achats(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.setCurrentIndex()-1)

    def load_stock(self):
        pass

    def load_client(self):
        self.stacked_widget.setCurrentIndex(3)

    def load_employe(self):
        self.stacked_widget.setCurrentIndex(4)

    def load_fournisseurs(self):
        self.stacked_widget.setCurrentIndex(5)


    def load_referentiel(self):
        self.stacked_widget.setCurrentIndex(6)


'''
class Clients(QMainWindow):
    def __init__(self):
        super(Clients, self).__init__()
        try:
            loadUi('INTERFACES/clients.ui', self)  # chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI :{e}')
            sys.exit(1)

        self.buttonclicked()

    def buttonclicked(self):
        self.inventaire_btn.clicked.connect(self.load_inventaire)
        self.achats_btn.clicked.connect(self.load_achats)
        self.stock_btn.clicked.connect(self.load_stock)
        self.client_btn.clicked.connect(self.load_client)
        self.employee_btn.clicked.connect(self.load_employee)
        self.fournisseurs_btn.clicked.connect(self.load_fournisseurs)
        self.referentiel_btn.clicked.connect(self.load_referentiel)


class Employes(QMainWindow):
    def __init__(self):
        super(Employes, self).__init__()
        try:
            loadUi('INTERFACES/employes.ui', self)  # chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI :{e}')
            sys.exit(1)

        self.buttonclicked()

    def buttonclicked(self):
        self.inventaire_btn.clicked.connect(self.load_inventaire)
        self.achats_btn.clicked.connect(self.load_achats)
        self.stock_btn.clicked.connect(self.load_stock)
        self.client_btn.clicked.connect(self.load_client)
        self.employee_btn.clicked.connect(self.load_employee)
        self.fournisseurs_btn.clicked.connect(self.load_fournisseurs)
        self.referentiel_btn.clicked.connect(self.load_referentiel)


class Fournisseurs(QMainWindow):
    def __init__(self):
        super(Fournisseurs, self).__init__()
        try:
            loadUi('INTERFACES/fournisseurs.ui', self)  # chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI :{e}')
            sys.exit(1)

        self.buttonclicked()

    def buttonclicked(self):
        self.inventaire_btn.clicked.connect(self.load_inventaire)
        self.achats_btn.clicked.connect(self.load_achats)
        self.stock_btn.clicked.connect(self.load_stock)
        self.client_btn.clicked.connect(self.load_client)
        self.employee_btn.clicked.connect(self.load_employee)
        self.fournisseurs_btn.clicked.connect(self.load_fournisseurs)
        self.referentiel_btn.clicked.connect(self.load_referentiel)


class Referentiel(QMainWindow):
    def __init__(self):
        super(Referentiel, self).__init__()
        try:
            loadUi('INTERFACES/referentiel.ui', self)  # chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI :{e}')
            sys.exit(1)

        self.buttonclicked()

    def buttonclicked(self):
        self.inventaire_btn.clicked.connect(self.load_inventaire)
        self.achats_btn.clicked.connect(self.load_achats)
        self.stock_btn.clicked.connect(self.load_stock)
        self.client_btn.clicked.connect(self.load_client)
        self.employee_btn.clicked.connect(self.load_employee)
        self.fournisseurs_btn.clicked.connect(self.load_fournisseurs)
        self.referentiel_btn.clicked.connect(self.load_referentiel) '''