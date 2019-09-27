'''
A prototype of FRC team 1817 scouting
ranking system

"It's tired, I'm late"~Gage 1/19/18 11:21PM
"There's a universe where I'm in my bed sleeping"
"Turns out that all Gages are in the same plane"
"There's like 3 Gages that aren't insane"

Convention:
o=offensive
d=defensive
s=scale

----------CSV----------
0. Team Number
1. Offensive Switch(Boxes:Time Held)
2. Defensive Switch(Boxes:Time Held)
3. Scale(Boxes:Time Held:Time Active)
4. Auto Cross
5. Auto Switch Time
6. Exchange Boxes
7. Climb Type
---------------------
'''

import csv

#CLIMB_TYPES=['lifting','self','reliant']
CLIMB_TYPES=['reliant','self','lifting']

SWITCH_TIME=135

class robot():
    
    #each of the ranking scores
    o_switch_boxes=0
    o_switch_time=0
    d_switch_boxes=0
    d_switch_time=0
    s_boxes=0
    s_time=0
    s_active=0
    exchange_boxes_=0
    auto_cross_=0
    auto_s_time=0
    
    #climb data
    climb_score=0
    climb_percent=0
    
    total_matches=0
    
    def __init__(self):
        '''Init all data to zero'''
        pass
    
    def update_with_csv(self,data):
        '''Update the team stats with new excel data'''
        o_switch=data[0].split(';')
        d_switch=data[1].split(';')
        s_data=data[2].split(';')
        self.total_matches+=1
        
        if data[3]=='y': self.auto_cross_+=1
        if int(data[4])>0: self.auto_s_time+=int(data[4])
        climb_val=0
        if data[6] in CLIMB_TYPES:
            self.climb_percent+=1
            climb_val+=1
            for elem in CLIMB_TYPES:
                if elem==data[6]: 
                    self.climb_score+=climb_val
                    break
                climb_val+=1
        if int(data[5])>9:
            self.exchange_boxes_+=9
        else: 
            self.exchange_boxes_+=int(data[5])    
        self.o_switch_boxes+=int(o_switch[0])
        self.o_switch_time+=int(o_switch[1])
        self.s_boxes+=int(s_data[0])
        self.s_time+=int(s_data[1])
        self.s_active+=int(s_data[2])
        self.d_switch_boxes+=int(d_switch[0])
        self.d_switch_time+=int(d_switch[1])
    
    def update_with_tba(self):
        '''Update the team stats with all present 2017 TBA data'''
        pass
    
    def _average(self):
        self.climb_percent=self.climb_percent/self.total_matches
        self.climb_score=self.climb_score/self.total_matches
        self.o_switch_boxes=self.o_switch_boxes/self.total_matches
        self.o_switch_time=self.o_switch_time/self.total_matches
        self.d_switch_boxes=self.d_switch_boxes/self.total_matches
        self.d_switch_time=self.d_switch_time/self.total_matches
        self.s_active=self.s_active/self.total_matches
        self.s_boxes=self.s_boxes/self.total_matches
        self.s_time=self.s_time/self.total_matches
        self.auto_cross_=self.auto_cross_/self.total_matches
        self.auto_s_time=self.auto_s_time/self.total_matches
        
    def getOPR(self):
        '''Calculate 1817 version of OPR and return it'''
        
        self._average()
        ret=0
        
        #Total Percentage of time owned
        o_switch_totalp=((self.o_switch_time/SWITCH_TIME*100)/100)*5
        #Total Percentage of blocks placed on offensive switch
        o_switch_playedp=2*(self.o_switch_boxes/(self.o_switch_boxes+self.d_switch_boxes+self.s_boxes)*100)/100
        ret+=o_switch_totalp+o_switch_playedp
        d_switch_totalp=1.5*((self.d_switch_time/SWITCH_TIME*100)/100)
        d_switch_playedp=0.5*(self.d_switch_boxes/(self.o_switch_boxes+self.d_switch_boxes+self.s_boxes)*100)/100
        ret+=d_switch_totalp+d_switch_playedp
        s_totalp=3*(self.s_time/(self.s_active))
        s_playedp=(self.s_boxes/(self.o_switch_boxes+self.d_switch_boxes+self.s_boxes)*100)/100
        ret+=s_totalp+s_playedp
        ret+=(self.exchange_boxes_/5)
        ret+=(self.auto_s_time/14)
        ret+=self.auto_cross_
        ret+=self.climb_percent*(self.climb_score/3)*5
        return(ret)
    
    def toString(self):
        print('offensive switch boxes',self.o_switch_boxes/self.total_matches)
        print('offensive switch time',self.o_switch_time/self.total_matches)
        print('Defensive switch boxes',self.d_switch_boxes/self.total_matches)
        print('Defensive switch time',self.d_switch_time/self.total_matches)
        print('Scale boxes',self.s_boxes/self.total_matches)
        print('Scale time',self.s_time/self.total_matches)
        print('Auto Cross',self.auto_cross_/self.total_matches)
        print('Auto Switch',self.auto_s_time/self.total_matches)
        print('Climb percentage',self.climb_percent/self.total_matches)
        print('Climb Score',self.climb_score/self.total_matches)
        print('Exchange Boxes',self.exchange_boxes_/self.total_matches)
        print('Scale Boxes',self.s_boxes/self.total_matches)
        print('Scale time',self.s_time/self.total_matches)
    
    
def main():
    #file=open('C:\\Users\\Brian\\Desktop\\FRC 2018\\Sample.csv','r')
    file=open('gages file path','r')
    reader=csv.reader(file)
    
    teams={}
    
    flag=False
    for row in reader:
        if not flag:
            flag=True
            continue
        if row[0] in teams.keys():
            bot=teams[row[0]]
            bot.update_with_csv(row[1:])
        else:
            teams.update({row[0]:robot()})
            bot=teams[row[0]]
            bot.update_with_csv(row[1:])
    
    picklist=[]
    flag=False
    
    for t, obj in teams.items():
        print('----------\nFRC team {}\n----------'.format(t))
        opr=obj.getOPR()
        if not flag:
            picklist.append(t+' '+str(opr))
            flag=True
        else:
            if opr<float(picklist[-1].split(' ')[-1]):
                picklist.append(t+' '+str(opr))
            else:
                pos=0
                while pos<len(picklist) and opr<=float(picklist[pos].split(' ')[-1]):
                    pos+=1
                picklist.insert(pos,t+' '+str(opr))
        print(opr)
    print('\n\n')
    for elem in picklist: print(elem)
    file.close()

main()
    
    
    


