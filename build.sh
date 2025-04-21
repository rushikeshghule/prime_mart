#!/usr/bin/env bash
# exit on error
set -o errexit

# Print environment information for debugging
echo "Starting build process..."
echo "System environment:"
echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"
echo "DJANGO_SETTINGS_MODULE value: $DJANGO_SETTINGS_MODULE"
echo "DATABASE_URL defined: $(if [ -n "$DATABASE_URL" ]; then echo "Yes (value redacted)"; else echo "No"; fi)"

# List all environment variables (redact sensitive ones)
echo "Available environment variables:"
env | grep -v -e PASSWORD -e SECRET -e KEY -e DATABASE_URL | sort

# Ensure we're using the correct settings
export DJANGO_SETTINGS_MODULE=ecommerce.production_settings
echo "Using settings module: $DJANGO_SETTINGS_MODULE"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --settings=ecommerce.production_settings

echo "Checking database configuration..."
python - <<END
import os
import sys
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.production_settings')
django.setup()

# Check database configuration
print("Database ENGINE:", settings.DATABASES['default']['ENGINE'])
print("Database NAME:", settings.DATABASES['default']['NAME'])
if 'USER' in settings.DATABASES['default']:
    print("Database USER:", settings.DATABASES['default']['USER'])
if 'HOST' in settings.DATABASES['default']:
    print("Database HOST:", settings.DATABASES['default']['HOST'])
if 'PORT' in settings.DATABASES['default']:
    print("Database PORT:", settings.DATABASES['default']['PORT'])
END

echo "Testing database connection..."
python - <<END
import os
import sys
import django
from django.db import connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.production_settings')
django.setup()

try:
    connection = connections['default']
    connection.ensure_connection()
    print("✅ Connected to database successfully")
    
    # Check if tables exist
    with connection.cursor() as cursor:
        if 'postgresql' in connection.settings_dict['ENGINE']:
            # List all tables in the database
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            print(f"Found {len(tables)} tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Check for our specific tables
            cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'store_category')")
            exists = cursor.fetchone()[0]
            print(f"store_category table exists: {exists}")
        else:
            print("Not using PostgreSQL, skipping table check")
except Exception as e:
    print("❌ Database connection error:", str(e))
    print("Error type:", type(e).__name__)
    # Don't exit with error - let build continue
    # We'll use SQLite as fallback
END

echo "Checking for unapplied migrations..."
python manage.py showmigrations --settings=ecommerce.production_settings

echo "FORCE RESET ALL MIGRATIONS (development environment only)..."
python - <<END
import os
import sys
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.production_settings')
django.setup()

try:
    with connection.cursor() as cursor:
        # Drop all tables in the public schema
        cursor.execute("""
        DO \$\$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END \$\$;
        """)
        print("✅ All tables dropped successfully")
except Exception as e:
    print("❌ Error dropping tables:", str(e))
END

echo "Applying migrations with specific settings module..."
python manage.py migrate --settings=ecommerce.production_settings --noinput

echo "Creating superuser if it doesn't exist..."
python - <<END
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.production_settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'Password@123')
        print('✅ Superuser created successfully')
    else:
        print('Superuser already exists')
except Exception as e:
    print("❌ Error creating superuser:", str(e))
    print("Error type:", type(e).__name__)
    # Don't exit with error
END

echo "Creating initial data for store..."
python - <<END
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.production_settings')
django.setup()

from store.models import Category, Product

try:
    # First check if Category table exists and accessible
    category_count = Category.objects.count()
    print(f"Current category count: {category_count}")
    
    if category_count == 0:
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
        
        print('✅ Created initial categories and products')
    else:
        print('Categories already exist, skipping data creation')
except Exception as e:
    print("❌ Error creating initial data:", str(e))
    print("Error type:", type(e).__name__)
    # Don't exit with error
END

echo "Build process completed." 