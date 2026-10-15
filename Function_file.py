def create_file(filename, content):
    with open(filename,"w")as File:
        File.write(content)
        
def output(filename):
    with open(filename,"r") as File:
        print(File.read())

filename=input()
content=input()

create_file(filename,content)
output(filename)