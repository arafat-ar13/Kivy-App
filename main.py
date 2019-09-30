import os

import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '400')

# Fixes to make
# TODO: Check for username accuracy along with password's
# TODO: Only show the latest user's email on login page
# TODO: Don't popup empty field warning if only password and repeat password fields are faulty

class WelcomeScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        self.welcome = Label(
            text="Welcome to my company!! Sign up or login below", color=[55, 0, 1, 1])
        self.add_widget(self.welcome)

        self.login = Button(text="Login", font_size=30, size_hint=(1.2, 0.5))
        self.login.bind(on_release=self.login_func)
        self.add_widget(self.login)

        animation = Animation(background_color=[0, 0, 1, 1])
        animation.start(self.login)

        self.signup = Button(text="Signup", font_size=30, size_hint=(1.2, 0.5))
        self.signup.bind(on_release=self.signup_func)
        self.add_widget(self.signup)

        animation = Animation(background_color=[0, 1, 0, 1])
        animation.start(self.signup)

    def signup_func(self, instance):
        ebay_who.screen_manager.current = "Signup Page"

    def login_func(self, instance):
        ebay_who.screen_manager.current = "Login Page"


class SignupScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="First Name: "))
        self.first_name = TextInput(multiline=False)
        self.inside.add_widget(self.first_name)

        self.inside.add_widget(Label(text="Last Name: "))
        self.last_name = TextInput(multiline=False)
        self.inside.add_widget(self.last_name)

        self.inside.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.inside.add_widget(Label(text="Password"))
        self.password = TextInput(password=True, multiline=False)
        self.inside.add_widget(self.password)

        self.inside.add_widget(Label(text="Enter password again"))
        self.again_password = TextInput(password=True, multiline=False)
        self.inside.add_widget(self.again_password)

        self.add_widget(self.inside)

        self.signup = Button(text="Sign up", font_size=30)
        self.add_widget(self.signup)
        self.signup.bind(on_press=self.check_if_empty)
        self.signup.bind(on_press=self.check_password)

    def check_password(self, instance):
        if self.password.text != "":
            if self.password.text == self.again_password.text:
                self.write_to_file()

                popup = Popup(title="Signup confirmation", content=Label(
                    text="Welcome!!", color=[0, 1, 0, 1]), size_hint=(0.6, 0.2))
                popup.open()

                ebay_who.home_page.update_info("Welcome to your home page")
                ebay_who.screen_manager.current = "Home Page"

            else:
                self.password.text = self.again_password.text = ""

                popup = Popup(title="Password check error", content=Label(
                    text="You passwords didn't match", color=[1, 0, 0, 1]), size_hint=(0.6, 0.2))
                popup.open()

    def check_if_empty(self, instance):
        if not self.first_name.text or not self.last_name.text or not self.email.text or not self.password.text:
            empty_warning = Popup(title="Input fields empty", content=Label(
                text="You cannot leave the fields empty", color=[1, 0, 0, 1]), size_hint=(0.6, 0.2))
            empty_warning.open()

    def write_to_file(self):
        first_name = self.first_name.text
        last_name = self.last_name.text
        email = self.email.text

        # Hashing the password for security
        password = self.password.text[::-1]

        with open("login_info.txt", "w") as file:
            file.write(f"{first_name},{last_name},{email},{password}")


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        if os.path.isfile("login_info.txt"):
            with open("login_info.txt", "r") as file:
                _, _, email, *_ = file.read().split(",")
        else:
            email = ""

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Email: ", color=[0, 0, 1, 1]))
        self.email = TextInput(text=email, multiline=False)
        self.inside.add_widget(self.email)

        self.inside.add_widget(Label(text="Password"))
        self.password = TextInput(password=True, multiline=False)
        self.inside.add_widget(self.password)

        self.add_widget(self.inside)

        self.submit = Button(text="Submit!", font_size=35)
        self.add_widget(self.submit)
        self.submit.bind(on_press=self.check_password)

    def check_password(self, instance):
        with open("login_info.txt", "r") as file:
            *_, hashed_password = file.read().split(",")
            real_password = hashed_password[::-1]

            if self.password.text == real_password:
                self.password.text = ""

                ebay_who.home_page.update_info("Welcome to your Home Page")
                ebay_who.screen_manager.current = "Home Page"

            else:
                self.password.text = ""

                popup = Popup(title="Wrong password", content=Label(
                    text="Your password is incorrect", color=[1, 0, 0, 1]), size_hint=(0.6, 0.2))
                popup.open()


class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign="center", valign="middle", font_size=35)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)

        # Adding a button to go back to the login screen
        self.back = Button(text="Logout", font_size=30)
        self.add_widget(self.back)
        self.back.bind(on_press=self.logout)

    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)

    def logout(self, *_):
        ebay_who.screen_manager.current = "Login Page"


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.welcome_page = WelcomeScreen()
        screen = Screen(name="Welcome Page")
        screen.add_widget(self.welcome_page)
        self.screen_manager.add_widget(screen)

        self.signup_page = SignupScreen()
        screen = Screen(name="Signup Page")
        screen.add_widget(self.signup_page)
        self.screen_manager.add_widget(screen)

        self.login_page = LoginScreen()
        screen = Screen(name="Login Page")
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)

        self.home_page = HomePage()
        screen = Screen(name="Home Page")
        screen.add_widget(self.home_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    ebay_who = MyApp()
    ebay_who.run()
