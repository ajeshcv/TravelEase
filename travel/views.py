from django.shortcuts import render,get_object_or_404, redirect
from .models import Place, Package, PackageImage
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, PackageForm
from django.contrib.auth.decorators import login_required
from .models import PackagerProfile
from .forms import PackagerProfileForm, CustomerProfileForm
from .models import  PackagerProfile
from .models import Review
from .forms import ReviewForm
from .models import Hotel
from .models import Package, Booking
from .forms import BookingForm
from.forms import GalleryImageForm
from.models import GalleryImage
from .models import FAQ
from .forms import FAQForm
from .forms import CustomPasswordChangeForm
from .models import PackagerProfile, ChatMessage
from .forms import ChatForm
from django.db.models import Q
from travel.models import CustomUser
from django.contrib.auth import update_session_auth_hash


def home(request):
    places = Place.objects.all()[:3]
    packages = Package.objects.all()[:3]
    packagers = PackagerProfile.objects.all()[:4]
    reviews = Review.objects.all().order_by('-created_at')[:3]
    hotels = Hotel.objects.all()[:3] 
    return render(request, 'travel/home.html', {
        'places': places,
        'packages': packages,
        'packagers': packagers,
        'reviews': reviews,
        'hotels': hotels,
    })


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            if user.user_type == 'packager':
                user.is_approved = False
                messages.success(request, 'Your account needs admin approval before you can log in.')
                document = form.cleaned_data['document']
                user.document = document 
                user.save()

            user.save()

            if user.user_type == 'customer':
                login(request, user)
                return redirect('home')

            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'travel/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.user_type == 'packager' and not user.is_approved:
                messages.error(request, 'Your account is not approved yet. Please wait for admin approval.')
                return redirect('login')

            login(request, user)
            if user.user_type == 'packager':
                return redirect('packager_dashboard') 
            return redirect('home')  

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'travel/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')  


@login_required
def user_profile(request):
    if request.user.user_type != 'customer':
        return redirect('home')

    profile = getattr(request.user, 'customer_profile', None)
    bookings = Booking.objects.filter(user=request.user)

    faqs = FAQ.objects.filter(user=request.user).order_by('-created_at')[:5]

    return render(request, 'travel/user_profile.html', {
        'profile': profile,
        'bookings': bookings,
        'faqs': faqs, 
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            
            if user.user_type == 'packager':
                return redirect('packager_dashboard')
            else:
                return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'travel/change_password.html', {'form': form})


@login_required
def ask_faq(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.user = request.user 
            faq.save()
            return redirect('view_faqs') 
    else:
        form = FAQForm()
    return render(request, 'travel/ask_faq.html', {'form': form})


@login_required
def view_faqs(request):
    faqs = FAQ.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'travel/view_faqs.html', {'faqs': faqs})


@login_required
def create_customer_profile(request):
    if request.user.user_type != 'customer':
        return redirect('home')

    if hasattr(request.user, 'customer_profile'):
        return redirect('user_profile') 

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('user_profile')
    else:
        form = CustomerProfileForm()

    return render(request, 'travel/create_customer_profile.html', {'form': form})


@login_required
def edit_customer_profile(request):
    if request.user.user_type != 'customer':
        return redirect('home')

    profile = getattr(request.user, 'customer_profile', None)
    if not profile:
        return redirect('create_customer_profile')

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = CustomerProfileForm(instance=profile)

    return render(request, 'travel/edit_customer_profile.html', {'form': form})


@login_required
def write_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('user_profile')
    else:
        form = ReviewForm()

    return render(request, 'travel/write_review.html', {'form': form})


def review_section(request):
    reviews = Review.objects.select_related('user').order_by('-created_at')[:3]
    return render(request, 'travel/review_section.html', {'reviews': reviews})


def all_reviews(request):
    reviews = Review.objects.select_related('user').order_by('-created_at')
    return render(request, 'travel/all_reviews.html', {'reviews': reviews})


@login_required
def packager_dashboard(request):
    if request.user.user_type != 'packager':
        return redirect('home')

    bookings = Booking.objects.filter(package__packager=request.user)
    packages = Package.objects.filter(packager=request.user)
    chat_users = ChatMessage.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    users_with_chats = CustomUser.objects.filter(id__in=chat_users)
    return render(request, 'travel/packager_dashboard.html', {
        'packages': packages,
        'bookings': bookings,
        'users_with_chats': users_with_chats,
    })


@login_required
def add_package(request):
    if request.user.user_type != 'packager':
        return redirect('home')

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, initial={'user': request.user})
        images = request.FILES.getlist('images') 
        if form.is_valid():
            package = form.save(commit=False)
            package.packager = request.user
            package.save()

            for image in images:
                extra_image = PackageImage.objects.create(image=image)
                package.extra_images.add(extra_image)

            messages.success(request, 'Package added successfully!')
            return redirect('packager_dashboard')
    else:
        form = PackageForm(initial={'user': request.user}) 

    return render(request, 'travel/add_package.html', {'form': form})


@login_required
def edit_package(request, pk):
    package = get_object_or_404(Package, pk=pk, packager=request.user)

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        images = request.FILES.getlist('images') 
        if form.is_valid():
            package = form.save()

            for image in images:
                extra_image = PackageImage.objects.create(image=image)
                package.extra_images.add(extra_image)

            messages.success(request, 'Package updated successfully!')
            return redirect('packager_dashboard')
    else:
        form = PackageForm(instance=package)

    return render(request, 'travel/edit_package.html', {'form': form, 'package': package})


@login_required
def delete_package(request, pk):
    package = get_object_or_404(Package, pk=pk, packager=request.user)
    package.delete()
    messages.success(request, 'Package deleted successfully!')
    return redirect('packager_dashboard')


@login_required
def create_profile(request):
    if request.user.user_type != 'packager':
        return redirect('home')

    if hasattr(request.user, 'packager_profile'):
        return redirect('packager_dashboard')

    if request.method == 'POST':
        form = PackagerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            profile.phone_number = request.user.phone_number if hasattr(request.user, 'phone_number') else ''
            profile.email = request.user.email

            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('packager_dashboard')
    else:
        form = PackagerProfileForm()

    return render(request, 'travel/create_profile.html', {'form': form})


@login_required
def edit_profile(request):
    if request.user.user_type != 'packager':
        return redirect('home')

    profile = getattr(request.user, 'packager_profile', None)
    if not profile:
        return redirect('create_profile')

    if request.method == 'POST':
        form = PackagerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('packager_dashboard')
    else:
        form = PackagerProfileForm(instance=profile)

    return render(request, 'travel/edit_profile.html', {'form': form})


@login_required
def view_profile(request):
    if request.user.user_type != 'packager':
        return redirect('home')

    profile = getattr(request.user, 'packager_profile', None)
    if not profile:
        return redirect('create_profile')

    return render(request, 'travel/view_profile.html', {'profile': profile})


@login_required
def packager_detail(request, packager_id):
    packager = get_object_or_404(PackagerProfile, id=packager_id)
    packages = packager.get_packages()
    return render(request, 'travel/packager_detail.html', {'packager': packager, 'packages': packages})


def all_packagers(request):
    packagers = PackagerProfile.objects.all()
    return render(request, 'travel/all_packagers.html', {'packagers': packagers})


def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    extra_images = place.extra_images.all() 
    return render(request, 'travel/place_detail.html', {
        'place': place,
        'extra_images': extra_images,
    })


def all_places(request):
    places = Place.objects.all() 
    return render(request, 'travel/all_places.html', {'places': places})


def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, 'travel/package_detail.html', {'package': package})


def all_packages(request):
    packages = Package.objects.all()
    return render(request, 'travel/all_packages.html', {'packages': packages})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    extra_images = hotel.extra_images.all()  
    return render(request, 'travel/hotel_detail.html', {
        'hotel': hotel,
        'extra_images': extra_images, 
    })


def all_hotels(request):
    hotels = Hotel.objects.all() 
    return render(request, 'travel/all_hotels.html', {'hotels': hotels})


def about_us(request):
    return render(request, 'travel/about_us.html')


def whats_new(request):
    return render(request, 'travel/whatsnew.html')

def technical_support(request):
    return render(request, 'travel/technical_support.html')


def faq(request):
    return render(request, 'travel/faq.html')

def privacy_policy(request):
    return render(request, 'travel/privacy_policy.html')


def terms_use(request):
    return render(request, 'travel/terms_use.html')

def trust_security(request):
    return render(request, 'travel/trust_security.html')


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect('gallery') 
    else:
        form = GalleryImageForm()
    return render(request, 'travel/upload_image.html', {'form': form})


def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'travel/gallery.html', {'images': images})


@login_required
def book_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.total_price = package.price * booking.num_travelers
            booking.save()
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('user_profile')
    else:
        form = BookingForm()
 
    return render(request, 'travel/book_package.html', {'form': form, 'package': package})


@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, package__packager=request.user)
    booking.status = 'accepted'

    payment_link = f"/pay/{booking.id}/"
    booking.payment_link = payment_link
    booking.save()

    messages.success(request, 'Booking accepted and payment link is now available for the customer.')
    return redirect('packager_dashboard')


@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, package__packager=request.user)
    booking.status = 'rejected'
    booking.save()
    messages.success(request, 'Booking rejected successfully!')
    return redirect('packager_dashboard')


@login_required
def start_chat(request, packager_id):
    packager = get_object_or_404(PackagerProfile, id=packager_id)

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user
            chat_message.receiver = packager.user 
            chat_message.save()
            return redirect('chat_view', packager.user.id) 

    else:
        form = ChatForm()

    return render(request, 'travel/start_chat.html', {'form': form, 'packager': packager})


@login_required
def chat_view(request, user_id):  
    other_user = get_object_or_404(CustomUser, id=user_id)
    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    form = ChatForm()
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            return redirect('chat_view', user_id)
    return render(request, 'travel/chat_view.html', {'messages': messages, 'form': form, 'other_user':other_user})


@login_required
def my_chats(request):
    chat_packagers = ChatMessage.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    packagers_with_chats = CustomUser.objects.filter(id__in=chat_packagers, user_type='packager') 

    return render(request, 'travel/my_chats.html', {'packagers_with_chats': packagers_with_chats})


@login_required
def users_chats(request):
    chat_customers = ChatMessage.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    customers_with_chats = CustomUser.objects.filter(id__in=chat_customers, user_type='customer')

    return render(request, 'travel/users_chats.html', {'customers_with_chats': customers_with_chats})