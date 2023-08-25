from django.http import Http404
from django.shortcuts import render, redirect
from ..main.models import UsersAuth

# Create your views here.


def home_page(request, userid):
    try:
        user = UsersAuth.objects.get(id=userid)
        if 'user_id' not in request.session and request.session['user_id'] != user.id:
            return redirect('/signin/')

        context = {'user': user}

        return render(request, 'index.html', context)

    except UsersAuth.DoesNotExist:
        raise Http404(f"No user registered under the id {userid}")
