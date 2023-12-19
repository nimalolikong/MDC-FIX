import re
num = 'となりの家のアネットさん THE ANIMATION'
if re.search(r)
num = number.upper()
if '-' in num:
    return num
index = 0
while num[index].isdigit():
    index += 1 

    
head = index    
while num[index].isdigit() == False:
         index = index + 1
prefix = num[head:index]
suffix = num[index:]
return prefix + '-' + suffix