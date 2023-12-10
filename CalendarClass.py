from PyQt5.QtWidgets import QWidget, QDialog  # Import necessary PyQt5 modules
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtSql import *
from datetime import datetime
import AccessControl

# CalendarClass.py



class CalendarClass(QWidget):
    
    
    def __init__(self, main_instance):
        super(CalendarClass, self).__init__()
        self.main_instance = main_instance
        self.connect_signals()
        self.user_id = AccessControl.AccessControl.get_current_user_id()
        print("Current user_id:", self.user_id)
        self.calendarDateChanged()
        
     
        

    def connect_signals(self):
        self.main_instance.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.main_instance.calendarWidget.activated.connect(self.handleDateDoubleClick)
        self.main_instance.deleteEventButton.clicked.connect(self.deleteEvent)

    def calendarDateChanged(self):
        print("The calendar date was changed.")
        dateSelected = self.main_instance.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", dateSelected)
        formattedDate = dateSelected.strftime("%Y-%m-%d")
        self.formattedDeleteDate = dateSelected.strftime("%Y-%m-%d")
        
        # Run query for title and desc info
        titles, infos = self.fetchEventData(formattedDate)

        # Check if there are results (assuming a single result for simplicity)
        if titles and infos:
            title = titles[0]
            info = infos[0]
            

            # Update the quickEventTitle and quickEventDesc
            self.main_instance.quickEventTitle.setText(title)
            self.main_instance.quickEventDesc.setPlainText(info)
        else:
            # Clear the quickEventTitle and quickEventDesc if no results           
            self.main_instance.quickEventTitle.clear()
            self.main_instance.quickEventDesc.clear()
        
    def handleDateDoubleClick(self, dateSelected):
        # Assuming self is an instance of CalendarClass
        
        date_str = dateSelected.toString('MMMM d, yyyy')
        formatted_date = dateSelected.toPyDate().strftime("%Y-%m-%d")

        # Run query for title and desc info
        titles, infos = self.fetchEventData(formatted_date)
          # Set date info in EventPopup
        # Create an instance of EventPopup
        
        if titles and infos:
            # If there is an SQL entry, pass the retrieved information to EventPopup
            title = titles[0]
            info = infos[0]
            event_popup = EventPopup(self, edit_mode = True)  # Create an instance of EventPopup
            event_popup.setDateInfo(dateSelected.toString('MMMM d, yyyy'))
            
            print("titles exist: ", event_popup.edit_mode)
            event_popup.setDateInfo(date_str, title, info)
            
        else:
            # If no SQL entry, just pass the date information to EventPopup
            event_popup = EventPopup(self, edit_mode = False)  # Create an instance of EventPopup
            event_popup.setDateInfo(dateSelected.toString('MMMM d, yyyy'))
            print("titles no exist: ", event_popup.edit_mode)
            event_popup.setDateInfo(date_str)
            
        event_popup.exec_()  # Show the EventPopup
    
    def deleteEvent(self):
        delete_popup = DeletePopup(self.formattedDeleteDate, self)  # Use the stored formattedDeleteDate
        delete_popup.exec_()

           
        
        
    
    def showEventPopup(self):
        # Get the center position of the main window

        # Create an instance of the EventPopup
        event_popup = EventPopup(self.main_instance)
        

        # Show the EventPopup
        event_popup.exec_()
        
    def fetchEventData(self, date):
        
        quickEventTableQuery = QSqlQuery()

        # Prepare the SELECT query
        quickEventTableQuery.prepare(
            """
            SELECT title, info
            FROM Event
            WHERE date = :date AND user_id = :user_id
            """
        )

        # Bind the date and user_id parameters
        quickEventTableQuery.bindValue(":date", date)
        quickEventTableQuery.bindValue(":user_id", AccessControl.AccessControl.get_current_user_id())

        # Execute the query
        quickEventTableQuery.exec()

        # Fetch the results
        titles = []
        infos = []
        while quickEventTableQuery.next():
            title = quickEventTableQuery.value(0)  # Assuming title is the first column
            info = quickEventTableQuery.value(1)   # Assuming info is the second column
            titles.append(title)
            infos.append(info)

        return titles, infos

    

    








    def current_date(self, date):
        # logic for handling the current date based on the date parameter
        pass

    def get_current_date(self):
        # logic for getting and displaying the current date
        pass

    def get_todo_list(self):
        #  logic for getting and displaying the to-do list
        pass
    
class EventPopup(QDialog):
    def __init__(self, parent=None, edit_mode=False):
        super(EventPopup, self).__init__(parent)
        loadUi("eventpopup.ui", self)

        self.edit_mode = edit_mode
        print("Popup Editmode: ", self.edit_mode)
        # Connect the button box signals to slots
        if self.edit_mode is True:
            self.dateAddEventDateButton.accepted.connect(self.editData)
        else:
            self.dateAddEventDateButton.accepted.connect(self.saveData)
        self.dateAddEventDateButton.rejected.connect(self.cancel)
    
    def editData(self):
         # This method is called when the "Save" button is clicked
        title_text = self.dateAddEventTitleInfo.text()
        desc_text = self.dateAddEventDescInfo.toPlainText()
        date_text = self.dateAddEventDateInfo.text()
        print("here", title_text)
        # Convert date_text to a datetime object. For the front end
        date_object = datetime.strptime(date_text, "%B %d, %Y")

        # Format the datetime object as a string in the desired format. For the SQL server
        formatted_date = date_object.strftime("%Y-%m-%d")
        
        
        enterEventTableQuery = QSqlQuery()
        date_text = self.dateAddEventDateInfo.text()

        
        enterEventTableQuery.prepare(
            """
            UPDATE Event
            SET title = :title, info = :info
            WHERE date = :date AND user_id = :user_id
            """
        )
        enterEventTableQuery.bindValue(":title", title_text)
        enterEventTableQuery.bindValue(":info", desc_text)
        enterEventTableQuery.bindValue(":date", formatted_date)
        enterEventTableQuery.bindValue(":user_id", AccessControl.AccessControl.get_current_user_id())
        print("add text:", date_text)
        
        if enterEventTableQuery.exec_():
            print("Data saved successfully")
            # Close the dialog
            self.accept()
        else:
            print("Error saving data:", enterEventTableQuery.lastError().text())

        
        # Display the text in the console (replace this with your database logic)
        print("Title:", title_text)
        print("Description:", desc_text)

        # Update quick info when saving new event
        CalendarClass.calendarDateChanged(self.parent())
        
        # Close the dialog
        self.accept()

    def saveData(self):
        # This method is called when the "Save" button is clicked
        title_text = self.dateAddEventTitleInfo.text()
        desc_text = self.dateAddEventDescInfo.toPlainText()
        date_text = self.dateAddEventDateInfo.text()
        
        # Convert date_text to a datetime object. For the front end
        date_object = datetime.strptime(date_text, "%B %d, %Y")

        # Format the datetime object as a string in the desired format. For the SQL server
        formatted_date = date_object.strftime("%Y-%m-%d")
        
        
        enterEventTableQuery = QSqlQuery()
        date_text = self.dateAddEventDateInfo.text()

        
        enterEventTableQuery.prepare(
            """
            INSERT INTO Event (title, info, date, user_id)
            VALUES (:title, :info, :date, :user_id)
            """
        )
        enterEventTableQuery.bindValue(":title", title_text)
        enterEventTableQuery.bindValue(":info", desc_text)
        enterEventTableQuery.bindValue(":date", formatted_date)
        enterEventTableQuery.bindValue(":user_id", AccessControl.AccessControl.get_current_user_id())
        
        print("add text:", date_text)
        
        if enterEventTableQuery.exec_():
            print("Data saved successfully")
            # Close the dialog
            self.accept()
        else:
            print("Error saving data:", enterEventTableQuery.lastError().text())

        
        # Display the text in the console (replace this with your database logic)
        print("Title:", title_text)
        print("Description:", desc_text)

        # Update quick info when saving new event
        CalendarClass.calendarDateChanged(self.parent())
        
        # Close the dialog
        self.accept()

    def cancel(self):
        # This method is called when the "Cancel" button is clicked
        # Close the dialog without saving
        self.reject()

    def setDateInfo(self, date_info, title_info="", desc_info=""):
        self.dateAddEventDateInfo.setText(date_info)
        self.dateAddEventTitleInfo.setText(title_info)
        self.dateAddEventDescInfo.setPlainText(desc_info)
        
        

    def showEventPopup(self, date_info, title_info="", desc_info=""):
        self.setDateInfo(date_info, title_info, desc_info)
        result = self.exec_()  # or use self.show() if you don't need a modal dialog

            
class DeletePopup(QDialog):
    def __init__(self, formatted_date, parent=None):
        super(DeletePopup, self).__init__(parent)
        loadUi("deleteevent.ui", self)
        self.formatted_date = formatted_date  # Store the formatted_date

        # Connect the button box signals to slots
        self.deleteEventButtons.accepted.connect(self.deleteData)
        self.deleteEventButtons.rejected.connect(self.reject)

    def deleteData(self):
        if self.formatted_date:
            deleteEventTableQuery = QSqlQuery()

            deleteEventTableQuery.prepare(
                """
                DELETE FROM Event
                WHERE date = :date AND user_id = :user_id
                """
            )

            deleteEventTableQuery.bindValue(":date", self.formatted_date)
            deleteEventTableQuery.bindValue(":user_id", AccessControl.AccessControl.get_current_user_id())
            deleteEventTableQuery.exec()
            print("Deleted:", self.formatted_date)

            # Update quick info when saving new event
            CalendarClass.calendarDateChanged(self.parent())
            self.accept()
        else:
            print("No date selected to delete.")
            self.reject()
            
# Example usage:
# if __name__ == "__main__":
#     calendar_instance = CalendarClass()

#     # Example calls for the methods
#     calendar_instance.current_date("2023-11-13")
#     calendar_instance.get_current_date()
#     calendar_instance.get_todo_list()
