#List of all apps and menu to open them
#copyright (c) 2015 Tyler Spadgenske
#GPL License
###############################
#To be packaged with stock TYOS
###############################

import sys, time
import pygame

class Run():
    def __init__(self, fona):
        #Stuff to follow app protocol
        self.exit = False
        self.blit_one_surface = {'surface':[], 'rects':[]}
        self.blit = {'surfaces':[], 'rects':[]}
        self.next_app = None

        #Get list of installed apps
        self.get_app_order()
        #Setup clock
        self.start_time = time.time()
        #Stuff for intro animation
        self.stock_image = pygame.image.load('/home/pi/zero-phone/' + self.app_order[0] + '.png')
        self.stock_rect = self.stock_image.get_rect()
        self.load_icons()
        #More variables
        self.open_app = None
        
    def run_app(self):
        if self.open_app != None and self.open_app < len(self.app_order):
            self.next_app = self.app_order[self.open_app]
            self.exit = True
        
    def get_events(self, event):
        #Check for touch to open an app
        if event.pos[0] < 52 and event.pos[1] > 29 and event.pos[1] < 78:
            self.open_app = 0
        if event.pos[0] < 104 and event.pos[0] > 52 and event.pos[1] < 78 and event.pos[1] > 29:
            self.open_app = 1
        if event.pos[0] < 156 and event.pos[0] > 104 and event.pos[1] < 78 and event.pos[1] > 29:
            self.open_app = 2
        if event.pos[0] < 208 and event.pos[0] > 156 and event.pos[1] < 78 and event.pos[1] > 29:
            self.open_app = 3

    def on_first_run(self):
        self.open_app = None

    def load_icons(self):
        for i in range(0, len(self.app_order)):
            #Add icon and rect
            self.blit['surfaces'].append(pygame.image.load('/home/pi/zero-phone/'  + self.app_order[i] + '.png'))

            self.stock_rect = self.stock_image.get_rect()
            self.stock_rect.centery = 52
            self.stock_rect.centerx = 26 + 52 * i
            self.blit['rects'].append(self.stock_rect)
                
    def get_app_order(self):
        #Get the order of the apps to be blitted
        order_file = open('/home/pi/zero-phone/order.txt', 'r')
        order = order_file.readlines()

        #Remove newlines /n
        for i in range(0, len(order)):
            order[i] = order[i].rstrip()

        self.app_order = order[4:]
