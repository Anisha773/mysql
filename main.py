import mysql.connector
mydb = mysql.connector.connect(host='localhost', user='root', passwd='ankit0807@#', database='library')
mycursor = mydb.cursor()

# table user_details
mycursor.execute("create table user_detail(user_id int(10) unique primary key,\
Name varchar(20) Not Null,\
password varchar(10) unique)")

# table books
mycursor.execute("create table book(Book_id varchar(20) Not Null primary key,\
Book_title varchar(20),\
Author varchar(10),\
Edition int(10),\
Copies int(20))")

# table  issued books
mycursor.execute("create table book_issued(user_id varchar(20) primary key,\
Book_id varchar(20),\
Book_title varchar(20),\
Author varchar(10),\
issue_date date,\
return_date date)")

# table return books
mycursor.execute("create table book_return(user_id varchar(20) primary key,\
Book_id varchar(20),\
Book_title varchar(20),\
Author varchar(10),\
issue_date date,\
return_date date)")


def login():
    user_id=int(input("enter your user_id:"))
    name=input("enter the username:")
    passwd=input("enter the password:")
    query="select from user_details"
    mycursor.execute(query)
    records=mycursor.fetchall()
    flag=0
    for i in records:
        if i[0]==user_id:
            password=i[2]
            flag=1
            if passwd==password:
                print("LOGIN SUCCESSFUL")
            else:
                print("PASSWORD INCORRECT")
                login()
    
    if flag==0:
        print("user id not found")
        login()
    print('')

def register():
    user_id=int(input("enter your user_id:"))
    name=input("enter the username:")
    password=input("enter the password:")
    data=(user_id,name,password)
    query='insert into user_details(user_id,name,password)values(%s,%s,%s)'
    mycursor.execute(query,data)
    mydb.commit()
    print('SIGN UP SUCCESSFULLY')

def add_book():
    book_id=input("enter your book_id:")
    book_title=input("enter the book_title:")
    author=input("enter the author name:")
    edition=int(input("enter the edition:"))
    copies=input("enter the number of copies:")
    data=(book_id,book_title,author,edition,copies)
    query='insert into books(book_id,book_title,author,edition,copies)values(%s,%s,%s,%s,%s)'
    mycursor.execute(query,data)
    mydb.commit()
    print('BOOK SUCCESSFULLY ADDED')

def view_books_list():
    print('BOOKS LIST')
    mycursor.execute('select*from books')
    record=mycursor.fetchall()
    for i in record:
        print(i)

def delete_book():
    nm=input('enter the book_title:')
    try:
        a="delete fromm books where book_title=%s"
        data=(nm,)
        mycursor.execute(a,data)
        print(mycursor.rowcount,'BOOK SUCCESSFULLY DELETED')
        mydb.commit()
    except: 
        mydb.commit()
        print('enter the coorrect book_title')
    mydb.close()

def update_book_copies(book_id,u):
    a='select copies from books where book_is=%s'
    data=(book_id,)
    mycursor.execute(a,data)
    record=mycursor.fetchone()
    t=record[0]+u
    query='update books set copies=%s where book_id=%s'
    d=(t,book_id)
    mycursor.execute(query,d)
    mydb.commit()
    print('STATUS SUCCESSFULLY UPDATED')

def issue_book():
    user_id=int(input('enter the user_id:'))
    book_id=input('enter the book_id:')
    book_title=input('enter the book_title:')
    issue_date=input('enter the issue date:')
    return_date=input('enter the return date:')
    query='insert into book_issued(user_id,book_id,book_title,issue_date,return date) values(%s,%s,%s,%s,%s)'
    data=(user_id,book_id,book_title,issue_date,return_date)
    mycursor.execute(query,data)
    mydb.commit()
    print("BOOK ISSUED SUCCESSFULLY TO:",user_id)
    update_book_copies(book_id,1)

def return_book():
    user_id=int(input('enter the user_id:'))
    book_id=input('enter the book_id:')
    book_title=input('enter the book_title:')
    issue_date=input('enter the issue date:')
    return_date=input('enter the return date:')
    query='insert into book_issued(user_id,book_id,book_title,issue_date,return date) values(%s,%s,%s,%s,%s)'
    data=(user_id,book_id,book_title,issue_date,return_date)
    mycursor.execute(query,data)
    mydb.commit()
    print("BOOK RETURNED SUCCESSFULLY TO:",user_id)
    update_book_copies(book_id,1)

def user_details():
    print('EMPLOYEE DETAILS')
    mycursor.execute('select*from user_details')
    record=mycursor.fetchall()
    for i in record:
        print(i)

print('**********WELCOME  TO  LIBRARY MANAGEMENT SYSTEM**********')
print('')

def start():
    print('1.SIGN UP')
    print('2.LOGIN')
    print('3.EXIT')
    opt=int(input('enter your choice:'))
    print('')
    if opt==1:
        print('To Sign up, enter your details')
        register()
    elif opt==2:
        print('To login,enter your details')
        login()
    elif opt==3:
        exit()
def data():
    ans='y'
    while ans=='y' or ans=='Y':
        print('1.Add_Book')
        print('2.Return_Book')
        print('3.Delete_Book')
        print('4.issue_Book')
        print('5.view_books_list')
        print('6.User details')
        opt=int(input('enter your choice:'))
        print('')
        if opt==1:
            print('To add_book, enter the details :')
            add_book()
        elif opt==2:
            print('To return book, enter the details :')
            return_book()
        elif opt==3:
            print('To delete book, enter the details :')
            delete_book()
        elif opt==4:
            print('To issue book, enter the details :')
            issue_book()
        elif opt==5:
            print('view books list :')
            view_books_list()
        elif opt==6:
            user_details()

        else:
            print('enter the correct option')
            data()
        ans=input('Do You Want To Continue(Y/N):')

start()
data()