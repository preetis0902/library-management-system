import json

class Book:
    def __init__(self, book_id, title, author, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity

    def display(self):
        print(f'Book ID:{self.book_id}\nTitle:{self.title}\nAuthor:{self.author}\nQuantity:{self.quantity}')

    def issue_book(self):
        if self.quantity > 0:
            self.quantity -= 1
            print("The book is issued!")
            print(f'The number of books available with ID {self.book_id} now are: {self.quantity}')
            return 1
        else:
            return 0

    def return_book(self):
        self.quantity += 1
        print("Book is returned successfully!")
        print(f'The number of books available with ID {self.book_id} now are: {self.quantity}')

class Library:
    def __init__(self):
        self.books_dict = {}
        self.borrowers_dict = {}

    def save_data(self):
        overall = {}
        books_data = {}

        for book_obj in self.books_dict.values():
            books_data[book_obj.book_id]={"Book ID":book_obj.book_id,"Title":book_obj.title,"Author":book_obj.author,"Quantity":book_obj.quantity}
        overall["books"]=books_data
        overall["borrowers"]= self.borrowers_dict

        with open("library_data.json","w") as f:
            json.dump(overall,f)

    def load_data(self):
        try:
            with open("library_data.json","r") as f:
             data = json.load(f)

             for book_id,book_data in data["books"].items():
                 b_id = int(book_id)
                 book_object=Book(b_id,book_data["Title"],book_data["Author"],book_data["Quantity"])
                 self.books_dict[book_object.book_id] = book_object

             for book_id,members in data["borrowers"].items():
                 b_id = int(book_id)
                 self.borrowers_dict[b_id]=members

        except FileNotFoundError:
             print("File not found")
        except json.JSONDecodeError:
            print("Error: The file contains invalid JSON formatting.")


    def add_book(self,book):
        if book.book_id in self.books_dict:
            print(f'The book ID {book.book_id} already exists in the library')
        else:
            self.books_dict[book.book_id] = book

    def find_book(self, book_id):
        if book_id in self.books_dict:
            return self.books_dict[book_id]
        else:
            return None

    def issue_book(self,book_id,m_id):
        book_obj=self.find_book(book_id)
        if book_obj is None:
            print("Book is not found in library")
        else:
            status = book_obj.issue_book()
            if status == 0:
                print("Book is Out of stock")
            elif book_id in self.borrowers_dict:
                self.borrowers_dict[book_id].append(m_id)
            else:
                self.borrowers_dict[book_id] = [m_id]


    def return_book(self, book_id, m_id):
        book_obj = self.find_book(book_id)
        if book_obj is None:
            print("Book is not found")
        elif book_id in self.borrowers_dict and m_id in self.borrowers_dict[book_id]:
            book_obj.return_book()
            self.borrowers_dict[book_id].remove(m_id)
            if not self.borrowers_dict[book_id]:
                del self.borrowers_dict[book_id]
        else:
            print(f'This member did not borrow the book with ID:{book_id}')

    def display_books(self):
        for book_obj in self.books_dict.values():
            print("*****************************")
            book_obj.display()
            print("*****************************")

    def remove_book(self,book_id):
        if book_id in self.books_dict:
            if book_id in self.borrowers_dict:
                print('Book cannot be removed as its been borrowed')
            else:
                del self.books_dict[book_id]
                print(f"Book with ID {book_id} deleted successfully")
        else:
            print("Book not found")

    def search_book_by_title(self,book_title):
        found=False
        for book_obj in self.books_dict.values():
            if book_title.lower().strip() in book_obj.title.lower():
                found = True
                book_obj.display()
                print("-------------------")
        if not found:
            print("This title is not available")

    def search_book_by_author(self,book_author):
        found=False
        for book_obj in self.books_dict.values():
            if book_author.lower().strip() in book_obj.author.lower():
                found = True
                book_obj.display()
                print("-------------------")
        if not found:
            print("This author is not available")

def main():
    l = Library()
    l.load_data()
    while True:
        print("1.Add book")
        print("2.Display books")
        print("3.Search by title")
        print("4.Search by author")
        print("5.Issue book")
        print("6.Return book")
        print("7.Remove book")
        print("8.Exit")

        try:
            option = int(input("Please choose from above menu:"))
        except ValueError:
            print("Please enter the numbers only")
            continue

        if option == 1:
            print("Please enter the following details to add a book")
            while True:
                try:
                    b_id = int(input("Enter the book ID: "))
                    book_obj = l.find_book(b_id)
                    if  book_obj is not None:
                            print("This book is already available in the Library")
                            continue
                    break
                except ValueError:
                    print("Please enter the numbers only")
            b_title = input("Enter the title: ")
            b_author = input("Enter the author: ")
            while True:
                try:
                    b_quantity = int(input("Enter the quantity:"))
                    if b_quantity <= 0:
                        print("Quantity should be more than 0")
                    else:
                        break
                except ValueError:
                    print("Please enter the numbers only")
            new_book = Book(b_id, b_title, b_author, b_quantity)
            l.add_book(new_book)
            l.save_data()

        elif option == 2:
            print("The books available in the Library are:")
            l.display_books()

        elif option == 3:
            book_title=input("Please enter the title you want to search:")
            l.search_book_by_title(book_title)

        elif option == 4:
            book_author=input("Please enter the Author you want to search:")
            l.search_book_by_author(book_author)

        elif option == 5:
            while True:
                try:
                    b_id=int(input("Please enter the Book ID:"))
                    break
                except ValueError:
                    print("Please enter the numbers only")
            book_obj=l.find_book(b_id)
            if book_obj is None:
                print("This book is not available in the Library")
            elif book_obj.quantity == 0:
                print("This book is currently out of stock")
            else:
                while True:
                    try:
                        m_id = int(input("Please enter the member ID: "))
                        break
                    except ValueError:
                        print("Please enter the numbers only")
                l.issue_book(b_id, m_id)
            l.save_data()

        elif option == 6:
            while True:
                try:
                    b_id = int(input("Please enter the Book ID:"))
                    break
                except ValueError:
                    print("Please enter the numbers only")
            book_obj = l.find_book(b_id)
            if book_obj is None:
                print("This book is not available in the Library")
            else:
                while True:
                    try:
                        m_id = int(input("Please enter the member ID: "))
                        break
                    except ValueError:
                        print("Please enter the numbers only")
                l.return_book(b_id,m_id)
            l.save_data()

        elif option == 7:
            while True:
                try:
                    b_id = int(input("Please enter the Book ID:"))
                    break
                except ValueError:
                    print("Please enter the numbers only")
            l.remove_book(b_id)
            l.save_data()

        elif option == 8:
            break
        else:
            print("Invalid Option.Please choose between 1 and 8")

main()




