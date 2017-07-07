# -*- coding: utf-8 -*-  
#!/usr/bin/python  
import rrdtool
import time
fd=open('1.txt','r')
mymsg=fd.readlines()
print(mymsg[0])
i=0

mylist=[]
#while mymsg[i]:

def message_ipmi(ipaddr):
    try:
        ipmi=ipmitool(ipaddr,'ADMIN','ADMIN')
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

    note_test='/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/lan_print/'+str(ipaddr[0])+'.txt'
    note_test="".join(note_test.split())
    outputfile=open(note_test,'wb')
    line=outputfile.write(str(my_msg))
    outputfile.flush()
    outputfile.close()
    del(outputfile)

    fd=open(note_test,'rw')
    mymsg=fd.readlines()
    print(mymsg[0])
    try:
        newmsg=mymsg[5].split(':')[0]
        nowmsg=mymsg[13].split(':')[0]
    except:
#       print(str(nowmsg))
        print("IIIIIIIIIIIIIIIIIII--------------------")
#    msg=list(msg.split())
#    print(msg)

for mylist in mymsg:
	message_ipmi(mylist)
	cur_time=str(int(time.time()))
		    
#	mystr='/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/view/'+str(mymsg[i])+'1.rrd'
	newstr=str(mymsg[i])
	mystr='/home/zhangshuo/sub/ipmitest/ipmitool/ipmi/rrdtext/'+newstr+'.rrd'
	mystr="".join(mystr.split())
	print(str(mystr))
	i=i+1
	rrd=rrdtool.create(str(mystr),'--step','300','--start',cur_time,

  'DS:new1:GAUGE:600:0:U',
  'DS:new2:GAUGE:600:0:U',
  'DS:new3:GAUGE:600:0:U',
  'DS:new4:GAUGE:600:0:U',
  'DS:new5:GAUGE:600:0:U',
  'DS:new6:GAUGE:600:0:U',

  'RRA:AVERAGE:0.5:1:600',
  'RRA:AVERAGE:0.5:6:700',
  'RRA:AVERAGE:0.5:24:775',
  'RRA:AVERAGE:0.5:288:797',
  'RRA:MAX:0.5:1:600',
  'RRA:MAX:0.5:6:700',
  'RRA:MAX:0.5:24:775',
  'RRA:MAX:0.5:444:797',
  'RRA:MIN:0.5:1:600',
  'RRA:MIN:0.5:6:700',
  'RRA:MIN:0.5:24:775',
  'RRA:MIN:0.5:444:797')

	if rrd:
	    print rrdtool.error()

