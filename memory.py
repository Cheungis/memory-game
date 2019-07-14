# Memory
# version 3
# this program does the following:
# Create window
# Create game
# Play game
# End game
'''
in this version:
 - all features are implemented
'''
from uagame import Window
import pygame, time, random
from pygame.locals import *
from random import shuffle
# User-defined functions

def main():

   window = Window('Memory', 500, 400)
   window.set_auto_update(False)
   game = Game(window)
   game.play()
   window.close()

# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, window):
      # Initialize a Game.
      # - self is the Game to initialize
      # - window is the uagame window object
      
      self.window = window
      self.pause_time = 0.001 # smaller is faster game
      self.close_clicked = False
      self.continue_game = True
      # This is how we call a class method
      Tile.set_window(window)
      Tile.set_image('image0.bmp')
      self.board = []
      self.image_list =[]
      self.create_image_list()
      self.create_board()
      self.score = 0
      self.selected_list = []
                     
   def create_image_list(self):
      for image in range(1,9):
         image_file = 'image'+str(image)+'.bmp'
         temp_img = pygame.image.load(image_file)
         self.image_list.append(temp_img)
         self.image_list.append(temp_img)
      shuffle(self.image_list)

      
   def create_board(self):
      for row_index in range(0,4):
         # create row
         row = self.create_row(row_index)
         # Add row to board
         self.board.append(row)
      
   def create_row(self,row_index):
      # creates one row of objects and returns it
      # -self is the Game object
      # -row_index is the row number to be created
      row = []
      #alternative
      #width = self.window.get_width()//5
      #height = self.window.get_height()//4
      image_index = 0 + 4*row_index
      for col_index in range(0,4):
         
         # Create Tile object
         image = self.image_list[image_index]
         
         width = image.get_width()
         height = image.get_height() 
         x = width * col_index
         y = height * row_index  
         tile = Tile(x,y,width,height,image)
         image_index += 1
         # Add tile to row
         row.append(tile)
      return row

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
          # play frame
         self.handle_event()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         time.sleep(self.pause_time) 

   def handle_event(self):
      # Handle each user event by changing the game state
      # appropriately.
      # - self is the Game whose events will be handled

      event = pygame.event.poll()
      if event.type == QUIT:
         self.close_clicked = True
      if event.type == MOUSEBUTTONUP and self.continue_game:
         self.handle_mouse_up(event)
         
   def handle_mouse_up(self,event):
      for row in self.board:
         for column in row:
            tile = self.board[self.board.index(row)][row.index(column)]
            if tile.select(event.pos):
               tile.swap_image()
               self.selected_list.append(tile)
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      score_string = str(self.score)
      self.window.clear()
      self.window.set_font_size(80)
      window_width = self.window.get_width()
      window_height = self.window.get_height()
      score_width = self.window.get_string_width(score_string)
      x = window_width - score_width
      y = 0
      self.window.draw_string(score_string,x,y)
      for row in self.board:
         for tile in row:
            tile.draw()
      self.window.update()

   def update(self):
      # Update the game objects.
      # - self is the Game to update
      self.score = pygame.time.get_ticks()//1000
      # if the length is 2 or more and is even (every 2 reveals)
      if len(self.selected_list) > 1 and len(self.selected_list)%2 == 0:
         self.check_tile_match()
         
   def check_tile_match(self):
      last_index = len(self.selected_list) - 1
      second_last_index = len(self.selected_list) - 2
      # most recent tile revealed
      last_selected_tile = self.selected_list[last_index]
      # second most recent tile revealed
      second_last_selected_tile = self.selected_list[second_last_index]
      # if they dont contain same image
      if last_selected_tile.get_image() != second_last_selected_tile.get_image():
         # cover both tiles up
         time.sleep(1)
         last_selected_tile.revert_image()
         second_last_selected_tile.revert_image()
         # remove them from the selected list so the game doesn't end prematurely
         del self.selected_list[last_index]
         del self.selected_list[second_last_index]
      
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      if len(self.selected_list) == len(self.image_list):
         self.continue_game = False
class Tile:
   # An object of this class represents a Tile
   # Class Attributes
   window = None
   border_size = 3
   border_color = pygame.Color('black')
   image_0 = None
   # Class Method
   @classmethod
   def set_image(cls, image_string):
      cls.image_0 = pygame.image.load(image_string)
   @classmethod
   def set_window(cls,window):
      cls.window = window
   #Instance Methods
   def __init__(self,x,y,width,height,picture):
      # initializes the Tile object
      # - self is the Tile
      # - x,y are top left corner int coordinates of Tile object
      # - width, height are int dimensions of Tile object
      self.rect = pygame.Rect(x,y,width,height)
      self.display_image = Tile.image_0
      self.real_image = picture
      
   def draw(self):
      # - self is the Tile object to draw
      surface = Tile.window.get_surface()
      # draw image
      surface.blit(self.display_image,self.rect)
      # draw tile
      pygame.draw.rect(surface,Tile.border_color,self.rect,Tile.border_size)
      
   def get_image(self):
      return self.real_image
   
   def select(self,position):
      if self.rect.collidepoint(position) and (Tile.image_0 is self.display_image):
         return True
      else:
         return False
   
   def swap_image(self):
      self.display_image = self.real_image
      
   def revert_image(self):
      self.display_image = Tile.image_0
      
   def __eq___(self, other_tile):
      if self is None or other_tile is None:
         return False
      else:
         print(self.real_image == other_tile.get_image())
         return (self.real_image == other_tile.get_image())
      
      #if self.real_image != None or other_tile.get_image() != None:
         #if self.real_image == other_tile.get_image():
            #return True
      #else:
         #return False

main()