from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import House, Amenity, HouseImage, UserProfile
from .forms import HouseForm, HouseImageForm, UserProfileForm
from django import forms
@login_required
def dashboard(request):
    houses = House.objects.filter(admin=request.user)
    return render(request, 'core/dashboard.html', {'houses': houses})

@login_required
def add_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)
        files = request.FILES.getlist('images')
        
        if form.is_valid():
            house = form.save(commit=False)
            house.admin = request.user
            house.save()
            
            # Process amenities from text input
            amenities_text = form.cleaned_data.get('amenities_text', '')
            if amenities_text:
                amenity_names = [name.strip() for name in amenities_text.split(',')]
                for name in amenity_names:
                    if name:
                        amenity, created = Amenity.objects.get_or_create(name=name)
                        house.amenities.add(amenity)
            
            # Save images
            for f in files[:10]:
                HouseImage.objects.create(house=house, image=f)
            return redirect('dashboard')
    else:
        form = HouseForm()
    
    return render(request, 'core/add_house.html', {'form': form})

@login_required
def edit_house(request, house_id):
    house = get_object_or_404(House, id=house_id, admin=request.user)
    
    if request.method == 'POST':
        form = HouseForm(request.POST, instance=house)
        files = request.FILES.getlist('images')
        
        if form.is_valid():
            form.save()
            
            # Process amenities from text input
            house.amenities.clear()  # Remove existing amenities
            amenities_text = form.cleaned_data.get('amenities_text', '')
            if amenities_text:
                amenity_names = [name.strip() for name in amenities_text.split(',')]
                for name in amenity_names:
                    if name:
                        amenity, created = Amenity.objects.get_or_create(name=name)
                        house.amenities.add(amenity)
            
            # Add new images
            for f in files:
                if HouseImage.objects.filter(house=house).count() < 10:
                    HouseImage.objects.create(house=house, image=f)
            return redirect('dashboard')
    else:
        # Populate the amenities field with existing amenities
        existing_amenities = ", ".join([amenity.name for amenity in house.amenities.all()])
        form = HouseForm(instance=house, initial={'amenities_text': existing_amenities})
    
    return render(request, 'core/edit_house.html', {
        'form': form,
        'house': house,
        'images': HouseImage.objects.filter(house=house)
    })
@login_required
def delete_house(request, house_id):
    house = get_object_or_404(House, id=house_id, admin=request.user)
    if request.method == 'POST':
        house.delete()
        return redirect('dashboard')
    return render(request, 'core/delete_house.html', {'house': house})

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(HouseImage, id=image_id, house__admin=request.user)
    if request.method == 'POST':
        image.delete()
        return redirect('edit_house', house_id=image.house.id)
    return render(request, 'core/delete_image.html', {'image': image})

@login_required
def profile_settings(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_settings')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'core/profile_settings.html', {'form': form})

# core/views.py
@login_required
def add_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            house = form.save(commit=False)
            house.admin = request.user
            house.save()
            form.save_m2m()  # Crucial for saving amenities
            
            # Limit to 10 images
            for f in files[:10]:
                HouseImage.objects.create(house=house, image=f)
            return redirect('dashboard')
    else:
        form = HouseForm()
    return render(request, 'core/add_house.html', {'form': form})