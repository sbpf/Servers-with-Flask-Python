from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET','POST'])
def addNewMenuItem(restaurant_id):
    if request.method == 'POST':
        newMenuItem = MenuItem(name = request.form['name'],
                               price = request.form['price'],
                               description = request.form['description'],
                               restaurant_id = restaurant_id)
        session.add(newMenuItem)
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('addMenuItem.html',restaurant_id = restaurant_id)
    
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return 'edit url added'

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return 'delete url added'

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)    
    return render_template('menu.html',restaurant = restaurant, items = items)    
    
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port = 5000)
