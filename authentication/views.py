from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    # return HttpResponse("Hello, world!")
    return render(request,"authentication/index.html")

def signup(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['first-name']
        lname = request.POST['last-name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['confirm-password']

        #ab ham register krenge use
        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        #ab hum message dikhayenge ki succesfull register hogya
        messages.success(request,"Your account has been successfully created")
        return redirect('signin')

    return render(request,"authentication/signup.html")

def signin(request):
    if(request.method == 'POST'):
        username1 = request.POST['username']
        password1 = request.POST['password']

        #ab authenticate krenge user
        user = authenticate(username=username1,password=password1)
        #ab user me value null ya not nulll ayega
        #if null then not authenticated else authenticte
        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request,"authentication/index.html",{'fname':fname})
        else:
            messages.error(request,"bad credential")
            return redirect('home')

    return render(request,"authentication/signin.html")

def signout(request):
    # pass
    logout(request)
    messages.success(request,"Logout succesfull")
    return redirect('home')
    

