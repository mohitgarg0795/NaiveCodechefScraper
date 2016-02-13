import os
import time

start_time=time.time()

def get_page(url):  #get page source code
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        print error
        exit()

def  get_src_code(url):
    while(1):
        src_code=get_page(url)
        if "Internal Server Error" not in src_code: #check if the page has loaded successfully
            return src_code

def get_links(text):
    end=text.find("Problems Successfully Solved:",0)
    flag=text.find("Problems Partially Solved:",end)
    links=[]
    start=text.find("a href",end)
    while(start<flag):
        start=text.find('"',start)
        end=text.find('"',start+1)
        links.append(text[start+1:end])
        start=text.find("a href",end)
    return links    

def get_ques_name(text):
    pos=text.find("status",0)
    return q[pos + 7:q.find(",",pos+1)]

def decode(text):
    text=text.replace("&#39;","'")
    text=text.replace('&quot;','"')
    text=text.replace('&gt;','>')
    text=text.replace('&lt;','<')
    return text.replace('&amp;','&')

def get_ans_code(text):     #get final solution code text 
    start=src_code.find("/viewsolution/",0)
    start=src_code.find("/",start+1)
    end=src_code.find("'",start)
    ans_id=src_code[start+1:end]    #id of a unique solution code
    ans_code=get_src_code("http://codechef.com/viewplaintext/"+ans_id)[5:-6]
    return decode(ans_code)

def display_time(time_taken):
    hr=int(time_taken)/3600
    min=int(time_taken)/60
    sec=int(time_taken)%60
    print "Total time taken : ",
    if(hr):
        print hr,"hrs",
    if(min):
        print min,"minutes",
    if(sec):
        print sec,"seconds"

flag=1
while(flag):
    username=raw_input("Enter The Username : ")
    username=username.encode("utf-8")

    url="http://codechef.com/users/"+username

    src_code=get_src_code(url)
    if "<title>CodeChef User | CodeChef</title>" in src_code:   #check if username exists or not
        flag=0
    else:
        print "INVALID USERNAME , Please enter the username again : \n"

ques_urls=get_links(src_code)

try:
    os.makedirs(username)
except:
    print "could not make directory"
    exit()

count=1
print "Total AC submissions :",len(ques_urls)
for q in ques_urls:
    url="http://codechef.com/"+q
    ques_name=get_ques_name(q)
    
    src_code=get_src_code(url)
    ans_code=get_ans_code(src_code)

    with open(username + "/" + ques_name + ".txt",'w') as f:
        f.write(ans_code)
    print count,"... done"
    count+=1

print "\nAll Done"
display_time(time.time()-start_time)
print "\nYou can find all your codes at : ",os.getcwd()+'\\' + username
raw_input("\nPress any key to exit")
