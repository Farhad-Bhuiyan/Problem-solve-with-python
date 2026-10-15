def safe_read(filename):
    try:
        with open(filename, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: File not found.")
    else:
        print(content)
    finally:
        print("Operation complete.")
        
def create_file(filename, content):
    with open(filename,"w")as File:
        File.write(content)
        
filename=input()
content=input()
if content:
    create_file(filename,content)

safe_read(filename)
