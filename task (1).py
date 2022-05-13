import sys
def list_sum(li):
    di={}
    end=0
    for i in range(len(li)):
        while(end<len(li)):
            key = tuple(li[i:end+1])
            di[key]=sum(li[i:end+1])
            end+=1
        end=0
    end1 = len(li)-1
    for j in range(len(li)):
        start=j
        while(end1>start+1):
            li1=[]
            li1.append(li[start])
            li1.append(li[end1])
            di[tuple(li1)]=sum(li1)
            end1-=1
        end1=len(li)-1

    return di
    
a = [1,2,3,4,5,6]
b = [9,10,11,12,13,14]


possible_sum_a=list_sum(a)
possible_sum_b=list_sum(b)




for (b_key,b_val) in possible_sum_b.items() :
        for(a_key,a_val) in possible_sum_a.items():
            if a_val==b_val:
                print(a_key,b_key)
                sys.exit()
print(0)

            
        
            
            


    


    

