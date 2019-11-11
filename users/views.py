from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .token_generator import account_activation_token
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from users.models import Profile

User = get_user_model()


def register(request):
    """Send Email to confirm validate user"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('users/account_activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        form = UserRegisterForm()
    return render(request, 'users/login.html', {'form': form})


def activate_account(request, uidb64, token):
    """Activate the account for the user using token and uid"""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


def users_list(request):
    """TO list all friends of a user"""
    users = Profile.objects.exclude(user=request.user)
    context = {
        'users': users
    }
    return render(request, "home.html", context)


def profile(request):
    """Profile to view the profile"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            msg = 'Your account has been successfully updated!'
            messages.success(request, msg)
            return render(request, 'users/profile.html', dict(u_form=u_form, p_form=p_form))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
        return render(request, 'users/profile.html', dict(u_form=u_form, p_form=p_form))


def search(request):
    """Search feature used to search friends """
    if request.method == 'GET':
        query = request.GET.get('q')
        if query is not None:
            results = User.objects.filter(username=query)
            return render(request, 'users/search.html', {'results': results})
        else:
            context = {
                'results': "Not found",
            }
            return render(request, 'users/search.html', context)
    else:
        return render(request, 'base.html')


def search_profile(request, pk):
    """User search Profile"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            msg = 'Your account has been successfully updated!'
            messages.success(request, msg)
            return render(request, 'users/profile.html', dict(u_form=u_form, p_form=p_form))
    else:
        return render(request, 'users/search_profile.html')


def profileDetail(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = dict(first_name=user.first_name,
                   last_name=user.last_name,
                   dateofbirth=user.dateofbirth,
                   email=user.email,
                   username=user.username
                   )
    return render(request, 'users/search_profile.html', context)
