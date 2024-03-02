import csv   #I imported CSV to be able to do the file-based system for storage
from datetime import datetime, timedelta    #I imported datetime and timedelta to be able to use dates and times for transactions

class Book:   #Created the class Book to implement the title, author, ISBN, and quantity of the books in the library
    def __init__(self, title, author, ISBN, quantity):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.quantity = quantity

    def display(self):   #Defined display to print out the outcome of the author, title, etc. requested
        print(f"Title: {self.title}")   #Used f-strings to print out the title, for example of the book
        print(f"Author: {self.author}")
        print(f"ISBN: {self.ISBN}")
        print(f"Quantity: {self.quantity}")

    def update_quantity(self, quantity):   #Defined update quantity to add to the current quantity when adding books
        self.quantity += quantity   #Using the += operator

class Patron:   #Created the class Patron to implement the name, ID, contact; of any patron that gets added to my library system
    def __init__(self, name, patron_ID, contact):
        self.name = name
        self.patron_ID = patron_ID
        self.contact = contact

    def display(self):    #Defined display to print out the outcome of the name,ID, and contact of the patron
        print(f"Name: {self.name}")
        print(f"ID: {self.patron_ID}")
        print(f"Contact: {self.contact}")

class Transaction:   #Created the class Transaction to implement all the transactions that happen when someone takes out a book
    def __init__(self, book, patron):
        self.book = book
        self.patron = patron
        self.checkout_date = None
        self.due_date = None
        self.return_date = None
        self.fine = 0

    def checkout_book(self):   #Defined checkout_book to handle the transactions of someone taking out a book
        if self.book.quantity <= 0:   #If the book quantity is less than 0 using <=, the book can't be taken out
            raise ValueError("This book is currently unavailable.")   #Used Raise Value Error to raise an Error which says the book is unavailable
        else:
            self.checkout_date = datetime.now()   #Used datetime.now() to show the current date and time when checked out
            self.due_date = self.checkout_date + timedelta(days=7)   #I used timedelta(days=7) to specify the due date is 7 days/ 1 week from the checkout date
            self.book.quantity -= 1
            return self.checkout_date, self.due_date

    def return_book(self):   #Created the return_book function for patrons who return books
        self.return_date = datetime.now()
        self.book.quantity += 1   #Added 1 to the total quantity when the book is returned using +=

        if self.return_date is not None and self.due_date is not None and self.return_date > self.due_date:
            days_overdue = (self.return_date - self.due_date).days
            self.fine = days_overdue * 5   #Created a fine function so patrons would have to pay a late fee
            return self.fine
        else:
            return 0

class Librarian:   #I created a Librarian/Employee class for just admin to access and do whatever they need to do
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_credentials(self, input_username, input_password):   #This function checks if the user can sign in or not by inputting the correct information
        return self.username == input_username and self.password == input_password

class Admin:   #This function is for admin sign in
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_credentials(self, input_username, input_password):
        return self.username == input_username and self.password == input_password

class Library:   #I created a Library Class for all library information
    def __init__(self, books_file="books.csv", patrons_file="patrons.csv", transactions_file="transactions.csv"):   #I used CSV files to be able to save the data added
        self.books = []
        self.patrons = []
        self.transactions = []
        self.librarians = []
        self.books_file = books_file
        self.patrons_file = patrons_file
        self.transactions_file = transactions_file

    def add_book(self, book):   #Method to add books to library collection
        self.books.append(book)

    def remove_book(self, book):   #Method to remove books from library collection
        self.books.remove(book)

    def add_patron(self, patron):   #Method to add Patrons to list of Patrons
        self.patrons.append(patron)

    def remove_patron(self, patron):   #Method to remove Patrons from list of Patrons
        self.patrons.remove(patron)

    def search_books(self, title):   #Method to search for any books from the collection of them
        return [book for book in self.books if title.lower() in book.title.lower()]

    def generate_report(self):   #Defined generate_report to print out reports of books, patrons, and transactions for librarians and admins
        print("Library Report:")
        print("Books:")
        for book in self.books:
            book.display()
            print()
        print("Patrons:")
        for patron in self.patrons:
            patron.display()
            print()
        print("Transactions:")
        for transaction in self.transactions:
            if isinstance(transaction, Transaction):  # This will check if the item is a Transaction object
                print(f"Book: {transaction.book.title}, Patron: {transaction.patron.name}, Checkout Date: {transaction.checkout_date.strftime('%Y-%m-%d %H:%M:%S')}, Due Date: {transaction.due_date.strftime('%Y-%m-%d %H:%M:%S')}")
                #This is where I used the new date method I learned
    def handle_transaction(self, book_title, patron_name):   #Method to handle transactions of a patron taking out a book
        book = next((b for b in self.books if b.title.lower() == book_title.lower()), None)   #b is for books and I used .lower() to accept lowercase answers
        patron = next((p for p in self.patrons if p.name.lower() == patron_name.lower()), None)   #p is for patron and I did the same thing with .lower()
        if book and patron:
            transaction = Transaction(book, patron)
            try:
                checkout_date, due_date = transaction.checkout_book()
                self.transactions.append(transaction)
            except ValueError as e:   #Except ValueError turns into e
                print(e)
        else:
            print("Book or patron not found.")
        #This is my error handling where I used Try and Except function
    def return_book(self, book_title, patron_name):
        transaction = next((t for t in self.transactions if   #I used next to retrieve the next item
                            isinstance(t, Transaction) and
                            t.book.title.lower() == book_title.lower() and
                            t.patron.name.lower() == patron_name.lower()), None)
        if transaction:
            fine = transaction.return_book()
            if fine:
                print(f"Fine for overdue book: ${fine}")   #This will print out how much someone will owe when overdue book is returned
            print("Book returned successfully!")
            self.transactions.remove(transaction)
        else:
            print("Transaction not found.")

    def save_data(self):   #Began to make the storage system using CSV file
        try:   #Used Try and Except Blocks to avoid any errors within the following code
            with open(self.books_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Author", "ISBN", "Quantity"])
                for book in self.books:
                    writer.writerow([book.title, book.author, book.ISBN, book.quantity])
        except Exception as e:
            print(f"Error saving books data: {e}")

        try:
            with open(self.patrons_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Patron ID", "Contact"])
                for patron in self.patrons:
                    writer.writerow([patron.name, patron.patron_ID, patron.contact])
        except Exception as e:
            print(f"Error saving patrons data: {e}")

        try:
            with open(self.transactions_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Book Title", "Patron Name", "Checkout Date", "Due Date"])
                for transaction in self.transactions:
                    if isinstance(transaction, Transaction):
                        writer.writerow([transaction.book.title, transaction.patron.name, transaction.checkout_date.strftime('%Y-%m-%d %H:%M:%S'), transaction.due_date.strftime('%Y-%m-%d %H:%M:%S')])
        except Exception as e:
            print(f"Error saving transactions data: {e}")

    def load_data(self):  #Loads any saved data if any
        try:
            with open(self.books_file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    book = Book(row["Title"], row["Author"], row["ISBN"], int(row["Quantity"]))
                    self.books.append(book)
        except FileNotFoundError:
            pass

        try:
            with open(self.patrons_file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    patron = Patron(row["Name"], row["Patron ID"], row["Contact"])
                    self.patrons.append(patron)
        except FileNotFoundError:
            pass

        try:
            with open(self.transactions_file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    book_title = row["Book Title"]
                    patron_name = row["Patron Name"]
                    checkout_date = datetime.strptime(row["Checkout Date"], "%Y-%m-%d %H:%M:%S")
                    due_date = datetime.strptime(row["Due Date"], "%Y-%m-%d %H:%M:%S")
                    book = next((b for b in self.books if b.title == book_title), None)
                    patron = next((p for p in self.patrons if p.name == patron_name), None)
                    if book and patron:
                        transaction = Transaction(book, patron)
                        transaction.checkout_date = checkout_date
                        transaction.due_date = due_date
                        self.transactions.append(transaction)
        except FileNotFoundError:
            pass

    def add_librarian(self, librarian):   #I created a method for admins to hire/add new librarians
        self.librarians.append(librarian)

    def display_librarians(self):   #Admins can see all the librarians that are hired using this
        print("List of Librarians:")
        for librarian in self.librarians:
            print("Username: ", librarian.username)

    def generate_patron_report(self):  #Generates a list of patrons
        print("Patron Report:")
        for patron in self.patrons:
            patron.display()
            print()

    def generate_book_report(self):   #Generate a list of books
        print("Book Report:")
        for book in self.books:
            book.display()
            print()

def display_menu():   #Menu that will be shown to Librarians only once signed in
    print("\nLibrary Management System")  #\n will start a new line
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Add Patron")
    print("4. Remove Patron")
    print("5. Search Books")
    print("6. Check Out Book")
    print("7. Return Book")
    print("8. Generate Report")
    print("9. Save Data")
    print("10. Exit")

def display_admin_menu():   #Menu that will be shown to Admins only once signed in
    print("\nAdmin System")
    print("11. Generate Library Transaction Report")
    print("12. Generate Library Patron Report ")
    print("13. Generate Library Book Report")
    print("14. Save Your Data")
    print("15. Hire Librarians")
    print("16. Fire Librarians")
    print("17. List of Librarians")
    print("18. Sign out.")

def librarian_menu(library, logged_in_librarian):
    display_menu()
    choice = input("Enter your choice: ")   #Allows you to pick the number
    #All the choices Librarians can choose from
    if choice == "1":
        title = input("Enter Book Title: ")   #Adding Books
        author = input("Enter Book Author: ")
        ISBN = input("Enter Book ISBN: ")
        quantity = int(input("Enter Quantity: "))
        book = Book(title, author, ISBN, quantity)
        library.add_book(book)
        print("Book added successfully!")

    elif choice == "2":
        title = input("Enter Book Title to remove: ")   #Removing Books
        books_to_remove = library.search_books(title)
        if books_to_remove:
            for book in books_to_remove:
                library.remove_book(book)
            print("Book removed successfully!")
        else:
            print("Book not found.")

    elif choice == "3":
        name = input("Enter Patron Name: ")   #Adding Patrons
        patron_ID = input("Enter Patron ID: ")
        contact = input("Enter Contact Information: ")
        patron = Patron(name, patron_ID, contact)
        library.add_patron(patron)
        print("Patron added successfully!")

    elif choice == "4":
        name = input("Enter Patron Name to remove: ")   #Removing Patrons
        patrons_to_remove = [patron for patron in library.patrons if patron.name.lower() == name.lower()]
        if patrons_to_remove:
            for patron in patrons_to_remove:
                library.remove_patron(patron)
            print("Patron removed successfully!")
        else:
            print("Patron not found.")

    elif choice == "5":
        query = input("Enter Search Query: ")   #Search for Books in Library Collection
        results = library.search_books(query)
        if results:
            print("Search Results: ")
            for book in results:
                book.display()
        else:
            print("No Books Found.")

    elif choice == "6":
        book_title = input("Enter Book Title to check out: ")   #Check out Books
        patron_name = input("Enter Patron Name: ")
        library.handle_transaction(book_title, patron_name)

    elif choice == "7":
        book_title = input("Enter Book Title to return: ")   #Return Books
        patron_name = input("Enter Patron Name: ")
        library.return_book(book_title, patron_name)

    elif choice == "8":
        library.generate_report()   #Generate Reports of Books, Patrons, and Transactions

    elif choice == "9":
        library.save_data()
        print("Data saved successfully!")   #Saves Data

    elif choice == "10":
        print("Exiting...")   #Sign out of Librarian Menu
        return False

    else:
        print("Invalid choice. Please enter a valid option.")   #Gives the User the chance to put another option

    return True

def admin_menu(library, admin):
    display_admin_menu()
    choice = input("Enter your choice: ")
    #All the choices Admins can pick from in their menu
    if choice == "11":
        library.generate_report()   #Generates a total Library Report similar to #8 in Librarian Menu

    elif choice == "12":
        library.generate_patron_report()   #Generates a Patron Only Report

    elif choice == "13":
        library.generate_book_report()   #Generates a Book Only Report

    elif choice == "14":
        library.save_data()
        print("Data was Saved!")   #Saves Data

    elif choice == "15":
        name = input("Enter Librarian name: ")    #Hire any new Librarians
        password = input("Enter Password: ")
        librarian = Librarian(name, password)
        library.add_librarian(librarian)
        print("Librarian was Hired!")

    elif choice == "16":
        name = input("Enter Librarian Username to fire: ")   #Fire/Remove any Librarians
        librarian_removal = next((lib for lib in library.librarians if lib.username == name), None)
        if librarian_removal:
            library.librarians.remove(librarian_removal)
            print("Librarian has Been Fired.")
        else:
            print("Librarian Not Found.")

    elif choice == "17":
        library.display_librarians()   #List of Current Librarians

    elif choice == "18":
        print("Exiting...")    #Sign Out of Admin
        return False

    else:
        print("Invalid choice. Please enter a valid option.")

    return True


def librarian_login(library):   #Librarian Login
    username = input("Enter your Username: ")
    password = input("Enter your Password: ")

    librarian = next((lib for lib in library.librarians if lib.username == username and lib.password == password), None)
    if librarian:
        return librarian
    else:
        print("Wrong Password or Username.")   #This will show when input is incorrect
        return None

def admin_login():   #Admin Login
    username = input("Enter your Username: ")
    password = input("Enter your Password: ")

    if username == "admin" and password == "admin123":
        return True
    else:
        print("Wrong Password or Username.")
        return False

def main():   #Main Menu
    library = Library()
    library.load_data()

    admin = Admin("admin", "admin123")
    librarian = Librarian("librarian", "librarian456")
    library.add_librarian(librarian)

    while True:   #What You will see when first starting the Program
        print("\nChoose User Type:")
        print("1. Librarian")
        print("2. Administrator")
        print("3. Sign Out.")
        user_type = input("Enter Your Choice: ")

        if user_type == "1":   #This will take you to the Librarian Menu
            logged_in_librarian = librarian_login(library)
            if logged_in_librarian:
                while librarian_menu(library, logged_in_librarian):
                    pass

        elif user_type == "2":   #This will take you to the Admin Menu
            logged_in_admin = admin_login()
            if logged_in_admin:
                while admin_menu(library, admin):
                    pass

        elif user_type == "3":   #This will just sign you out and End the Program
            print("Disconnecting.")
            break

        else:
            print("Invalid Option.")

if __name__ == "__main__":
    main()

#Librarian Login Information:
#Username - librarian
#Password - librarian456

#Admin Login Information:
#Username - admin
#Password - admin123