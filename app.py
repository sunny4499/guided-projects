# -*- coding: utf-8 -*-
"""
Created on Mon May 31 22:08:10 2021

@author: Admin
"""
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from flask import Flask, request, jsonify , render_template, url_for
loaded=CountVectorizer(decode_error='replace',vocabulary=pickle.load(open(r'C:\Users\Admin\Desktop\Flask\word_features.pkl','rb')))
app = Flask(__name__)
def clean_text(text):
    text = text.lower()
    text = text.lower()
    text = re.sub(r"what's","what is",text)
    text = re.sub(r"\'s"," ",text)
    text = re.sub(r"\'ve'","have",text)
    text = re.sub(r"cant't","cannot",text)
    text = re.sub(r"n't","not",text)
    text = re.sub(r"i'm","i am",text)
    text = re.sub(r"\'re","are",text)
    text = re.sub(r"\'d","would",text)
    text = re.sub(r"\'ll","will",text)
    text = re.sub(r"\'scuse","excuse",text)
    text = re.sub('\W',' ',text)
    text = re.sub('\s+',' ',text)
    text = text.strip(' ')
    return text
@app.route('/')
def landingpage():
    img_url = url_for('static',filename =r'C:\Users\Admin\Desktop\Flask\images/hello.png')
    print(img_url)
    flag=0
    return render_template(r'C:\Users\Admin\Desktop\Flask\Template\toxic.html',flag=flag)
@app.route('/predict')
@app.route('/',methods=['GET','POST'])
def predict():
    if request.method == 'GET':
        img_url = url_for('static',filename = r'C:\Users\Admin\Desktop\Flask\images/hello.png')
        return render_template(r'C:\Users\Admin\Desktop\Flask\Template\toxic.html',url=img_url)
    if request.method == 'POST':
        comment = request.form['comment']
        new_row = {'comment_text':comment}
        user_df = pd.DataFrame(columns = ['coments_text'])
        user_df = user_df.append(new_row,ignore_index = True)
        user_df['comment_text']= user_df['comment_text'].map(lambda com : clean_text(com))
        user_text = user_df['comment_text']
        user_features = loaded.transform(user_text)
        cols_target = ['obscene','insult','toxic','severe_toxic','identity_hate','threat']
        lst =[]
        mapper = {}
        for label in cols_target:
            filename = str(label+'_model.sav')
            filename
            model = pickle.load(open(filename,'rb'))
            print('---Processing{}'.format(label))
            user_y_prob = model.predict_proba(user_features)[:,1]
            print(label,":",user_y_prob[0])
            lst.append([label,user_y_prob])
        print(lst)
        
        final=[]
        flag=0
        for i in lst:
            if i[1]>0.5:
                final.append(i[0])
                flag=2
        if not len(final):
            text = "yaayy!!The comment is clean"
            img_url = url_for('static',filename =r'C:\Users\Admin\Desktop\Flask\images/happy.png')
            flag=1
            print(img_url)
        else:
            text ="the comment is "
            for i in final:
                text = text+i+" "
            img_url = url_for('static',filename = r'C:\Users\Admin\Desktop\Flask\images/toxic.png')
        print(text)    
        return render_template(r'C:\Users\Admin\Downloads\Telegram Desktop\toxic.html',ypred = text,url = img_url,flag=flag) 
        
app.run(host = 'localhost',debug = True, threaded = False)             
                
