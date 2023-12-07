# Only needed for access to command line arguments
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import CalendarClass
import AccessControl


class Main(QMainWindow):
    def __init__(self):
        
        super(Main, self).__init__()
        self.create_db()

        # Instantiate AccessControl inside Main
        self.access_control = AccessControl.LoginDialog()

        self.show_login_dialog()
        if not self.is_authenticated:
            sys.exit()
        
        loadUi("main.ui", self)
        self.listItems()
        

        # Set the background color for the main window
        # self.setStyleSheet("background-color: lightgrey;")
        
        
        #date selection on calendar
        self.calendar_handler = CalendarClass.CalendarClass(self)
        
        
        
        # Add List Button
        self.addTaskButton.clicked.connect(self.addList)

    def show_login_dialog(self):
        login_dialog = AccessControl.LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            print("User logged in successfully!")
            self.is_authenticated = True
        else:
            print("User canceled login. Exiting...")
            self.is_authenticated = False    

    # Add other methods here


       
    # SQLite DB creation
    def create_db(self):
        forecastDB = QSqlDatabase.addDatabase('QSQLITE')

        forecastDB.setDatabaseName('Forecastdb')

        
        if not forecastDB.open():
            print("Qt failed to open database")
            return False
        else:
            print("Database Connected")

        # # Table Creation
        # createTableQuery = QSqlQuery()

        
        # createTableQuery.exec(
        #     """
        #     CREATE TABLE IF NOT EXISTS User (
        #         user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         username TEXT UNIQUE NOT NULL,
        #         hashed_password TEXT NOT NULL,
        #         salt TEXT NOT NULL
        #     );

        #     CREATE TABLE IF NOT EXISTS Event (
        #         event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         title TEXT NOT NULL,
        #         info TEXT NOT NULL,
        #         date VARCHAR(10) NOT NULL,
        #         user_id INTEGER,
        #         FOREIGN KEY (user_id) REFERENCES User(user_id)
        #     );
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
        # self.todo_listWidget.setStyleSheet("background-color: lightpink; border: 1px solid pink;")

    # Event for add button pressed, Needs to add "list" entry to MySQL TodoList table
    def addList(self):
        print("pressed")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()
