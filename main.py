from flask import Flask, render_template,request,make_response,session,redirect,g
from mydb import mydb
from werkzeug import secure_filename
import mymail,json
import os
from zeep import Client
from datetime import date
test = mydb()
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n/'
@app.before_request
def before_request():
	g.email = None
	if 'email' in session :
		g.email = session['email']
@app.route('/')
def index():
	email = request.cookies.get('email')
	if email :
		session['email'] = email
		g.email = email  
		return render_template('profile.html')  
	else :      
		return redirect('/login')
@app.route('/login',methods =['POST','GET'])
def login():
	if request.method == 'POST' :
		get_department = test.check(request) 
		if get_department  and (request.form['role'] =='officer' or request.form['role']=='teacher'):
			session['email'] = request.form['email']
			resp = make_response(render_template('profile.html'))
			resp.set_cookie('email',request.form['email'])
			resp.set_cookie('role',request.form['role'])
			resp.set_cookie('department',get_department)
			get_head = test.get_head(get_department,request)
			resp.set_cookie('head_name',get_head['name'])
			resp.set_cookie('head_email',get_head['email'])
			return resp 
		if get_department and request.form['role'] == 'head' :
			session['email'] = request.form['email']
			resp = make_response(render_template('head_profile.html'))
			resp.set_cookie('email',request.form['email'])
			resp.set_cookie('role',request.form['role'])
			resp.set_cookie('department',get_department)
			
			return resp 


	else :
		return render_template('login.html')
@app.route('/logout')
def logout():
	session.clear()
	resp = make_response(redirect('/'))
	resp.set_cookie('email','')
	return resp

@app.route('/leave_list')
def leave_list():
	if not g.email :
		return redirect('/')
	else :
		query = {'email':request.cookies.get('email')}
		leave_list = test.leave_list(query)
		return render_template('leave_list.html',leave_list=leave_list,role=request.cookies.get('role'))
@app.route('/leave_form')
def leave_form():
	if not g.email :
		return redirect('/')
	else :
		mydata = {'email':request.cookies.get('email'),'department':request.cookies.get('department'),'role':request.cookies.get('role'),'head_name':request.cookies.get('head_name'),'head_email':request.cookies.get('head_email')}
		return render_template('leave_form.html',mydata=mydata)
	
@app.route('/leave_form_data',methods = ['POST','GET'])
def leave_form_data():
	if request.method == 'POST':
		leave_from = request.form.get('leave_from')
		leave_to   = request.form.get('leave_to')
		leave_from = leave_from.split('-')
		leave_to = leave_to.split('-')
		leave_from_year = leave_from[0]
		leave_from_month = leave_from[1]
		leave_from_day = leave_from[2]
		leave_to_year = leave_to[0]
		leave_to_month = leave_to[1]
		leave_to_day = leave_to[2]

		d0 = date(int(leave_from_year), int(leave_from_month), int(leave_from_day))
		d1 = date(int(leave_to_year), int(leave_to_month), int(leave_to_day))
		delta = str(d1 - d0)
		
		if request.files['file'] :
			f = request.files['file']
			UPLOAD_FOLDER = 'C:/Users/nasim/Desktop/LMS/static'
			app.config['UPLOAD_FOLDER'] =UPLOAD_FOLDER
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
			filename = f.filename
		else :
			filename = None

		s = test.insert_leave_form(request,filename,delta)
		return redirect('/leave_list')

@app.route('/leave_pending_list')
def leave_pending_list():
	if not g.email :
		return redirect('/')
	else :
		query = {'approved_by':request.cookies.get('email'),'approved':'pending'}
		leave_pending_list = test.leave_list(query)
		return render_template('leave_pending_list.html',leave_list=leave_pending_list,role=request.cookies.get('role'))

@app.route('/leave_approval_list')
def leave_approval_list():
	if not g.email :
		return redirect('/')
	else :
		query = {'approved_by':request.cookies.get('email')}
		leave_approval_list = test.leave_list(query)
		return render_template('leave_list.html',leave_list=leave_approval_list,role=request.cookies.get('role'))
@app.route('/approved/<email>/<leave_from>/<yes_no>',methods =['POST','GET'])
def approved(email,leave_from,yes_no):
	if not g.email :
		return redirect('/')
	else :
		if request.method =='GET' :
			email = email
			leave_from = leave_from
			yes_no = yes_no
			s = test.set_approval(email, leave_from, yes_no)
			return redirect('/leave_approval_list')



		 




if __name__ == '__main__':
   app.run(debug = True,host='0.0.0.0')
