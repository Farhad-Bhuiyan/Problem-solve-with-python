names = """aLiCe
  bob  
CHARLIE
alice
 Bob 
dave
EVE
charlie
   frank   
ALICE
  eve  """
  
with open("names.txt","w")as File:
    File.write(names)

with open("names.txt","r")as File:
    name_lst=File.readlines()

clean=[]
for i in name_lst:
    i=i.strip()
    i=i.capitalize()
    if i:
        clean.append(i)

uniq=set(clean)
srt=sorted(uniq)

with open("clean_names.txt","w")as File:
    for n in srt:
        File.write(n+"\n")

with open("clean_names.txt","r")as File:
    print(File.read())