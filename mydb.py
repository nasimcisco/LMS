import pymongo
import json
import random


class mydb:
        def check(self,request):
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["mydatabase"]
            mycol = mydb["user"]
            myquery = {'email' : request.form['email'],'password':request.form['password'],'role' :request.form['role']}
            mydoc = mycol.find_one(myquery,{'_id' : 0}) 
            if mydoc :
                
                return mydoc['department']  
            else :
                return False
        def get_head(self,get_department,request) :
            if request.form['role'] == 'Head':
                return 'dean'
            else : 
                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["mydatabase"]
                mycol = mydb["user"]
                myquery = {'department':get_department,'role':'head'}
                mydoc = mycol.find_one(myquery,{'_id' : 0}) 
                if mydoc :
                   
                    return mydoc

                else :
                    return None
        def leave_list(self,query) :
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["mydatabase"]
            mycol = mydb["lms"]
            mydoc = mycol.find(query,{'_id' : 0}) 
            if mydoc :
               
                return mydoc

            else :
                return None
        def insert_leave_form(self,request,filename,delta) :
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["mydatabase"]
            mycol = mydb["lms"]
            mydata = {'email':request.form['email'],'leave_from':request.form['leave_from'],'leave_to':request.form['leave_to'],'days':delta,'filename':filename,'approved':'pending','approved_by':request.form['head_email'],'type':request.form['type']}
            mydoc = mycol.insert_one(mydata)
            return mydoc

        def set_approval(self,email,leave_from,yes_no) :
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["mydatabase"]
            mycol = mydb["lms"]
            myquery = { 'email': email,'leave_from':leave_from }
            newvalues = { "$set": { "approved": yes_no } }

            mycol.update_one(myquery, newvalues)
            return 'successfully done'    





            # ls = []
            # for x in mydoc:
            #     ls.append(x)
            # return ls

        # def insert2(self,request,filename,fakefilename):
        #         myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #         mydb = myclient["mydatabase"]
        #         mycol = mydb["studentdb"]
        #         mydict = { 'name': request.form['name'], 'roll' :request.form['roll'],'mobile':request.form['mobile'],'email':request.form['email'],'department':request.form['department'],'session':request.form['session'],'father':request.form['father'],'fathermobile':request.form['fathermobile'],'filename':filename,'fakefilename':fakefilename,'nid':request.form['nid'],'address':request.form['address']}
        #         x = mycol.insert_one(mydict)
        #         return('<h1>successfully uploaded in server</h1>')
        # def insert(self,request,filename,fakefilename,user):
        #         myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #         mydb = myclient["mydatabase"]
        #         mycol = mydb["elearning"]
        #         mydict = { request.form['department']: request.form['semester'], 'year': request.form['year'],'course':request.form['course'] ,'filename':filename,'fakefilename':fakefilename,'user':user}
        #         x = mycol.insert_one(mydict)
        #         return('<h1>successfully uploaded in server</h1>')
        # def get(self,mydata):
        #         myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #         mydb = myclient["mydatabase"]
        #         mycol = mydb["studentdb"]
        #         myquery = mydata
        #         mydoc = mycol.find(myquery).sort("roll",-1)
        #         ls = []
        #         for x in mydoc:
        #             ls.append(x)
        #         return ls
        # def getcourse(self,coursequery):
        #      myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #      mydb = myclient["mydatabase"]
        #      mycol = mydb["elearning"]
        #      myquery = coursequery
        #      mydoc = mycol.find(myquery)
        #      ls = []
        #      for x in mydoc:
        #         ls.append(x)
        #      return ls
        # def getusercourse(self,getusercoursequery):
        #      myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #      mydb = myclient["mydatabase"]
        #      mycol = mydb["course"]
        #      myquery = getusercoursequery
        #      mydoc = mycol.find(myquery)
        #      ls = []
        #      for x in mydoc:
        #         ls.append(x)
        #      return ls

        # def getuserfilelist(self,editquery):
        #      myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #      mydb = myclient["mydatabase"]
        #      mycol = mydb["elearning"]
        #      myquery = editquery
        #      mydoc = mycol.find(myquery)
        #      ls = []
        #      for x in mydoc:
        #         ls.append(x)
        #      return ls
        # def delete(self,roll):
        #      myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #      mydb = myclient["mydatabase"]
        #      mycol = mydb["studentdb"]
        #      myquery = {'roll' : roll }
        #      mycol.delete_one(myquery)
        #      return('<h1>successfully deleted in server</h1>')
        # def duplicate(self,roll):
        #     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #     mydb = myclient["mydatabase"]
        #     mycol = mydb["studentdb"]
        #     myquery = {'roll':roll}
        #     mydoc = mycol.find(myquery)
        #     ls = []
        #     for x in mydoc:
        #         ls.append(x)
        #     return ls
        # def passwd(self,mydata):
        #     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #     mydb = myclient["mydatabase"]
        #     mycol = mydb["studentdb"]
        #     myquery = mydata
        #     genpass = random.randint(100000,1000000)
        #     newvalues = { "$set": { "passwd": genpass } }
        #     mycol.update_one(myquery, newvalues)
        #     return ('successfully')
