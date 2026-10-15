emails = """Alice@Gmail.com
bob@yahoo.com
CHARLIE@outlook.com
alice@gmail.com
Bob@Yahoo.com
dave@hotmail.com
EVE@GMAIL.COM
charlie@outlook.com
frank@gmail.com
alice@gmail.com   
DAVE@hotmail.com"""

with open("emails.txt","w") as File:
    File.write(emails)

with open("emails.txt","r")as File:
    raw_mail=File.readlines()
    
cleand=[]
for i in raw_mail:
    i=i.strip().lower()
    if i:
        cleand.append(i)
        
uniqe=set(cleand)
new_mails=sorted(uniqe)

with open("unique_emails.txt","w") as File:
    for i in new_mails:
        File.write(i+"\n")

with open("unique_emails.txt","r")as File:
    string=File.read()
    
    print(string)