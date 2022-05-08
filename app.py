"""
                         _________________________________ Import all the required Libraries ________________________________

"""

from flask import Flask, request, render_template, redirect, session, url_for, flash
import mysql.connector
import numpy as np
import pickle
import os
import warnings
# from twilio.twiml.messaging_response import MessagingResponse
# from twilio.rest import Client

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = os.urandom(24)

"""
                         _________________________________ Whatsapp settings ________________________________

"""

# from sinchsms import SinchSMS

# sid = "ACf6deaa9624b8c734fa1e2bf9919751e8"
# auth = "37ba1f163788a7ee14f8a1f677910a4f"
# client = Client(sid, auth)
#
#
# def whatsapp(x, y):
#     client.messages.create(
#         from_='whatsapp:+14155238886',
#         body=x,
#         to='whatsapp:+91' + y
#     )


"""
                         _________________________________ ML Models ______________________________

"""

model = pickle.load(open('ML Models/parkinsons.pkl', 'rb'))
model2 = pickle.load(open("ML Models/heartPKL.pkl", 'rb'))
model3 = pickle.load(open('ML Models/liver.pkl', 'rb'))
model4 = pickle.load(open("ML Models/cancer.pkl", 'rb'))
model5 = pickle.load(open("ML Models/diabetes.pkl", 'rb'))
model7 = pickle.load(open("ML Models/kidneyPKL.pkl", 'rb'))

"""
                         _________________________________ Database Connection ______________________________

"""
conn = mysql.connector.connect(host="localhost", user="root", password="", database="0dUfVC8t7r")
# conn = mysql.connector.connect(host="sql6.freesqldatabase.com",user="sql6467292",password="2sHkSdgrQE",database="sql6467292")
cursor = conn.cursor()


def users_info():
    cursor.execute("""SELECT * FROM `users` WHERE `user_id`={}""".format(session['user_id']))
    users = cursor.fetchall()
    return users


@app.route('/')
def hello_world():
    return render_template("loginpage.html")


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/login_valid',methods=['POST'])
def login_valid():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return render_template('loginpage.html', info='invalid credentials',infocor='red')


@app.route('/add_user',methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    dob = request.form.get('dob')
    mobile = request.form.get('mobile')
    blood = request.form.get('blood')
    password = request.form.get('upassword')
    cursor.execute("""INSERT INTO `users` (`user_id`, `name`, `email`, `password`, `dob`,`mobile`,`blood`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}')""".format(name,email,password,dob,mobile,blood))
    conn.commit()
    return render_template('loginpage.html', info='user succesfully registered',infocor='#2DBD6B')

@app.route('/feedback', methods=['POST'])
def add_feedback():
    name = request.form.get('fname')
    email = request.form.get('femail')
    subject = request.form.get('sub')
    message = request.form.get('msg')
    cursor.execute(
        """INSERT INTO `feedback`(`user_id`, `name`, `email`, `subject`, `message`) VALUES (NULL,'{}','{}','{}','{}')""".format(
            name, email, subject, message))
    conn.commit()
    msg = 'Your message has been sent. Thank you!'
    return render_template('home.html',msg=msg)


@app.route('/form_loginpage', methods=['POST', 'GET'])
def login():
    name1 = request.form['uname']
    pwd = request.form['pass']
    if name1 not in database:
        return render_template('loginpage.html', info='Invalid User')
    else:
        if database[name1] != pwd:
            return render_template('loginpage.html', info='Invalid Password')
        else:
            return render_template('home.html', name=name1)


@app.route('/logout')
def logout():
    # users = users_info()
    # whatsapp('Thank You for using HealthServ!!', users[0][5])
    session.pop('user_id')
    return redirect('/')


"""
                         _________________________________ Parkinson's ______________________________

"""


@app.route('/page')
def page():
    return render_template("parkinson_s.html", length=0)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_features = [float(x) for x in request.form.values()]
        features_value = [np.array(input_features)]
        output = model.predict(features_value)
        allcol = ["MDVP:Jitter(%) ", "MDVP:Jit ter(Abs) ", "MDVP:RAP ", "MDVP:PPQ ", "Jitter:DDP", "MDVP:Shimmer ",
                  "MDVP:Shimmer(dB)", "MDVP:APQ", "NHR", "RPDE", "spread1", "spread2", "PPE"]
        users = users_info()
        if output == 1:
            # whatsapp('your kidney report : Parkinson’s Disease Detected', users[0][5])
            return render_template("parkinson_s.html", predict_text='Parkinson’s Disease Detected', cor="red",
                                   pentered=input_features, length=len(input_features), kcol=allcol, email=users[0][2],
                                   name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        elif output == 0:
            # whatsapp('your kidney report : Parkinson’s Disease Not Detected', users[0][5])
            return render_template("parkinson_s.html", predict_text='Parkinson’s Disease Not Detected', cor="green",
                                   pentered=input_features, length=len(input_features), kcol=allcol, email=users[0][2],
                                   name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        else:
            return render_template("parkinson_s.html", predict_text='Something went wrong')


"""
                         _________________________________ Heart ______________________________

"""


@app.route('/heart')
def heart():
    return render_template('heart.html', length=0)


@app.route('/resultH', methods=['POST'])
def resultH():
    if request.method == 'POST':
        input_features2 = [float(x) for x in request.form.values()]
        features_value2 = np.array(input_features2)
        output2 = model2.predict([features_value2])
        allcol = ["cp ", "trestbps ", "chol ", "fbs ", "restecg ", "Thalach ", "slope "]
        users = users_info()
        if output2 == 1:
            # whatsapp('your kidney report : Heart Disease Detected', users[0][5])
            return render_template('heart.html', predict_text='Heart Disease Detected', cor="red",
                                   pentered=input_features2, length=len(input_features2), kcol=allcol,
                                   email=users[0][2], name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        elif output2 == 0:
            # whatsapp('your kidney report : Heart Disease Not Detected', users[0][5])
            return render_template('heart.html', predict_text='Heart Disease Not Detected', cor="green",
                                   pentered=input_features2, length=len(input_features2), kcol=allcol,
                                   email=users[0][2], name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        else:
            return render_template('heart.html', predict_text='Something went wrong')


"""
                         _________________________________ Liver ______________________________

"""


@app.route('/liver')
def liver():
    return render_template('liver.html', length=0)


@app.route('/resultL', methods=['POST'])
def resultL():
    if request.method == 'POST':
        input_features3 = [float(x) for x in request.form.values()]
        features_value3 = np.array(input_features3)
        print(features_value3)
        output3 = model3.predict([features_value3])
        print(output3)
        allcol = ["Total_Bilirubin", "Alamine_Aminotransferase", "Total_Protiens", "Albumin",
                  "Albumin_and_Globulin_Ratio"]
        # cursor.execute("""SELECT * FROM `users` WHERE `user_id`={}""".format(session['user_id']))
        # users = cursor.fetchall()
        users = users_info()
        if output3 == 1:
            # whatsapp('your kidney report : liver Disease Detected', users[0][5])
            return render_template('liver.html', predict_text='liver Disease Detected', cor="red",
                                   pentered=input_features3, length=len(input_features3), kcol=allcol,
                                   email=users[0][2], name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        elif output3 == 2:
            # whatsapp('your kidney report : liver Disease Not Detected', users[0][5])
            return render_template('liver.html', predict_text='liver Disease Not Detected', cor="green",
                                   pentered=input_features3, length=len(input_features3), kcol=allcol,
                                   email=users[0][2], name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        else:
            return render_template('liver.html', predict_text='Something went wrong')


"""
                         _________________________________ Diabetes ______________________________

"""


@app.route('/sugar')
def sugar():
    return render_template('sugar.html', length=0)

@app.route('/resultD', methods=['POST'])
def resultD():
    if request.method == 'POST':
        input_features5 = [float(x) for x in request.form.values()]
        features_value5 = np.array(input_features5)
        output5 = model5.predict([features_value5])
        allcol = ["Glucose ", "BloodPressure", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
        users = users_info()
        if output5 == 1:
            # whatsapp('your kidney report : Diabetes Detected', users[0][5])
            return render_template('sugar.html', predict_text='Diabetes Detected', cor='red', pentered=input_features5,
                                   length=len(input_features5), kcol=allcol, email=users[0][2], name=users[0][1],
                                   dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        elif output5 == 0:
            # whatsapp('your kidney report : Diabetes Not Detected', users[0][5])
            return render_template('sugar.html', predict_text='Diabetes Not Detected', cor='green',
                                   pentered=input_features5, length=len(input_features5), kcol=allcol,
                                   email=users[0][2], name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        else:
            return render_template('suagr.html', predict_text='Something went wrong')


"""
                         _________________________________ Cancer ______________________________

"""


@app.route('/cancer')
def cancer():
    return render_template('cancer.html', length=0)


@app.route('/resultC', methods=['POST'])
def resultC():
    if request.method == 'POST':
        input_features4 = [float(x) for x in request.form.values()]
        features_value4 = np.array(input_features4)
        output4 = model4.predict([features_value4])
        allcol = ["radius_mean ", "perimeter_mean ", "area_mean ", "concavity_mean ", "concave points_mean","radius_se ", "perimeter_se", "area_se", "radius_worst", "perimeter_worst", "area_worst","concavity_worst", "concave points_worst"]
        users = users_info()
        if output4 == 0:
            # whatsapp('your kidney report : Benign Tumor Detected', users[0][5])
            return render_template('cancer.html', predict_text='Benign Tumor Detected', cor="green",
                                   pentered=input_features4, length=len(input_features4), kcol=allcol,
                                   email=users[0][2], name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        elif output4 == 1:
            # whatsapp('your kidney report : Malignant Tumor Detected', users[0][5])
            return render_template('cancer.html', predict_text='Malignant Tumor Detected', cor="red",
                                   pentered=input_features4, length=len(input_features4), kcol=allcol,
                                   email=users[0][2], name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        else:
            return render_template('cancer.html', predict_text='Something went wrong')


"""
                         _________________________________ Kidney ______________________________

"""


@app.route('/kidney')
def kidney():
    return render_template('kidney.html', length=0)


@app.route('/resultK', methods=['POST'])
def resultK():
    if request.method == 'POST':
        input_features5 = [float(x) for x in request.form.values()]
        features_value5 = np.array(input_features5)
        output5 = model7.predict([features_value5])
        allcol = ["Albumin", "Sugar", "Red Blood Cells", "Pus Cell", "Pus Cell Clumps", "Bacteria", "Blood Urea","Serum Creatinine", "Hypertension", "Diabetes Mellitus", "Pedal Edema", "Anemia"]
        users = users_info()
        if output5 == 0:
            # whatsapp('your kidney report : Chronic Kidney Disease Not Detected', users[0][5])
            return render_template('kidney.html', predict_text='Chronic KIdney Disease Not Detected', cor="green",
                                   pentered=input_features5, length=len(input_features5), kcol=allcol,
                                   email=users[0][2], name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        elif output5 == 1:
            # wmsg="Hii,{v1} \nyour final Kidney report is \n*'Chronic Kidney Disease Detected'*,\nget well soon! ".format(v1=users[0][1])
            # whatsapp(wmsg, users[0][5])
            return render_template('kidney.html', predict_text='Chronic KIdney Disease Detected', cor="red",
                                   pentered=input_features5, length=len(input_features5), kcol=allcol,
                                   email=users[0][2], name=users[0][1], dob=users[0][4],mobile=users[0][5],blood=users[0][6])
        else:
            return render_template('kidney.html', predict_text='Something went wrong')


if __name__ == '__main__':
    app.run(debug=True)
