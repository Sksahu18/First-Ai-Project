import pandas as pd
import sys
import math
sys.setrecursionlimit(10**6)

#here throughout the code we used index as node number for simplicity to map and access simply
#index of (name of node) ie; Index(df.name) as node no. just to print the output as name of location(Str) not node no.(Int)

n=50     #max number of nodes
df=pd.read_csv("C:\\Users\\sant\\Desktop\\lpu_mapc.csv")
neigh=df.neighbour1  
#x and y coordinate of node [index of cx and cy as node no.]
cx=df.x_coordinate
cy=df.y_coordinate
neighbour=[] #list of neighbours,list contains the list of neighbouring nodes
Name=df.name
Name=list(Name) #list of name of node(ie;location) 


path=[]
dist=0.0
min_dist=math.inf
best_path=[]
d=0
total_path=0
def trace_path(end,start,parent):
    global dist
    global min_dist
    global d
    global total_path
    path.append(end)
    node=path[-1]
    
    if len(path)<=1:
        dist=0
    else:
        if len(path)>1:
            node2=path[-2]
            d=(((cx[node]-cx[node2])**2)+((cy[node]-cy[node2])**2))**(1/2)    #distance to reach last node from second last node
            dist+=(((cx[node]-cx[node2])**2)+((cy[node]-cy[node2])**2))**(1/2)  #adding each new distance
            #print("distance++ ",dist,"d= ",d)
            
    if end==start:
        total_path+=1   #it counts the total no. of path to reach the goal
        P=[]
        for k in path[::-1]:
            P.append(df.name[k])
        print(P)
        print("distance= ",dist)
        min_dist=min(dist,min_dist)
        if dist<=min_dist:
            best_path.clear()
            for c in P:
                best_path.append(c)
        return
    else:
        parents=parent[node]
        for i in parents:
            trace_path(i,start,parent)
            dist-=d
            path.pop(-1)
            #print("distance-- ",dist,"d= ",d)
            if len(path)<=1:
                dist=0
            else:
                if len(path)>1:
                    node2=path[-2]
                    d=(((cx[node]-cx[node2])**2)+((cy[node]-cy[node2])**2))**(1/2)
            
            
parent=[[-1]]*n     #it will contain the list of (list of previous nodes) via which we reached here, each node(represented by index)
def bfs(start,end):
    q=[]
    visited=[False]*n
    explored=[False]*n
    
    q.append(start)
    visited[start]=True
    
    while len(q)!=0:
        node=q.pop(0)
        explored[node]=True
        
        child=neighbour[node]
        if node==end:
            break
        
        for next in child:
            next=int(next)
            if visited[next]!=True:
                q.append(next)
                visited[next]=True
            if explored[next]!=True:
                x=[]
                for i in parent[next]:
                    if i!=-1:
                        x.append(i)
                x.append(node)
                parent[next]=x
            if next==end:
                break
                
                
                
                                
dic={}
count=0
#it will recommend the exact name and node no. of all nodes available matching with your input string if name is not known fully 
def recm(src):
    global count
    for i in range(len(src),0,-1):
        dic.clear()
        for j in df.name:
            if src[:i]==j[:i]:
                count=1
                dic[Name.index(j)]=j
        if count==1:
            break
    print(dic)

if __name__=="__main__":
    print(" 1.Drive\n","2.Walk\n")
    a=int(input())
    if a==2:
        neigh=df.neighbour2
#since in csv file column neighbour contain neighbour nodes separated by commas[reads as a string]    
    for i in range(len(neigh)):
        x=[]
        j=0
        while j<len(neigh[i]):
            s=""         #since each letter counts as a new string, to get correct value loop till it encounters a comma
            while j<len(neigh[i]) and neigh[i][j]!=",":
                s+=neigh[i][j]
                j+=1
            s=int(s)
            x.append(s)
            j+=1
        neighbour.append(x)
    
    src=input("Source name: ")
    recm(src)
    conf_src=int(input("confirm node: "))
    dest=input("Destination name: ")
    recm(dest)
    conf_dest=int(input("confirm node: "))
    print("\n")
    bfs(conf_src,conf_dest)
    trace_path(conf_dest,conf_src,parent)
    print("\noptimal path= ",best_path)
    print("distance= ",min_dist)
    print("total path available: ",total_path)
