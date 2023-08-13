from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
            request=request,
            username=username,
            password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'userapp/sign_in.html')

def sign_out(request):
    logout(request)
    return redirect('/')