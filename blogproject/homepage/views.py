from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .models import post, postLike


# Create your views here.
def homepage(request):
    #getting all post from database
    getposts = post.objects.all()
    return render(request, 'index.html', {'posts': getposts})

def singlepost(request, id):
    getsinglepost = post.objects.get(pk=id)
    # getting total likes for this post
    totalLike = postLike.objects.get(post=getsinglepost).totalLike
    # print(singlepost)
    return render(request, 'single-post.html', {'post': getsinglepost, 'likes': totalLike})

@login_required(login_url='login')
def createpost(request):
    if request.method == 'POST':
        postTitle = request.POST['posttitle']
        postDescription = request.POST['postdescription']

        if postTitle.strip() != '' and postDescription.strip() != '' and len(request.FILES) != 0:

            postImage = request.FILES['postImagefilejpg']
            newpost = post()
            newpost.postTitle = postTitle
            newpost.postImage = postImage
            newpost.description = postDescription
            newpost.author = request.user
            newpost.save()
            #onetoonefieldpostlike
            postLikefornewpost = postLike(post=newpost)
            postLikefornewpost.totalLike = 0
            postLikefornewpost.save()


            return redirect('userpanel')
        else:
            return render(request, 'create-post.html', {'error': 'You must fill up all field!'})
    else:
        return render(request, 'create-post.html')

@login_required(login_url='login')
def editpost(request, id):

    if request.method == 'POST':
        if request.POST['posttitle'].strip() != '' and request.POST['postdescription'].strip() != '' and len(request.FILES) != 0:
            editpost = post.objects.get(pk=id)
            editpost.postTitle = request.POST['posttitle']
            editpost.postImage = request.FILES['postImagefile']
            editpost.description = request.POST['postdescription']
            editpost.author = request.user
            editpost.save()

            return redirect('userpanel')
        else:
            return render(request, 'edit-post.html', {'error': 'You must fill up every field'})

    if post.objects.filter(pk=id, author=request.user).count() == 0:
        return render(request, 'edit-post.html', {'error': 'You have not enough permission to edit this post'})
    else:
        getsinglepost = post.objects.get(pk=id, author=request.user)
        print(getsinglepost.postTitle)
        return render(request, 'edit-post.html', {'post': getsinglepost})

@login_required(login_url='login')
def userpanel(request):
    if post.objects.filter(author=request.user).count() == 0:
        return render(request, 'user-panel.html', { 'error': 'You ahve no Post'})
    else:
        userposts = post.objects.filter(author=request.user)
        
        return render(request, 'user-panel.html', {'myposts': userposts })

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('userpanel')
        else:
            return render(request, 'login.html', {'error': 'Login Failed!'})
    else: 
        return render(request, 'login.html')

def registration(request):
    if request.method == 'POST':
        fullanme = request.POST['fullname']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if fullanme.strip() != '' and username.strip() != '' and password.strip() != '' and cpassword != '':
            if password == cpassword:
                try:
                    user = User.objects.get(username=username)
                    return render(request, 'registration.html', {'error': 'An user already exists with this username'})
                except:
                    newuser = User.objects.create_user(username=username, email=None, password=password, first_name=fullanme, last_name=fullanme)
                #    auth.login(request, newuser)
                    return redirect('userpanel')
            else:
                return render(request, 'registration.html', {'error': 'Password does not match!'})

        else:
            return render(request, 'registration.html', {'error': 'All fields must be fillup'})
    else:
        return render(request, 'registration.html')
        

@login_required(login_url='login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('homepage')
    else:
        return redirect('login')

@login_required(login_url='login')
def delete(request, id):
    if request.method == 'POST':
        if post.objects.filter(pk=id, author=request.user).count() > 0:
            post.objects.filter(pk=id).delete()
            return redirect('userpanel')
        else:
            return redirect('homepage')
    else:
        return redirect('login')

@login_required(login_url='login')
def liketopost(request, id):
    if request.method == 'POST':
        targetPost = post.objects.get(pk=id)
        if postLike.objects.filter(post=targetPost).count() > 0:
            newlike = postLike.objects.get(post=targetPost)
            oldlike = postLike.objects.get(post=targetPost).totalLike
            newtotallike = oldlike + 1
            newlike.totalLike = newtotallike
            newlike.post = targetPost
            newlike.save()
            return redirect('homepage')
        else:
            newpostlike = postLike()
            newpostlike.totalLike = 1
            newpostlike.post = targetPost
            newpostlike.save()
            return redirect('homepage')
    else:
        return redirect('homepage')