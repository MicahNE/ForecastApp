
# Only needed for access to command line arguments
import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtSql import *



class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("main.ui", self)
        self.create_db()
        
    #List items     |     This will need to be SQL
        todos = ["first", "second", "third"]
        for todo in todos:
            item = QListWidgetItem(todo)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.todo_listWidget.addItem(item)
            
        
        
        #Add List Button  
        self.todolistedit_toolButton.clicked.connect(self.addList)
 
        
        
            
    def addList(self):
    
        
        print("pressed")


    #SQLite DB creation
    def create_db(self):
        forecastDB = QSqlDatabase.addDatabase('QSQLITE')
        
        forecastDB.setDatabaseName('Forecastdb')
        
        forecastDB.open()
        
        #Table Creation
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
        
        # createTableQuery.exec(
        #     """
        #     CREATE TABLE Todolist (
        #         todoitemid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        #         listitem VARCHAR(60) NOT NULL              
        #     )
        #     """
        # )
        
        print(forecastDB.tables())

        if not forecastDB.open():
            print("Qt failed to open database")
            return False
        else :
            print("Database Connected")
            return True
        

            

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()











# # You need one (and only one) QApplication instance per application.
# # Pass in sys.argv to allow command line arguments for your app.
# # If you know you won't use command line arguments QApplication([]) works too.
# app = QApplication(sys.argv)

# # Create a Qt widget, which will be our window.
# window = QWidget()
# window.show()  # IMPORTANT!!!!! Windows are hidden by default.
# window.setWindowTitle("Forecast")
# window.setStyleSheet("background: white;")

# grid = QGridLayout()
# smallgrid = QGridLayout()

# #button widget
# button = QPushButton("Add Event")
# button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
# button.setStyleSheet("border-radius: 15px")

# #calendar widget
# calendar = QCalendarWidget()

# #Calendar formatting
# format = QTextCharFormat()
# format.setFont(QFont('Times', 15))


# # date
# date = QDate(2020, 6, 10)
 
# # setting date text format
# calendar.setDateTextFormat(date, format)
# calendar.setVerticalHeaderFormat(0)

# #grid
# grid.addLayout(smallgrid, 0, 0)
# grid.addWidget(calendar,0,1)

# smallgrid.addWidget(button,0,0)


# window.setLayout(grid)
# window.show()
# # Start the event loop.
# sys.exit(app.exec())
