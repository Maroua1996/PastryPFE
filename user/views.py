from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from blog_pastry.models import Article
from quiz.models import Résultat

from .form import *
# Create your views here.
from .models import Follow, User
from notification.models import Notification

from .decorator import not_logged_required

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@not_logged_required
def login_user(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Wrong credentials")

    context = {
        "form": form
    }
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@not_logged_required
def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


@login_required(login_url='login')
def profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=account)
    user_articles = Article.objects.filter(user=request.user)
    user_quiz_results = Résultat.objects.filter(user=request.user)
    print(user_quiz_results)

   
    if request.method == 'POST':
        if request.user.pk != account.pk:
            return redirect('home')
        form = UserProfileUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            print(form.errors)
        

    context = {
        'account': account,
        'form': form,
        'user_articles': user_articles,
        'user_quiz_results': user_quiz_results
      
       
        
    }
    return render(request, 'profile.html', context)

def change_profile_picture(request):
    if request.method == 'POST':
        image = request.FILES.get('profile_image')

        if image:
            user = request.user
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            user.image = filename
            user.save()
            return redirect('profile')
        else:
            return JsonResponse({'error': 'No image file provided.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)




def user_information_view(request, username):
    account = get_object_or_404(User, username=username)
    muted = None 
    following = False
    

    if request.user.is_authenticated:
        if  request.user.id == account.id:
            return redirect('profile')
        followers = account.user_followers.filter(follower_id = request.user.id)
        if followers.exists():
            following = True
    if following:
        query = followers.first()
        if query.muted:
            muted = True
        else:
            muted = False

    context = {
        'account': account,
        'following': following,
        'muted': muted
    }
    return render(request, 'information_user.html', context)

@login_required(login_url='login')
def follow_or_not(request,user_id):
    followed = get_object_or_404(User, id=user_id)
    follower = get_object_or_404(User, id=request.user.id)


    follow,created = Follow.objects.get_or_create(
        follower=follower,
        followed=followed
    )

    if created :
        followed.followers.add(follow)
    
    else:
        followed.followers.remove(follow)
        follow.delete()
    
    return redirect('user_information_view', username=followed.username)

@login_required(login_url='login')
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_seen=False).order_by('-create_date')

    for notification in notifications:
        notification.is_seen = True
        notification.save()
    return render(request, 'notifications.html')


@login_required(login_url='login')
def mute_or_not(request, user_id):
    user = get_object_or_404(User, id=user_id)
    follower = get_object_or_404(User, id=request.user.id)
    instance = get_object_or_404(Follow, follower=follower, followed=user)
    if instance.muted:
        instance.muted = False
        instance.save()
    else:
        instance.muted = True
        instance.save()
    
    return redirect('user_information_view', username=user.username)

@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        # Supprimez l'utilisateur actuellement connecté
        request.user.delete()
        # Déconnectez l'utilisateur
        logout(request)
        # Redirigez l'utilisateur vers la page d'inscription ou toute autre page souhaitée
        return redirect('register')  # Assurez-vous d'ajuster la redirection en fonction de votre configuration

    return render(request, 'profile.html')