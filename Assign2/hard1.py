class Book:
    def __init__(self,book_id,title,author):
        self.book_id=book_id
        self.title= title
        self.author=author
        self.available=True
        
    def display_line(self):
        status={
            True:"Available",
            False:"Borrowed"
        }
      
   
        print(self.book_id,self.title,self.author,status[self.available])
       

class Library:
    def __init__(self):

        self.bookList=[]
        self.count=0  
  
    def add_book(self,title,author):
        self.count+=1
        book=Book(self.count,title,author)
        self.bookList.append(book)

    def find_book(self,book_id):
        for book in self.bookList:
            if book.book_id==book_id:
                return book
            
        return None
        
    def borrow_book(self,book_id):
        book=self.find_book(book_id)

        if book is None:
            print("Book is not available")

        elif not book.available:
            print("Already borrowed")
        else:
            book.available=False
            print("You borrowed:",book_id)

       
    def return_book(self,book_id):
        book=self.find_book(book_id)

        if book is None:
            print("Book is not available")
        elif book.available:
            print("Book is already in library")
        else:
            book.available = True


    def display_inventory(self):
        if len(self.bookList) ==0:
            print("No book avialable")

        else:
            for book in self.bookList:
                book.display_line()


lib=Library()

print("""---Library Management----
1. Add book
2.Borrow Book
3. Return Book
4. Dispaly inventory
5.Exit""")

while True:
    try:
        choice=(int(input("Enter your choice: ")))
 
        if choice == 1:
            title=input("Enter the title of book: ")
            author=input("Enter the name of author: ")

            lib.add_book(title,author)


        elif choice==2:
            bookId=int(input("Enter the book id to borrow: "))
            lib.borrow_book(bookId)
            

        elif choice==3:
            bookId=int(input("Enter the book id you want to return"))
            lib.return_book(bookId)

            
        elif choice==4:
            lib.display_inventory()

        elif choice==5:
            break

        else:
            print("Invalid option---")
            
    except ValueError:
        print("Please enter corect value")


