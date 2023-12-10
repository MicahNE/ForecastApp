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
        
        
        loadUi("main.ui", self)
        self.listItems()
        self.todo_listWidget.itemChanged.connect(self.handleItemChanged)
        
        
        # Set the background color for the main window
        # self.setStyleSheet("background-color: lightgrey;")
        
        
        #date selection on calendar
        self.calendar_handler = CalendarClass.CalendarClass(self)
        
        
        
        # Add List Button
        self.addTaskButton.clicked.connect(self.addList)
        self.deleteListItem.clicked.connect(self.deleteSelectedItem)
    
    def deleteSelectedItem(self):
        selected_items = self.todo_listWidget.selectedItems()

        if not selected_items:
            return  # No item selected, do nothing

        for item in selected_items:
            todo_id = item.data(QtCore.Qt.UserRole)

            # Delete the item from the database
            delete_query = QSqlQuery()
            delete_query.prepare("DELETE FROM Todo WHERE todo_id = :todo_id AND user_id = :user_id")
            delete_query.bindValue(":todo_id", todo_id)
            delete_query.bindValue(":user_id", AccessControl.AccessControl.get_current_user_id())

            if not delete_query.exec_():
                print("Error deleting todo item:", delete_query.lastError().text())
                return  # Abort if there's an error

            # Delete the item from the widget
            self.todo_listWidget.takeItem(self.todo_listWidget.row(item))    
    
    def show_login_dialog(self):
        login_dialog = AccessControl.LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            print("User logged in successfully!")
            self.is_authenticated = True
        

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
        self.todo_listWidget.clear()
        
        listQuery = QSqlQuery()

        # Prepare the SELECT query
        listQuery.prepare(
            """
            SELECT todo_id, todo_text, is_completed FROM Todo WHERE user_id = :user_id
            """
        )

        # Bind the date and user_id parameters
        listQuery.bindValue(":user_id", AccessControl.AccessControl.get_current_user_id())

        # Execute the query
        listQuery.exec()
        
        while listQuery.next():
            todo_id = listQuery.value(0)
            todo_text = listQuery.value(1)
            is_completed = listQuery.value(2)
            
            item = QListWidgetItem(todo_text)
            
            # Set flags for user checkability
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            
            # Set the initial check state based on the value from the database
            item.setCheckState(QtCore.Qt.Checked if is_completed else QtCore.Qt.Unchecked)
            
            # Attach the todo_id to the item so that we can use it later
            item.setData(QtCore.Qt.UserRole, todo_id)
            
            self.todo_listWidget.addItem(item)

    def handleItemChanged(self, item):
        # Retrieve the todo_id associated with the item
        todo_id = item.data(QtCore.Qt.UserRole)

        # Update the completion status in the database
        is_completed = item.checkState() == QtCore.Qt.Checked
        update_query = QSqlQuery()
        update_query.prepare(
            """
            UPDATE Todo SET is_completed = :is_completed 
            WHERE todo_id = :todo_id AND user_id = :user_id
            
            """
            )
        
        update_query.bindValue(":is_completed", 1 if is_completed else 0)
        update_query.bindValue(":todo_id", todo_id)
        update_query.bindValue(":user_id", AccessControl.AccessControl.get_current_user_id())
        
        if not update_query.exec_():
            print("Error updating completion status:", update_query.lastError().text())


        # Set the background color and border for the todo_listWidget
        # self.todo_listWidget.setStyleSheet("background-color: lightpink; border: 1px solid pink;")

    # Event for add button pressed, Needs to add "list" entry to MySQL TodoList table
    def addList(self):
        add_dialog = AddTodoDialog(self)
        result = add_dialog.exec_()
        self.listItems()
        if result == QDialog.Accepted:
            todo_texts = add_dialog.getTodoTexts()
            for todo_text in todo_texts:
                self.addItem(todo_text)
                
class AddTodoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("addlistitem.ui", self)
        self.setWindowTitle("Add Todo Items")
        # Connect button signals
        self.addListItemButtonBox.button(QDialogButtonBox.Save).clicked.connect(self.saveTodoItems)
        self.addListItemButtonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        
    
    
    def saveTodoItems(self):
        # Retrieve the entered todo items
        todo_text = self.listItemsInputPlainTextEdit.toPlainText()

        # Split the entered text into individual todo items
        todo_items = [item.strip() for item in todo_text.split('\n') if item.strip()]

        # Save each todo item to the database
        for todo_item in todo_items:
            self.saveTodoItem(todo_item)

        # Manually close the dialog after saving
        self.close()

    def saveTodoItem(self, todo_item):
        # Perform the SQL query to save the todo item to the database
        insert_query = QSqlQuery()
        insert_query.prepare("INSERT INTO Todo (todo_text, user_id) VALUES (:todo_text, :user_id)")
        insert_query.bindValue(":todo_text", todo_item)
        insert_query.bindValue(":user_id", AccessControl.AccessControl.get_current_user_id())

        if not insert_query.exec_():
            print("Error adding todo item:", insert_query.lastError().text())
    
    def getTodoTexts(self):
        text = self.plainTextEdit.toPlainText()
        return [item.strip() for item in text.split('\n') if item.strip()]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()
