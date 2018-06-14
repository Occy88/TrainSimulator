import json
import time

class SpriteSheet:

    def __init__(self, spriteAnimator,spriteFps):
        self.animator = spriteAnimator

        self.currentRow=0
        self.currentColumn=0

        self.startRow = 1
        self.startColumn = 1

        self.endColumn = 1
        self.endRow = 1

        self.numRows = 1
        self.numColumns = 1


        self.hasLooped = False
        self.currentTime=time.time()
        self.oldTime=time.time()
        self.fps=spriteFps


    def draw(self, canvas, cam, pos, angle):
        self.animator.draw(canvas, cam, pos, self.numColumns, self.numRows, self.currentRow, self.currentColumn, angle)

    def setRow(self, numRows, numColumns,startRow, startColumn,endRow,endColumn):
        self.numRows=numRows
        self.numColumns=numColumns
        self.startRow=startRow
        self.startColumn=startColumn
        self.endRow=endRow
        self.endColumn=endColumn

        self.currentColumn=self.startColumn
        self.currentRow=self.startRow

    def resetLoop(self):
        self.hasLooped = False

    def update(self):
        if self.startColumn<self.endColumn:
            if self.currentTime - self.oldTime > 1/self.fps:
                self.oldTime=self.currentTime
                self.currentColumn+=1
                if self.endColumn+1 - self.startColumn>0:
                    if (self.currentColumn-self.startColumn)%(self.endColumn+1-self.startColumn)==0:
                        self.currentRow+=1
                        self.currentColumn=self.startColumn
                        if self.endRow+1-self.startRow>0:
                            if (self.currentRow-self.startRow)%(self.endRow+1-self.startRow)==0:
                                self.hasLooped=True
                                self.currentRow=self.startRow
                        else:
                            self.currentRow=self.startRow
                            self.hasLooped=True
                else:
                    self.hasLooped=True
                    self.currentColumn=self.startColumn
            self.currentTime=time.time()
        if self.startColumn>self.endColumn:
            if self.currentTime - self.oldTime > 1/self.fps:
                self.oldTime=self.currentTime
                self.currentColumn-=1

                if self.currentColumn+ self.numColumns>self.numColumns-2:
                    if (self.currentColumn<=0):
                        self.currentRow+=1
                        self.currentColumn=self.startColumn
                        if self.endRow+1-self.startRow>0:
                            if (self.currentRow-self.startRow)%(self.endRow+1-self.startRow)==0:
                                self.hasLooped=True
                                self.currentRow=self.startRow
                        else:
                            self.currentRow=self.startRow
                            self.hasLooped=True
                else:
                    self.hasLooped=True
                    self.currentColumn=self.startColumn
            self.currentTime=time.time()

    def encode(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
