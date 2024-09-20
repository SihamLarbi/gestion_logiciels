import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog, QDesktopWidget,QMessageBox
from SCRIPTS.connexion import Connexion
from SCRIPTS.achat import Achats
from SCRIPTS.stock import Stock
from SCRIPTS.clients import Clients
from SCRIPTS.employe import Employes
from SCRIPTS.fournisseurs import Fournisseurs
from SCRIPTS.referentiel import Referentiel
from SCRIPTS.MainWindow import MainWindow
from SCRIPTS.bon import Bon



def main():
    app = QApplication(sys.argv)

    # Crée la fenêtre de connexion


    connexion = Connexion()

    # Si la fenêtre de connexion est acceptée (connexion réussie), crée et affiche la fenêtre principale
    if connexion.exec_() == QDialog.Accepted:
        stacked_widget = QStackedWidget() #objet QstackedWidget



        mainwindow = MainWindow(stacked_widget)
        stacked_widget.addWidget(mainwindow)

        achats_page = Achats(stacked_widget)
        stacked_widget.addWidget(achats_page)

        stock_page = Stock(stacked_widget)
        stacked_widget.addWidget(stock_page)

        clients_page = Clients(stacked_widget)
        stacked_widget.addWidget(clients_page)

        employes_page = Employes(stacked_widget)
        stacked_widget.addWidget(employes_page)

        fournisseurs_page = Fournisseurs(stacked_widget)
        stacked_widget.addWidget(fournisseurs_page)

        referentiel_page = Referentiel(stacked_widget)
        stacked_widget.addWidget(referentiel_page)

        # Connecter la table d'achats de Achats à Referentiel
        referentiel_page.set_achat_interface(achats_page)

        # connecter la table inventaire de MainWindow a Referentiel
        referentiel_page.set_inventaire_interface(mainwindow)

        # récupération des dimensions de l'écran
        screen_geometry = app.desktop().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Définir la taille minimale de la fenêtre en fonction de la taille de l'écran
        min_width = min(800, int(screen_width * 0.70))  # 80% de la largeur de l'écran
        min_height = min(600, int(screen_height * 0.75))  # 80% de la hauteur de l'écran
        stacked_widget.setMinimumSize(min_width, min_height)




        stacked_widget.show()
        sys.exit(app.exec_())

    # Quitte l'application après que la fenêtre principale est fermée
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()





