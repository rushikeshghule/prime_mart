from django.contrib.auth.models import User
from accounts.models import Profile, Address
from store.models import Category, Product, Cart, CartItem, Order, OrderItem
from django.utils import timezone
import random

# Create dummy users
def create_dummy_users():
    users = []
    for i in range(1, 6):
        user, created = User.objects.get_or_create(username=f'user{i}', defaults={
            'email': f'user{i}@example.com',
            'first_name': f'User{i}',
            'last_name': f'Last{i}',
        })
        user.set_password('password123')
        user.save()
        users.append(user)
    return users

# Create dummy categories
def create_dummy_categories():
    categories = []
    category_data = [
        {'name': 'Shirts', 'description': 'Formal and casual shirts for all occasions'},
        {'name': 'Pants', 'description': 'Trousers, jeans and formal pants for men and women'},
        {'name': 'Shoes', 'description': 'Footwear including casual shoes, formal shoes, and sports shoes'},
        {'name': 'Dresses', 'description': 'Stylish dresses for women for all occasions'},
        {'name': 'Accessories', 'description': 'Bags, belts, sunglasses and other fashion accessories'}
    ]
    
    for data in category_data:
        cat, _ = Category.objects.get_or_create(name=data['name'], defaults={'description': data['description']})
        categories.append(cat)
    return categories

# Create dummy products
def create_dummy_products(categories):
    products = []
    sizes = ['XS', 'S', 'M', 'L', 'XL']
    colors = ['Red', 'Blue', 'Green', 'Black', 'White', 'Yellow', 'Purple', 'Orange']
    
    # Shirts category products
    shirts_category = next((cat for cat in categories if cat.name == 'Shirts'), None)
    if shirts_category:
        shirts_data = [
            {
                'name': 'Classic Oxford Shirt',
                'brand': 'Allen Solly',
                'description': 'A timeless oxford shirt crafted from premium cotton fabric. Features a button-down collar and a comfortable regular fit. Perfect for formal occasions or office wear.',
                'price': 1499.99,
                'color': 'White',
                'size': 'M'
            },
            {
                'name': 'Slim Fit Casual Shirt',
                'brand': 'H&M',
                'description': 'Modern slim-fit casual shirt with a subtle pattern. Made from soft, breathable cotton fabric that provides all-day comfort. Versatile enough to be worn for both casual and semi-formal occasions.',
                'price': 999.99,
                'color': 'Blue',
                'size': 'L'
            },
            {
                'name': 'Printed Casual Shirt',
                'brand': 'Jack & Jones',
                'description': 'Trendy printed casual shirt with a modern fit. Features a stylish pattern and is made from lightweight cotton blend fabric. Perfect for weekend outings or casual gatherings.',
                'price': 1299.99,
                'color': 'Green',
                'size': 'S'
            },
            {
                'name': 'Formal Business Shirt',
                'brand': 'Arrow',
                'description': 'Premium formal business shirt designed for the modern professional. Features a spread collar, double cuffs and is tailored from high-quality cotton for a sophisticated look and lasting comfort.',
                'price': 1799.99,
                'color': 'Light Blue',
                'size': 'XL'
            }
        ]
        
        for data in shirts_data:
            prod, _ = Product.objects.get_or_create(
                category=shirts_category,
                name=data['name'],
                defaults={
                    'slug': slugify(data['name']),
                    'brand': data['brand'],
                    'description': data['description'],
                    'price': data['price'],
                    'size': get_size_code(data['size']),
                    'color': data['color'],
                    'stock': random.randint(10, 50),
                    'available': True,
                    'image': 'products/default.png'
                }
            )
            products.append(prod)
    
    # Pants category products
    pants_category = next((cat for cat in categories if cat.name == 'Pants'), None)
    if pants_category:
        pants_data = [
            {
                'name': 'Slim Fit Jeans',
                'brand': 'Levi\'s',
                'description': 'Classic slim fit jeans with a modern cut. Made from premium denim that offers the perfect balance of comfort and durability. Features a five-pocket design and a zip fly with button closure.',
                'price': 2299.99,
                'color': 'Blue',
                'size': 'M'
            },
            {
                'name': 'Formal Trousers',
                'brand': 'Van Heusen',
                'description': 'Elegant formal trousers tailored for a refined silhouette. Made from a premium polyester-wool blend that offers comfort and a crisp look all day long. Perfect for office wear or formal occasions.',
                'price': 1699.99,
                'color': 'Black',
                'size': 'L'
            },
            {
                'name': 'Chino Pants',
                'brand': 'Gap',
                'description': 'Versatile chino pants that easily transition from casual to semi-formal settings. Made from soft cotton twill with a small amount of stretch for comfort. Features a flat front and a straight leg cut.',
                'price': 1599.99,
                'color': 'Khaki',
                'size': 'M'
            },
            {
                'name': 'Track Pants',
                'brand': 'Puma',
                'description': 'Comfortable track pants designed for an active lifestyle. Made from moisture-wicking fabric that keeps you dry during workouts. Features an elastic waistband with drawstring and side pockets.',
                'price': 1199.99,
                'color': 'Grey',
                'size': 'L'
            }
        ]
        
        for data in pants_data:
            prod, _ = Product.objects.get_or_create(
                category=pants_category,
                name=data['name'],
                defaults={
                    'slug': slugify(data['name']),
                    'brand': data['brand'],
                    'description': data['description'],
                    'price': data['price'],
                    'size': get_size_code(data['size']),
                    'color': data['color'],
                    'stock': random.randint(10, 50),
                    'available': True,
                    'image': 'products/default.png'
                }
            )
            products.append(prod)
    
    # Shoes category products
    shoes_category = next((cat for cat in categories if cat.name == 'Shoes'), None)
    if shoes_category:
        shoes_data = [
            {
                'name': 'Leather Oxford Shoes',
                'brand': 'Clarks',
                'description': 'Classic leather oxford shoes crafted from premium full-grain leather. Features a traditional lace-up design, leather lining and a durable outsole. Perfect for formal occasions and business wear.',
                'price': 3999.99,
                'color': 'Brown',
                'size': 'L'
            },
            {
                'name': 'Running Shoes',
                'brand': 'Nike',
                'description': 'High-performance running shoes designed for comfort and speed. Features responsive cushioning and a breathable mesh upper. Ideal for daily runs and training sessions.',
                'price': 4999.99,
                'color': 'Black',
                'size': 'M'
            },
            {
                'name': 'Casual Sneakers',
                'brand': 'Adidas',
                'description': 'Stylish casual sneakers that combine comfort and contemporary design. Features a canvas upper and rubber sole. Perfect for everyday wear and casual outings.',
                'price': 2499.99,
                'color': 'White',
                'size': 'L'
            },
            {
                'name': 'Leather Boots',
                'brand': 'Timberland',
                'description': 'Durable leather boots with waterproof construction. Features a padded collar for added comfort and a rugged outsole for excellent traction. Perfect for outdoor activities and casual wear.',
                'price': 5999.99,
                'color': 'Tan',
                'size': 'XL'
            }
        ]
        
        for data in shoes_data:
            prod, _ = Product.objects.get_or_create(
                category=shoes_category,
                name=data['name'],
                defaults={
                    'slug': slugify(data['name']),
                    'brand': data['brand'],
                    'description': data['description'],
                    'price': data['price'],
                    'size': get_size_code(data['size']),
                    'color': data['color'],
                    'stock': random.randint(10, 50),
                    'available': True,
                    'image': 'products/default.png'
                }
            )
            products.append(prod)
    
    # Add products for other categories
    for category in categories:
        if category.name not in ['Shirts', 'Pants', 'Shoes']:
            for i in range(4):
                name = f"{category.name} Item {i+1}"
                prod, _ = Product.objects.get_or_create(
                    category=category,
                    name=name,
                    defaults={
                        'slug': slugify(name),
                        'brand': f'Brand{i+1}',
                        'description': f'High-quality {category.name.lower()} product with premium features. Made from the finest materials to ensure durability and comfort. A must-have item for your collection.',
                        'price': 1000 + (i * 500),
                        'size': random.choice(sizes),
                        'color': random.choice(colors),
                        'stock': random.randint(10, 50),
                        'available': True,
                        'image': 'products/default.png'
                    }
                )
                products.append(prod)
    
    return products

# Helper function to convert size to size code
def get_size_code(size):
    size_map = {
        'XS': 'XS',
        'S': 'S',
        'M': 'M',
        'L': 'L',
        'XL': 'XL'
    }
    return size_map.get(size, 'M')

# Helper function to create slug
def slugify(name):
    return name.lower().replace(' ', '-')

# Create dummy addresses
def create_dummy_addresses(users):
    address_data = [
        {'type': 'home', 'street': '123 Main St', 'city': 'Mumbai', 'state': 'Maharashtra', 'postal_code': '400001'},
        {'type': 'work', 'street': '456 Park Avenue', 'city': 'Delhi', 'state': 'Delhi', 'postal_code': '110001'},
        {'type': 'home', 'street': '789 Garden Road', 'city': 'Bangalore', 'state': 'Karnataka', 'postal_code': '560001'},
        {'type': 'home', 'street': '101 Lake View', 'city': 'Chennai', 'state': 'Tamil Nadu', 'postal_code': '600001'},
        {'type': 'work', 'street': '202 Hill Street', 'city': 'Kolkata', 'state': 'West Bengal', 'postal_code': '700001'}
    ]
    
    for i, user in enumerate(users):
        data = address_data[i % len(address_data)]
        Address.objects.get_or_create(
            user=user, 
            address_type=data['type'], 
            street_address=data['street'], 
            city=data['city'], 
            state=data['state'], 
            postal_code=data['postal_code'], 
            is_default=True
        )

# Create dummy carts and cart items
def create_dummy_carts(users, products):
    for user in users:
        cart, _ = Cart.objects.get_or_create(user=user)
        selected_products = random.sample(products, min(3, len(products)))
        for prod in selected_products:
            CartItem.objects.get_or_create(
                cart=cart, 
                product=prod, 
                defaults={'quantity': random.randint(1, 3)}
            )

# Create dummy orders and order items
def create_dummy_orders(users, products):
    status_choices = ['pending', 'processing', 'shipped', 'delivered']
    
    for user in users:
        # Create 1-3 orders per user
        for _ in range(random.randint(1, 3)):
            # Select random products for the order
            order_products = random.sample(products, min(4, len(products)))
            total_amount = 0
            
            # Calculate total amount
            for prod in order_products:
                quantity = random.randint(1, 3)
                total_amount += prod.price * quantity
            
            # Create the order
            order = Order.objects.create(
                user=user, 
                address=f"{user.username}'s Address, City, State, 12345", 
                phone=f"99{random.randint(10000000, 99999999)}", 
                total_amount=total_amount, 
                status=random.choice(status_choices)
            )
            
            # Create order items
            for prod in order_products:
                quantity = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order, 
                    product=prod, 
                    quantity=quantity, 
                    price=prod.price
                )

def run():
    users = create_dummy_users()
    categories = create_dummy_categories()
    products = create_dummy_products(categories)
    create_dummy_addresses(users)
    create_dummy_carts(users, products)
    create_dummy_orders(users, products)
    print('Dummy data created successfully.')
