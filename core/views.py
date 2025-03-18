from random import shuffle
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Profile, Post, Follow,Message,Comment


@login_required
def search(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    following = list(Follow.objects.filter(follower=user_profile))
    ids = []
    for follow in following:
        ids.append(follow.following.id)
    ids.append(user_profile.id)
    exclude_suggestion = ids
    suggested_profiles = list(Profile.objects.exclude(id__in=exclude_suggestion).values())
    shuffle(suggested_profiles)
    suggested_profiles = suggested_profiles[:10]
    for profile in suggested_profiles:
        profile_obj = Profile.objects.get(id=profile['id'])
        profile['username'] = profile_obj.user.username
        profile['followers_count'] = profile_obj.followers.count()
        profile['profile_img'] = profile_obj.profile_img.url
    context = {
        'search':"active",
        'user_profile': user_profile,
        'suggested_profiles': suggested_profiles,
    }    
    return render(request, 'search.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        context = {
            'username': username,
            'email': email,
        }

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return render(request, 'signup.html', context)
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken')
                return render(request, 'signup.html', context)
            else:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                auth.login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Passwords don\'t match')
            return render(request, 'signup.html', context)
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        context = {
            'username': username
        }

        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.error(request, 'Invalid credentials')
            return render(request, 'signin.html', context)
        auth.login(request, user)
        return redirect('index')
    return render(request, 'signin.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {'user_profile': user_profile}

    if request.method == 'POST':
        profile_img = user_profile.profile_img if not request.FILES.get(
            'profile_img') else request.FILES.get('profile_img')
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        email = request.POST.get('email')

        # Update the database entry
        user_profile.profile_img = profile_img
        user_profile.bio = bio
        user_profile.location = location
        user_profile.user.email = email
        user_profile.save()
        user_profile.user.save()

    return render(request, 'settings.html', context)


@login_required
def upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        profile = Profile.objects.get(user=request.user)
        Post.objects.create(profile=profile, image=image, caption=caption) 
        return redirect('index')
    user_profile=Profile.objects.get(id_user=request.user.id)
    context={'user_profile': user_profile,'post':'active'}
    return render(request,'post.html',context)


@login_required
@csrf_exempt
def like_post(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(post_id=post_id)
    like = post.liked.filter(user=request.user)
    if like.exists():
        post.liked.remove(like.first())
    else:
        post.liked.add(Profile.objects.get(user=request.user))
    user=Profile.objects.get(user_id=request.user.id).id_user
    post.save()
    likes = {'user_profile':user,'post_id': post.post_id, 'likes': list(post.liked.all().values())}
    return JsonResponse(likes)


import json
@login_required
@csrf_exempt
def Jsonchat(request):
    user_id = request.GET.get('user_id')
    receiver=Profile.objects.get(id_user=user_id)
    profile=Profile.objects.get(id_user=request.user.id)
    messages=Message.objects.filter((Q(sender=profile) & Q(receiver=receiver))|(Q(sender=receiver)&(Q(receiver=profile)))).order_by('created')
    context=[]
    mess={}
    for message in messages:
        mess['sender']=message.sender.id_user
        mess['receiver']=message.receiver.id_user
        mess['text']=message.text
        mess['created']=message.created
        context.append(mess)
        mess={}
    likes = {'context':context,'user_profile':profile.id_user}
    return JsonResponse(likes,safe=False)

@login_required
@csrf_exempt
def Chatting(request,pk):
     user= get_object_or_404(Profile, id_user=pk)
     my_profile=Profile.objects.get(id_user=request.user.id)
     context={"user":user,"user_profile":my_profile}
     return render(request,'Jsonchat.html',context)
@login_required
def profile(request, pk):
    profile = get_object_or_404(Profile, id_user=pk)
    my_profile = Profile.objects.get(user=request.user)
    followers = profile.followers.all()
    following = profile.following.all()
    is_followed = followers.filter(follower=my_profile).exists()
    context = {
        'profile': profile,
        'user_profile':my_profile,
        'posts': Post.objects.filter(profile=profile),
        'followers': followers,
        'following': following,
        'is_followed': is_followed,
        'userprofile':'active'
    }

    return render(request, 'profile.html', context)


@login_required
@csrf_exempt
def follow(request):
    if request.method == 'GET':
        followed_id = request.GET.get('followed_id')
        following_profile = get_object_or_404(Profile, id_user=followed_id)
        follower_profile = Profile.objects.get(user=request.user)

        if Follow.objects.filter(following=following_profile, follower=follower_profile).exists():
            follow = Follow.objects.get(following=following_profile, follower=follower_profile)
            follow.delete()
            is_followed = False
        else:
            Follow.objects.create(follower=follower_profile, following=following_profile)
            is_followed = True

        followers = list(following_profile.followers.all().values())
        following = list(following_profile.following.all().values())

        response = {
            'followers': followers,
            'following': following,
            'is_followed': is_followed,
        }
        return JsonResponse(response)
    

@login_required
@csrf_exempt
def searchJson(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if len(username) == 0:
            return JsonResponse({})
        
        users = User.objects.filter(username__icontains=username, is_staff=False).exclude(id=request.user.id)
        profiles = Profile.objects.filter(user__in=users)
        profile_imgs = []
        usernames = []
        for profile in profiles:
            profile_imgs.append(profile.profile_img.url)
            usernames.append(profile.user.username)
        profiles = list(profiles.values())
        profiles = list(zip(profiles, profile_imgs, usernames))
        return JsonResponse(profiles, safe=False)
@login_required
def message(request):
    if request.method == 'POST':   
        text=request.POST.get("message")
        id_=request.POST.get("receiver")
        sender=Profile.objects.get(id_user=request.user.id)
        receiver=Profile.objects.get(id_user=id_)

        Message.objects.create(
            text=text,
            sender=sender,
            receiver=receiver

        )


        return redirect('chat',pk=id_)
    profile = Profile.objects.exclude(id_user=request.user.id)
    my_profile= Profile.objects.get(id_user=request.user.id)
    messages=Message.objects.all()
    context={"profile":profile,"messages":messages,"user_profile":my_profile,'chat':'active'}
    return render(request,'messages.html',context)
@login_required
def chat(request,pk):
    profile = Profile.objects.get(id_user=request.user.id)
    receiver = Profile.objects.get(id_user=pk)
    all_profile = Profile.objects.exclude(id_user=request.user.id)
    messages=Message.objects.filter((Q(sender=profile) & Q(receiver=receiver))|(Q(sender=receiver)&(Q(receiver=profile)))).order_by('created')
    context={"user_profile":profile,"messages":messages,"receiver":receiver,"all_profile":all_profile,'chat':'active'}
    return render(request,'chat.html',context)
@login_required
def home(request):
    profile = Profile.objects.get(id_user=request.user.id)
    home="active"
    user = request.user
    user_profile = Profile.objects.get(user=user)
    following = list(Follow.objects.filter(follower=user_profile))
    ids = []
    if request.method == 'POST':
        user=Profile.objects.get(id_user=request.user.id)
        comment=Comment.objects.create(
            text = request.POST.get("text"),
            profile = user
        )
        post_id= request.POST.get("post_id")
        post=Post.objects.get(post_id=post_id)
        post.comments.add(comment)
        post.save()
    for follow in following:
        ids.append(follow.following.id)
    ids.append(user_profile.id)

    posts = Post.objects.filter(profile__in=ids).order_by('-created_at')
    exclude_suggestion = ids
    suggested_profiles = list(Profile.objects.exclude(id__in=exclude_suggestion).values())
    shuffle(suggested_profiles)
    suggested_profiles = suggested_profiles[:10]
    for profile in suggested_profiles:
        profile_obj = Profile.objects.get(id=profile['id'])
        profile['username'] = profile_obj.user.username
        profile['followers_count'] = profile_obj.followers.count()
        profile['profile_img'] = profile_obj.profile_img.url
    
    context = {
        'user_profile': user_profile,
        'my_profile': user_profile,
        'posts': posts,
        'suggested_profiles': suggested_profiles,
        "home":home,
        "profile":profile
    }
    
    return render(request, 'index.html', context)

@login_required
def updateprofile(request):
    bio=request.POST.get('biolife')
    email= request.POST.get('email')
    username=request.POST.get('name')
    profile_img=request.FILES.get('profile_img')
    error=success=None
    if User.objects.filter(Q(email=email)).exclude(id=request.user.id).exists():
        messages.error(request, 'Existed Email')
        error='active'        
    elif User.objects.filter(username=username).exclude(id=request.user.id).exists():
        messages.error(request, 'Exited Username')
        error='active'
    else :
        success='active'
        user=request.user.id 
        profile=Profile.objects.get(user_id=user)
        if bio:
            profile.bio=bio
        
        if profile_img != None:
            profile.profile_img=profile_img
        profile.save()
        users=User.objects.get(id=user)
        users.username=username
        users.email=email
        users.save()
        messages.info(request, 'Successfully Updated ')
    my_profile = Profile.objects.get(user=request.user)
    followers = my_profile.followers.all()
    following = my_profile.following.all()
    is_followed = followers.filter(follower=my_profile).exists()
    
    context = {
        'error':error,
        'success':success,
        'profile':my_profile,
        'user_profile':my_profile,
        'posts': Post.objects.filter(profile=my_profile),
        'followers': followers,
        'following': following,
        'is_followed': is_followed,
        'userprofile':'active',
        'my_profile': my_profile,

    }
    return render(request, 'profile.html', context)
