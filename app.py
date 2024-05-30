from flask import Flask,render_template,request
import sqlite3
import json
import pickle
app = Flask(__name__)
@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/contact',methods=["GET","POST"])
def contactus():
    if request.method=='POST':
        name=request.form.get("name")
        email=request.form.get("email")
        state=request.form.get("state")
        country=request.form.get("country")
        message=request.form.get("message")
        print(name,email,state,country,message)
        conn = sqlite3.connect("contactus.db")
        cur = conn.cursor()
        cur.execute(f'''
                INSERT INTO CONTACT VALUES(
                    "{name}","{email}","{country}","{state}",
                    "{message}"
                    )
                    ''')
        conn.commit()
        return render_template("message.html")
    else:
        return render_template("contactus.html")
@app.route("/price",methods = ["GET","POST"])
def predict():
    if request.method=='POST':
        make = request.form.get("make")
        model = request.form.get("model")
        year = request.form.get("year")
        kms_driven = request.form.get("kms")
        fuel =  request.form.get("fuel")
        reg_city = request.form.get("registration_city")
        car_documents = request.form.get("car_documents")
        assembly = request.form.get("assembly")
        transmission =  request.form.get("transmission")
        print(make,model,year,kms_driven,fuel,reg_city,car_documents,assembly,transmission)
        with open("encdata.json","r") as file:
            data = json.load(file)
        mkenc = int(data["Make"][make])
        mdlenc = int(data["Model"][model])
        flenc = int(data["Fuel"][fuel])
        rgclenc = int(data["Registration city"][reg_city])
        carlenc = int(data["Car documents"][car_documents])
        assenc = int(data["Assembly"][assembly])
        trasenc = int(data["Transmission"][transmission])
        print(mkenc,mdlenc,flenc,rgclenc,carlenc,assenc,trasenc)
        file.close()
        with open("model.pickle","rb") as model:
            mymodel = pickle.load(model)
        res = mymodel.predict([[int(year),int(kms_driven),mkenc,mdlenc,flenc,rgclenc,carlenc,assenc,trasenc]])
        print(res[0])
        return render_template("result.html",car_price = str(int(res[0]*0.3))+" Rs")
    else:
        return render_template("predict.html")
    

if __name__=='__main__':
    app.run(host="0.0.0.0",port=5500)