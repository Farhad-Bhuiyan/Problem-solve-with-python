def read_from_position(filename, position):
    with open(filename,"r")as f:
        f.seek(position)
        print(f.read())
        
def create_file(filename, content):
    with open(filename,"w")as File:
        File.write(content)
        
filename=input()
content=input()
position=int(input())
create_file(filename,content)
read_from_position(filename,position)