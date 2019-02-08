import re
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import (CountryCode, User, PhoneCategory,
                     PhoneMemorySize, PhonesColor, PhoneList,
                     SocialMedia, Review, HotDeal, NewsItem, Order, OrderStatus)
from django.views import generic
from django.core.cache import cache
from .forms.user_forms import (UserCreationForm, AuthenticationForm,
                               UserForm, OldPasswordForm, ChangeEmailForm,
                               EmailAuthenticationForm, resend_email,
                               resend_activation_email, PhoneProfileUserDataCollectionForm)
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
from django.contrib import messages
from django.db.models import Sum


def page_view(request):
    (phone_categories, social_media) = various_caches()
    hot_deals = cache.get('hot_deals') or set_cache(
        HotDeal.objects.filter(item__phone_color_quantity__is_in_stock=True,
                               item__phone_color_quantity__quantity__gte=1).distinct(), 'hot_deals')
    context = {'categories': phone_categories, 'social_media': social_media, 'hot_deals': list(set(hot_deals))}
    return render(request, 'front/landing_page.html', context)


def phone_category_view(request, category_id):
    phones = cache.get('phones_{}'.format(category_id)) or set_cache(
        PhoneList.objects.filter(category=category_id, phone_color_quantity__is_in_stock=True,
                                 phone_color_quantity__quantity__gte=1).distinct(), 'phones_{}'.format(category_id))
    return shared_phone_view(request, phones, category_id)


def phone_category_size_view(request, category_id, size):
    phones = PhoneList.objects.filter(
        category=category_id, size_sku=size, phone_color_quantity__is_in_stock=True,
        phone_color_quantity__quantity__gte=1).distinct()
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


@login_required
def add_cart_session_data(request):
    item = request.POST['cart_item_add']
    quantity = request.POST['quantity']
    price = request.POST['cart_phone_price']
    total_price = int(quantity) * float(price)
    phone = PhoneList.objects.filter(pk=item).first()
    status = OrderStatus.objects.filter(status='pending').first()
    item_in_list = Order.objects.filter(owner=request.user, phone=phone, price=price)
    messages.error(request, 'Oops it seems like you have already added this item to your cart')
    if item_in_list:
        return redirect('/profile/{}'.format(phone.pk))
    Order.objects.create(owner=request.user, phone=phone,
                         status=status, quantity=quantity,
                         price=price, total_price=total_price)
    return redirect("/before_checkout")


def generate_profile_view_load(phone_id, form):
    phone = PhoneList.objects.filter(pk=phone_id).first()
    if not phone:
        return redirect("/error")
    form = form
    secondary_details = PhonesColor.objects.filter(phone=phone_id,
                                                   is_in_stock=True)
    phone_sizes = PhoneMemorySize.objects.filter(category=phone.category)
    (phone_categories, social_media) = various_caches()
    context = {
                "phone": phone, "secondary_details": secondary_details,
                "image_list": phone.phone_images.all(),
                "customer_reviews": phone.phone_reviews.all(),
                "features": phone.phone_features.all(),
                "infos": phone.phone_information.all(),
                'categories': phone_categories, 'social_media': social_media,
                'sizes': phone_sizes, 'form': form
                }
    return context


def phone_profile_view(request, phone_id):
    if request.method == "POST":
        form = PhoneProfileUserDataCollectionForm(request.POST)
        if form.is_valid():
            return add_cart_session_data(request)
        context = generate_profile_view_load(phone_id, form)
        return render(request, 'front/phone_profile.html', context)
    phone = PhoneList.objects.filter(pk=phone_id).first()
    if not phone:
        return redirect("/error")
    form = PhoneProfileUserDataCollectionForm()
    context = generate_profile_view_load(phone_id, form)
    return render(request, 'front/phone_profile.html', context)


def phone_view(request):
    return render(request, 'front/phone.html')


def reset_password_view(request):
    return render(request, 'front/reset_password.html')


def new_password_view(request):
    return render(request, 'front/new_password.html')


def checkout_view(request):
    (phone_categories, social_media) = various_caches()
    return render(request, 'front/checkout.html', {'categories': phone_categories,
                                                   'social_media': social_media})


def get_cart_total(items):
    sum = 0
    for item in items:
        sum += item.total_price
    return sum


@login_required
def before_checkout_view(request):
    (phone_categories, social_media) = various_caches()
    items = Order.objects.filter(owner=request.user)
    item_count = Order.objects.filter(owner=request.user).count()
    total = get_cart_total(items)
    context = {
                'categories': phone_categories,
                'social_media': social_media, 'items': items,
                'item_count': item_count, 'cart_total': total
                }
    return render(request, 'front/before_checkout.html', context)


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


def check_inactive_user(request, email):
    (phone_categories, social_media) = various_caches()
    active_user = User.objects.filter(email=email).first()
    return render(request, 'front/inactive_user.html', {'user_name': active_user.first_name,
                  'user_email': active_user.email,
                  'provider': get_user_email_provider(active_user.email)})


@remember_user
def login_view(request):
    (phone_categories, social_media) = various_caches()
    if request.method == "POST":
        form = AuthenticationForm(None, request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        return validate_active_user(request, form, user, email)
    args = {'form':  AuthenticationForm(), 'social_media': social_media,
            'categories': phone_categories}
    return render(request, 'front/login.html', args)


def validate_active_user(request, form, user, email):
    (phone_categories, social_media) = various_caches()
    if form.is_valid() and user is not None:
        login(request, user)
        return redirect('/')
    if form.redirect:
        return check_inactive_user(request, email)
    args = {'form':  form, 'social_media': social_media,
            'categories': phone_categories}
    return render(request, 'front/login.html', args)


def logout_view(request):
    logout(request)
    return redirect(get_referer_view(request))


def get_referer_view(request):
    """
    This method returns the referer view of the current request.
    It is currently being used for the logout page since this is a button that
    has to be clicked when the user is on the site's application.
    A scenario where a user comes from another application site may bring
    undesired errors in redirecting the user.
    """
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return "/"
    return referer


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
            args = {'user_email': user.email,
                    'provider': get_user_email_provider(user.email)}
            return render(request, 'registration/signup_email_sent.html', args)
        args = {'form':  form, 'social_media': social_media, 'categories': phone_categories}
        return render(request, 'front/signup.html', args)
    else:
        args = {'form':  UserCreationForm(), 'social_media': social_media,
                'categories': phone_categories}
        return render(request, 'front/signup.html', args)


def get_user_email_provider(email):
    new_email = re.split(r'@|\.', email)
    return new_email[1]


def activate(request, uidb64, token):
    user = UserCreationForm().get_user(uidb64)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/dashboard')
    return render(request, 'registration/signup_activation_invalid.html')


def imei_view(request):
    (phone_categories, social_media) = various_caches()
    return render(request, 'front/imei.html', {'categories': phone_categories,
                                               'social_media': social_media})


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
        args = {'form': form, 'social_media': social_media,
                'categories': phone_categories,
                'current_user_email': user.email}
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
    (phone_categories, social_media) = various_caches()
    context = {'news': news, 'categories': phone_categories,
               'social_media': social_media}
    return render(request, 'front/news_press.html', context)


def help_view(request):
    (phone_categories, social_media) = various_caches()
    return render(request, 'front/help.html', {'categories': phone_categories,
                                               'social_media': social_media})


def teke_vs_others_view(request):
    (phone_categories, social_media) = various_caches()
    return render(request, 'front/teke_vs_others.html', {'categories': phone_categories,
                                                         'social_media': social_media})


def error_view(request):
    return render(request, 'front/error.html')


def review_view(request):
    return render(request, 'front/review.html')


def review_submit_view(request):
    return render(request, 'front/review_submit.html')


def privacy_view(request):
    (phone_categories, social_media) = various_caches()
    return render(request, 'front/privacy.html', {'categories': phone_categories,
                                                  'social_media': social_media})


def search_view(request):
    (phone_categories, social_media) = various_caches()
    if request.method == "POST":
        search_name = request.POST.get("search-name")
        results = list(PhoneList.objects.filter(phone_name__icontains=search_name,
                       phone_color_quantity__is_in_stock=True,
                       phone_color_quantity__quantity__gte=1))
        results += list(PhoneList.objects.filter(category__phone_category__icontains=search_name,
                        phone_color_quantity__is_in_stock=True,
                        phone_color_quantity__quantity__gte=1))
        results += list(PhoneList.objects.filter(phone_features__feature__icontains=search_name,
                        phone_color_quantity__is_in_stock=True,
                        phone_color_quantity__quantity__gte=1))
        results += list(PhoneList.objects.filter(phone_information__feature__icontains=search_name,
                        phone_color_quantity__is_in_stock=True,
                        phone_color_quantity__quantity__gte=1))
        results += list(PhoneList.objects.filter(phone_information__value__icontains=search_name,
                        phone_color_quantity__is_in_stock=True,
                        phone_color_quantity__quantity__gte=1))
        results += list(PhoneList.objects.filter(phone_reviews__comments__icontains=search_name,
                        phone_color_quantity__is_in_stock=True,
                        phone_color_quantity__quantity__gte=1))
        results += list(PhoneList.objects.filter(price__icontains=search_name,
                        phone_color_quantity__is_in_stock=True,
                        phone_color_quantity__quantity__gte=1))
        results += list(PhoneList.objects.filter(size_sku__size_number__icontains=search_name,
                        phone_color_quantity__is_in_stock=True,
                        phone_color_quantity__quantity__gte=1))
        results = list(set(results))
        args = {"results": results, "instructions": False,
                'categories': phone_categories,  'social_media': social_media}
        return render(request, 'front/search.html', args)
    args = {"instructions": True, 'categories': phone_categories,
            'social_media': social_media}
    return render(request, 'front/search.html', args)


def change_activation_email(request, old_email):
    return render(request, 'registration/change_activation_email.html',
                  {'old_email': old_email})


def send_link_to_new_address(request, old_email):
    user = User.objects.get(email=old_email)
    user_email = request.POST['email']
    if request.method == "POST":
        if User.objects.filter(email=user_email).exists():
            return render(request, 'registration/change_activation_email.html',
                                   {'error': 'That Email is Already Registered',
                                    'old_email': old_email})
        elif resend_email(request, user, user_email):
            User.objects.filter(pk=user.pk).update(former_email=old_email)
            User.objects.filter(pk=user.pk).update(email=user_email)
            return render(request, 'registration/signup_email_sent.html',
                          {'user_email': user_email})
        else:
            return render(request, 'registration/change_activation_email.html',
                                   {'error': 'Invalid Email', 'old_email': old_email})
    return render(request, 'registration/change_activation_email.html')


def resend_activation_link(request, email):
    if email:
        user = User.objects.get(email=email)
        resend_email(request, user, email)
        return redirect('/login')
    return redirect('/signup')


def resend_new_email_activation_link(request):
    user = User.objects.filter(email=request.user.email).first()
    if resend_activation_email(request, user, user.change_email):
        messages.success(request,
                         ('A new link has successfuly been sent to {}'.
                             format(user.change_email)))
        return redirect('/dashboard')
    messages.error(request, ('Something went wrong!'))
    return redirect('/dashboard')
