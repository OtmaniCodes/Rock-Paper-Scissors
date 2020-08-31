from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation as an


class ManagerSc(ScreenManager):
    pass
class HomePage(Screen):
    pass
class PlayPage(Screen):
    pass

class ImageBtn(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageBtn, self).__init__(**kwargs)
        self.allow_stretch= True
        self.keep_rotio= False


class MainApp(App):
    def build(self):
        Window.size=(360, 640)
        return Builder.load_file('main.kv')

    def animate_go_btn1(self, target):
        anime= an(sz=[.6, .06], clr=[1,0,0,.8], ps={'top':.08, 'x':.2},
                 d=0.1, c= [1,0,0,.8])
        anime.start(target)

    def animate_go_btn2(self, target):
        anime= an(sz=[.9, .08], clr=[1,1,1,1], ps= {'top':.1, 'x':.05},
                  d=0.5, c= [0,0,0,1])
        anime.start(target)

if __name__ == '__main__':
    app= MainApp()
    app.run()