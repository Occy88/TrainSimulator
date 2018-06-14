class GameState:

    def __init__(self,intro,main):
        self.intro=intro
        self.main=main
        self.story=False

    def introToMain(self):
        self.intro=False
        self.main=True

    def introToStory(self):
        self.intro=False
        self.story=True

    def storyToIntro(self):
        self.intro=True
        self.story=False

    def mainToIntro(self):
        self.main=False
        self.intro=True

    def encode(self):
        dict={'idClass': 10, 'intro': self.intro, 'main': self.main}
        return dict