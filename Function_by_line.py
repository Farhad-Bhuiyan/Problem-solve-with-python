def read_lines(filename):
    with open(filename,"r")as file:
        txt=file.readlines()
        cnt=1;
        for i in txt:
            print(f"{cnt}: {i}",end='')
            cnt+=1

def create_file(filename, content):
    with open(filename,"w")as File:
        File.write(content)
    
content="""Apple
Banana
Cherry
"""
filename=input()
create_file(filename,content)
read_lines(filename)