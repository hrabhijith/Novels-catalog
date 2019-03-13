from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from database_setup import Authors, Base, Novels
from flask import request
from flask import redirect
from flask import url_for

#Creates sqlite db connection
def dbConnection():
    engine = create_engine('sqlite:///authorlibrary.db')
    Base.metadata.bind = engine
 
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

app = Flask(__name__)

# Categories' home page
@app.route('/')
@app.route('/home/', methods=['GET'])
def categoryHomePage():
    session = dbConnection()
    authors = session.query(Authors).all()
    return render_template('categorypage.html', authors = authors)


# Author's novels detail page
@app.route('/home/<int:author_id>/', methods=['GET'])
def categoryDetail(author_id):
    session = dbConnection()
    author = session.query(Authors).filter_by(id = author_id).one()
    novels = session.query(Novels).filter_by(author_id = author_id).all()
    return render_template('categoryitemspage.html', novels = novels, author = author)

# Edit category item
@app.route('/home/<int:author_id>/<int:novel_id>/edit', methods=['GET','POST'])
def itemEdit(author_id, novel_id):
    token = 1
    session = dbConnection()
    if request.method == 'POST':
        novel = session.query(Novels).filter_by(id = novel_id).one()
        if request.form['editedName']:
            novel.name = request.form['editedName']
            session.add(novel)
        
        if request.form['editedYear']:
            novel.year = request.form['editedYear']
            session.add(novel)

        session.commit()
        session.close()
        #flash('New Menu item Created')
        return redirect(url_for('categoryDetail', author_id = author_id))

    author = session.query(Authors).filter_by(id = author_id).one()
    novel = session.query(Novels).filter_by(id = novel_id).one()
    return render_template('edititempage.html', token = token, novel = novel, author = author)

# Delete category item
@app.route('/home/<int:author_id>/<int:novel_id>/delete', methods=['GET','POST'])
def itemDelete(author_id, novel_id):
    token = 1
    session = dbConnection()
    novel = session.query(Novels).filter_by(id = novel_id).one()
    return render_template('deleteitempage.html', token = token, novel = novel)

# New category item
@app.route('/home/<int:author_id>/new', methods=['GET','POST'])
def itemNew(author_id):
    session = dbConnection()
    if request.method == 'POST':
        newNovel = Novels(name = request.form['newName'], year = request.form['newYear'], description = request.form['newDescription'], author_id = author_id)
        session.add(newNovel)
        session.commit()
        #flash('New Menu item Created')
        return redirect(url_for('categoryDetail', author_id = author_id))

    author = session.query(Authors).filter_by(id = author_id).one()
    return render_template('newitempage.html', author = author)

# Categories' description page
@app.route('/home/<int:author_id>/<int:novel_id>/description/', methods=['GET'])
def categoryDescription(author_id, novel_id):
    session = dbConnection()
    author = session.query(Authors).filter_by(id = author_id).one()
    novel= session.query(Novels).filter_by(id = novel_id).one()
    return render_template('descriptionpage.html', novel = novel, author = author)


# Edit description
@app.route('/home/<int:author_id>/<int:novel_id>/description/edit', methods=['GET','POST'])
def descriptionEdit(author_id, novel_id):
    token = 2
    session = dbConnection()
    if request.method == 'POST':
        novel = session.query(Novels).filter_by(id = novel_id).one()
        if request.form['editedDescription']:
            novel.description = request.form['editedDescription']
            session.add(novel)

        session.commit()
        session.close()
        #flash('New Menu item Created')
        return redirect(url_for('categoryDescription', author_id = author_id, novel_id = novel_id))

    author = session.query(Authors).filter_by(id = author_id).one()
    novel = session.query(Novels).filter_by(id = novel_id).one()
    return render_template('edititempage.html', token = token, novel = novel, author = author)

# delete description
@app.route('/home/<int:author_id>/<int:novel_id>/description/delete', methods=['GET','POST'])
def descriptionDelete(author_id, novel_id):
    token = 2
    session = dbConnection()
    novel = session.query(Novels).filter_by(id = novel_id).one()
    return render_template('deleteitempage.html', token = token, novel = novel)





# Server host listening starts
if __name__ == '__main__':
    app.secret_key = 'super_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000 )
