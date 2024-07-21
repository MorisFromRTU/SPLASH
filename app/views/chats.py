from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from app.models import Chat, Message, CustomUser
from app.forms import MessageForm


@login_required
def get_or_create_chat(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)
    
    return redirect('chat_detail', chat_id=chat.id)


@login_required
def chats(request):
    chats = Chat.objects.filter(participants=request.user)
    users = []
    for chat in chats:
        message_count = chat.messages.count()
        if message_count > 0:
            participants = chat.participants.all()
            participant_names = [p.username for p in participants]
            if participant_names:
                for name in participant_names:
                    if name != request.user.username:
                        user = CustomUser.objects.get(username = name)
                        users.append([user, chat])
    return render(request, 'chats/chats.html', {'users' : users})

@login_required
def chat_detail(request, chat_id):
    chats = Chat.objects.filter(participants=request.user)
    users = []
    for chat in chats:
        message_count = chat.messages.count()
        if message_count > 0:
            participants = chat.participants.all()
            participant_names = [p.username for p in participants]
            if participant_names:
                for name in participant_names:
                    if name != request.user.username:
                        user = CustomUser.objects.get(username = name)
                        users.append([user, chat])
                        

    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.participants.all():
        return redirect('main')
    
    messages = chat.messages.all().order_by('timestamp')
    receiver = chat.participants.exclude(id=request.user.id).first()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()
    
    return render(request, 'chats/chat_detail.html', {'chat': chat, 'messages': messages, 'form': form, 'receiver': receiver, 'users' : users})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    if message.sender == request.user:
        message.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
