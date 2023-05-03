import json
import os
def func(path):
    content= ''''''
    corrected= []
    with open(path, 'r') as file:
        content= file.read()
    file.close()
    lines= content.split('\n')
    for line in  lines:
        parts= line.split(':')
        if len(parts)>=3:
            text_= parts[1].strip()
            text_= text_.split('-')
            if len(text_)==2:
                name= text_[1].strip()
                message= parts[2].strip()
                text_msg= name+": "+message
                corrected.append(text_msg)
    return corrected
files= os.listdir()
files= [file for file in files if file.endswith('.txt')]
prompt= []
for path in files:
    corrected= func(path)
    person= path.split('with')[1].split('.')[0].strip()
    with open("Conversation with {}.txt".format(person),'w') as file:
        file.write('\n'.join(corrected))
    file.close()    

