st=input()
st=st.split()
ans=[]
for i in st:
    ans.append(i[::-1])

print(' '.join(ans))