from django.shortcuts import render, redirect
from user.forms import SimpleSignupForm

def signup(request):
    if request.method == 'POST':
        form = SimpleSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
    else:
        form = SimpleSignupForm()
    return render(request, 'registration/signup.html', {'form': form})
