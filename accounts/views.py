from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Address

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('store:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('store:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('store:home')

@login_required
def profile(request):
    user_profile = request.user.profile
    addresses = request.user.addresses.all()
    context = {
        'profile': user_profile,
        'addresses': addresses
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        # Update user info
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        # Update profile info
        profile.phone = request.POST.get('phone')
        profile.gender = request.POST.get('gender')
        profile.date_of_birth = request.POST.get('date_of_birth')
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/edit_profile.html')

@login_required
def address_list(request):
    addresses = request.user.addresses.all()
    return render(request, 'accounts/address_list.html', {'addresses': addresses})

@login_required
def add_address(request):
    # Create an empty address object with default values to avoid template errors
    from .models import Address
    
    if request.method == 'POST':
        # Get form data with fallbacks for required fields
        address_type = request.POST.get('address_type', 'home')
        street_address = request.POST.get('street_address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        postal_code = request.POST.get('postal_code', '')
        is_default = request.POST.get('is_default') == 'on'
        
        # Validate required fields
        if not all([address_type, street_address, city, state, postal_code]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'accounts/add_address.html', {'address': Address()})
        
        # Create address
        Address.objects.create(
            user=request.user,
            address_type=address_type,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            is_default=is_default
        )
        messages.success(request, 'Address added successfully!')
        return redirect('accounts:address_list')
    
    # Provide an empty address object for the template
    address = Address()
    address.id = None  # Explicitly set id to None to avoid template errors
    
    return render(request, 'accounts/add_address.html', {'address': address})

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        # Get form data with fallbacks for required fields
        address_type = request.POST.get('address_type', 'home')
        street_address = request.POST.get('street_address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        postal_code = request.POST.get('postal_code', '')
        is_default = request.POST.get('is_default') == 'on'
        
        # Validate required fields
        if not all([address_type, street_address, city, state, postal_code]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'accounts/add_address.html', {'address': address})
        
        # Update address
        address.address_type = address_type
        address.street_address = street_address
        address.city = city
        address.state = state
        address.postal_code = postal_code
        address.is_default = is_default
        address.save()
        
        messages.success(request, 'Address updated successfully!')
        return redirect('accounts:address_list')
    
    return render(request, 'accounts/add_address.html', {'address': address})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('accounts:address_list')

@login_required
def set_default_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, 'Default address updated successfully!')
    return redirect('accounts:address_list')