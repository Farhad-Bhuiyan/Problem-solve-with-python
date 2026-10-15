def read_lines():
    with open("log.txt","r")as file:
        txt=file.read()
        print(txt)

def add_log(content):
    with open("log.txt","a")as File:
        File.write(content+"\n")

with open("log.txt","w")as f:
    f.write("")
     
content1="User logged in"
content2="File uploaded"
add_log(content1)
add_log(content2)
read_lines()