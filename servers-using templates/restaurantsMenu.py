from flask import Flask, render_template, url_for, request, redirect, flash
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
        flash("New menu item created!")
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('addMenuItem.html',restaurant_id = restaurant_id)
    
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method =='POST':
        menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
        menuItem.name = request.form['name']
        menuItem.price = request.form['price']
        menuItem.description = request.form['description']
        session.add(menuItem)
        session.commit()
        flash("Menu item updated successfully!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    
    else:
        oldMenuItem = session.query(MenuItem).filter_by(id = menu_id).one()
        return render_template('editMenuItem.html', menuItem = oldMenuItem)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':        
            item = session.query(MenuItem).filter_by(id = menu_id).one()
            session.delete(item)
            session.commit()
            flash("Menu item deleted!")
            return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        item = session.query(MenuItem).filter_by(id = menu_id).one()
        return render_template('deleteMenuItem.html', menuItem = item)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)    
    return render_template('menu.html',restaurant = restaurant, items = items)

@app.route('/')
@app.route('/restaurants/')
def restaurants():
    allRestaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = allRestaurants)
    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    #app.debug = True
    #app.run(host = '0.0.0.0',port = 5000)
    app.run()
