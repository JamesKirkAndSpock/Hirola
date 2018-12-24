from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import *
from django.views import generic
from django.core.cache import cache
from .forms.user_forms import (
    UserCreationForm, AuthenticationForm, UserForm, OldPasswordForm, ChangeEmailForm,
    EmailAuthenticationForm)
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from .token import account_activation_token, email_activation_token
from .decorators import (
    old_password_required, remember_user, is_change_allowed_required)
from django.utils import timezone


def page_view(request):
    (phone_categories, social_media) = various_caches()
    deals = cache.get('hot_deals') or set_cache(
        HotDeal.objects.all(), 'hot_deals')
    hot_deals = []
    for deal in deals:
        colors_list = PhonesColor.objects.all()
        for color in colors_list:
            if color.is_in_stock and color.quantity >= 1:
                in_stock_id = color.phone
                if str(in_stock_id) == str(deal.item):
                    hot_deals.append(deal)
    context = {'categories': phone_categories, 'social_media': social_media, 'hot_deals': list(set(hot_deals))}
    return render(request, 'front/landing_page.html', context)


def phone_category_view(request, category_id):
    phones_list = cache.get('phones_{}'.format(category_id)) or set_cache(
        PhoneList.objects.filter(category=category_id),
        'phones_{}'.format(category_id))
    phones = []
    for phone_object in phones_list:
        pk = phone_object.pk
        colors_list = PhonesColor.objects.filter(phone=pk)
        for color in colors_list:
            if color.is_in_stock and color.quantity >= 1:
                existing_id = color.phone
                if str(existing_id) == str(phone_object.phone_name):
                    phones.append(phone_object)
    # print(phones[1].currency, '****************')
    return shared_phone_view(request, list(set(phones)), category_id)


def phone_category_size_view(request, category_id, size):
    phones = PhoneList.objects.filter(category=category_id, size_sku=size)
    size_obj = PhoneMemorySize.objects.get(pk=size)
    size_message = "with a size of " + str(size_obj)
    return shared_phone_view(request, phones, category_id, size_message)


def shared_phone_view(request, phones, category_id, message=""):
    category_pk = cache.get('category_{}'.format(category_id)) or set_cache(
        PhoneCategory.objects.get(pk=category_id),
        'category_{}'.format(category_id))
    (phone_categories, social_media) = various_caches()
    sizes = cache.get('sizes_{}'.format(category_id)) or set_cache(
        PhoneMemorySize.objects.filter(category=category_id).order_by('size_number'),
        'sizes_{}'.format(category_id))
    context = {'categories': phone_categories, 'phones': phones,
               'category': category_pk, 'category_id': category_id,
               'size_message': message, 'sizes': sizes, "social_media": social_media}
    print(context.get('phones')[1].currency, '*****')
    return render(request, 'front/phone_category.html', context)


def set_cache(data, cache_name):
    cache.set(cache_name, data)
    return data


def sizes(request):
    sizes = PhoneMemorySize.objects.all()
    list_sizes = {}
    size_key = 1
    size_id = 0
    for size in sizes:
        list_sizes[size_key] = size.category
        size_key += 1
    if request.GET["id"] == "":
        filtered_sizes = PhoneMemorySize.objects.filter(category=None)
    else:
        filtered_sizes = PhoneMemorySize.objects.filter(
            category=request.GET["id"])
        if PhoneList.objects.filter(pk=request.GET["id"]).first():
            size_id = PhoneList.objects.filter(pk=request.GET["id"]).first().size_sku.pk
    data = {}
    for size in filtered_sizes:
        data[size.pk] = str(size)
    data = {"size_id": size_id, "data": data}
    return JsonResponse(data)


def country_codes(request):
    country_code_data = CountryCode.objects.all()
    users_country_code = request.user.country_code.id
    data = {}
    for country_code in country_code_data:
        data[country_code.pk] = str(country_code)
    data = {"users_country_code": users_country_code, "data": data}
    return JsonResponse(data)


def phone_profile_view(request, phone_id):
    if request.method == "POST":
        item = request.POST['cart_item_add']
        return redirect("/checkout")
    phone = PhoneList.objects.filter(pk=phone_id).first()
    colors_list = PhonesColor.objects.filter(phone=phone_id)
    colors = []
    for color in colors_list:
        if color.is_in_stock:
            colors.append(color)
    if not phone:
        return redirect("/error")
    context = {"phone": phone, "colors": colors, "image_list": phone.phone_images.all(),
               "customer_reviews": phone.phone_reviews.all(),
               "features": phone.phone_features.all(), "infos": phone.phone_information.all()}
    return render(request, 'front/phone_profile.html', context)


def phone_view(request):
    return render(request, 'front/phone.html')


def reset_password_view(request):
    return render(request, 'front/reset_password.html')


def new_password_view(request):
    return render(request, 'front/new_password.html')


def checkout_view(request):
    return render(request, 'front/checkout.html')


@login_required
def dashboard_view(request):
    (phone_categories, social_media) = various_caches()
    orders = Order.objects.filter(owner=request.user.pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            redirect("/dashboard")
        user = User.objects.get(email=request.user.email)
        context = {"form": form, "user": user, 'categories': phone_categories,
                   "social_media": social_media, 'orders':orders}
        return render(request, 'front/dashboard.html', context=context)
    context = {"form": UserForm(instance=request.user),
               "reviews": Review.objects.filter(owner=request.user),
               'categories': phone_categories, "social_media": social_media, 'orders': orders}
    return render(request, 'front/dashboard.html', context=context)


@remember_user
def login_view(request):
    (phone_categories, social_media) = various_caches()
    if request.method == "POST":
        form = AuthenticationForm(None, request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if form.is_valid() and user is not None:
            login(request, user)
            return redirect('/')
        args = {'form':  form, 'social_media': social_media, 'categories': phone_categories}
        return render(request, 'front/login.html', args)
    args = {'form':  AuthenticationForm(), 'social_media': social_media,
            'categories': phone_categories}
    return render(request, 'front/login.html', args)


def logout_view(request):
    logout(request)


def about_view(request):
    (phone_categories, social_media) = various_caches()
    context = {"categories": phone_categories, "social_media": social_media}
    return render(request, 'front/about.html', context=context)


def signup_view(request):
    (phone_categories, social_media) = various_caches()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            form.send_email(request, user)
            return render(request, 'registration/signup_email_sent.html')
        args = {'form':  form, 'social_media': social_media, 'categories': phone_categories}
        return render(request, 'front/signup.html', args)
    else:
        args = {'form':  UserCreationForm(), 'social_media': social_media,
                'categories': phone_categories}
        return render(request, 'front/signup.html', args)


def activate(request, uidb64, token):
    user = UserCreationForm().get_user(uidb64)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/dashboard')
    return render(request, 'registration/signup_activation_invalid.html')


def imei_view(request):
    return render(request, 'front/imei.html')


class PasswordResetViewTailored(PasswordResetView):

    success_url = reverse_lazy('password_reset_done', urlconf='front.urls')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = cache.get('phone_categories') or set_cache(
            PhoneCategory.objects.all(),
            'phone_categories')
        context['social_media'] = cache.get('social_media') or set_cache(
            SocialMedia.objects.all(), 'social_media')
        return context


class PasswordResetConfirmViewTailored(PasswordResetConfirmView):

    success_url = reverse_lazy('password_reset_complete', urlconf='front.urls')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        (context['categories'], context['social_media']) = various_caches()
        return context


@login_required
@old_password_required
def change_password_view(request):
    (phone_categories, social_media) = various_caches()
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(email=request.user.email)
            user.is_change_allowed = False
            user.save()
            return redirect('/login')
        args = {"form": form, 'social_media': social_media, 'categories': phone_categories}
        return render(request, 'front/change_password.html', args)
    args = {"form": SetPasswordForm(request.user), 'social_media': social_media,
            'categories': phone_categories}
    return render(request, 'front/change_password.html', args)


@login_required
def old_password_view(request):
    (phone_categories, social_media) = various_caches()
    if request.method == 'POST':
        form = OldPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.user.email)
            user.is_change_allowed = True
            user.save()
            return redirect('/change_password')
        args = {'form':  form, 'social_media': social_media, 'categories': phone_categories}
        return render(request, 'front/old_password.html', args)
    args = {"form": OldPasswordForm(request.user), 'social_media': social_media,
            'categories': phone_categories}
    return render(request, 'front/old_password.html', args)


@login_required
def confirm_user_view(request):
    (phone_categories, social_media) = various_caches()
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if form.is_valid() and user is not None:
            user = User.objects.get(email=request.user.email)
            user.is_change_allowed = True
            user.save()
            return redirect('/change_email')
        args = {'form':  form, 'social_media': social_media, 'categories': phone_categories}
        return render(request, 'front/confirm_user.html', args)
    args = {"form": EmailAuthenticationForm(), 'social_media': social_media,
            'categories': phone_categories}
    return render(request, 'front/confirm_user.html', args)


@login_required
@is_change_allowed_required
def change_email_view(request):
    (phone_categories, social_media) = various_caches()
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, instance=request.user)
        user = User.objects.get(email=request.user.email)
        if form.is_valid() and user is not None:
            user.is_change_allowed = False
            user.change_email = form.cleaned_data.get('email')
            user.change_email_tracker = timezone.now()
            user.save()
            form.send_email(request, user)
            return render(request, 'front/change_email_sent.html')
        args = {"form": form, 'social_media': social_media, 'categories': phone_categories}
        return render(request, 'front/change_email.html', args)
    args = {"form": ChangeEmailForm(), 'social_media': social_media,
            'categories': phone_categories}
    return render(request, 'front/change_email.html', args)


def activate_new_email(request, uidb64, token):
    user = UserCreationForm().get_user(uidb64)
    if user is not None and email_activation_token.check_token(user, token):
        user.former_email = user.email
        user.email = user.change_email
        user.change_email = None
        user.is_change_allowed = True
        user.change_email_tracker = None
        user.save()
        return redirect('/dashboard')
    return render(request, 'registration/signup_activation_invalid.html')


def various_caches():
    phone_categories = cache.get('phone_categories') or set_cache(
        PhoneCategory.objects.all(),
        'phone_categories')
    social_media = cache.get('social_media') or set_cache(
        SocialMedia.objects.all(), 'social_media')
    return (phone_categories, social_media)


def press_view(request):
    news = NewsItem.objects.all()
    context = {'news': news}
    return render(request, 'front/news_press.html', context)


def help_view(request):
    return render(request, 'front/help.html')


def teke_vs_others_view(request):
    return render(request, 'front/teke_vs_others.html')


def error_view(request):
    return render(request, 'front/error.html')


def review_view(request):
    return render(request, 'front/review.html')


def review_submit_view(request):
    return render(request, 'front/review_submit.html')


def privacy_view(request):
    return render(request, 'front/privacy.html')


def search_view(request):
    if request.method == "POST":
        search_name = request.POST.get("search-name")
        results = list(PhoneList.objects.filter(phone_name__icontains=search_name))
        results += list(PhoneList.objects.filter(category__phone_category__icontains=search_name))
        results += list(PhoneList.objects.filter(phone_features__feature__icontains=search_name))
        results += list(PhoneList.objects.filter(phone_information__feature__icontains=search_name))
        results += list(PhoneList.objects.filter(phone_information__value__icontains=search_name))
        results += list(PhoneList.objects.filter(phone_reviews__comments__icontains=search_name))
        results += list(PhoneList.objects.filter(price__icontains=search_name))
        results += list(PhoneList.objects.filter(size_sku__size_number__icontains=search_name))
        results = list(set(results))
        args = {"results": results, "instructions": False}
        return render(request, 'front/search.html', args)
    args = {"instructions": True}
    return render(request, 'front/search.html', args)
