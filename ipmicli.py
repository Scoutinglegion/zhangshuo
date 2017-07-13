#!/usr/local/bin/python
#-*- coding:utf-8 -*-
from __future__ import print_function

import threading
import random
from time import sleep
import re, sys, site, getpass, socket, argparse, collections
import rrdtool
import time
import sys
import os
import atexit
from threading import Thread
from ipmi import ipmitool
import subprocess,os
import smtplib
from email.MIMEText import MIMEText
from email.header import Header
import httplib
import urllib

host  = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"
account  = "C39732322"
password = "5f1127c1b0c233af2cf8a9187d2a158f"

def send_sms(text, mobile):
    params = urllib.urlencode({'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' })
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def SendEmail(fromAdd,toAdd,subject,attachfile,htmlText):
        strFrom=fromAdd;
        strTo=toAdd;
        msg=MIMEText(htmlText);
        msg['Content-Type']='Text/HTML';
        msg['Subject']=Header(subject,'gb2312');
        msg['To']=strTo;
        msg['Ftom']=strFrom;
        smtp=smtplib.SMTP('smtp.163.com');
        smtp.login('18810919149@163.com','123321asdA');
        try:
                smtp.sendmail(strFrom,strTo,msg.as_string());
        finally:
                smtp.close;

#def newtemp(ipaddr):
def fru_ipmi(ipaddr):
    try:
        ipmi=ipmitool(ipaddr[0],ipaddr[1],ipaddr[2])
    except:
        print("Fail to connect")
        return 0
    print(ipmi)
    print(ipaddr)
    try:
        web_ip=ipmi.execute('fru list')
    except:
        print("Error")
        web_ip="None"
        return 0
    msg=ipmi.output
    my_msg=ipmi.output
    note_test='/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/fru_list/'+str(ipaddr[0])+'.txt'
    note_test="".join(note_test.split())
    outputfile=open(note_test,'wb')
    line=outputfile.write(str(my_msg))
    outputfile.flush()
    outputfile.close()
    del(outputfile)
    fd=open(note_test,'rw')
    mymsg=fd.readlines()
    new=""
    print(my_msg)
    return my_msg

def myipaddr(ipaddr):
    try:
	ipmi=ipmitool(ipaddr[0],ipaddr[1],ipaddr[2])
    except:
	print("Fail to connect")
	return 0
    print(ipmi)
    print(ipaddr)
    try:	
	web_ip=ipmi.execute('sel list')
    except:
	print("Error")
	web_ip="None"
	return 0
    msg=ipmi.output
    my_msg=ipmi.output
    print(msg)
#    print("**************")
    note_test='/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/data/'+str(ipaddr[0])+'.txt'
    note_test="".join(note_test.split())
    new_file=open(note_test).read()
#    print(new_file)
#   msg=list(msg.split())
    res=cmp(len(msg),len(new_file))
    print(len(new_file))
    print(res)

    frustr=fru_ipmi(ipaddr)
    frustr=frustr.split('\n')
    mysub=""
    frustr=list(frustr)
    mylen=len(frustr)
    i=0
    for i in range(mylen):
	mysub=mysub+str(frustr[i])+'''<p>'''
    mysub="出现异常的设备："+str(ipaddr[0])+'''<p>'''+mysub
    mysub=mysub+'''<p>'''+'''详细信息：请您进入 http://172.31.105.11:12345/message/'''
    SendEmail("18810919149@163.com","2916639503@qq.com","warning","Error",mysub);

    if res != 0:
	print(my_msg)
	outputfile=open(note_test,'wb')
	line=outputfile.write(str(my_msg))
	outputfile.flush()
	outputfile.close()
	del(outputfile)
	my_msg=my_msg.split('\n')
	new_page=list(my_msg)
	print(new_page[1].split('|')[3])
	flag_str=' Unknown'
	i=0
	mystr=""
	while new_page[i] :
		if 1 != cmp(str(new_page[i].split('|')[3]),flag_str) :
			sel_msg=new_page[i].split('|')
			print(sel_msg)
			if 1 != cmp(str(sel_msg[3]),'Unknown') :
				print(sel_msg[3])
				mystr=mystr+'\n'+''' <p>  日期：'''+str(sel_msg[1])+''' <p>  时间：'''+str(sel_msg[2])+''' <p>  配置：'''+str(sel_msg[3])+''' <p>  事件：'''+str(sel_msg[4])+''' <p> '''+'\n'+'''<p>.'''
#	mystr.append('\n\r')
				msg_str=msg_str+'''  日期：'''+str(sel_msg[1])+'''  时间：'''+str(sel_msg[2])+''' 配置：'''+str(sel_msg[3])+'''  事件：'''+str(sel_msg[4])
		i=i+1
	print(mystr)





	mylist=[]
	def execCmd(cmd):
        	r = os.popen(cmd)
        	text = r.read()
        	r.close()
        	return text
    	myCmd="/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/view/"+str(ipaddr[0])
    	myCmd="".join(myCmd.split())
    	myCmd="sudo cat  "+myCmd+".txt | awk '{print $1,$3,$4,$5,$6}'"
#    	mystr=execCmd("cat new.txt | awk '{print $1,$3,$4}'")

    	mystr=execCmd(myCmd)
    	mystr=mystr.split('\r')
    	i=len(mystr)
    	print(i)
    	new=mystr        #.remove("|")
    	print('working...')
    	print("ip network   ")
    	now=mystr[0].splitlines()
#    	print(now)
    	my_sub=""
    	print(new)
    	mylist=""
    	for mylist in now:
        	mylist= filter(lambda x:x !='|',mylist)
        	my_sub=my_sub+str(mylist)+'''<p>'''
        	print(mylist)
	my_sub="出现异常的设备："+str(ipaddr[0])+'''<p>'''+"以下是最新服务器IPMI状态，包括温度和电压："+'''<p>'''+my_sub
	SendEmail("18810919149@163.com","2916639503@qq.com","warning","Error",my_sub);









	newgraph(ipaddr)
	os.system("cp Flow.png /home/zhangshuo/sub/ipmitest/ipmitool/ipmi/pic")
	os.system("sudo python email_png.py")

	frustr=fru_ipmi(ipaddr)
	frustr=frustr.split('\n')
	mysub=""
	frustr=list(frustr)
	mylen=len(frustr)
	i=0
	for i in range(mylen):
		mysub=mysub+str(frustr[i])+'''<p>'''
	mysub="出现异常的设备："+str(ipaddr[0])+'''<p>'''+mysub
	mysub=mysub+'''<p>'''+'''详细信息：请您进入 http://172.31.105.11:12345/message/'''
	SendEmail("18810919149@163.com","2916639503@qq.com","warning","Error",mysub);








	mobile = "18810919149"
	text="警报：设备"+ipaddr[0]+"，出现异常："+str(msg_str)
	text=str(text)
	print(send_sms(text, mobile))
    else:
	print("without any problem")




def message_ipmi(ipaddr):
    try:
        ipmi=ipmitool(ipaddr[0],ipaddr[1],ipaddr[2])
    except:
        print("Fail to connect")
        return 0
    print(ipmi)
    print(ipaddr)
    try:
        web_ip=ipmi.execute('lan print 1')
    except:
        print("Error")
        web_ip="None"
        return 0
    msg=ipmi.output
    my_msg=ipmi.output
    note_test='/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/lan_print/'+str(ipaddr[0])+'.txt'
    note_test="".join(note_test.split())
    outputfile=open(note_test,'wb')
    line=outputfile.write(str(my_msg))
    outputfile.flush()
    outputfile.close()
    del(outputfile)

def newgraph(ipaddr):
	title="CPU1 Temp && CPU2 Temp ("+time.strftime('%Y-%m-%d',time.localtime(time.time()))+")"
	"MINUTE:12" 
	"HOUR:1"  
	"HOUR:1" 
	"0:%H"  
	myurl=ipaddr[0]
	mystr1="DEF:msg1="+myurl+".rrd:new1:AVERAGE"
	mystr2="DEF:msg2="+myurl+".rrd:new2:AVERAGE"
	mystr3="DEF:msg3="+myurl+".rrd:new3:AVERAGE"
	mystr4="DEF:msg4="+myurl+".rrd:new4:AVERAGE"
	mystr5="DEF:msg5="+myurl+".rrd:new5:AVERAGE"
	mystr6="DEF:msg6="+myurl+".rrd:new6:AVERAGE"
	mystr1="".join(mystr1.split())
	mystr2="".join(mystr2.split())
	mystr3="".join(mystr3.split())
	mystr4="".join(mystr4.split())
	mystr5="".join(mystr5.split())
	mystr6="".join(mystr6.split())
	mystr1=str(mystr1)
	mystr2=str(mystr2)
	mystr3=str(mystr3)
	mystr4=str(mystr4)
	mystr5=str(mystr5)
	mystr6=str(mystr6)
	rrdtool.graph( "Flow.png", "--start", "-1d","--vertical-label='machine CPU Temp' ","--x-grid","MINUTE:12:HOUR:1:HOUR:1:0:%H","--width","650","--height","230","--title",title,
        mystr1,
        mystr2,
        mystr3,
        mystr4,
        mystr5,
        mystr6,
 "LINE1:msg1#00FF00:CPU1 Temp",  
 "LINE1:msg2#000FFF:CPU2 Temp", 
 "LINE1:msg3#00F0FF:PCH Temp",  
 "LINE1:msg4#0F00FF:System Temp",
 "LINE1:msg5#F000FF:Peripheral Temp",    #以线条方式绘制出流量  
 "LINE1:msg6#00000F:Inlet Temp",    #以线条方式绘制出流量  
 "HRULE:6144#FF0000:Alarm value\\r",    #绘制水平线，作为告警线，阈值为6.1k  
 "COMMENT:\\r",                    #在网格下方输出一个换行符  
 "COMMENT:\\r",
 "GPRINT:msg1:AVERAGE:CPU1 Temp\: %6lf.C",    #绘制入流量平均值  
 "COMMENT: ",
 "GPRINT:msg2:AVERAGE: CPU2 Temp\: %6lf.C",    #绘制出流量平均值  
 "COMMENT:  ",
 "GPRINT:msg3:AVERAGE: PCH Temp\: %6lf.C",    #绘制出流量平均值  
 "COMMENT:      ",
 "GPRINT:msg4:AVERAGE: System Temp\: %6lf.C",    #绘制出流量平均值  
 "COMMENT: ",
 "GPRINT:msg5:AVERAGE: Peripheral Temp\: %6lf.C",    #绘制出流量平均值  
 "COMMENT:  ",
 "GPRINT:msg6:AVERAGE:Inlet Temp\: %6lf.C",    
 "COMMENT:  "
	) 

def hide_page(ipaddr):
    try:
        ipmi=ipmitool(ipaddr[0],ipaddr[1],ipaddr[2])
    except:
        return 0
    web_ip=ipmi.execute('sensor')
    print('working...')
    print("ip network   ")
    msg=ipmi.output
    print(msg)
    mynote='/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/view/'+str(ipaddr[0])+'.txt'
    mynote="".join(mynote.split())

    putfile=open(mynote,'a')
    outputfile=open(mynote,'wb')
    line=outputfile.write(msg)
#line = fo.write( str )
    outputfile.flush()
    outputfile.close()
    del(outputfile)
#    os.system('bash new_graph.sh')

    print("正在进行数据采集....")
    mylist=[]
    def execCmd(cmd):
        r = os.popen(cmd)
        text = r.read()
        r.close()
        return text
#myCmd="cat /home/zhangshuo/sub/ipmitest/ipmitool/ipmi/view/"+str(ipaddr[0])+".txt | awk '{print $1,$3,$4}'"    
    myCmd="/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/view/"+str(ipaddr[0])

    myCmd="".join(myCmd.split())
    myCmd="sudo cat  "+myCmd+".txt | awk '{print $1,$3,$4}'"
#    mystr=execCmd("cat new.txt | awk '{print $1,$3,$4}'")
    mystr=execCmd(myCmd)
    mystr=mystr.split()
    num=len(mystr)


def new_page(ipaddr):
    try:
	ipmi=ipmitool(ipaddr[0],ipaddr[1],ipaddr[2])
    except:
	return 0
    web_ip=ipmi.execute('sensor')
    print('working...')
    print("ip network   ")
    msg=ipmi.output
    print(msg)
    mynote='/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/view/'+str(ipaddr[0])+'.txt'
    mynote="".join(mynote.split())

    putfile=open(mynote,'a')
    outputfile=open(mynote,'wb')
    line=outputfile.write(msg)
#line = fo.write( str )
    outputfile.flush()
    outputfile.close()
    del(outputfile)
#    os.system('bash new_graph.sh')

    print("正在进行数据采集....")
    mylist=[]
    def execCmd(cmd):
	r = os.popen(cmd)
	text = r.read()
	r.close()
	return text
#myCmd="cat /home/zhangshuo/sub/ipmitest/ipmitool/ipmi/view/"+str(ipaddr[0])+".txt | awk '{print $1,$3,$4}'"	
    myCmd="/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/view/"+str(ipaddr[0])

    myCmd="".join(myCmd.split())
    myCmd="sudo cat  "+myCmd+".txt | awk '{print $1,$3,$4}'"	
#    mystr=execCmd("cat new.txt | awk '{print $1,$3,$4}'")
    mystr=execCmd(myCmd)
    mystr=mystr.split()
    num=len(mystr)

    print(num)
    i=2
    new_number=[]
    while i<num :
	mylist.append(mystr[i])
	if len(mystr[i]) > 3 :
		print(mystr[i])
		new_num=float(mystr[i])
		print(new_num)
		new_num=int(new_num)
		new_number.append(new_num)
	i=i+3
    print(new_number)
    queue=list(new_number)
    starttime=int(time.time())  
    myrrd_text='/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/rrdtext/'+str(ipaddr[0])+'.rrd'
    myrrd_text="".join(myrrd_text.split())

    print(myrrd_text)
    update=rrdtool.updatev(myrrd_text,'%s:%s:%s:%s:%s:%s:%s' % (str(starttime),str(queue[0]),str(queue[1]),str(queue[2]),str(queue[3]),str(queue[4]),str(queue[5])))
    print(update)

def test_func(note,ip):
        myipaddr(ip)
	message_ipmi(ip)
	new_page(ip)
	os.system("sudo cp -rf ")

if __name__ == "__main__":
#    ip=('172.30.30.25','ADMIN','ADMIN')
#    ipmi=ipmitool('172.30.30.25','ADMIN','ADMIN')
#    mynum=sys.argv[1]	
    fd=open('1.txt','rw')
    mymsg=fd.readlines()
    print(mymsg[0])
    mylist=[]
    for mylist in mymsg:
        ip=[str(mylist),'ADMIN','ADMIN']
	threads = []
	all_number = 5
	thread_lines = 2
	start_line = 0
	for note in range(0,thread_lines):
		t = threading.Thread(target=test_func, args=(note,ip))
        	threads.append(t)
        	start_line +=1
	for t in threads:
        	t.start()
	for number_line in xrange(start_line,all_number):
        	thread_status = False
        	loop_line = 0
        	while thread_status == False :
			if threads[loop_line].isAlive() == False :
                		t = threading.Thread(target=test_func, args=(loop_line,number_line,))
                		threads[loop_line]=t
                		threads[loop_line].start()
                		thread_status = True
            		else:
                		if loop_line >= thread_lines-1 :
                    			loop_line=0
                		else:
                    			loop_line+=1
	for number_line in xrange(start_line,thread_lines):
        	thread[number_line].exit()

#	main_pthread(ip)
#    i=0
#    while mymsg[i] :
#	ip=[str(mymsg[i]),'ADMIN','ADMIN']
#	myipaddr(ip)    
#	new_page(ip)
#	i=i+1
#    print(ipmi.output)







