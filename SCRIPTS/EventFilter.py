from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QColor

class EventFilter(QObject):
    def __init__(self, parent, tableWidget):
        super(EventFilter, self).__init__(parent)
        self.parent = parent
        self.tableWidget = tableWidget

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.KeyPress, QEvent.MouseButtonPress):
            self.deselectionner_ligne()
        return super(EventFilter, self).eventFilter(obj, event)

    def deselectionner_ligne(self):
        # Désélectionner la ligne dans le QTableWidget
        self.tableWidget.clearSelection()

        # Réinitialiser la couleur de fond de toutes les lignes à leur couleur par défaut (blanc)
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    item.setBackground(QColor("white"))
