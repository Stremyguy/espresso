import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("main.ui", self)
        
        self.initUi()
        
    def initUi(self) -> None:
        self.changeButton.clicked.connect(self.add_coffee)
        
        self.conn = sqlite3.connect("coffee.sqlite")
        self.cur = self.conn.cursor()
        
        self.update_info()
    
    def update_info(self) -> None:
        result = self.cur.execute(
            """
            SELECT coffee_information.ID, coffee_information.sort_name,
            roasting.type, ground_grains.type,
            coffee_information.taste_description, coffee_information.price,
            coffee_information.packing_volume
            FROM coffee_information
            JOIN ground_grains ON coffee_information.ground_or_in_grains = ground_grains.ID
            JOIN roasting ON coffee_information.roasting_degree = roasting.ID
            """
        )
        
        table_labels = ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах",
                        "Описание вкуса", "Цена", "Объем упаковки"]
        
        self.coffeeTable.setColumnCount(len(table_labels))
        self.coffeeTable.setRowCount(0)
        
        self.coffeeTable.setHorizontalHeaderLabels(table_labels)
        
        for i, row in enumerate(result):
            self.coffeeTable.setRowCount(self.coffeeTable.rowCount() + 1)
            for j, elem in enumerate(row):
                self.coffeeTable.setItem(i, j, QTableWidgetItem(str(elem)))

        self.coffeeTable.resizeColumnsToContents()

    def add_coffee(self) -> None:
        self.add_coffee_widget = AddCoffeWidget(self)
        self.add_coffee_widget.show()
        

class AddCoffeWidget(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        
        self.initUi()
    
    def initUi(self) -> None:
        self.pushButton.clicked.connect()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_window = MyWidget()
    my_window.show()
    sys.exit(app.exec())
