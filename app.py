
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd 

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/get')
def get_table():
    dataset = pd.read_excel('Book_list.xlsx', index_col=False) # read a excel file 
    return render_template('get.html', data=dataset.to_html())

@app.route('/edit', methods=['GET','POST'])
def edit_author_national_book_form():
    author_name_id  = request.form.get('author_name_id', False)
    author_name_text = request.form.get('author_name_text', False)
    # national_name_id  = request.form.get('national_name_id', False)
    national_name_text = request.form.get('national_name_text', False)
    # book_name_id  = request.form.get('national_name_id', False)
    book_name_text = request.form.get('book_name_text', False)
    dataset = pd.read_excel('Book_list.xlsx', index_col=False) # read a excel file 
    dataset = dataset[['الرواية', 'المؤلف', 'البلد']] # selecting the column will be shown 

    length  = dataset.shape[0] # getting a length of the table 

    if request.method == 'POST': # checking if post method and the input text is not empty 
        if request.form['author_btn'] == "تعديل" and author_name_text != ''  and national_name_text != '' and book_name_text != '':
            author_name_id = int(author_name_id) # converting the the output to be a interger to be input to the next line  
            dataset['المؤلف'][author_name_id] = author_name_text
            dataset.to_excel('Book_list.xlsx', index=False)

            dataset['البلد'][author_name_id] = national_name_text
            dataset.to_excel('Book_list.xlsx', index=False)

            dataset['الرواية'][author_name_id] = book_name_text
            dataset.to_excel('Book_list.xlsx', index=False)
            return redirect(url_for("get_table"))
        
        else:
            return render_template('edit.html',
        data=dataset.to_html(), 
            length=length)

    else:
        return render_template('edit.html',
        data=dataset.to_html(), 
            length=length)

@app.route('/delete', methods=['GET', 'POST'])
def delete_form():
    author_name_id  = request.form.get('author_name_id')
    dataset = pd.read_excel('Book_list.xlsx', index_col=False)
    dataset = dataset[['الرواية', 'المؤلف', 'البلد']] # selecting the column will be shown 

    length  = dataset.shape[0]
    if request.method == 'POST' : 
        author_name_id = int(author_name_id)
        dataset = dataset.drop(labels=author_name_id, axis=0) # delete the row depend a selected id 
        dataset.to_excel('Book_list.xlsx', index=False)
   
    return render_template('delete.html',
     data=dataset.to_html(), 
     length=length)

@app.route('/create', methods = ['GET', 'POST'])
def create_form():
    dataset = pd.read_excel('Book_list.xlsx', index_col=False)
    dataset = dataset[['الرواية', 'المؤلف', 'البلد']] # selecting the column will be shown 
    author_input = request.form.get('author_input')
    book_input = request.form.get('book_input')
    national_input = request.form.get('national_input')
    new_row = {'الرواية':book_input, 'المؤلف':author_input, 'البلد':national_input}
    if request.method == 'POST' and author_input != '' and  book_input != '' and national_input != '':
        dataset = dataset.append(new_row, ignore_index=True)
        dataset.to_excel('Book_list.xlsx', index=False)


    return render_template('create.html', data=dataset.to_html())

if __name__ == '__main__':
    app.run(debug=True)
