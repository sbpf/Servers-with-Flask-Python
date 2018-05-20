from flask import Flask, render_template, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return 'edit url added'


@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return 'delete url added'

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    print"helllooooo"
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    editUrl = url_for('editRestaurant',restaurant_id=restaurant_id)
    deleteUrl= url_for('deleteRestaurant',restaurant_id = restaurant_id)
    return render_template('menu.html',restaurant = restaurant, items = items, editURL = editUrl, deleteUrl = deleteUrl)    
    
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port = 5000)
