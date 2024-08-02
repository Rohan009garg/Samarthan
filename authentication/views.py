from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from Samarthan import settings
from django.core.mail import send_mail

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

        if User.objects.filter(username=username):
            messages.error(request,"Username already exists! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,"Email already exists! Please try some other email.")
            return redirect('home')
        
        if len(username)>15:
            messages.error(request,"Username must be under 15 characters")

        if password != cpassword:
            messages.error(request,"Passwords didn't match")

        if not username.isalphanumeric:
            messages.error(request,"Username should only contain letters and numbers")
            return redirect('home')

        #ab ham register krenge use
        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        #ab hum message dikhayenge ki succesfull register hogya
        messages.success(request,"Your account has been successfully created, we have also sent you an confirmstion email,please confirm your account")

        #welcome email
        subject= "Welcome to Samarthan Login"
        message = "Hello " + myuser.first_name + "!" + "\n" + "Welcome to Samarthan \n Thank you for visiting our website. \n We have also sent you a confirmation email, please confirm your email address in order to activate you account. \n\n Thanking you \n Rohan Garg"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email] #kisko email jayega
        send_mail(subject,message,from_email,to_list,fail_silently=True)






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
    

