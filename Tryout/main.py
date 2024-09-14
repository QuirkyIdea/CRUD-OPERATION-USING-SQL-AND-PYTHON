from flask import Flask,render_template,request,session,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors#collecting my required library
app=Flask(__name__)#keep the flask inside a variable
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'#giving all inputs to access to the database
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='test'
mysql=MySQL(app)#keeping my sql library inside variable

@app.route('/',methods=['GET'])#creating route along with proper use of http method
def index():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM crud")#collecting dta using cursor method from crud in database
    data=cursor.fetchall()#storing data inside a local variable 
    return render_template("index.html",data=data)#running the [page with data]

@app.route('/form',methods=['POST','GET'])
def form():
    msg=''
    if request.method=='POST'and 'name' in request.form and 'class' in request.form and 'subject' in request.form:
        name=request.form['name']
        class1=request.form['class']
        subject=request.form['subject']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO crud VALUES(NULL,%s,%s,%s)',(name,class1,subject,))
        mysql.connection.commit()
        msg='Data inserted successfully'
    else:
        msg='Data insertion failure'
    return render_template("form.html",msg=msg)
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
   cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   if request.method=='POST':
       name=request.form['name']
       class1=request.form['class']
       subject=request.form['subject']
       cursor.execute('UPDATE crud SET name=%s,class=%s,subject=%s WHERE id=%s',(name,class1,subject,id))
       mysql.connection.commit()
       return redirect(url_for('index'))
   else:
       cursor.execute('SELECT * FROM crud WHERE id=%s',[id])
       user=cursor.fetchone()
       return render_template('edit.html',user=user)
@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete(id):
   cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   cursor.execute('DELETE FROM crud WHERE id=%s',[id])
   mysql.connection.commit()
   return redirect(url_for('index'))


if __name__==('__main__'):
    app.run(debug=True)#update page without re-execution

