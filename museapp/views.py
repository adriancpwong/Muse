from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from museapp.forms import UserForm, UserProfileForm, ProjectForm, CommentForm, ExtraFileFormSet
from museapp.models import MusicProject, Comment, ExtraFile
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.core import serializers
from django.contrib.auth.decorators import login_required

def homePage(request):
    context_dict = {}
    return render ( request, "muse/home.html", context_dict)

def about(request):
    context_dict = {}

    return render ( request, "muse/about.html", context_dict)

def user_login(request):
    context_dict = {}

    if request.method == "POST":

        login_form = AuthenticationForm(data = request.POST)

        if login_form.is_valid():
            login(request, login_form.get_user())

            #redirect to users page
            user_id = login_form.get_user().id
            return HttpResponseRedirect("/muse/users/%d/" %user_id)

    else:
        login_form = AuthenticationForm()
        context_dict["message"] = "Please login!"

    context_dict["form"] = login_form
    return render ( request, "muse/login.html", context_dict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/muse/")
	
def register(request):
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		
		if user_form.is_valid():
			user = user_form.save()
			login(request, user)
			return HttpResponseRedirect("/muse/users/%d/" %user.id)
		    
	else:
	    user_form = UserForm()
	    
        return render ( request, 'muse/register.html', {'user_form': user_form})

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()#updates password and logs user out
            update_session_auth_hash(request, user)#logs user back in
            return render ( request, "muse/changePassword.html", {"message":"Your password has been changed"})
        else:
            return render ( request, "muse/changePassword.html", {"message":"There was an error changing your password"})
    else:
        form = PasswordChangeForm(request.user)

    context_dict = {"form":form}
    return render(request, "muse/changePassword.html",context_dict)

@login_required
def user_delete(request):
    user = request.user
    user_id = user.id

    if (request.method == "POST"):
        user.delete()
        return render ( request, "muse/givemessage.html", {"message":"user " + str(user_id) + " deleted"})

    return render ( request, "muse/givemessage.html", {"message":"Delete failed"})
	
def getProjectPreviews(request):
    response = {}

    number = request.GET.get('number', default = "")
    project_list = MusicProject.objects
    user_id = request.GET.get('user_id', default = "")

    if (user_id.isdigit()):
        user_id = int(user_id)
    else:
        user_id = -1

    if (user_id != -1):
        #get only owner's projects
        project_list = project_list.filter(user__id__exact=user_id)
    else:
        #return random projects
        project_list = project_list.order_by("?")[:]

        #workout number of projects to return
    if (not number.isdigit()):
        number = 5
    else:
        number = int(number)

    #clip the number of returned projects
    if number < len(project_list) and number != 0:#if 0 return all projects
        project_list = project_list[:number]

    projects = []
    for project in project_list:
        next_project = {"name":project.name,
                        "slug":project.slug,
                        "genre":project.genre,
                        "PageDescription":project.PageDescription}        
        number_of_comments = Comment.objects.filter(project__slug=project.slug).count()
        next_project["NumberOfComments"] = number_of_comments
        next_project["Author"] = {"name": project.user.username,
                                  "id": project.user.id}

        rendered_project = render(request,'muse/projectPreview.html',next_project)
        del rendered_project["Content-Type"]

        projects.append(str(rendered_project))


    response["ProjectPreviews"] = projects
    
    return JsonResponse(response)

@login_required
def project(request, project_name_slug):
    context_dict = {}
    if (request.method == "GET"):
        #get a project
        try:
            musicProject = MusicProject.objects.get(slug=project_name_slug)
        except:
            #project doesn't exist
            raise Http404("Project does not exist")
        extra_files = ExtraFile.objects.filter(project=musicProject)
        context_dict["ExtraFiles"] = extra_files
        context_dict["Project"] = musicProject
        context_dict["commentForm"] = CommentForm()

        return render ( request, "muse/projectView.html", context_dict)

    else:
        #not a valid request
        return render ( request, "muse/givemessage.html", {"message":"Found no projects"})

@login_required
def createProject(request):

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, prefix="project")
        extra_form = ExtraFileFormSet(request.POST, request.FILES, prefix="extra_files")
        if form.is_valid() and extra_form.is_valid():
            project = form.save(commit=False)
            try:
                project.musicFile = request.FILES["project-MusicFile"]
            except:
                pass
            project.user = request.user
            project.save()

            #extra_files = extra_form.save(commit=False)
            for extra in extra_form:
                extra_file = extra.save(commit=False)

                if extra_file.extra:#only commit if there is a file
                    extra_file.project = project
                    extra_file.user = request.user
                    extra_file.save()
            return HttpResponseRedirect("/muse/users/%d/" %request.user.id)

    else:
        form = ProjectForm(prefix="project")
        extra_form = ExtraFileFormSet(prefix="extra_files")

    return render (request, "muse/newProject.html", {"projectForm":form, "FileFormSet":extra_form})

def deleteProject(request, project_name_slug):

    if request.method =="POST":
        try:
            project = MusicProject.objects.get(slug=project_name_slug)
        except:
            raise Http404("Project does not exist")
        user = request.user
        if project.user.id == user.id:
            project.delete()
            return HttpResponseRedirect("/muse/users/"+str(user.id)+"/")

    HttpResponseRedirect("/muse/projects/"+project_name_slug+"/")


@login_required
def userPage(request, user_id):
    context_dict = {}
    try:
        pageOwner = User.objects.get(id__exact=int(user_id)).username
        context_dict["owner"] = pageOwner
    except:
        #user doesn't exist 404 error
        raise Http404("User does not exist")
    return render(request, "muse/accountPage.html", context_dict)


@login_required
def comments(request, project_name_slug):

    comments = Comment.objects.filter(project__slug__exact=project_name_slug)


    comment_list = []
    for comment in comments.iterator():
        can_Edit = (comment.user == request.user or comment.project.user == request.user)
        next_comment = render(request, "muse/comment.html",{"comment":comment,"canEdit":can_Edit})
        del next_comment["Content-Type"]
        print next_comment
        comment_list.append(str(next_comment))

    #If no comments give message
    if len(comment_list) == 0:
        comment_list = ["There are no comments here!"]
        
    response = {"comments":comment_list}


    return JsonResponse(response)

@login_required
def newComment(request, project_name_slug):
    try:
        project = MusicProject.objects.get(slug=project_name_slug)
    except MusicProject.DoesNotExist:
        project = None

    author = request.user

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            try:
                comment.audio = request.FILES['audio']
            except:
                pass
            comment.user = author
            comment.project = project
            comment.save()

    return HttpResponseRedirect("/muse/projects/"+project_name_slug+"/")


@login_required
def deleteComment(request, project_name_slug, comment_id):

    comment = Comment.objects.get(id__exact=int(comment_id))

    #check user can edit
    if ((request.user.id == comment.user.id) or (request.user.id == comment.project.user.id)):
        
        if (request.method == "POST"):
            comment.delete()
            return HttpResponseRedirect("/muse/projects/"+project_name_slug+"/")

    return render ( request, "muse/message.html", {"message":"Delete failed"})
