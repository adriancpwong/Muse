import os
import django
#from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muse.settings")
django.setup()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLE_DIR = os.path.join(BASE_DIR, "example_files")

def populate():

##    users = [{"username":"phil",
##              "password":"pju6gi",},
##             {"username":"huffy",
##              "password":"wb5t3s5"},]
##
##    projects = [{"name":"

    user_phil = add_user("phil","pju6gi")
    user_huffbert = add_user("huffy","wb5t3s5")
    user_jake = add_user("jake","qd9874")
    user_jolie = add_user("jolie","wf84635")
    user_roman =add_user("roman","rt8759")
    #music13bb = get_file('13barblues.mp3')
    #ydtsmusic = get_file('youdeservethesun.mp3')
    
    project_13bb = add_project("13-Bar-Blues",user_phil,"blues","like 12 bar blues",)#muic13bb)
    project_ydts = add_project("You deserve the sun",user_phil,"folk","A song I wrote a while back",)#ydtsmusic) 
    project_rc = add_project("Rock it",user_jake,"rock","An experimental song our group created",)
    project_pop = add_project("Jamming in the street",user_jolie,"pop","A fun little thing that i want to work on",)
    project_sin = add_project("Straight into life",user_jake,"rock","The start of a new project, not much here yet",)
    project_fin = add_project("Bunch of stuff",user_roman,"all","Bunch of little pieces with no really connection, looking for opinions")
    project_rap = add_project("My rap rhymes",user_roman,"rap","My rap rhymes that I want to work on.")

    add_comment(project_13bb, user_huffbert, "The 13th bar just sounds weird")
    add_comment(project_13bb, user_phil, "It was probably best to stop at 12 but I wanted to see what would happen")
    add_comment(project_rc, user_roman,"I really liked this! refren is a bit sloppy but otherwise awesome")
    add_comment(project_pop,user_jake,"The tempo is a little bit too fast.")
    add_comment(project_pop,user_jolie,"Thank you for the input! I will se what i can do.")
    add_comment(project_pop,user_roman,"Seems a little bit too chaotic")
    add_comment(project_sin,user_jolie,"Already looking good")
    add_comment(project_13bb,user_jake,"I agree, ending at 12 would sound better")

def add_user(username,password):
    user = User.objects.get_or_create(username=username, password=password)[0]
    #user.save()
    #user.set_password(password)
    user.save()
    print "User: " + str(user)
    return user

def add_project(name,user,genre,description):#,musicFile):
    project = MusicProject.objects.get_or_create(name=name,
                                                 user=user,
                                                 genre=genre,
                                                 PageDescription=description,
                                                 #musicFile=musicFile,
                                                 )[0]
    project.save()
    print "Project: " + str(project)
    return project

def add_extra_file(project, user, file_type,extra):
    extra_file = ExtraFile.objects.get_or_create(project=project,
                                                 user=user,
                                                 file_type=filetype,
                                                 extra=extra)[0]
    extra_file.save()
    print "Extra file: " + str(extra_file)
    return extra_file

def add_comment(project, user, text):
    comment = Comment.objects.get_or_create(project=project,
                                            user=user,
                                            text=text,)[0]
    comment.save()
    print "Comment: " + str(comment)
    return comment

def get_file(filename):
    filepath = os.path.join(EXAMPLE_DIR, filename)
    with open(filepath, "r")as new_file:
        djangoFile = File(new_file)
    return djangoFile



if __name__ == '__main__':
    print "Starting Muse population script"
    
    #from muse.settings import *
    from museapp.models import MusicProject, Comment, ExtraFile
    from django.contrib.auth.models import User
    populate()
