from django.test import TestCase
from museapp.models import MusicProject
from django.contrib.auth.models import User, UserManager
from django.contrib import auth
from django.core.urlresolvers import reverse

def createTestUser(client):
    user = User.objects.create_user(username = "TestUser",password = "TestPassword")


class homePageViewTests(TestCase):

    def testView(self):
        #check view renders
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

class accountPanelTests(TestCase):
    def setUp(self):
        user = createTestUser(self.client)

    def testWhenNotLoggedIn(self):
        #check that account Panel displays correctly when not logged in

        response = self.client.get(reverse("home"))
        
        #Should have Sign In and Sign Up buttons
        self.assertEqual(response.status_code, 200)                                   
        self.assertContains(response, "Sign In")
        self.assertContains(response, "Sign Up")
        
        #Should not have Sign Out, UserPage, NewProject or Delete Account Buttons
        self.assertNotContains(response, "Sign Out")
        self.assertNotContains(response, "'s Page")
        self.assertNotContains(response, "Create New Project")
        self.assertNotContains(response, "Delete Account")

    def testWhenLoggedIn(self):
        #check that account panel displays correctly when logged in

        self.client.login(username = "TestUser", password = "TestPassword")
        response = self.client.get(reverse("home"))

        #Should have Sign Out, UserPage, NewProject and Delete Account Buttons
        self.assertEqual(response.status_code, 200)                                   
        self.assertContains(response, "Sign Out")
        self.assertContains(response, "'s Page")
        self.assertContains(response, "Create New Project")
        self.assertContains(response, "Change Password")
        self.assertContains(response, "Delete Account")

        #Should not have Sign In or Sign Up buttons
        self.assertNotContains(response, "Sign In")
        self.assertNotContains(response, "Sign Up")

    def testUserPageButton(self):
        #check that the userpage button displays the username

        self.client.login(username = "TestUser", password = "TestPassword")
        response = self.client.get(reverse("home"))

        #UserPage button should display "username's Page"
        self.assertContains(response, "TestUser's Page")


class aboutViewTests(TestCase):

    def testView(self):
        #check view renders
        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)

class userLoginViewTests(TestCase):
    def setUp(self):
        user = createTestUser(self.client)

    def testGetView(self):
        #Test get returns a form and a message

        response = self.client.get(reverse("login"))
        
        self.assertEqual(response.status_code, 200)                                   
        self.assertContains(response, "login_form")
        self.assertContains(response, "Please login!")

    def testBadDetails(self):
        #Test bad login details don't log the user in

        response = self.client.post(reverse("login"),{"name":"TestUser","passwd":"WrongPassword"})

        #Check page displays
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "login_form")

        #Check user not logged in
        self.assertFalse(User.objects.get(username="TestUser").is_authenticated())

    def testCorrectDetails(self):
        #Test user is logged in and redirected

        response = self.client.post(reverse("login"),{"name":"TestUser","passwd":"TestPassword"}, follow = True)

        self.assertEqual(response.status_code, 200)

        #Check user logged in
        self.assertTrue(User.objects.get(username="TestUser").is_authenticated())

        #Check page redirects
        self.assertTrue(len(response.redirect_chain)>0)

class userLogoutViewTests(TestCase):
    def setUp(self):
        user = createTestUser(self.client)
        

    def testGetView(self):
        #check view redirects and that user is logged out afterwards

        self.client.login(username = "TestUser", password = "TestPassword")
        response = self.client.get(reverse("logout"))

        #Check view redirects
        self.assertEqual(response.status_code, 302)

        #Check user logged out
        self.assertFalse(User.objects.get(username="TestUser").is_authenticated())

class registerViewTests(TestCase):

    def testGetView(self):
        #check view renders

        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)

    def testEmptyPost(self):
        #check user not created on an empty post

        response = self.client.post(reverse("register"))

        self.assertEqual(response.status_code, 200)

        #check no user has been created
        self.assertEqual(User.objects.count(), 0)

    def testCorrectPost(self):
        #check user created on a correct post

        response = self.client.post(reverse("login"),{"name":"TestUser","passwd":"TestPassword"}, follow = True)

        self.assertEqual(response.status_code, 200)

        #check a user is created
        self.assertEqual(User.objects.count(), 1)

        #check logged in
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

        

        

        
            
        

        
        


                                
