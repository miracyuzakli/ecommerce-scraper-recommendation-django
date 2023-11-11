from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# Create your views here.


from api.models import Product, UserProductViewing









def index_view(request):
    current_user = request.user

    category = request.GET.get('category')


    
    return render(request, 'index.html', {'current_user': current_user, "category": category})



def product_details(request):
    product_id = request.GET.get('product_id')
    current_user = request.user
    product = Product.objects.get(id=int(product_id))

    # product_view değerini 1 artırın
    product.product_view += 1
    product.save()

    new_user_product_viewing = UserProductViewing(
        user=User.objects.get(id=current_user.id),  
        product = Product.objects.get(id=int(product_id)),  
        user_viewing=1, 
    )
    new_user_product_viewing.save()

    product_dict = {
        'id': product.id,
        'category': product.category,
        'product_name': product.product_name,
        'price': product.price,
        'rating': product.rating,
        'rating_score': product.rating_score,
        'answered_questions': product.answered_questions,
        'favorite': product.favorite,
        'feature_0': product.feature_0.replace("|", " - "),
        'feature_1': product.feature_1.replace("|", " - "),
        'feature_2': product.feature_2.replace("|", " - "),
        'feature_3': product.feature_3.replace("|", " - "),
        'feature_4': product.feature_4.replace("|", " - "),
        'feature_5': product.feature_5.replace("|", " - "),
        'feature_6': product.feature_6.replace("|", " - "),
        'feature_7': product.feature_7.replace("|", " - "),
        'image_name': product.image_name,
    }

    return render(request, 'product-details.html', {
        'current_user': current_user, 
        "product_id": product_id, 
        "product_dict": product_dict
    })












def recommendation_view(request):
    current_user = request.user

    category = request.GET.get('category')


    
    return render(request, 'recommendation-product.html', {'current_user': current_user, "category": category})


























def login_view(request):

    if request.user.is_authenticated:
        return redirect('index') 
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
           
            if user is not None:
                login(request, user)
                return redirect('index')  
            else:
                error_message = 'Geçersiz kullanıcı adı veya şifre'
                return render(request, 'login.html', {'error_message': error_message})
        else:
            return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            email = request.POST['email']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']

            # Basit bir parola doğrulama işlemi eklemek için
            if password == password_confirm:
                # Kullanıcıyı oluştur ve oturum aç
                user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
                user.save()
                login(request, user)
                return redirect('index')
            else:
                error_message = 'Parolalar eşleşmiyor.'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            return render(request, 'register.html')


def logout_view(request):
    
    logout(request)
    return redirect('index') 
