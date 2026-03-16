from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Restaurant, MenuItem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'check_same_thread': False}
}

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables and sample data
def create_tables():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(username='admin', email='admin@restaurant.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample restaurants
        restaurant1 = Restaurant(
            name="Italian Bistro",
            description="Authentic Italian cuisine with fresh ingredients",
            image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400",
            category="Italian",
            phone="(555) 123-4567",
            email="info@italianbistro.com"
        )
        restaurant2 = Restaurant(
            name="Sushi Haven",
            description="Fresh sushi and Japanese specialties",
            image_url="https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400",
            category="Asian",
            phone="(555) 123-4568",
            email="hello@sushihaven.com"
        )
        restaurant3 = Restaurant(
            name="Burger Palace",
            description="Gourmet burgers and American classics",
            image_url="https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=400",
            category="American",
            phone="(555) 123-4569",
            email="orders@burgerpalace.com"
        )
        
        db.session.add_all([restaurant1, restaurant2, restaurant3])
        db.session.commit()
        
        # Sample menu items for Italian Bistro
        italian_items = [
            MenuItem(name="Margherita Pizza", description="Fresh tomatoes, mozzarella, basil", price=12.99, category="Main Course", restaurant_id=1),
            MenuItem(name="Spaghetti Carbonara", description="Creamy pasta with pancetta", price=14.99, category="Main Course", restaurant_id=1),
            MenuItem(name="Bruschetta", description="Toasted bread with tomatoes and basil", price=8.99, category="Appetizer", restaurant_id=1),
            MenuItem(name="Tiramisu", description="Classic Italian dessert", price=7.99, category="Dessert", restaurant_id=1),
        ]
        
        # Sample menu items for Sushi Haven
        sushi_items = [
            MenuItem(name="California Roll", description="Crab, avocado, cucumber", price=8.99, category="Sushi", restaurant_id=2),
            MenuItem(name="Salmon Nigiri", description="Fresh salmon on rice", price=5.99, category="Sushi", restaurant_id=2),
            MenuItem(name="Miso Soup", description="Traditional Japanese soup", price=3.99, category="Appetizer", restaurant_id=2),
            MenuItem(name="Green Tea Ice Cream", description="Refreshing dessert", price=4.99, category="Dessert", restaurant_id=2),
        ]
        
        # Sample menu items for Burger Palace
        burger_items = [
            MenuItem(name="Classic Cheeseburger", description="Beef patty with cheese and veggies", price=10.99, category="Main Course", restaurant_id=3),
            MenuItem(name="BBQ Bacon Burger", description="Burger with BBQ sauce and crispy bacon", price=12.99, category="Main Course", restaurant_id=3),
            MenuItem(name="French Fries", description="Crispy golden fries", price=3.99, category="Side", restaurant_id=3),
            MenuItem(name="Chocolate Milkshake", description="Creamy chocolate shake", price=5.99, category="Drink", restaurant_id=3),
        ]
        
        db.session.add_all(italian_items + sushi_items + burger_items)
        db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurants')
def restaurants():
    restaurants = Restaurant.query.all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/menu/<int:restaurant_id>')
def menu(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('restaurants'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('signup.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# Admin Routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    restaurants = Restaurant.query.all()
    total_menu_items = sum(len(restaurant.menu_items) for restaurant in restaurants)
    return render_template('admin_dashboard.html', restaurants=restaurants, total_menu_items=total_menu_items)

@app.route('/admin/restaurants')
@login_required
def admin_restaurants():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    restaurants = Restaurant.query.all()
    total_menu_items = sum(len(restaurant.menu_items) for restaurant in restaurants)
    return render_template('admin_restaurants.html', restaurants=restaurants, total_menu_items=total_menu_items)

@app.route('/admin/restaurant/add', methods=['POST'])
@login_required
def add_restaurant():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    name = request.form['name']
    description = request.form['description']
    category = request.form.get('category', 'Other')
    phone = request.form.get('phone', '')
    email = request.form.get('email', '')
    
    restaurant = Restaurant(
        name=name, 
        description=description, 
        category=category,
        phone=phone,
        email=email
    )
    db.session.add(restaurant)
    db.session.commit()
    
    flash('Restaurant added successfully!', 'success')
    return redirect(url_for('admin_restaurants'))

@app.route('/admin/restaurant/<int:restaurant_id>/edit', methods=['POST'])
@login_required
def edit_restaurant(restaurant_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    restaurant.name = request.form['name']
    restaurant.description = request.form['description']
    restaurant.category = request.form.get('category', 'Other')
    
    db.session.commit()
    flash('Restaurant updated successfully!', 'success')
    return redirect(url_for('admin_restaurants'))

@app.route('/admin/restaurant/<int:restaurant_id>/delete')
@login_required
def delete_restaurant(restaurant_id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    db.session.delete(restaurant)
    db.session.commit()
    
    flash('Restaurant deleted successfully!', 'success')
    return redirect(url_for('admin_restaurants'))

@app.route('/admin/menu/<int:restaurant_id>')
@login_required
def admin_menu(restaurant_id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return render_template('admin_menu.html', restaurant=restaurant, menu_items=menu_items)

@app.route('/admin/menu/item/add', methods=['POST'])
@login_required
def add_menu_item():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    restaurant_id = request.form['restaurant_id']
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    category = request.form['category']
    
    menu_item = MenuItem(
        name=name,
        description=description,
        price=price,
        category=category,
        restaurant_id=restaurant_id,
        is_available=True
    )
    db.session.add(menu_item)
    db.session.commit()
    
    flash('Menu item added successfully!', 'success')
    return redirect(url_for('admin_menu', restaurant_id=restaurant_id))

@app.route('/admin/menu/item/<int:item_id>/edit', methods=['POST'])
@login_required
def edit_menu_item(item_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    menu_item = MenuItem.query.get_or_404(item_id)
    menu_item.name = request.form['name']
    menu_item.description = request.form['description']
    menu_item.price = float(request.form['price'])
    menu_item.category = request.form['category']
    
    db.session.commit()
    flash('Menu item updated successfully!', 'success')
    return redirect(url_for('admin_menu', restaurant_id=menu_item.restaurant_id))

@app.route('/admin/menu/item/<int:item_id>/delete')
@login_required
def delete_menu_item(item_id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    menu_item = MenuItem.query.get_or_404(item_id)
    restaurant_id = menu_item.restaurant_id
    db.session.delete(menu_item)
    db.session.commit()
    
    flash('Menu item deleted successfully!', 'success')
    return redirect(url_for('admin_menu', restaurant_id=restaurant_id))

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0',debug=True,port=8080)