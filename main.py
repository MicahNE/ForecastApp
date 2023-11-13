# Only needed for access to command line arguments
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("main.ui", self)
        self.create_db()
        self.listItems()

        # Set the background color for the main window
        self.setStyleSheet("background-color: lightgrey;")

        # Add List Button
        self.todolistedit_toolButton.clicked.connect(self.addList)

        # Populating and printing the list information. Needs to be linked to MySQL
        # ...

    # Add other methods here

    # SQLite DB creation
    def create_db(self):
        forecastDB = QSqlDatabase.addDatabase('QSQLITE')

        forecastDB.setDatabaseName('Forecastdb')

        forecastDB.open()

        # Table Creation
        createTableQuery = QSqlQuery()

        createTableQuery.exec(
            """
            CREATE TABLE Calendar (
                calendarid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                date VARCHAR(40) NOT NULL,
                FOREIGN KEY(date) REFERENCES Event(start)
            )
            """
        )
        createTableQuery.exec(
            """
            CREATE TABLE Event (
                eventid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                title VARCHAR(40) NOT NULL,
                info VARCHAR(150),
                start VARCHAR(9) NOT NULL,
                end VARCHAR(9) NOT NULL
            )
            """
        )

        # CreateTableQuery.exec(
        #     """
        #     CREATE TABLE Todolist (
        #         todoitemid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        #         listitem VARCHAR(60) NOT NULL
        #     )
        #     """
        # )

        # This is debug code
        print(forecastDB.tables())

        if not forecastDB.open():
            print("Qt failed to open database")
            return False
        else:
            print("Database Connected")
            return True

    def listItems(self):
        todos = ["first", "second", "third"]
        for todo in todos:
            item = QListWidgetItem(todo)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.todo_listWidget.addItem(item)

        # Set the background color and border for the todo_listWidget
        self.todo_listWidget.setStyleSheet("background-color: lightpink; border: 1px solid pink;")

    # Event for add button pressed, Needs to add "list" entry to MySQL TodoList table
    def addList(self):
        print("pressed")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()
