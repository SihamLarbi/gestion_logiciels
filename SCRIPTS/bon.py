import sys
from PyQt5.QtWidgets import QApplication, QMessageBox,QDialog
from PyQt5.uic import loadUi


class Bon(QDialog):
    """
    Cette classe gère l'interface utilisateur et les fonctionnalités liées aux employés.
    """

    def __init__(self):
        super(Bon, self).__init__()
        try:
            loadUi('INTERFACES/bon.ui', self)  # Chargement de l'interface achats
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Erreur de chargement de UI: {e}')
            sys.exit(1)


        self.imprimer_btn.clicked.connect(self.imprimer_function)
        self.setFixedSize(600, 600)



    def imprimer_function(self):
        pass
