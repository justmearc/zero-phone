#Message App
#copyright (c) 2015 Tyler Spadgenske
#MIT License
################################
#To be packaged with stock TYOS#
################################

import pygame, time, os
from pygame.locals import *

class Run():
    def __init__(self, fona):
        self.fona = fona
        self.next_app = None

        #Colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.send = False
        self.valid = False

        #Variables
        self.mode = 3
        self.number = ''
        self.message = ''
        self.first = False

        self.sms_messages = {'messages':[], 'senders':[]}
        self.page = 1

        #Load images
        self.keyboard_image = pygame.image.load('/home/pi/zero-phone/keyboard.png')
        self.num_keyboard_image = pygame.image.load('/home/pi/zero-phone/numbered_keyboard.png')
        self.bubble = pygame.image.load('/home/pi/zero-phone/bubble.png')
        self.keyboard_rect = self.keyboard_image.get_rect()
        self.keyboard_rect.x = 4
        self.keyboard_rect.y = 190

        #Main conversation image
        self.conversation_image = pygame.image.load('/home/pi/zero-phone/conversation.png')
        self.conversation_rect = self.conversation_image.get_rect()
        self.conversation_rect.centerx = 104
        self.conversation_rect.centery = 169

        #Setup text
        #Setup fonts
        self.font = pygame.font.Font('/home/pi/zero-phone/arial.ttf', 20)
        self.message_font = pygame.font.Font('/home/pi/zero-phone/arial.ttf', 12)

        #please wait Text
        self.wait = self.font.render('Please wait...', True, self.BLACK, self.WHITE)
        self.wait_rect = self.wait.get_rect()
        self.wait_rect.centerx = 104
        self.wait_rect.centery = 156

        #Says... text
        self.says_text1 = self.font.render('Tyler says...', True, self.BLACK, self.WHITE)
        self.says_rect1 = self.says_text1.get_rect()
        self.says_rect1.x = 23
        self.says_rect1.y = 78
        self.says_text2 = self.font.render('Billy says...', True, self.BLACK, self.WHITE)
        self.says_rect2 = self.says_text2.get_rect()
        self.says_rect2.x = 23
        self.says_rect2.y = 151

        #Message lines
        self.message_line1 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message_line1_rect = self.message_line1.get_rect()
        self.message_line1_rect.x = 27
        self.message_line1_rect.y = 101
        self.message_line2 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message_line2_rect = self.message_line2.get_rect()
        self.message_line2_rect.x = 27
        self.message_line2_rect.y = 115
        self.message_line3 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message_line3_rect = self.message_line3.get_rect()
        self.message_line3_rect.x = 27
        self.message_line3_rect.y = 129

        self.message2_line1 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message2_line1_rect = self.message2_line1.get_rect()
        self.message2_line1_rect.x = 27
        self.message2_line1_rect.y = 176
        self.message2_line2 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message2_line2_rect = self.message2_line2.get_rect()
        self.message2_line2_rect.x = 27
        self.message2_line2_rect.y = 190
        self.message2_line3 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message2_line3_rect = self.message2_line3.get_rect()
        self.message2_line3_rect.x = 27
        self.message2_line3_rect.y = 205

        #Number to send
        #Setup numbers Text
        self.number_text = self.font.render(self.number, True, self.BLACK, self.WHITE)
        self.number_rect = self.number_text.get_rect()
        self.number_rect.x = 10
        self.number_rect.y = 37

        #Setup numbers Text
        self.line1 = self.font.render(self.message, True, self.BLACK, self.WHITE)
        self.line1_rect = self.line1.get_rect()
        self.line1_rect.x = 10
        self.line1_rect.y = 85

        #Setup numbers Text
        self.line2 = self.font.render(self.message, True, self.BLACK, self.WHITE)
        self.line2_rect = self.line2.get_rect()
        self.line2_rect.x = 10
        self.line2_rect.y = 98

        #Setup numbers Text
        self.line3 = self.font.render(self.message, True, self.BLACK, self.WHITE)
        self.line3_rect = self.line3.get_rect()
        self.line3_rect.x = 10
        self.line3_rect.y = 111

        self.bubble_rect = self.bubble.get_rect()
        self.bubble_rect.x = 3
        self.bubble_rect.y = 33

        #Stuff to follow app protocol
        self.exit = False
        self.blit_one_surface = {'surface':[], 'rects':[]}
        self.blit_mode1 = {'surfaces':[self.keyboard_image, self.bubble, self.line1, self.line2,
                                 self.line3, self.number_text], 'rects':[self.keyboard_rect, self.bubble_rect, self.line1_rect, self.line2_rect,
                                                       self.line3_rect, self.number_rect]}
        self.blit_mode2 = {'surfaces':[self.conversation_image, self.says_text1, self.says_text2, self.message_line1,
                                       self.message_line2, self.message_line3,
                                       self.message2_line1, self.message2_line2,
                                       self.message2_line3], 'rects':[self.conversation_rect,
                                                                                           self.says_rect1, self.says_rect2,
                                                                      self.message_line1_rect, self.message_line2_rect,
                                                                      self.message_line3_rect, self.message2_line1_rect,
                                                                       self.message2_line2_rect,self.message2_line3_rect]}
        self.blit_mode3 = {'surfaces':[self.wait], 'rects':[self.wait_rect]}
        self.blit = self.blit_mode2
        self.load_contacts()

    def load_contacts(self):
        self.contacts = {'names':[], 'numbers':[]}
        try:
            contact_file = open('/home/pi/zero-phone/configure/contacts.conf', 'r')
        except:
            print '***********************************************************'
            print 'NO CONTACTS FOUND'
            print 'PLEASE EDIT /home/pi/zero-phone/configure/contacts.conf FILE'
            print '***********************************************************'
            if not os.path.exists('/home/pi/zero-phone/configure'):
                os.mkdir('/home/pi/zero-phone/configure')
            if not os.path.exists('/home/pi/zero-phone/logs'):
                os.mkdir('/home/pi/zero-phone/logs') #May be in wrong spot, but it works
            contact_file = open('/home/pi/zero-phone/configure/contacts.conf', 'w+')
            contact_file.write('#Contacts\n')
            contact_file.write('#Use format name=number i.e. Joe=1555666777 # are comments\n')
            contact_file.close()
            contact_file = open('/home/pi/zero-phone/configure/contacts.conf', 'r')

        self.contact_list = contact_file.readlines()
        contact_file.close()

        for i in range(0, len(self.contact_list)):
            if self.contact_list[i][0] == '#':
                pass
                #Do Nothing. Line is comment
            else:
                self.contact_list[i] = self.contact_list[i].rstrip().split('=')

    def on_first_run(self):
        self.first = False
        self.mode = 3

    def get_sms(self):
        #Set to text mode
        self.fona.transmit('AT+CMGF=1')
        self.fona.transmit('AT+CSDH=1')
        #Get number of sms messages
        num_sms = self.fona.transmit('AT+CPMS?')
        num_sms = num_sms[1]
        num_sms = num_sms.split(',')
        num_sms = num_sms[1]
        print 'SMS FOUND IN MEMORY: ' + num_sms
        print 'LOADING SMS MESSAGES...'
        #Retrieve sms messages
        for i in range(1, int(num_sms) + 1):
            self.sms_messages['senders'].append(self.fona.transmit('AT+CMGR=' + str(i))[1].split('"')[3].replace('+',''))
            self.sms_messages['messages'].append(self.fona.transmit('AT+CMGR=' + str(i))[2])

        #If in contacts, replace number with name
        for i in self.contact_list:
            index = 0
            for senders in self.sms_messages['senders']:
                if i[1] == senders:
                    self.sms_messages['senders'][index] = i[0]
                index += 1

        #If there are less than two messages, do some configuring
        if int(num_sms) < 2:
            self.sms_messages['senders'].append('')
            self.sms_messages['messages'].append('')
            if int(num_sms) == 0:
                self.sms_messages['senders'].append('')
                self.sms_messages['messages'].append('')

    def config_sms(self):
        self.blit['surfaces'][1] = self.font.render(self.sms_messages['senders'][(self.page + 1) * -1] + ' says...', True, self.BLACK, self.WHITE)
        self.blit['surfaces'][2] = self.font.render(self.sms_messages['senders'][self.page * -1] + ' says...', True, self.BLACK, self.WHITE)
        #Box 1
        self.blit['surfaces'][3] = self.font.render(self.sms_messages['messages'][(self.page + 1) * -1][:25], True, self.BLACK, self.WHITE)
        if len(self.sms_messages['messages'][(self.page + 1) * -1]) > 25:
            self.blit['surfaces'][4] = self.font.render(self.sms_messages['messages'][(self.page + 1)* -1][25:50], True, self.BLACK, self.WHITE)
            if len(self.sms_messages['messages'][(self.page + 1) * -1]) > 50:
                self.blit['surfaces'][5] = self.font.render(self.sms_messages['messages'][(self.page + 1)* -1][50:75], True, self.BLACK, self.WHITE)
            else:
                self.blit['surfaces'][5] = self.font.render('', True, self.BLACK, self.WHITE)
        else:
            self.blit['surfaces'][4] = self.font.render('', True, self.BLACK, self.WHITE)
            self.blit['surfaces'][5] = self.font.render('', True, self.BLACK, self.WHITE)

        #Box 2
        self.blit['surfaces'][6] = self.font.render(self.sms_messages['messages'][self.page * -1][:25], True, self.BLACK, self.WHITE)
        if len(self.sms_messages['messages'][self.page * -1]) > 25:
            self.blit['surfaces'][7] = self.font.render(self.sms_messages['messages'][self.page * -1][25:50], True, self.BLACK, self.WHITE)
            if len(self.sms_messages['messages'][self.page * -1]) > 50:
                self.blit['surfaces'][8] = self.font.render(self.sms_messages['messages'][self.page * -1][50:75], True, self.BLACK, self.WHITE)
            else:
                self.blit['surfaces'][8] = self.font.render('', True, self.BLACK, self.WHITE)
        else:
            self.blit['surfaces'][7] = self.font.render('', True, self.BLACK, self.WHITE)
            self.blit['surfaces'][8] = self.font.render('', True, self.BLACK, self.WHITE)

    def run_app(self):
        if self.mode == 3:
            self.blit = self.blit_mode3
            if self.first:
                time.sleep(5)
                self.mode = 2
                self.blit = self.blit_mode2
                self.sms_messages = {'messages':[], 'senders':[]}
                self.get_sms()
                self.config_sms()
            self.first = True

        if self.exit:
            self.mode = 2
        if len(self.number) > 0:
            self.valid = True
        else:
            self.valid = False
            self.send = False
        if self.send and self.valid:
            self.send = False
            self.valid = False
            self.fona.transmit('AT+CMGF=1')
            time.sleep(.25)
            self.fona.transmit('AT+CMGS="' + self.number + '"')
            time.sleep(0.25)
            self.fona.transmit(self.message)
            time.sleep(.25)
            self.fona.transmit(chr(26))
            self.mode = 2
            self.blit = self.blit_mode2

    def get_events(self, event):
        if self.mode != 2:
            self.get_keyboard_events(event)
        else:
            self.get_read_events(event)

    def get_read_events(self, event):
        if event.pos[0] > 23 and event.pos[0] < 185:
            if event.pos[1] > 40 and event.pos[1] < 68:
                self.page += 1
                if self.page == len(self.sms_messages['senders']):
                    self.page = len(self.sms_messages['senders']) - 1
                self.config_sms()

            if event.pos[1] > 229 and event.pos[1] < 262:
                self.page -= 1
                if self.page == 0:
                    self.page = 1
                self.config_sms()
            if event.pos[1] > 267 and event.pos[1] < 296:
                self.mode = 0
                self.blit = self.blit_mode1

    def get_keyboard_events(self, event):
        #Get key pressed
        #Row 1
        if event.pos[1] > 189 and event.pos[1] < 215:
            if event.pos[0] > 4 and event.pos[0] < 20:
                if self.mode == 1:
                    self.message = self.message + 'q'
                else:
                    self.number = self.number + '1'
            if event.pos[0] > 24 and event.pos[0] < 40:
                if self.mode == 1:
                    self.message = self.message + 'w'
                else:
                    self.number = self.number + '2'
            if event.pos[0] > 44 and event.pos[0] < 60:
                if self.mode == 1:
                    self.message = self.message + 'e'
                else:
                    self.number = self.number + '3'
            if event.pos[0] > 64 and event.pos[0] < 81:
                if self.mode == 1:
                    self.message = self.message + 'r'
                else:
                    self.number = self.number + '4'
            if event.pos[0] > 85 and event.pos[0] < 101:
                if self.mode == 1:
                    self.message = self.message + 't'
                else:
                    self.number = self.number + '5'
            if event.pos[0] > 105 and event.pos[0] < 121:
                if self.mode == 1:
                    self.message = self.message + 'y'
                else:
                    self.number = self.number + '6'
            if event.pos[0] > 125 and event.pos[0] < 141:
                if self.mode == 1:
                    self.message = self.message + 'u'
                else:
                    self.number = self.number + '7'
            if event.pos[0] > 145 and event.pos[0] < 161:
                if self.mode == 1:
                    self.message = self.message + 'i'
                else:
                    self.number = self.number + '8'
            if event.pos[0] > 165 and event.pos[0] < 181:
                if self.mode == 1:
                    self.message = self.message + 'o'
                else:
                    self.number = self.number + '9'
            if event.pos[0] > 185 and event.pos[0] < 202:
                if self.mode == 1:
                    self.message = self.message + 'p'
                else:
                    self.number = self.number + '0'
        #Row 2
        if event.pos[1] > 219 and event.pos[1] < 244:
            if event.pos[0] > 12 and event.pos[0] < 28:
                if self.mode == 1:
                    self.message = self.message + 'a'
            if event.pos[0] > 32 and event.pos[0] < 48:
                if self.mode == 1:
                    self.message = self.message + 's'
            if event.pos[0] > 52 and event.pos[0] < 75:
                if self.mode == 1:
                    self.message = self.message + 'd'
            if event.pos[0] > 72 and event.pos[0] < 88:
                if self.mode == 1:
                    self.message = self.message + 'f'
            if event.pos[0] > 92 and event.pos[0] < 109:
                if self.mode == 1:
                    self.message = self.message + 'g'
            if event.pos[0] > 112 and event.pos[0] < 129:
                if self.mode == 1:
                    self.message = self.message + 'h'
            if event.pos[0] > 133 and event.pos[0] < 149:
                if self.mode == 1:
                    self.message = self.message + 'j'
            if event.pos[0] > 153 and event.pos[0] < 169:
                if self.mode == 1:
                    self.message = self.message + 'k'
            if event.pos[0] > 173 and event.pos[0] < 189:
                if self.mode == 1:
                    self.message = self.message + 'l'
        #Row 3
        if event.pos[1] > 248 and event.pos[1] < 274:
            if event.pos[0] > 32 and event.pos[0] < 48:
                if self.mode == 1:
                    self.message = self.message + 'z'
            if event.pos[0] > 52 and event.pos[0] < 75:
                if self.mode == 1:
                    self.message = self.message + 'x'
            if event.pos[0] > 72 and event.pos[0] < 88:
                if self.mode == 1:
                    self.message = self.message + 'c'
            if event.pos[0] > 92 and event.pos[0] < 109:
                if self.mode == 1:
                    self.message = self.message + 'v'
            if event.pos[0] > 112 and event.pos[0] < 129:
                if self.mode == 1:
                    self.message = self.message + 'b'
            if event.pos[0] > 133 and event.pos[0] < 149:
                if self.mode == 1:
                    self.message = self.message + 'n'
            if event.pos[0] > 153 and event.pos[0] < 169:
                if self.mode == 1:
                    self.message = self.message + 'm'
        #Row 4
        if event.pos[1] > 278 and event.pos[1] < 304:
            if event.pos[0] > 32 and event.pos[0] < 75:
                if self.mode == 1:
                    self.message = self.message[:-1]
                else:
                    self.number = self.number[:-1]
            if event.pos[0] > 72 and event.pos[0] < 129:
                if self.mode == 1:
                    self.message = self.message + ' '
            if event.pos[0] > 133 and event.pos[0] < 169:
                self.send = True

        #Keyboard mode
        if event.pos[0] > 3 and event.pos[0] < 207 and event.pos[1] > 33 and event.pos[1] < 51:
            self.mode = 0
        if event.pos[0] > 3 and event.pos[0] < 207 and event.pos[1] > 57 and event.pos[1] < 142:
            self.mode = 1

        if self.mode == 0:
            self.blit['surfaces'][0] = self.num_keyboard_image
        else:
            self.blit['surfaces'][0] = self.keyboard_image

        self.blit['surfaces'][2] = self.font.render(self.message[:32], True, self.BLACK, self.WHITE)
        self.blit['surfaces'][3] = self.font.render(self.message[32:64], True, self.BLACK, self.WHITE)
        self.blit['surfaces'][4] = self.font.render(self.message[64:96], True, self.BLACK, self.WHITE)
        self.blit['surfaces'][5] = self.font.render(self.number, True, self.BLACK, self.WHITE)
