from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import datetime
import pytz

def wall(request):
    errors = User.objects.validate_success(request.session)
    if len(errors) > 0: # permission denied appears twice
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    context = {
        "all_messages": Message.objects.all().order_by("-created_at"),
    }
    return render(request, 'wall.html', context)

def post_message(request):
    this_user = User.objects.get(id=request.session['user_id'])
    Message.objects.create(message=request.POST['message'], user=this_user)
    return redirect('/wall')

def post_comment(request):
    this_user = User.objects.get(id=request.session['user_id'])
    this_message = Message.objects.get(id=request.POST['msg_id'])
    Comment.objects.create(comment=request.POST['comment'], user=this_user, message=this_message)
    return redirect('/wall')

def delete_message(request):
    this_message = Message.objects.get(id=request.POST['msg_id'])

    utc=pytz.UTC
    check_created = this_message.created_at + datetime.timedelta(minutes=30)
    now = utc.localize(datetime.datetime.now())
    if (now > check_created):
        messages.error(request, "Cannot delet message posted 30 minutes ago.")
    else:
        this_message.delete()
    return redirect('/wall')