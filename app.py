import pickle
from flask import Flask, request, app, jsonify, url_for, render_template 
import numpy as np

app= Flask(__name__)

# loading the model
scaling= pickle.load(open('scaling.pkl', 'rb'))
reg_model= pickle.load(open('linearReg.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods= ['POST'])
def predict_api():
    data= request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data= scaling.transform(np.array(list(data.values())).reshape(1,-1))
    output= reg_model.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    final_input=scaling.transform(np.array(data).reshape(1,-1))
    print(final_input)
    output=reg_model.predict(final_input)[0]
    return render_template('home.html',prediction_text='The House price prediction is: % .4f' %(output))


if __name__=='__main__':
    app.run(debug=True)

