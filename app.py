
from operator import index
from flask import Flask, render_template, request
import pandas as pd 

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def myform():
    dataset = pd.read_excel('Book_list.xlsx', index_col=False)
    dataset = dataset.iloc[0]
    return render_template('index.html', data=dataset.to_html())



if __name__ == '__main__':
    app.run(debug=True)
