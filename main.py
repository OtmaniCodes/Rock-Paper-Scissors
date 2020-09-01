from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation as an
from random import randint, choice
from kivy.clock import Clock
from time import sleep
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class ImageBtn(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageBtn, self).__init__(**kwargs)
        self.allow_stretch= True
        self.keep_rotio= False


class Popups(Popup):
    def __init__(self, title, txt, **kwargs):
        super(Popups, self).__init__(**kwargs)
        self.size_hint= [None, None]
        self.size= [300, 140]
        self.pos_hint= {'top':.7, 'center_x':.5}
        self.title= title
        self.title_size= '15sp'
        self.separator_height= 5
        self.separator_color= get_color_from_hex('#FFFFFF')
        self.the_container= FloatLayout(size_hint=[1,1])
        self.warning= Label(text=txt.title(), font_size='18sp', bold=True, size_hint=[.9, .3],
                            pos_hint={'center_y':.6,'center_x':.5})
        if title == 'Exit!':
            self.height= 180
            self.auto_dismiss= False
            self.btn1= Button(text='cancel', size_hint=[.4, .2], font_size='15sp',
                              pos_hint={'top':.22, "x":.05}, background_normal="", background_color=[0,0,0,1])
            self.btn2= Button(text='yes', size_hint=[.4, .2], font_size='15sp',
                              pos_hint={'top':.22, "x": .55}, background_normal="", background_color=[0,0,0,1])
            self.btn1.bind(on_release= lambda x: self.dismiss())
            self.btn2.bind(on_release= lambda x: app.kill_app())
            self.the_container.add_widget(self.btn1)
            self.the_container.add_widget(self.btn2)
        elif title == 'about this game?':
            self.height= 300
            self.pos_hint= {'top':.83, 'center_x':.5}
            self.warning.font_size='15sp'
            self.warning.size_hint=[.9,.9]
            self.pos_hint={'top':.85,'center_x':.5}

        self.the_container.add_widget(self.warning)
        self.add_widget(self.the_container)

class ManagerSc(ScreenManager):
    pass
class HomePage(Screen):
    pass
class PlayPage(Screen):
    pass


class MainApp(App):
    clicked= ''
    clocks= 0
    opp= ""
    you= ""

    def build(self):
        Window.size=(360, 640)
        return Builder.load_file('main.kv')

    def reset_all(self):
        self.clicked= ''
        self.clocks= 0
        self.opp= ""
        self.you= ""
        self.root.ids.play.ids.opponent.source= 'imgs/empty.png'
        self.root.ids.play.ids.you.source= 'imgs/empty.png'
        self.root.ids.play.ids.score.text= 'the score'
        self.root.ids.play.ids.score.szz= '45sp'
        self.root.ids.play.ids.score.clr= [0,0,0,.3]

    def process(self, me, him):
        self.res= ""
        self.me= me
        self.him= him
        if self.me == 'scissors' and self.him == 'scissors':
            self.res= 'tie'
        elif self.me == 'scissors' and self.him == 'paper':
            self.res= 'you'
        elif self.me == 'scissors' and self.him == 'rock':
            self.res= 'foe'
        if self.me == 'paper' and self.him == 'scissors':
            self.res= 'foe'
        elif self.me == 'paper' and self.him == 'paper':
            self.res= 'tie'
        elif self.me == 'paper' and self.him == 'rock':
            self.res= 'you'
        if self.me == 'rock' and self.him == 'scissors':
            self.res= 'you'
        elif self.me == 'rock' and self.him == 'paper':
            self.res= 'foe'
        elif self.me == 'rock' and self.him == 'rock':
            self.res= 'tie'
        return self.res

    def animate_go_btn(self, target, what):
        if what == 1:
            anime= an(sz=[.7, .06], clr=[1,0,0,.8], ps={'top':.08, 'x':.15},
                    d=0.1, c= [1,0,0,.8])
            anime.start(target)
        elif what == 2:
            animea= an(sz=[.9, .08], clr=[1,1,1,1], ps= {'top':.1, 'x':.05},
                    d=0.5, c= [0,0,0,1])
            animea.start(target)

    def play(self):
        self.bomb= Clock.schedule_interval(self.change_img, 0.2)
        
    def change_img(self, *args):
        self.clocks+= 1
        if self.clocks <= 20:
            opponent= self.root.ids.play.ids.opponent
            self.one= {1:'imgs/rock.png', 2:'imgs/paper.png', 3:'imgs/scissors.png'}[randint(1,3)]
            opponent.source= self.one
        else:
            self.bomb.cancel()
            if self.one == 'imgs/rock.png':
                self.opp= 'rock'
            elif self.one == 'imgs/paper.png':
                self.opp= 'paper'
            elif self.one == 'imgs/scissors.png':
                self.opp= 'scissors'
        self.get_res()

    def get_res(self):
        if self.you != '' and self.opp != '':
            self.the_res= self.process(self.you, self.opp)
            self.show_res(self.the_res)

        else: pass

    def show_res(self, res, *args):
        self.board= self.root.ids.play.ids.score
        if res == 'you':
            self.board.text= 'you won'.upper()
            self.board.clr= [0,1,0,1]
            self.board.szz= '60sp'

        elif res == 'foe':
            self.board.text= 'you lost'.upper()
            self.board.clr= [1,0,0,1]
            self.board.szz= '60sp'

        elif res == 'tie':
            self.board.text= 'a tie'.upper()
            self.board.clr= [0,0,0,1]
            self.board.szz= '60sp'
        self.you= ''
        self.opp= ''

    def show_popup(self, why_popup):
        if why_popup == 'BtnUnclicked':
            pop= Popups(title='little warning!',
                        txt='you should select one\nof the three options first...')
        elif why_popup == 'exit':
            pop= Popups(title='Exit!',
                        txt='are you sure you want to exit?')
        elif why_popup == 'about':
            with open('about.txt', 'r') as f:
                content= f.read()
            pop= Popups(title='about this game?',
                        txt=content)
        pop.open()

    def kill_app(self):
        self.stop()


if __name__ == '__main__':
    app= MainApp()
    app.run()