#!/usr/bin/env bash
# exit on error
set -o errexit

# Ensure we're using the correct settings
export DJANGO_SETTINGS_MODULE=ecommerce.production_settings

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Checking for unapplied migrations..."
python manage.py showmigrations

echo "Applying migrations with specific settings module..."
python manage.py migrate --settings=ecommerce.production_settings --noinput

echo "Creating superuser if it doesn't exist..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Password@123')
    print('Superuser created successfully');
else:
    print('Superuser already exists')
"

echo "Creating initial data for store..."
python manage.py shell -c "
from store.models import Category, Product;
if Category.objects.count() == 0:
    # Create categories
    cat1 = Category.objects.create(name='Clothing')
    cat2 = Category.objects.create(name='Footwear') 
    cat3 = Category.objects.create(name='Accessories')
    
    # Create some products
    Product.objects.create(
        name='Basic T-shirt',
        category=cat1,
        description='Comfortable cotton T-shirt',
        price=19.99,
        stock=100,
        is_available=True
    )
    
    Product.objects.create(
        name='Running Shoes',
        category=cat2,
        description='Lightweight running shoes',
        price=49.99,
        stock=50,
        is_available=True
    )
    
    Product.objects.create(
        name='Leather Belt',
        category=cat3,
        description='Premium leather belt',
        price=29.99,
        stock=30,
        is_available=True
    )
    
    print('Created initial categories and products')
else:
    print('Categories already exist, skipping data creation')
" 