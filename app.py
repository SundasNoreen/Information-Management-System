# Student Information Management System.

# Importing Necessary Modules
from flask import Flask, escape, request, render_template, redirect, url_for,session
from mysql.connector import Error
import mysql.connector
from flask_mail import Mail,Message
from functools import wraps
import gc

app = Flask(__name__)

# Creating Database Connection.
connection = mysql.connector.connect(host='localhost',database='ims', user='root',password='')
cursor = connection.cursor()
app.secret_key = 'sundas'
# Standard Flask config API for Flask MAil.
app.config['MAIL_SERVER'] = 'smtp.gmail.com'          # Standard.
app.config['MAIL_PORT'] = 465                         # Standard.
app.config['MAIL_USERNAME'] = ""  # Account used for Sending Mails.
app.config['MAIL_PASSWORD'] = ""         # Password for the Google Account.
app.config['MAIl_USE_TLS'] = False                        # Standard.
app.config['MAIL_USE_SSL'] = True                         # Standard.

mail=Mail(app)

# Home Page i.e., Welcome to IMS Page.
@app.route('/')
def welcome():
    return render_template('Welcome_IMS.html')

###################################################### ADMIN PORTAL ####################################################

# Login for Admins. It will Fetch the Login Credentials from the database Table and move the user to the next page if credentialas are correct.
@app.route('/admin/login',methods=['GET','POST'])
def login_1():
    sql = "SELECT * FROM `admins`"
    cursor.execute(sql)
    read = cursor.fetchall()
    error = None
    if request.method == 'POST':
        for row in read:
            if request.form['username'] != row[0] or request.form['password'] != row[3]:
                error = 'Invalid Credentials. Please try again.'
            else:
                session['logged in'] = True
                session['user_id'] = row[0]
                session['name']= row[1]
                return redirect(url_for('adminfirstpage'))
    return render_template('AdminPortal (LogIn Page).html',error=error)

# This Function is created so that No user can Enter without Login.
def login_required1(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login1'))
    return decorated_function

# It will clear the existing Sessions.
@app.route('/logout')
@login_required1
def logout():
    session.clear()
    gc.collect()
    return render_template('Welcome_IMS.html')

# Welcome Page for Admin
@app.route('/welcome/admin')
@login_required1
def adminfirstpage():
    user=session.get('name')
    return render_template('AdminPortal (Welcome).html',user=user)


##### Student Panel in Admin Portal, Here Student Details can be Viewed and Modified ####

# View All Students, Enter the Name of Class of which Students need to be displayed.
@app.route('/admin/view/students',methods=['GET','POST'])
@login_required1
def view_students_class():
    sql="SELECT * FROM `classes`"
    cursor.execute(sql)
    record = cursor.fetchall()
    count = cursor.rowcount
    sql = "SELECT * FROM `students_personal`"
    cursor.execute(sql)
    read = cursor.fetchall()
    error = None
    if request.method == 'POST':
        for row in read:
            if request.form['id'] != row[0]:
                error = 'This class doesnot exist or is empty.'
            else:
                session['class'] = row[0]
                return redirect(url_for('view_students_list'))
    return render_template('AdminPortal (View Students).html',error=error,record=record,count=count)

# View list of Students.
@app.route('/admin/view/students/{{classname}}')
@login_required1
def view_students_list():
    try:
        classname=session.get('class')
        sql = "SELECT * FROM `students_personal` WHERE `class`=%s "
        cursor.execute(sql,(classname,))
        record=cursor.fetchall()
        count=cursor.rowcount
        return render_template('AdminPortal (View Students Session Wise).html', record=record, count=count, Department=classname)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (View Students Session Wise).html')

# Adding New Students to the Record.
@app.route('/admin/add/students',methods=['GET','POST'])
@login_required1
def add_students():
    try:
        if request.method == 'POST':
            class1=request.form['class']
            name = request.form['name']
            reg = request.form['reg']
            father = request.form['fath']
            gender = request.form['gen']
            cnic = request.form['cnic']
            user = request.form['id']
            area = request.form['dis']
            address = request.form['add']
            dob = request.form['dob']
            email = request.form['email']
            contact = request.form['contact']
            userid=request.form['id']
            pin = request.form['pin']
            ish = request.form['hos']
            dues = request.form['dues']
            rem = request.form['rem']
            # Adding Data to Student Profile.
            sql = "INSERT INTO `students_personal`(`Class`, `Name`, `Registration_Number`, `Father_Name`, `Date_of_Birth`, `Gender`, `District`, `Address`, `Phone`, `CNIC`, `Email ID`, `Is-host`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(class1,name,reg,father,dob,gender,area,address,contact,cnic,email,ish)
            cursor.execute(sql,val)
            connection.commit()
            # Adding Data to Emails Table.
            sql="INSERT INTO `student-emails`(`Registration_Number`, `Email`,`Class`) VALUES (%s,%s,%s)"
            val=(reg,email,class1)
            cursor.execute(sql, val)
            connection.commit()
            # Adding Data to Dues Section.
            sql = "INSERT INTO `students-dues`(`Class`,`Registration_Number`, `Name`, `Amount Paid till Now`, `Dues_Left`, `Total Amout Paid`) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (class1,reg, name, dues, rem, dues)
            cursor.execute(sql, val)
            connection.commit()
            # Adding Data to Subjects.
            sql="INSERT INTO `subjects`( `Class`,`Registration_Number`,`Name`, `1`,  `2`,  `3`,  `4`,  `5`, `6`, `7`,  `8`,  `9`,  `10`, `11`,  `12`,  `13`,  `14`,  `15`, `16`, `17`,  `18`,  `19`,  `20`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (class1,reg,name,'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0')
            cursor.execute(sql, val)
            connection.commit()
            # Add Data to Student Logins.
            sql="INSERT INTO `student-lgins`(`Class`,`User_ID`, `Password`, `Reg`) VALUES (%s,%s,%s,%s)"
            val=(class1,userid,pin,reg)
            cursor.execute(sql, val)
            connection.commit()
            add='Student Added Successfully.'
            return render_template('AdminPortal (Add Students).html', add=add)
    except Error as e:
        print("Error writing data from MySQL table", e)
        return render_template('AdminPortal (Add Students).html', add='This Student Already Exists.')
    return render_template('AdminPortal (Add Students).html')

# Removing Students.
@app.route('/admin/remove/students',methods=['GET','POST'])
@login_required1
def remove_students():
    try:
        if request.method == 'POST':
            user = request.form['id']
            useridis=request.form['user']
            cursor = connection.cursor()
            sql = ("DELETE FROM `students_personal` WHERE  Registration_Number = %s")
            cursor.execute(sql,(user,))
            connection.commit()
            sql = ("DELETE FROM `students-dues` WHERE  Registration_Number = %s")
            cursor.execute(sql, (user,))
            connection.commit()
            sql = ("DELETE FROM `subjects` WHERE  Registration_Number = %s")
            cursor.execute(sql, (user,))
            connection.commit()
            sql = ("DELETE FROM `student-emails` WHERE  Registration_Number = %s")
            cursor.execute(sql, (user,))
            connection.commit()
            sql = ("DELETE FROM `student-lgins` WHERE  User_ID = %s")
            cursor.execute(sql, (useridis,))
            connection.commit()
            add='Removed Successfully!!'
            return render_template('AdminPortal (Remove Students).html', add=add)
    except mysql.connector.Error as error:
        print("Failed to delete record from table: {}".format(error))
        return render_template('AdminPortal (Remove Students Section Wise).html', add='Failed to Delete, Try Again.')
    return render_template('AdminPortal (Remove Students).html')

# Add a New Class
@app.route('/admin/add_class',methods=['GET','POST'])
@login_required1
def add_class():
    try:
        if request.method == 'POST':
            name = request.form['id']
            sql = ("INSERT INTO `classes` VALUES (%s)")
            cursor.execute(sql,(name,))
            connection.commit()
            add='Class Created Successfully!!'
            return render_template('AdminPortal (Add Class).html', add=add)
    except mysql.connector.Error as error:
        print("Failed to delete record from table: {}".format(error))
        return render_template('AdminPortal (Add Class).html', add='Failed to Add, Try Again with a different Name.')
    return render_template('AdminPortal (Add Class).html')

# Delete an existing Class.
@app.route('/admin/delete_class',methods=['GET','POST'])
@login_required1
def del_class():
    try:
        if request.method == 'POST':
            user = request.form['id']
            sql = ("DELETE FROM `classes` WHERE  name = %s")
            cursor.execute(sql,(user,))
            connection.commit()
            sql = ("DELETE FROM `students_personal` WHERE  Class = %s")
            cursor.execute(sql, (user,))
            connection.commit()
            sql = ("DELETE FROM `students-dues` WHERE  Class = %s")
            cursor.execute(sql, (user,))
            connection.commit()
            sql = ("DELETE FROM `subjects` WHERE  Class = %s")
            cursor.execute(sql, (user,))
            connection.commit()
            sql = ("DELETE FROM `student-emails` WHERE  Class = %s")
            cursor.execute(sql, (user,))
            connection.commit()
            sql = ("DELETE FROM `student-lgins` WHERE  Class = %s")
            cursor.execute(sql, (user,))
            connection.commit()
            add='Class and its contents Deleted Successfully!!'
            return render_template('AdminPortal (Remove Class).html', add=add)
    except mysql.connector.Error as error:
        print("Failed to delete record from table: {}".format(error))
        return render_template('AdminPortal (Remove Class).html', add='Failed to Delete, Try Again.')
    return render_template('AdminPortal (Remove Class).html')

# View Dues Details. Here it will ask for the Respective Class of which dues Details need to be viewed.
@app.route('/admin/view/dues_details',methods=['GET','POST'])
@login_required1
def view_students_dues():
    sql = "SELECT * FROM `classes`"
    cursor.execute(sql)
    read = cursor.fetchall()
    count = cursor.rowcount
    sql = "SELECT * FROM `students-dues`"
    cursor.execute(sql)
    record = cursor.fetchall()
    error = None
    if request.method == 'POST':
        for row in record:
            if request.form['id'] != row[0] :
                error = 'Invalid Credentials. Please try again.'
            else:
                session['class'] = row[0]
                return redirect(url_for('view_details_dues'))
    return render_template('AdminPortal (ViewDues).html',error=error,read=read,count=count)

# It will Display names of all Students with Dues Details.
@app.route('/admin/view_dues/{{name}}')
@login_required1
def view_details_dues():
    name = session.get('class')
    try:
        sql = "SELECT * FROM `students-dues`WHERE `class`=%s"
        cursor.execute(sql,(name,))
        record=cursor.fetchall()
        count=cursor.rowcount
        return render_template('AdminPortal (View Dues).html', record=record, count=count,name=name)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (View Dues).html', name='name')

# Here new Dues can be added.
@app.route('/admin/update_dues/add',methods=['GET','POST'])
@login_required1
def add_dues():
    name = session.get('class')
    try:
        if request.method == 'POST':
            new = request.form['new']
            remarks=request.form['remarks']
            dues = request.form['total']
            reg = request.form['reg']
            rem=request.form['name']
            cursor=connection.cursor()
            sql="UPDATE `students-dues` SET `Dues_Left`=%s ,`Remarks`=%s WHERE `Dues_Left`=%s"
            val=(new,remarks,'0')
            cursor.execute(sql,val)
            connection.commit()
            sql = "UPDATE `students-dues` SET `Dues_Left`=%s, `Remarks`=%s WHERE `Registration_Number`=%s"
            val = (dues,rem,reg)
            cursor.execute(sql, val)
            connection.commit()
            count='Students Record updated Successfully!!'
            return render_template('AdminPortal (Add Dues).html', count=count, name=name)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (Add Dues).html', name=name)

# Here Dues Record can be updated.
@app.route('/admin/update_dues/update',methods=['GET','POST'])
@login_required1
def update_all_dues():
    name=session.get('class')
    try:
        if request.method == 'POST':
            remarks = request.form['name']
            sql = "SELECT * FROM `students-dues`"
            cursor = connection.cursor()
            cursor.execute(sql)
            record = cursor.fetchall()
            for row in record:
                a=row[4]
                b=row[3]
            dues=a+b
            sql="UPDATE `students-dues` SET `Amount Paid till Now`=%s ,`Dues_Left`=%s ,`Remarks`=%s, `Total Amout Paid`=%s WHERE `Is Paid?`= %s"
            val=(dues,'0',remarks,dues,'yes')
            cursor.execute(sql,val)
            connection.commit()
            count='Students Record updated Successfully!!'
            sql="UPDATE `students-dues` SET `Is Paid?`= %s WHERE `Dues_Left`= %s"
            val=('','0')
            cursor.execute(sql, val)
            connection.commit()
            return render_template('AdminPortal (Update Dues).html', count=count, name=name)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (Update Dues).html', name=name)

# Here Logins can be viewed.
@app.route('/admin/view_students_logins',methods=['GET','POST'])
@login_required1
def login_students():
    sql = "SELECT * FROM `student-lgins` "
    cursor.execute(sql)
    record=cursor.fetchall()
    count=cursor.rowcount
    return render_template('AdminPortal (St-Logins).html', record=record,count=count)

# Here Admin can add available subjects for Students.
@app.route('/admin/available_subjects',methods=['GET','POST'])
@login_required1
def reg_sub ():
    if request.method == 'POST':
        sess=request.form['session']
        sem=request.form['sem']
        sub1 = request.form['Course1']
        ins1 = request.form['ins1']
        sub2 = request.form['Course2']
        ins2 = request.form['ins2']
        sub3 = request.form['Course3']
        ins3 = request.form['ins3']
        sub4 = request.form['Course4']
        ins4 = request.form['ins4']
        sub5 = request.form['Course5']
        ins5 = request.form['ins5']
        sub6 = request.form['Course6']
        ins6 = request.form['ins6']
        sub7 = request.form['Course7']
        ins7 = request.form['ins7']
        sub8 = request.form['Course8']
        ins8 = request.form['ins8']
        sub9 = request.form['Course9']
        ins9 = request.form['ins9']
        sub10 = request.form['Course10']
        ins10 = request.form['ins10']
        # Add Data to Registered Subjects.
        sql = "INSERT INTO `available`(`Class`, `Semester`, `1`, `I1`, `2`, `I2`, `3`, `I3`, `4`, `I4`, `5`, `I5`, `6`, `I6`, `7`, `I7`, `8`, `I8`, `9`, `I9`, `10`, `I10`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (sess,sem,sub1,ins1,sub2,ins2,sub3,ins3,sub4,ins4,sub5,ins5,sub6,ins6,sub7,ins7,sub8,ins8,sub9,ins9,sub10,ins10)
        cursor.execute(sql, val)
        connection.commit()
        sql= "UPDATE `subjects` SET `1`=%s,`2`=%s,`3`=%s,`4`=%s,`5`=%s,`6`=%s,`7`=%s,`8`=%s,`9`=%s,`10`=%s,`11`=%s,`12`=%s,`13`=%s,`14`=%s,`15`=%s,`16`=%s,`17`=%s,`18`=%s,`19`=%s,`20`=%s WHERE `Class`=%s"
        val=(sub1,'0',sub2,'0',sub3,'0',sub4,'0',sub5,'0',sub6,'0',sub7,'0',sub8,'0',sub9,'0',sub10,'0',)
        add='Subjects Added Successfully !!'
        return render_template('AdminPortal (Available Subjects).html', add=add)
    return render_template('AdminPortal (Available Subjects).html')

# Notifications for Students
@app.route('/admin/notify/students')
@login_required1
def notify_students():
    try:
        sql = "SELECT * FROM `notify_students` ORDER BY `Date` DESC limit 10"
        cursor.execute(sql)
        record=cursor.fetchall()
        count=cursor.rowcount
        return render_template('AdminPortal (Notify Students).html', record=record)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (Notify Students).html')

# Add New Notifications on Portal.
@app.route('/admin/add_student_notifications',methods=['GET','POST'])
@login_required1
def add_st_not():
    try:
        if request.method == 'POST':
            heading = request.form['id']
            message = request.form['name']
            sql = "INSERT INTO `notify_students`(`Heading`, `Message`) VALUES (%s,%s)"
            cursor = connection.cursor()
            val = (heading,message)
            cursor.execute(sql, val)
            connection.commit()
            add = 'Notification Added Successfully.'
            return render_template('AdminPortal (Add Student Notifications).html', add=add)
    except Error as e:
        print("Error writing data from MySQL table", e)
    return render_template('AdminPortal (Add Student Notifications).html')

# Send Notifications in Emails
@app.route('/admin/mail_student_notifications',methods=['GET','POST'])
@login_required1
def mail_st_not():
    try:
        if request.method == 'POST':
            subject = request.form['id']
            mesg = request.form['name']
            sql= "SELECT `Email` FROM `student-emails`"
            cursor.execute(sql)
            email=cursor.fetchall()
            for x in range (0,len(email),1):
                y=email[x]
                l=y[0]
                message = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[l])
                message.body = mesg
                mail.send(message)
            add = 'Email Sent Successfully !!'
            return render_template('AdminPortal (Mail Student Notifications).html', add=add)
    except Error as e:
        print("Error writing data from MySQL table", e)
    return render_template('AdminPortal (Mail Student Notifications).html')

#######################################################################################################################

##### Teacher Panel in Admin Portal, Here Teacher Details can be Viewed and Modified ####

# Teachers Details can be viewed here.
@app.route('/admin/view_teachers')
@login_required1
def teachers():
    try:
        sql = "SELECT * FROM `teachers`"
        cursor.execute(sql)
        record=cursor.fetchall()
        count=cursor.rowcount
        return render_template('AdminPortal (View Teachers).html', record=record, count=count)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (View Teachers).html')

# New Teachers can be Added Here.
@app.route('/admin/add_teachers',methods=['GET','POST'])
@login_required1
def add_teachers():
    try:
        if request.method=='POST':
            id=request.form['id']
            name=request.form['name']
            fname=request.form['fname']
            cnic=request.form['nic']
            email=request.form['email']
            grade = request.form['grade']
            qual=request.form['qual']
            num=request.form['num']
            address= request.form['address']
            joining = request.form['join']
            password = request.form['pass']
            year = request.form['year']
            cursor = connection.cursor()
            sql = "INSERT INTO `teachers`(`User_ID`, `Full_Name`, `Father/Husband Name`, `CNIC`, `Email`, `Grade`, `Qualification`, `Contact`, `Address`, `JoiningDate`, `password`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (id,name,fname,cnic,email,grade,qual,num,address,joining,password)
            cursor.execute(sql, val)
            connection.commit()
            sql="INSERT INTO `salary`(`User_ID`, `Full_Name`, `Teacher's Grade`, `Salary Details for the Year`) VALUES (%s,%s,%s,%s)"
            val = (id, name, grade, year)
            cursor.execute(sql, val)
            connection.commit()
            sql="INSERT INTO `courses`(`User_ID`, `Full_Name`, `Course1`, `Session1`, `Course2`, `Session2`, `Course3`, `Session3`, `Course4`, `Session4`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(id,name,'0','0','0','0','0','0','0','0')
            cursor.execute(sql,val)
            connection.commit()
            add = 'Teacher Added Successfully !!'
            return render_template('AdminPortal (Add Teachers).html', add=add)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (Add Teachers).html')

# Here Teachers can be Removed.
@app.route('/admin/remove_teachers',methods=['GET','POST'])
@login_required1
def remove_teachers():
    if request.method=='POST':
        rem = request.form['user']
        query = "DELETE FROM `teachers` WHERE `User_ID`=%s"
        value = (rem,)
        cursor.execute(query, value)
        connection.commit()
        query = "DELETE FROM `salary` WHERE `User_ID`=%s"
        value = (rem,)
        cursor.execute(query, value)
        connection.commit()
        query = "DELETE FROM `courses` WHERE `User_ID`=%s"
        value = (rem,)
        cursor.execute(query, value)
        connection.commit()
        remove = 'Teacher Removed Successfully !!'
        return render_template('AdminPortal (Remove Teachers).html', remove=remove)
    return render_template('AdminPortal (Remove Teachers).html')

# Classes Record can be viewed from here.
@app.route('/admin/view_teachers_courses',methods=['GET','POST'])
@login_required1
def class_record():
    try:
        sql = "SELECT * FROM `courses`"
        cursor.execute(sql)
        record=cursor.fetchall()
        count=cursor.rowcount
        return render_template('AdminPortal (View Courses).html', record=record, count=count)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (View Courses).html')

# Classes Record can be updated from here.
@app.route('/admin/update_teachers_courses',methods=['GET','POST'])
@login_required1
def up():
    if request.method =='POST':
        a=request.form['id']
        b=request.form['1']
        c = request.form['2']
        d = request.form['3']
        e = request.form['4']
        f = request.form['5']
        g = request.form['6']
        h = request.form['7']
        i = request.form['8']
        sql="UPDATE `courses` SET `Course1`=%s,`Session1`=%s,`Course2`=%s,`Session2`=%s,`Course3`=%s,`Session3`=%s,`Course4`=%s,`Session4`=%s WHERE `User_ID`=%s"
        val=(b,c,d,e,f,g,h,i,a)
        cursor.execute(sql, val)
        connection.commit()
        add = 'Record Updated Successfully !!'
        return render_template('AdminPortal (Update Teachers).html', add=add)
    return render_template('AdminPortal (Update Teachers).html')

#  Salary Details can be viewed here.
@app.route('/admin/view_salary_details')
@login_required1
def view_salary():
    try:
        sql = "SELECT * FROM `salary`"
        cursor.execute(sql)
        record=cursor.fetchall()
        count=cursor.rowcount
        return render_template('AdminPortal (Salary Record).html', record=record, count=count)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (Salary Record).html')

# Selecting the Month for Salary Updates.
@app.route('/admin/update_salary_details')
@login_required1
def record_salary():
    return render_template('AdminPortal (Update Salary).html')

# One by One Months
@app.route('/admin/update_salary_details/january',methods=['GET','POST'])
@login_required1
def record_jan():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        sql=("UPDATE `salary` SET `1`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='January', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/february',methods=['GET','POST'])
@login_required1
def record_feb():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        sql=("UPDATE `salary` SET `2`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='February', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/march',methods=['GET','POST'])
@login_required1
def record_march():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `3`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='March', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/april',methods=['GET','POST'])
@login_required1
def record_april():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `April`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='April', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/may',methods=['GET','POST'])
@login_required1
def record_may():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `May`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='May', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/june',methods=['GET','POST'])
@login_required1
def record_june():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `June`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='June', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/july',methods=['GET','POST'])
@login_required1
def record_july():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `July`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='July', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/august',methods=['GET','POST'])
@login_required1
def record_august():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `August`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='August', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/september',methods=['GET','POST'])
@login_required1
def record_sep():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `September`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='September', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/october',methods=['GET','POST'])
@login_required1
def record_oct():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `October`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='October', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/november',methods=['GET','POST'])
@login_required1
def record_nov():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `November`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='November', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

@app.route('/admin/update_salary_details/december',methods=['GET','POST'])
@login_required1
def record_dec():
    if request.method=='POST':
        grade=request.form['grade']
        amount=request.form['amount']
        cursor=connection.cursor()
        sql=("UPDATE `salary` SET `December`=%s WHERE `Teacher's Grade`=%s")
        value=(amount,grade)
        cursor.execute(sql,value)
        connection.commit()
        add="Salary Successfully updated."
        return render_template('AdminPortal (Monthly Salary).html', name='December', add=add)
    return render_template('AdminPortal (Monthly Salary).html')

# Notifications for Teachers.
@app.route('/admin/notify_teachers')
@login_required1
def notify_taechers():
    try:
        sql = "SELECT * FROM `notify_teachers` ORDER BY `date` DESC limit 10"
        cursor.execute(sql)
        record=cursor.fetchall()
        count=cursor.rowcount
        return render_template('AdminPortal (Notify Teachers).html', record=record)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (Notify Teachers).html')

# Adding New Notifications for Teachers.
@app.route('/admin/add_teacher_notifications',methods=['GET','POST'])
@login_required1
def add_teacher_not():
    try:
        if request.method == 'POST':
            heading = request.form['id']
            message = request.form['name']
            sql = "INSERT INTO `notify_teachers`(`Heading`, `Message`) VALUES (%s,%s)"
            cursor = connection.cursor()
            val = (heading,message)
            cursor.execute(sql, val)
            connection.commit()
            add = 'Notification Added Successfully.'
            return render_template('AdminPortal (Add Teacher Notifications).html', add=add)
    except Error as e:
        print("Error writing data from MySQL table", e)
    return render_template('AdminPortal (Add Teacher Notifications).html')

# Send Notifications in Emails.
@app.route('/admin/mail_teacher_notifications',methods=['GET','POST'])
@login_required1
def mail_teacher_not():
    try:
        if request.method == 'POST':
            subject = request.form['id']
            mesg = request.form['name']
            sql="SELECT `Email` FROM `teachers` WHERE 1"
            cursor.execute(sql)
            email=cursor.fetchall()
            for x in range (0,len(email),1):
                y=email[x]
                l=y[0]
                message = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[l])
                message.body = mesg
                mail.send(message)
            add = 'Email Sent Successfully !!'
            return render_template('AdminPortal (Mail Teacher Notifications).html ', add=add)
    except Error as e:
        print("Error writing data from MySQL table", e)
    return render_template('AdminPortal (Mail Teacher Notifications).html')

# Here Logins can be viewed.
@app.route('/admin/view_teachers_logins',methods=['GET','POST'])
@login_required1
def login_teachers():
    sql = "SELECT `Full_Name`,`User_ID`,`password` FROM `teachers` "
    cursor.execute(sql)
    record=cursor.fetchall()
    count=cursor.rowcount
    return render_template('AdminPortal (Tea-Logins).html', record=record,count=count)
########################################################################################################################

##### Admin Settings can be Changed from here. ####

# Other Admins can be viewed from here.
@app.route ('/admin/view_administrators')
@login_required1
def view_admins():
    sql = "SELECT * FROM `admin_details`"
    cursor = connection.cursor()
    cursor.execute(sql)
    record = cursor.fetchall()
    count = cursor.rowcount
    return render_template('AdminPortal (View Admins.html', record=record, count=count)

# New admins can be added from here.
@app.route ('/admin/view_admins/add_admins',methods=['GET','POST'])
@login_required1
def add_admins():
    if request.method == 'POST':
        user = request.form['id']
        name = request.form['name']
        pws = request.form['pws']
        phone=request.form['phone']
        cursor = connection.cursor()
        sql = "INSERT INTO `admins`(`Name`, `UserID`, `Phone`, `Password`) VALUES (%s,%s,%s,%s)"
        val = (name,user ,phone,pws)
        cursor.execute(sql, val)
        connection.commit()
        cursor = connection.cursor()
        sql = "INSERT INTO `admin_details`(`Name`, `Phone`, `UserID`) VALUES (%s,%s,%s)"
        val = (name,phone,user)
        cursor.execute(sql, val)
        connection.commit()
        add = 'Admin Added Successfully.'
        return render_template('AdminPortal (Add Admins).html', add=add)
    return render_template('AdminPortal (Add Admins).html')

# Admins can be removed from here.
@app.route('/admin/view_admins/remove_admins',methods=['GET','POST'])
@login_required1
def remove_admins():
    if request.method == 'POST':
        user = request.form['id']
        cursor = connection.cursor()
        sql = ("DELETE FROM `admins` WHERE  `UserID` = %s")
        cursor.execute(sql, (user,))
        connection.commit()
        sql = ("DELETE FROM `admin_details` WHERE  `UserID` = %s")
        cursor.execute(sql, (user,))
        connection.commit()
        add = 'Removed Successfully!!'
        return render_template('AdminPortal (Remove Admins).html', add=add)
    return render_template('AdminPortal (Remove Admins).html')

# General Settings, Here Admin can change his Password.
@app.route('/admin/password_reset', methods=['GET','POST'])
@login_required1
def reset():
    try:
        user_id=session.get('user_id')
        if request.method == 'POST':
            id = request.form['id']
            old = request.form['old']
            new = request.form['new']
            sql = "UPDATE `admins` SET `Password`=%s WHERE `Password`=%s and `UserID`=%s"
            val = (new,old,user_id)
            cursor.execute(sql, val)
            connection.commit()
            count = 'Password Updated Successfully!!'
            return render_template('AdminPortal (Change Pws).html' ,count=count)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (Change Pws).html')

# Teachers Passwords can be changed from here.
@app.route('/admins/change_pws/teachers',methods=['GET','POST'])
@login_required1
def change_pws_teachers():
    try:
        if request.method == 'POST':
            id = request.form['id']
            old = request.form['old']
            new = request.form['new']
            cursor = connection.cursor()
            sql = "UPDATE `teachers` SET `password`=%s WHERE `User_ID`=%s and `password`=%s "
            val = (new,id,old)
            cursor.execute(sql, val)
            connection.commit()
            count = 'Password Updated Successfully!!'
            return render_template('AdminPortal (Change Teachers Pws).html', count=count)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (Change Teachers Pws).html')

# Here Admin can Change Student Passwords.
@app.route('/admins/change_pws/students',methods=['GET','POST'])
@login_required1
def change_pws_2017():
    try:
        if request.method == 'POST':
            id = request.form['id']
            old = request.form['old']
            new = request.form['new']
            cursor = connection.cursor()
            sql = "UPDATE `student-lgins` SET `Password`=%s WHERE `User_ID`=%s and `Password`=%s "
            val = (new,id,old)
            cursor.execute(sql, val)
            connection.commit()
            count = 'Password Updated Successfully!!'
            return render_template('AdminPortal (Student Pws).html', count=count)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('AdminPortal (Student Pws).html')

################################################ Admin Portal Ended ##################################################


################################################ Student Portal ######################################################

# Login for Students.
@app.route('/student/login',methods=['GET','POST'])
def login():
    sql = "SELECT * FROM `student-lgins`"
    cursor.execute(sql)
    read = cursor.fetchall()
    error = None
    if request.method == 'POST':
        for row in read:
            if request.form['username'] != row[1] or request.form['password'] != row[2]:
                error = 'Invalid Credentials. Please try again.'
            else:
                session['logged in'] = True
                session['class'] = row[0]
                session['id'] = row[1]
                session['reg'] = row[3]
                return redirect(url_for('my_profile'))
    return render_template('StudentPortal (LoginPage).html')

# So that No user can enter without login.
def login_required2(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function

@app.route('/logout')
@login_required2
def logout_st():
    session.clear()
    gc.collect()
    return render_template('Welcome_IMS.html')

# Students can View their profile here.
@app.route('/student/profile', methods=['GET'])
@login_required2
def my_profile():
    id=session.get('id')
    reg=session.get('reg')
    try:
        sql_select_query =("SELECT * FROM `students_personal` WHERE Registration_Number=%s")
        cursor.execute(sql_select_query,(reg,))
        record = cursor.fetchall()
        for row in record:
            a=row[0]
            b=row[1]
            c=row[2]
            d= row[3]
            e=row[4]
            f =row[5]
            g =row[6]
            h = row[7]
            i = row[8]
            j = row[9]
            k = row[10]
            l = row[11]
        sql_select_query = ("SELECT * FROM `student-lgins` WHERE Reg=%s")
        cursor.execute(sql_select_query, (reg,))
        record = cursor.fetchall()
        for row in record:
            m = row[1]
            n = row[2]
        return render_template('StudentPortal (Student Profile).html', a=a, b=b, c=c, d=d, e=e, f=f, g=g, h=h, i=i, j=j, k=k, l=l, m=m, n=n)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('StudentPortal (Student Profile).html')

# Students can View Notifications here.
@app.route('/student/notifications')
@login_required2
def notifications_students():
    try:
        sql = "SELECT * FROM `notify_students` ORDER BY `Date` DESC limit 10"
        cursor.execute(sql)
        record=cursor.fetchall()
        count=cursor.rowcount
        return render_template('StudentPortal (Notifications).html', record=record)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('StudentPortal (Notifications).html')

# Students can view their Dues Record here.
@app.route('/student/dues_record',methods=['GET','POST'])
@login_required2
def dues():
    reg = session.get('reg')
    sql_select_query = ("SELECT * FROM `students-dues` WHERE `Registration_Number` =%s")
    cursor.execute(sql_select_query, (reg,))
    record = cursor.fetchall()
    for row in record:
        a = row[0]
        b = row[1]
        c = row[2]
        d = row[3]
        e = row[4]
        f = row[5]
        g = row[6]
        h = row[7]
        print(a, b, c, d, e, f,g, h)
        return render_template('StudentPortal (Dues).html', a=a, b=b, c=c, d=d, e=e, f=f,g=g,h=h)
    return render_template('StudentPortal (Dues).html')

# Students can update their Status of Dues here.
@app.route('/student/dues_record/update_status',methods=['GET','POST'])
@login_required2
def update_status():
    reg=session.get('reg')
    if request.method == 'POST':
        yes=request.form['yes']
        sql = "UPDATE `students-dues` SET `Is Paid?`= %s WHERE `Registration_Number`= %s"
        val = ('yes', reg)
        cursor.execute(sql,val)
        connection.commit()
        add='Your Status is Updated Successfully !!'
        return render_template('StudentPortal (Update Dues Status).html',add=add)

    return render_template('StudentPortal (Update Dues Status).html')

# Students can view their Registered Subjects here.
@app.route('/student/available_subjects',methods=['GET','POST'])
@login_required2
def view_subjects():
    year = session.get('class')
    sql = "SELECT * FROM `available` WHERE `Class`= %s"
    cursor.execute(sql,(year,))
    record = cursor.fetchall()
    return render_template('StudentPortal (Subjects).html',record=record)

@app.route('/student/register_subjects',methods=['GET','POST'])
@login_required2
def reg_subjects():

    if request.method =='POST':
        reg = session.get('reg')
        print(reg)
        sess = request.form['session']
        sem = request.form['sem']
        sub1 = request.form['Course1']
        sub2 = request.form['Course2']
        sub3 = request.form['Course3']
        sub4 = request.form['Course4']
        sub5 = request.form['Course5']
        sub6 = request.form['Course6']
        sub7 = request.form['Course7']
        sub8 = request.form['Course8']
        sub9 = request.form['Course9']
        sub10 = request.form['Course10']
        sql = "UPDATE `subjects` SET `1`=%s,`3`=%s,`5`=%s,`7`=%s,`9`=%s,`11`=%s,`13`=%s,`15`=%s,`17`=%s,`19`=%s,`2`=%s,`4`=%s,`6`=%s,`8`=%s,`10`=%s,`12`=%s,`14`=%s,`16`=%s,`18`=%s,`20`=%s WHERE `Registration_Number`=%s "
        val = (sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8,sub9,sub10,'0','0','0','0','0','0','0','0','0','0',reg)
        cursor.execute(sql, val)
        connection.commit()
        count = 'Subjects Updated Successfully!!'
        return render_template('StudentPortal (reg).html', count=count)
    return render_template('StudentPortal (reg).html')


# Students can view their Grades or Marks here.
@app.route('/student/results',methods=['GET','POST'])
@login_required2
def view_res():
    reg = session.get('reg')
    sql = "SELECT * FROM `subjects` WHERE `Registration_Number`= %s"
    cursor.execute(sql,(reg,))
    record = cursor.fetchall()
    for row in record:
        a = row[0]
        b = row[1]
        c = row[2]
        d = row[3]
        e = row[4]
        f = row[5]
        g = row[6]
        h = row[7]
        i = row[8]
        j = row[9]
        k = row[10]
        l = row[11]
        m = row[12]
        n = row[13]
        o = row[14]
        p = row[15]
        q = row[16]
        r = row[17]
        s = row[18]
        t = row[19]
        u = row[20]
        v = row[21]
        w = row[22]

        return render_template('StudentPortal (Result).html',a=a,b=b,c=c,d=d,e=e,f=f,g=g,h=h,i=i,j=j,k=k,l=l,m=m,n=n,o=o,p=p,r=r,s=s,t=t,u=u,v=v,w=w)
    return render_template('StudentPortal (Result).html')


################################################ Student Portal Ended ##################################################


################################################ Teacher Portal ######################################################

# Login for Teachers.
@app.route('/teacher/login',methods=['GET','POST'])
def login_teach():
    sql = "SELECT * FROM `teachers`"
    cursor.execute(sql)
    read = cursor.fetchall()
    error = None
    if request.method == 'POST':
        for row in read:
            if request.form['username'] != row[0] or request.form['password'] != row[10]:
                error = 'Invalid Credentials. Please try again.'
            else:
                session['logged in'] = True
                session['use_id'] = row[0]
                session['name']=row[1]
                return redirect(url_for('teacher_profile'))
    return render_template('Teacher_Login.html')

# So that No user can enter without login.
def login_required3(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login_teach'))
    return decorated_function

@app.route('/logout')
@login_required3
def logout_te():
    session.clear()
    gc.collect()
    return render_template('Welcome_IMS.html')

# Teachers can View their profile here.
@app.route('/teacher/profile', methods=['GET'])
@login_required3
def teacher_profile():
    teacher_id=session.get('use_id')
    print(teacher_id)
    sql_select_query =("SELECT * FROM `teachers` WHERE User_ID=%s")
    cursor.execute(sql_select_query,(teacher_id,))
    record = cursor.fetchall()
    for row in record:
            a=row[0]
            b=row[1]
            c=row[2]
            d= row[3]
            e=row[4]
            f =row[5]
            g =row[6]
            h = row[7]
            i = row[8]
            j = row[9]
            k= row [10]
            return render_template('TeacherPortal (Teacher Profile).html', a=a, b=b, c=c, d=d, e=e,f=f,g=g,h=h,i=i,j=j,k=k)
    return render_template('TeacherPortal (Teacher Profile).html')

# Teacher can view Salary Details here.
@app.route('/teacher/salary_details')
def sal_det():
    teacher_id = session.get('use_id')
    sql = ("SELECT * FROM `salary` WHERE User_ID=%s")
    cursor.execute(sql,(teacher_id,))
    record=cursor.fetchall()
    return render_template('TeacherPortal (Salary).html',record=record)

# Teachers can View Notifications here.
@app.route('/teacher/notifications')
def notifications_teachers():
    try:
        sql = "SELECT * FROM `notify_teachers` ORDER BY `Date` DESC limit 10"
        cursor.execute(sql)
        record=cursor.fetchall()
        count=cursor.rowcount
        return render_template('TeacherPortal (Notifications).html', record=record)
    except Error as e:
        print("Error reading data from MySQL table", e)
    return render_template('TeacherPortal (Notifications).html')

# Teacher can view respective Classes here.
@app.route('/teacher/view_students')
def call_st():
    teacher_id = session.get('use_id')
    sql ="SELECT `User_ID`, `Full_Name`,`Course1`, `Session1`, `Course2`, `Session2`, `Course3`, `Session3`, `Course4`, `Session4` FROM `courses` WHERE  `User_ID`=%s"
    val=(teacher_id,)
    cursor.execute(sql,val)
    record=cursor.fetchall()
    for row in record:
            a=row[0]
            b=row[1]
            c=row[2]
            d= row[3]
            e=row[4]
            f =row[5]
            g =row[6]
            h = row[7]
            i = row[8]
            j = row[9]
            session['course1']=row[2]
            session['i1']=row[3]
            session['course2'] = row[4]
            session['i2'] = row[5]
            session['course3'] = row[6]
            session['i3'] = row[7]
            session['course4'] = row[8]
            session['i4'] = row[9]
            return render_template('TeacherPortal (ViewStudents).html', a=a, b=b, c=c, d=d, e=e,f=f,g=g,h=h,i=i,j=j)
    return render_template('TeacherPortal (ViewStudents).html')

# Teachers can view List of all Students in their Classes.
@app.route('/teacher/list-of-students')
def gos():
    course1=session.get('course1')
    ins1=session.get('i1')
    course2 = session.get('course2')
    ins2 = session.get('i2')
    course3 = session.get('course3')
    ins3 = session.get('i3')
    course4 = session.get('course4')
    ins4 = session.get('i4')
    sql="SELECT `Registration_Number`, `Name` FROM `subjects` WHERE `Class`=%s"
    cursor.execute(sql,(ins1,))
    record1 = cursor.fetchall()
    count1 = cursor.rowcount
    sql = "SELECT `Registration_Number`, `Name` FROM `subjects` WHERE `Class`=%s"
    cursor.execute(sql, (ins2,))
    record2 = cursor.fetchall()
    count2 = cursor.rowcount
    sql = "SELECT `Registration_Number`, `Name` FROM `subjects` WHERE `Class`=%s"
    cursor.execute(sql, (ins3,))
    record3 = cursor.fetchall()
    count3 = cursor.rowcount
    sql = "SELECT `Registration_Number`, `Name` FROM `subjects` WHERE `Class`=%s"
    cursor.execute(sql, (ins4,))
    record4 = cursor.fetchall()
    count4 = cursor.rowcount
    return render_template('TeacherPortal (List).html',count1=count1, record1=record1,count2=count2, record2=record2,count3=count3, record3=record3,count4=count4, record4=record4,course1=course1,course2=course2,course3=course3,course4=course4,ins1=ins1,ins2=ins2,ins3=ins3,ins4=ins4)

# Teachers can mark Grades of Students here.
@app.route('/teacher/grade-of-students/class1',methods=['GET','POST'])
def los1():
    course1 = session.get('course1')
    ins1 = session.get('i1')
    sql = "SELECT `Registration_Number`, `Name` FROM `subjects` WHERE `Class`=%s"
    cursor.execute(sql, (ins1,))
    record1 = cursor.fetchall()
    count1 = cursor.rowcount
    if request.method == 'POST':
        reg=request.form['reg']
        grade1=request.form['grade1']
        sql = "UPDATE `subjects` SET `2`=%s WHERE `Registration_Number`=%s and `Class`=%s and `1`=%s"
        cursor.execute(sql, (grade1, reg, ins1,course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `4`=%s WHERE `Registration_Number`=%s and `Class`=%s and `3`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `6`=%s WHERE `Registration_Number`=%s and `Class`=%s and `5`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `8`=%s WHERE `Registration_Number`=%s and `Class`=%s and `7`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `10`=%s WHERE `Registration_Number`=%s and `Class`=%s and `9`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `12`=%s WHERE `Registration_Number`=%s and `Class`=%s and `11`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `14`=%s WHERE `Registration_Number`=%s and `Class`=%s and `13`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `16`=%s WHERE `Registration_Number`=%s and `Class`=%s and `15`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `18`=%s WHERE `Registration_Number`=%s and `Class`=%s and `17`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `20`=%s WHERE `Registration_Number`=%s and `Class`=%s and `19`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
    return (render_template('TeacherPortal (Grades).html',record1=record1,count1=count1,course1=course1,ins1=ins1))

@app.route('/teacher/grade-of-students/class2',methods=['GET','POST'])
def los2():
    course1 = session.get('course2')
    ins1 = session.get('i2')
    sql = "SELECT `Registration_Number`, `Name` FROM `subjects` WHERE `Class`=%s"
    cursor.execute(sql, (ins1,))
    record1 = cursor.fetchall()
    count1 = cursor.rowcount
    if request.method == 'POST':
        reg = request.form['reg']
        grade1 = request.form['grade1']
        sql = "UPDATE `subjects` SET `2`=%s WHERE `Registration_Number`=%s and `Class`=%s and `1`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `4`=%s WHERE `Registration_Number`=%s and `Class`=%s and `3`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `6`=%s WHERE `Registration_Number`=%s and `Class`=%s and `5`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `8`=%s WHERE `Registration_Number`=%s and `Class`=%s and `7`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `10`=%s WHERE `Registration_Number`=%s and `Class`=%s and `9`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `12`=%s WHERE `Registration_Number`=%s and `Class`=%s and `11`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `14`=%s WHERE `Registration_Number`=%s and `Class`=%s and `13`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `16`=%s WHERE `Registration_Number`=%s and `Class`=%s and `15`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `18`=%s WHERE `Registration_Number`=%s and `Class`=%s and `17`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `20`=%s WHERE `Registration_Number`=%s and `Class`=%s and `19`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
    return (render_template('TeacherPortal (Grades).html', record1=record1, count1=count1, course1=course1, ins1=ins1))

@app.route('/teacher/grade-of-students/class3',methods=['GET','POST'])
def los3():
    course1 = session.get('course3')
    ins1 = session.get('i3')
    sql = "SELECT `Registration_Number`, `Name` FROM `subjects` WHERE `Class`=%s"
    cursor.execute(sql, (ins1,))
    record1 = cursor.fetchall()
    count1 = cursor.rowcount
    if request.method == 'POST':
        reg = request.form['reg']
        grade1 = request.form['grade1']
        sql = "UPDATE `subjects` SET `2`=%s WHERE `Registration_Number`=%s and `Class`=%s and `1`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `4`=%s WHERE `Registration_Number`=%s and `Class`=%s and `3`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `6`=%s WHERE `Registration_Number`=%s and `Class`=%s and `5`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `8`=%s WHERE `Registration_Number`=%s and `Class`=%s and `7`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `10`=%s WHERE `Registration_Number`=%s and `Class`=%s and `9`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `12`=%s WHERE `Registration_Number`=%s and `Class`=%s and `11`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `14`=%s WHERE `Registration_Number`=%s and `Class`=%s and `13`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `16`=%s WHERE `Registration_Number`=%s and `Class`=%s and `15`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `18`=%s WHERE `Registration_Number`=%s and `Class`=%s and `17`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `20`=%s WHERE `Registration_Number`=%s and `Class`=%s and `19`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
    return (render_template('TeacherPortal (Grades).html', record1=record1, count1=count1, course1=course1, ins1=ins1))

@app.route('/teacher/grade-of-students/class4',methods=['GET','POST'])
def los4():
    course1 = session.get('course4')
    ins1 = session.get('i4')
    sql = "SELECT `Registration_Number`, `Name` FROM `subjects` WHERE `Class`=%s"
    cursor.execute(sql, (ins1,))
    record1 = cursor.fetchall()
    count1 = cursor.rowcount
    if request.method == 'POST':
        reg = request.form['reg']
        grade1 = request.form['grade1']
        sql = "UPDATE `subjects` SET `2`=%s WHERE `Registration_Number`=%s and `Class`=%s and `1`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `4`=%s WHERE `Registration_Number`=%s and `Class`=%s and `3`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `6`=%s WHERE `Registration_Number`=%s and `Class`=%s and `5`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `8`=%s WHERE `Registration_Number`=%s and `Class`=%s and `7`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `10`=%s WHERE `Registration_Number`=%s and `Class`=%s and `9`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `12`=%s WHERE `Registration_Number`=%s and `Class`=%s and `11`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `14`=%s WHERE `Registration_Number`=%s and `Class`=%s and `13`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `16`=%s WHERE `Registration_Number`=%s and `Class`=%s and `15`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `18`=%s WHERE `Registration_Number`=%s and `Class`=%s and `17`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
        sql = "UPDATE `subjects` SET `20`=%s WHERE `Registration_Number`=%s and `Class`=%s and `19`=%s"
        cursor.execute(sql, (grade1, reg, ins1, course1))
        connection.commit()
    return (render_template('TeacherPortal (Grades).html', record1=record1, count1=count1, course1=course1, ins1=ins1))

if __name__ == "__main__":
    app.run(debug=True)
