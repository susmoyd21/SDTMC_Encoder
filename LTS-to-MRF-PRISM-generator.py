import sys
import os
fn=sys.argv[1]
fn1=os.path.basename(fn)
with open(fn,'r') as f:
    lines=f.readlines()
f.close()
# Pre-processing the file to infer states, transitions, actions, probabilities and initial distribution.
tran_list=[]
initial=''
for i in range(len(lines)):
    if i==0:
        origin='s'+lines[i].split(',')[-1].rstrip()[:-1]
        initial=origin
        action='tau'
        dest=[]
        prob=[]
        cp=1.0
        il=lines[i].split('(')[-1].split(',')[0].split(' ')
        if len(il)>1:
            il1=0
            il2=1
            while il1<=len(il):
                dest.append(il[il1])
                il1+=2
            while il2<len(il):
                p=float(il[il2].split('/')[0])/float(il[il2].split('/')[-1])
                prob.append(p)
                cp-=p
                il2+=2
            prob.append(str(cp))
        else:
            dest.append(il[0])
            prob.append('1.0')
        for j in range(len(prob)):
            tlm=[]
            tlm.append(origin)
            tlm.append(action+'.s'+dest[j])
            tlm.append(str(prob[j]))
            tran_list.append(tlm)
        continue
    a=lines[i].rstrip().split(',')
    origin=''
    action=''
    dest=[]
    prob=[]
    cp=1.0
    for j in range(1,len(a[0])):
        origin+=a[0][j]
    for h in range(1,len(a)-1):
        for j in range(1,len(a[h])):
            if a[h][j]!=')' and a[h][j]!='"':
                action+=a[h][j]
            if j+1==len(a[h]) and a[h][j]!=')' and a[h][j]!='"':
                action+='_'  
    if action.startswith("label("):
        continue
    action=action.replace('(','_')
    action=action.replace(')','')    
    action=action.replace(',','_')
    action=action.replace(' ','')
    a[-1]=a[-1][:-1]
    b=a[-1].split(' ')
    if len(b)>1:
        j=0
        k=1
        while j<=len(b):
            dest.append(b[j])
            j+=2
        while k<len(b):
            p=float(b[k].split('/')[0])/float(b[k].split('/')[-1])
            prob.append(p)
            cp-=p
            k+=2
        prob.append(str(cp))
    else:
        dest.append(b[0])
        prob.append('1.0')
    for k in range(len(dest)):
        tlm=[]
        tlm.append('s'+origin)
        tlm.append(action+'.s'+dest[k])
        tlm.append(str(prob[k]))
        tran_list.append(tlm)
state={}
action=[]
prism_pr_adj={}
for i in range(len(tran_list)):
    if tran_list[i][0].split('s')[-1] not in state:
        state[tran_list[i][0].split('s')[-1]]=tran_list[i][0]
    if tran_list[i][1].split('.')[-1].split('s')[-1] not in state:
        state[tran_list[i][1].split('.')[-1].split('s')[-1]]=tran_list[i][1].split('.')[-1]
    if tran_list[i][1].split('.')[0] not in action and tran_list[i][1].split('.')[0]!='tau':
        action.append(tran_list[i][1].split('.')[0])
    if str(tran_list[i][0]) not in prism_pr_adj:
        prism_pr_adj[str(tran_list[i][0])]={}
        prism_pr_adj[str(tran_list[i][0])][str(tran_list[i][1])]=str(tran_list[i][-1])
    else:
        prism_pr_adj[str(tran_list[i][0])][str(tran_list[i][1])]=str(tran_list[i][-1])
deadlock=list(set(state.values())-set(prism_pr_adj.keys()))
# print(state)
# print(action)
# print(prism_pr_adj)
# CONVERTING THE ADTMC TO SDTMC USING THE MODEL EMBEDDING ats FOR PROBABILISTIC SYSTEMS.
labels={}
mapping={}
ats_adj={}
transition_count=1
ctr=0
for x in prism_pr_adj:
    a=x
    b=prism_pr_adj[x]
    #print(a,b)
    if a not in labels:
        labels[a]='bot'
    if a not in mapping:
        mapping[a]=a
    for y in b:
        if y not in mapping and y.split('.')[0]!='tau':
            mapping[y]='s'+str(len(state)+ctr)
            ctr+=1
        if y not in labels and y.split('.')[0]!='tau':
            labels[mapping[y]]=y.split('.')[0]
    if x not in ats_adj:
        ats_adj[x]={}
        for y in prism_pr_adj[x]:
            if y.split('.')[0]!='tau':
                ats_adj[x][mapping[y]]=prism_pr_adj[x][y]
                transition_count+=1
            else:
                ats_adj[x][y.split('.')[-1]]=prism_pr_adj[x][y]
                transition_count+=1
for x,y in mapping.items():
    if x!=y:
        ats_adj[y]={x.split('.')[-1]:1.0}
        transition_count+=1
for x in deadlock:
    labels[x]='bot'
    mapping[x]=x
# Creating the Labels (.lab) File.
Lab={'"init"':0,'"deadlock"':1,'"bot"':2}
ctr=3
for i in labels.values():
    if '"'+i+'"' not in Lab:
        Lab['"'+i+'"']=ctr
        ctr+=1
ats_labels=''
for i in Lab:
    ats_labels+=str(Lab[i])+'='+str(i)+' '
ats_labels=ats_labels[:-1]
sorted_lab1={}
for i in labels:
    sorted_lab1[int(i.split('s')[-1])]=labels[i]
sorted_lab2 = {key: value for key, value in sorted(sorted_lab1.items())}
for i in sorted_lab2:
    if 's'+str(i)!=initial and 's'+str(i) not in deadlock:
        ats_labels+='\n'+str(i)+':'+' '+str(Lab['"'+sorted_lab2[i]+'"'])
    elif 's'+str(i)==initial:
        ats_labels+='\n'+str(i)+':'+' 0'+' '+str(Lab['"'+sorted_lab2[i]+'"'])
    else:
        ats_labels+='\n'+str(i)+':'+' 1'+' '+str(Lab['"'+sorted_lab2[i]+'"'])
#print(ats_labels)
# Creating the State and Transitions File.
tran=str(len(mapping))+' '+str(transition_count)
sorted_adj1={}
for i in ats_adj:
    sorted_adj1[int(i.split('s')[-1])]={}
    for j in ats_adj[i]:
        sorted_adj1[int(i.split('s')[-1])][int(j.split('s')[-1])]=ats_adj[i][j]
sorted_adj2 = {key: value for key, value in sorted(sorted_adj1.items())}
#print(sorted_adj2)
for i in sorted_adj2:
    for j in sorted_adj2[i]:
        if sorted_adj2[i][j]=='1.0':
            tran+='\n'+str(i)+' '+str(j)+' '+'1'
        else:
            tran+='\n'+str(i)+' '+str(j)+' '+str(sorted_adj2[i][j])
#print(tran)
state_file='(s)'
for i in range(len(mapping)):
    state_file+='\n'+str(i)+': ('+str(i)+')'
#print(state_file)
# Writing the Information into respective Files.
if fn1.endswith('.lts'):
    fn1=fn1.split('.lts')[0]
else:
    fn1=fn1.split('.aut')[0]
with open('ats'+fn1+'.tra','w') as file:
    file.write(tran)
file.close()
with open('ats'+fn1+'.lab','w') as file:
    file.write(ats_labels)
file.close()
with open('ats'+fn1+'.sta','w') as file:
    file.write(state_file)
file.close()
