
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import *
import random
from random import randint
import pandas as pd
from brainflow.board_shim import *
from brainflow.board_shim import BoardShim, BrainFlowInputParams,BoardIds
from PyQt5.QtCore import Qt
import winsound as sd
from threading import Thread
import os
from pprint import pprint
from datetime import datetime
import zmq
from time import time, sleep
import numpy as np
import struct
random.seed()

# parameters
    
class WindowClass(QMainWindow):
    def __init__(self) :
        super().__init__()
        self.setGeometry(0,0,width, height)
        self.setWindowTitle('Set Protocol')
        self.data_list=[]
        self.time_list=[]
        self.count_list=[]
        self.timer = QTimer(self)
        self.time =0
        #label
        self.label = QLabel("실험을 시작하려면 시작하기 버튼을 눌러주세요", self)
        font1 = self.label.font()
        font1.setBold(True)
        font1.setPointSize(40)
        self.label.setFont(font1)
        self.label.setGeometry(1200,350,1300,500)
        #button
        self.btn_1= QPushButton("시작하기",self)
        self.btn_1.setGeometry(1650,800,200,80)
        self.btn_1.clicked.connect(self.btn_1_clicked)
        
    
    def btn_1_clicked(self):
        global trial
        global last
        self.label.clear()
        self.btn_1.hide()
        global ref ,r_num, ran_n, a, target, total_time
        ref =2000
        last=0
        r_num=0
        
        
        target=["받아","보내","꺼줘","켜줘","열어","닫아","이전","다음","감사","미안"]
        QTimer.singleShot(0, self.beepsound) #1
        QTimer.singleShot(0, self.time_1)
        QTimer.singleShot(2000, self.time_1)
        QTimer.singleShot(2000, self.beepsound)


        for trial in range(1):    
            ran_n = 0 
            random.shuffle(target)
            
            for i in range(10):
                QTimer.singleShot(ref, self.point) #1
                QTimer.singleShot(ref+5000, self.close1) 

                
                QTimer.singleShot(ref+5000, self.record)
                 
    
                QTimer.singleShot(ref+5002, self.point1) 
                
                QTimer.singleShot(ref+11000,self.close3)
                last= 5000 + 6000 
                ref += last
            
            '''
            if trial != 9:
                QTimer.singleShot(ref+125000,self.resting)
                QTimer.singleShot(ref+134950, self.close5)
                QTimer.singleShot(ref+135000, self.beepsound)
            else:
                break 
            '''
                
        QTimer.singleShot(ref+125000+5,self.thank)
        QTimer.singleShot(ref+125000+500,self.pr_data)   
        QTimer.singleShot(ref+125000+5000,self.clo)
            
    def pr_data(self):
        #board.stop_stream()
        #board.release_session()
        data = board.get_board_data()
        data=pd.DataFrame(data)
        data.to_csv("result_01.csv")
        
    def record(self):
        global a, target, ran_n
        if target[ran_n] == "받아":
            a = 2
        elif target[ran_n] == "보내":
            a = 3
        elif target[ran_n] == "꺼줘":
            a = 4
        elif target[ran_n] == "켜줘":
            a = 5
        elif target[ran_n] == "열어":
            a = 6
        elif target[ran_n] == "닫아":
            a = 7
        elif target[ran_n] == "이전":
            a = 8
        elif target[ran_n] == "다음":
            a = 9
        elif target[ran_n] == "감사":
            a = 10
        elif target[ran_n] == "미안":
            a = 11                 

    def ran(self):
        global ran_n
        ran_n += 1    
    def save(self):
        #data_save=pd.concat(self.data_list)
        data_save = pd.DataFrame(self.data_list)
        data_save.to_csv("result_01.csv")

    def thank(self):
        protocol.thank(self)

    def rest(self):
        protocol.rest(self)

    def time_n(self):
        global a
        board.insert_marker(a)
        
        #self.time_list.append(time.time())
        #self.count_list.append(a)
      

    def time_1(self):
        board.insert_marker(1)
    
        
    def clo(self):
        self.close()
    def beepsound(self):
        fr = 2000    # range : 37 ~ 32767
        du = 150     # 1000 ms ==1second
        sd.Beep(fr, du) # winsound.Beep(frequency, duration)
         
    def point (self):
        global a
        protocol.point(self)

       

    def random(self): 
        global transparency_level
        protocol.random(self)
        
        
    def point1(self):
        global transparency_level, ran_n, total_time
        total_time = 0
        transparency_level = 4
        protocol.point1(self)
        self.timer = QTimer(self)
        self.reset_timer_interval()
        self.timer.timeout.connect(self.update_label_color)
        self.timer.start()

    def reset_timer_interval(self):
        global total_time
        intervaltime = random.randrange(600, 1501)
        self.timer.setInterval(intervaltime)
        total_time += intervaltime

    def resting(self):
        protocol.resting(self)
        a =randint(0, 50)   
        random.seed(a) 
        random.shuffle(target)          

    def close1(self):
        label2.close()  
       
    def close2(self):
        label3.close() 
      
    def close3(self):
        global ran_n
        label4.close()  
  
        
    def close4(self):
        label5.close() 
        
    def close5(self):
        label7.close()

    def update_label_color(self):
        global label4, receive_data, transparency_level, a, total_time,ran_n
        receive_data = a

        if receive_data != a:
            transparency_level += 1
            if transparency_level > 4:
                transparency_level = 4
        elif receive_data == a:
            transparency_level -= 1
            if transparency_level < 0:
                transparency_level = 0
        else:
            transparency_level = 0

        opacity = 1 - transparency_level / 4
        label4.setStyleSheet(f"color: rgba(0, 0, 255, {opacity})")

        if transparency_level == 0:
            self.timer.stop()
            
            ran_n += 1
            if ran_n == 10:
                ran_n = 0

        self.reset_timer_interval()   
        
class protocol(WindowClass):
    def __init__(self) :
        super().__init__()
        
    def point(self):
        global label2
        label2 = QLabel("+",self)
        font2 = label2.font()
        #font2.setBold(True)
        font2.setPointSize(400)
        label2.setFont(font2)
        label2.setGeometry(1600,530,400,320)
        label2.show()
    
                
    def close1():
        label2.close()
                
    def random(self):
        global target
        global label3   
        
        
        label3= QLabel(target[ran_n],self)
        font2 = label3.font()
        font2.setBold(True)
        font2.setPointSize(240)
        label3.setFont(font2)
        font2.setFamily('초코쿠키체')
        label3.setGeometry(1480,530,640,320)
        label3.show()
        
    def close2():
        label3.close()
        
    def point1(self):
        global label4 
        label4 = QLabel(target[ran_n],self)
        font2 = label4.font()
        font2.setBold(True)
        font2.setPointSize(240)
        label4.setStyleSheet(f"color: rgba(0, 0, 255, {0})")
        label4.setFont(font2)
        label4.setGeometry(1480,530,640,320)
        label4.show()
        

 

        
    def close3():
        label4.close() 
    def point_blue(self):
        global label5
        label5 = QLabel("·",self)
        font2 = label5.font()
        label5.setStyleSheet("color: blue")
        font2.setBold(True)
        font2.setPointSize(300)
        label5.setFont(font2)
        label5.setGeometry(1700,650,200,100)
        label5.show()
        
    def close4():
        label5.close()
    def thank(self):
        global label6
        label6=QLabel("      실험이 모두 종료되었습니다.\n 참가하신 피험자님 고생 많으셨습니다.",self)
        font3 = label6.font()
        font3.setBold(True)
        font3.setPointSize(50)
        label6.setFont(font3)
        label6.setGeometry(1100,550,1500,300)
        label6.show()
    '''   
    def rest(self):
        global label7
        label7=QLabel("                           쉬는 시간입니다.\n 5분간 휴식 후 진행 할 예정이니 휴대폰을 하거나 안정을 취하세요.",self)
        font4 = label7.font()
        font4.setBold(True)
        font4.setPointSize(50)
        label7.setFont(font4)
        label7.setGeometry(900,550,2100,300)
        label7.show()
    '''
    def resting(self):
        global label7
        label7=QLabel("휴식",self)
        font4 = label7.font()
        font4.setBold(True)
        font4.setPointSize(50)
        label7.setFont(font4)
        label7.setGeometry(1700,550,2100,300)
        label7.show()    
    
    def close5(self):
        label7.close()    

        
class fun:
    def start_board():
        serial_port= "COM4"
    
        params = BrainFlowInputParams() 
        params.serial_port = serial_port 
        params.serial_number = '' 
        params.timeout = 0 
        params.other_info = '' 
        params.file = '' 
        params.mac_address = '' 
        params.ip_address = '' 
        params.ip_port = 0 
        params.ip_protocol = 0
        board = BoardShim(BoardIds.CYTON_DAISY_BOARD, params)

        board.prepare_session()
        #board.config_board('xU060100X') 
        board.start_stream()
        return board



        
        
if __name__ == "__main__" :

    board_id=2
    pprint(BoardShim.get_board_descr(board_id))
    board = fun.start_board()

    
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    screen_rect = app.desktop().screenGeometry()
    width,height = screen_rect.width(), screen_rect.height()
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()
    
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    
    