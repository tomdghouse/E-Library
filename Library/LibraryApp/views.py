from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
import os
import pymysql
from django.core.files.storage import FileSystemStorage
from datetime import date

global username, password, contact, email, address

def SearchBookAction(request):
    if request.method == 'POST':
        query = request.POST.get('t1', False)
        file_type = request.POST.get('t2', False)
        query = query.lower()
        array = query.split(" ")
        output = '<table border=2px solid black align="center" width="100%" bgcolor="#E6E6FA" bordercolor="#8c0209">'
        font = '<font size="" color="black" align="center">'
        arr = ['ID','Name','Author','Description','Book Date','Book Type','Filename','Access Data']
        output += "<tr>"
        dup = []
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM addbook")
            rows = cur.fetchall()
            for row in rows:
                book_id = row[0]
                book_name = row[1]
                author = row[2]
                description = row[3]
                book_date = row[4]
                book_type = row[5]
                filename = row[6]
                books = book_name.lower()
                authorname = str(author).lower()
                descs = description.lower()
                booktype = book_type.lower()
                for k in range(len(array)):
                    if array[k] in books or array[k] in authorname or array[k] in descs or array[k] in booktype: 
                        if (file_type == 'ALL' or book_type == file_type) and filename not in dup:
                            dup.append(filename)
                            output += "<tr><td>"+font+str(book_id)+"</td>"
                            output += "<td>"+font+book_name+"</td>"
                            output += "<td>"+font+str(author)+"</td>"
                            output += "<td>"+font+description+"</td>"
                            output += "<td>"+font+book_date+"</td>"
                            output += "<td>"+font+book_type+"</td>"
                            output += "<td>"+font+filename+"</td>"
                            if book_type == "Video":
                                output+='<td><a href="PlayVideo?t1='+filename+'"><img src=/static/images/video1.png height=50 width=50/></a></td>'
                            elif book_type == "URL":    
                                output+='<td><a href="'+filename+'" target="_blank"><img src=/static/images/url1.png height=50 width=50/></a></td>'
                            else:
                                output+='<td><a href="http://127.0.0.1:8000/static/books/'+filename+'"><img src=/static/images/book.png height=50 width=50/></a></td>'
        context= {'data':output}        
        return render(request, 'SearchResult.html', context)              
        

def SearchBook(request):
    if request.method == 'GET':
       return render(request, 'SearchBook.html', {})

def DeleteFile(request):
    if request.method == 'GET':
        filename = request.GET['t1']
        book_type = request.GET['t2']
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "delete from addbook where file_name = '"+filename+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if book_type != 'URL':
            os.remove("LibraryApp/static/books/"+filename)
        output = filename+' deleted from database'
        context= {'data':output}        
        return render(request, 'AdminScreen.html', context)


def PlayVideo(request):
    if request.method == 'GET':
        video = request.GET['t1']
        output = '<source src="static/books/'+video+'" type="video/mp4">Your browser does not support the video tag.'
        context= {'data':output}        
        return render(request, 'PlayVideo.html', context)


def ViewBooks(request):
    if request.method == 'GET':
        output = '<table border=2px solid black align="center" width="100%" bgcolor="#E6E6FA">'
        font = '<font size="" color="black">'
        arr = ['ID','Name','Author','Description','Book Date','Book Type','Filename','Access Data','Delete File']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM addbook")
            rows = cur.fetchall()
            for row in rows:
                book_id = row[0]
                book_name = row[1]
                author = row[2]
                description = row[3]
                book_date = row[4]
                book_type = row[5]
                filename = row[6]
                output += "<tr><td>"+font+str(book_id)+"</td>"
                output += "<td>"+font+book_name+"</td>"
                output += "<td>"+font+str(author)+"</td>"
                output += "<td>"+font+description+"</td>"
                output += "<td>"+font+book_date+"</td>"
                output += "<td>"+font+book_type+"</td>"
                output += "<td>"+font+filename+"</td>"
                if book_type == "Video":
                    output+='<td><a href="PlayVideo?t1='+filename+'"><img src=/static/images/video1.png height=50 width=50/></a></td>'
                elif book_type == "URL":    
                    output+='<td><a href="'+filename+'" target="_blank"><img src=/static/images/url1.png height=50 width=50/></a></td>'
                else:
                    output+='<td><a href="http://127.0.0.1:8000/static/books/'+filename+'"><img src=/static/images/book.png height=50 width=50/></a></td>'
                output+='<td><a href="DeleteFile?t1='+filename+'&t2='+book_type+'"><img src=/static/images/delete.png height=35 width=35/></a></td>'    
        context= {'data':output}        
        return render(request, 'ViewBooks.html', context)


def ViewBooks1(request):
    if request.method == 'GET':
        output = '<table border=2px solid black align="center" width="80%" cellspacing="1" cellpadding="0" bgcolor="#E6E6FA" bordercolor="#8c0209" border-collapse="collapse">'
        font = '<font size="" color="black">'
        arr = ['ID','Name','Author','Description','Book Date','Book Type','Filename','Access Data']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM addbook")
            rows = cur.fetchall()
            for row in rows:
                book_id = row[0]
                book_name = row[1]
                author = row[2]
                description = row[3]
                book_date = row[4]
                book_type = row[5]
                filename = row[6]
                output += "<tr><td>"+font+str(book_id)+"</td>"
                output += "<td>"+font+book_name+"</td>"
                output += "<td>"+font+str(author)+"</td>"
                output += "<td>"+font+description+"</td>"
                output += "<td>"+font+book_date+"</td>"
                output += "<td>"+font+book_type+"</td>"
                output += "<td>"+font+filename+"</td>"
                if book_type == "Video":
                    output+='<td><a href="PlayVideo?t1='+filename+'"><img src=/static/images/video1.png height=50 width=50/></a></td>'
                elif book_type == "URL":    
                    output+='<td><a href="'+filename+'" target="_blank"><img src=/static/images/url1.png height=50 width=50/></a></td>'
                else:
                    output+='<td><a href="http://127.0.0.1:8000/static/books/'+filename+'"><img src=/static/images/book.png height=50 width=50/></a></td>'
                #output+='<td><a href="DeleteFile?t1='+filename+'">Click Here</a></td>'    
        context= {'data':output}        
        return render(request, 'ViewBooks1.html', context)


def AddUrlAction(request):
    if request.method == 'POST':
        global username
        name= request.POST.get('t1', False)
        url = request.POST.get('t2', False)
        desc = request.POST.get('t3', False)
        today = date.today()
        output = "none"
        count = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select count(*) from addbook")
            rows = cur.fetchall()
            for row in rows:
                count = row[0]
        count = count + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO addbook(book_id,book_name,description,book_date,book_type,file_name) VALUES('"+str(count)+"','"+name+"','"+desc+"','"+str(today)+"','URL','"+url+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':url+' Details saved in Database'}
            return render(request, 'AddBook.html', context)
        else:
            context= {'data':'Error in adding book details'}
            return render(request, 'AddBook.html', context)

def AddUrl(request):
    if request.method == 'GET':
       return render(request, 'AddUrl.html', {})

def AddBook(request):
    if request.method == 'GET':
       return render(request, 'AddBook.html', {})
    
def AddBookAction(request):
    if request.method == 'POST':
        global username, password, contact, email, address
        name = request.POST.get('t1', False)
        author = request.POST.get('t2', False)
        desc = request.POST.get('t3', False)
        book_type = request.POST.get('t5', False)
        book_name = request.FILES['t4'].name
        book_data = request.FILES['t4']
        fs = FileSystemStorage()
        today = date.today()
        output = "none"
        count = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select count(*) from addbook")
            rows = cur.fetchall()
            for row in rows:
                count = row[0]
        count = count + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO addbook(book_id,book_name,author,description,book_date,book_type,file_name) VALUES('"+str(count)+"','"+name+"','"+author+"','"+desc+"','"+str(today)+"','"+book_type+"','"+book_name+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            fs.save('LibraryApp/static/books/'+book_name, book_data)
            context= {'data':book_type+' Details saved in Database'}
            return render(request, 'AddBook.html', context)
        else:
            context= {'data':'Error in adding book details'}
            return render(request, 'AddBook.html', context) 

def UserLogin(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        output = "none"
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    username = row[0]
                    output = "Login success"
                    break
        if output != 'none':
            context= {'data':output}
            return render(request, 'UserScreen.html', context)
        if output == 'none':
            context= {'data':'Invalid username/password'}
            return render(request, 'Login.html', context)


def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})
    
def RegisterAction(request):
    if request.method == 'POST':
        global username, password, contact, email, address
        username = request.POST.get('t1', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        password = request.POST.get('t2', False)
        
        fs = FileSystemStorage()
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,email FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break
                if row[1] == email:
                    output = email+" Email id already exists"
                    break
        if output == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'elibrary',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                context= {'data':'Signup Process Completed'}
                return render(request, 'Register.html', context)
            else:
                context= {'data':'Error in signup process'}
                return render(request, 'Register.html', context)             
        else:
            context= {'data':output}
            return render(request, 'Register.html', context)
    

def AdminLoginAction(request):
    if request.method == 'POST':
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if user == 'admin' and password == 'admin':
            context= {'data':'Welcome '+user}
            return render(request, 'AdminScreen.html', context)
        elif user == 'ghouse' and password == '12345678':
            context= {'data':'Welcome '+user}
            return render(request, 'AdminScreen.html', context)
        elif user == 'abrar' and password == '123456789':
            context= {'data':'Welcome '+user}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid login'}
            return render(request, 'AdminLogin.html', context)
            
        
        
