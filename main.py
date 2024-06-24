import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', passwd='ankit0807@#', database='library')
mycursor = mydb.cursor()

# Create tables (assuming they are not already created)
mycursor.execute("create table if not exists user_details(user_id int(10) unique primary key,\
Name varchar(20) Not Null,\
password varchar(10) unique)")

mycursor.execute("create table if not exists books(Book_id varchar(20) Not Null primary key,\
Book_title varchar(100),\
Author varchar(25),\
Edition int(10),\
Copies int(20))")

mycursor.execute("create table if not exists book_issued(user_id varchar(20) primary key,\
Book_id varchar(20),\
Book_title varchar(100),\
Author varchar(25),\
issue_date date,\
return_date date)")

mycursor.execute("create table if not exists book_return(user_id varchar(20) primary key,\
Book_id varchar(20),\
Book_title varchar(100),\
Author varchar(25),\
issue_date date,\
return_date date)")

def login():
    user_id = int(input("enter your user_id:"))
    name = input("enter the username:")
    passwd = input("enter the password:")
    query = "select * from user_details where user_id=%s"
    mycursor.execute(query, (user_id,))
    record = mycursor.fetchone()
    if record:
        if passwd == record[2]:
            print("LOGIN SUCCESSFUL")
        else:
            print("PASSWORD INCORRECT")
            login()
    else:
        print("user id not found")
        login()

def register():
    user_id = int(input("enter your user_id:"))
    name = input("enter the username:")
    password = input("enter the password:")
    data = (user_id, name, password)
    query = 'insert into user_details(user_id, Name, password) values (%s, %s, %s)'
    mycursor.execute(query, data)
    mydb.commit()
    print('SIGN UP SUCCESSFULLY')

def add_book():
    book_id = input("enter your book_id:")
    book_title = input("enter the book_title:")
    author = input("enter the author name:")
    edition = int(input("enter the edition:"))
    copies = input("enter the number of copies:")
    data = (book_id, book_title, author, edition, copies)
    query = 'insert into books(Book_id, Book_title, Author, Edition, Copies) values (%s, %s, %s, %s, %s)'
    mycursor.execute(query, data)
    mydb.commit()
    print('BOOK SUCCESSFULLY ADDED')

def view_books_list():
    print('BOOKS LIST')
    mycursor.execute('select * from books')
    records = mycursor.fetchall()
    for record in records:
        print(record)

def delete_book():
    book_title = input('enter the book_title:')
    try:
        query = "delete from books where Book_title = %s"
        data = (book_title,)
        mycursor.execute(query, data)
        print(mycursor.rowcount, 'BOOK SUCCESSFULLY DELETED')
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def issue_book():
    user_id = int(input('enter the user_id:'))
    book_id = input('enter the book_id:')
    book_title = input('enter the book_title:')
    issue_date = input('enter the issue date:')
    return_date = input('enter the return date:')
    query = 'insert into book_issued(user_id, book_id, book_title, issue_date, return_date) values (%s, %s, %s, %s, %s)'
    data = (user_id, book_id, book_title, issue_date, return_date)
    mycursor.execute(query, data)
    mydb.commit()
    print("BOOK ISSUED SUCCESSFULLY TO:", user_id)
    update_book_copies(book_id, -1)

def return_book():
    user_id = int(input('enter the user_id:'))
    book_id = input('enter the book_id:')
    book_title = input('enter the book_title:')
    issue_date = input('enter the issue date:')
    return_date = input('enter the return date:')
    query = 'insert into book_return(user_id, book_id, book_title, issue_date, return_date) values (%s, %s, %s, %s, %s)'
    data = (user_id, book_id, book_title, issue_date, return_date)
    mycursor.execute(query, data)
    mydb.commit()
    print("BOOK RETURNED SUCCESSFULLY TO:", user_id)
    update_book_copies(book_id, 1)

def user_details():
    print('USER DETAILS')
    mycursor.execute('select * from user_details')
    records = mycursor.fetchall()
    for record in records:
        print(record)

def update_book_copies(book_id, change):
    query = 'update books set Copies = Copies + %s where Book_id = %s'
    data = (change, book_id)
    mycursor.execute(query, data)
    mydb.commit()
    print('STATUS SUCCESSFULLY UPDATED')

def start():
    print('**********WELCOME TO LIBRARY MANAGEMENT SYSTEM**********')
    print('')
    print('1. SIGN UP')
    print('2. LOGIN')
    print('3. EXIT')
    opt = int(input('enter your choice:'))
    print('')
    if opt == 1:
        print('To Sign up, enter your details')
        register()
    elif opt == 2:
        print('To login, enter your details')
        login()
    elif opt == 3:
        exit()

def data():
    ans = 'y'
    while ans == 'y' or ans == 'Y':
        print('1. Add Book')
        print('2. Return Book')
        print('3. Delete Book')
        print('4. Issue Book')
        print('5. View Books List')
        print('6. User Details')
        opt = int(input('enter your choice:'))
        print('')
        if opt == 1:
            print('To add book, enter the details:')
            add_book()
        elif opt == 2:
            print('To return book, enter the details:')
            return_book()
        elif opt == 3:
            print('To delete book, enter the details:')
            delete_book()
        elif opt == 4:
            print('To issue book, enter the details:')
            issue_book()
        elif opt == 5:
            print('View books list:')
            view_books_list()
        elif opt == 6:
            user_details()
        else:
            print('Enter the correct option')
        ans = input('Do You Want To Continue (Y/N): ').strip().lower()

try:
    start()
    data()
except KeyboardInterrupt:
    print("\nExiting the program.")
finally:
    mydb.close()
