from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.http import HttpResponse
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
# Create your views here.

class LoginPageView(View):
    def get(self,request):
        return render(request, "users/login.html")

    def post(self, request):
        login_form = AuthenticationForm(data = request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request,user)
            context = {"user":user}
            
            return render(request,"home.html",context)
        else:
            print("errorsss")
            context = {
                "form":login_form
            }
            return render(request,"users/login.html",context)

        # username = request.POST["username"]
        # password = request.POST["password"]
        # user = authenticate(request, username=username,password = password)

        # if user is None:
        #     return redirect("login-page")
        # else:
        #     return redirect("profile-page")


class RegisterPageView(View):
    def get(self, request):
        return render(request, "users/register.html")

    def post(self,request):
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        data = {
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "email": request.POST["email"],
            "username": request.POST["username"],
            "password": password1,
        }
        user = UserRegisterForm(data,request.FILES)
        if user.is_valid() and password1 == password2:
            user.save()
            return redirect("login-page")
        else:
            print("ERRor")
            context = {"form":user}
            return render(request, "users/register.html",context)

        # first_name = request.POST["first_name"]
        # last_name = request.POST["last_name"]
        # email = request.POST["email"]
        # username = request.POST["username"]
        # password = request.POST["password"]
        # user = User(
        #     first_name = first_name,
        #     last_name = last_name,
        #     email = email,
        #     username = username
        # )
        # user.set_password(password)
        # user.save()
        return redirect("login-page")


class UserListView(LoginRequiredMixin, View):
    def get(self,request):
        search = request.GET.get("search")
        if search is None:
            users = User.objects.all()
            context = {"users":users}
            return render(request, "users/user_list.html",context)

        else:
            users = User.objects.filter(first_name__icontains=search) | User.objects.filter(last_name__icontains=search)
            context = {"users":users,"search":search}
            return render(request, "users/user_list.html", context)
    def post(self):
        pass


class UserDetailView(View):
    def get(self,request,id):
        user = User.objects.get(id=id)
        context = {
            "user":user,
            "id":id
        }
        return render(request, "users/user_detail.html", context)


class UserSettingsView(View):
    def get(self,request,id):
        user = User.objects.get(id = id)
        context = {
            "user":user
        }
        return render(request,"users/user_settings.html",context)

    def post(self,request,id):
        user = User.objects.get(id = id)
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        old_password = request.POST[
            "password"
        ] 
        new_password = request.POST[
            "new-password"
        ]  
        profile_image = request.FILES.get("image")  

        # Update the user's non-password fields
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        # print(user.username)
        # print(username)
        if username != user.username:
            # Check if the new username already exists
            if User.objects.filter(username=username).exists():
                return HttpResponse ( "The username you entered is already taken.")
                return redirect("some_view_name")

        # Check if the old password is correct
        data = {
            "username": username,
            "password": old_password
        }
        form = AuthenticationForm(data = data)
        if form.is_valid():
            user = form.get_user()
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)

        # If new password is provided, set the new password
        # Important: to keep the user logged in after changing the password

        # If a new profile image is provided, update the user's image
        if profile_image:
            user.image = profile_image

        user.save()  # Save the user object with all the updates

        return HttpResponse("Your profile was successfully updated.")

        return redirect("some_view_name")  # Redirect to a new URL

    # user = User.objects.get(id=id)

    # first_name = request.POST.get("first_name")
    # last_name = request.POST.get("last_name")
    # email = request.POST.get("email")
    # username = request.POST.get("username")
    # password = request.POST.get("password")
    # new_password = request.POST.get("new-password")
    # print(password, new_password)
    # if (password == '' and new_password == ''):
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.email = email
    #     user.username = username
    #     user.save()
    #     return redirect("users-page")

    # user = authenticate(request, username=user.username, password=password)
    # if user is None:
    #     return HttpResponse("wrong password")

    # else:
    #     data = {

    #         "first_name": first_name,
    #         "last_name": last_name,
    #         "email": email,
    #         "username": username,
    #         "password":new_password
    #     }
    #     form = UserRegisterForm(data=data, files = request.FILES, instance=user)
    #     form.save()
    #     return redirect("users-page")

class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect("home_page_name")

class UserAddView(View):
    def get(self,request):
        return render(request, "users/user_add.html")

    def post(self,request):
        form = UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("users-page")
        else:
            return redirect("add_user")


class UserDeleteView(View):
    def get(self,request,id):
        user = User.objects.get(id=id)
        user.delete()
        return redirect("users-page")
