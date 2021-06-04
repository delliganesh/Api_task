from flask import Flask, render_template,request, redirect, url_for, session
from flask_restful import Resource, Api, reqparse
from flask_mysql_connector import MySQL



app = Flask(__name__)
api = Api(app)
#app.secret_key = '123456'

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'delli'
app.config['MYSQL_DATABASE'] = 'api_account'
mysql = MySQL(app)

    
def cursor_(query):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(query)
    account = cur.fetchall()
    return account
       

class finished(Resource):
    def get(self):
        result={}
        re=cursor_('SELECT TaskName,Status FROM task WHERE Status="Finished"')
        for j in range(len(re)):
            result[j+1]={'task':re[j][0],'status':re[j][1]}
        return result

class overdue(Resource):
    def get(self):
        result={}
        re=cursor_("select TaskName , Status from  task where Date <= CURDATE() AND Status NOT IN('Finished')")
        for j in range(len(re)):
            result[j+1]={'task':re[j][0],'status':re[j][1]}
        return result

class due(Resource):
    def get(self,due_date):
        result={}
        query = "select TaskName , Status from  task where Date = '"+str(due_date)+"' AND Status NOT IN('Finished')"
        re=cursor_(query)
        for j in range(len(re)):
            result[j+1]={'task':re[j][0],'status':re[j][1]}
        return result

class Add(Resource):
     def get(self,TaskName,due_date,Status):
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("insert into task(TaskName, Date, Status) values(%s, %s, %s)",(TaskName,due_date,Status))
        conn.commit()
        task ="Added Sucessfully"
        return task
        
class Change(Resource):
     def get(self,TaskName,Status):
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("Update task set Status=%s where TaskName=%s",(Status,TaskName))
        conn.commit()
        task ="Updated Sucessfully"
        return task
        


api.add_resource(finished, '/finished')
api.add_resource(overdue, '/overdue')
api.add_resource(due, '/due/<due_date>')
api.add_resource(Add, '/Add/<TaskName>,<due_date>,<Status>')
api.add_resource(Change, '/Change/<TaskName>,<Status>')

if __name__ == '__main__':
    app.run(debug=True)
