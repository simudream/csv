import csv
import paramiko
import re
    
#delcare all the variable as list
hostnames = []
sitenames = []
macaddresses =[]
passwords = []
ips = []

#declare readcsv function and parameters required
def readcsv(csvname,user='admin',port='221'):
    
    #open the csv file
    with open(csvname) as csvfile:
        readcsv = csv.reader(csvfile,delimiter=',')
    
        
        #start the loop to insert all data on the lists
        for counter,row in enumerate (readcsv): 
            #this line is to skip the first record on each column, because it's just a title
            if counter == 0:
                continue
            #add the data into the list
            hostnames.append(row[0])
            sitenames.append(row[1]) 
            macaddresses.append(row[2])
            passwords.append(row[7])
            ips.append(row[10])
        
        #print the lists
        print (hostnames)
        print (sitenames) 
        print (macaddresses)
        print (passwords)
        print (ips)
        
#declare the main function    
#hahaha fuck you
def main():
    
    
    
    #call the readcsv function
    readcsv('cara.csv')
    
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.31.2', username='sbaruffi', password='foreignguy')
    
    chan = ssh.invoke_shell()
    
    buff = ''
    
    while not buff.endswith('# '):
        resp = chan.recv(9999)
        buff += str.encode(resp)
    
    # Ssh and wait for the password prompt.
    chan.send('show clients\n')
    buff = ''
    
    while not buff.endswith('# '):
        resp = chan.recv(9999)
        buff += resp
        print ('buff', buff)
    
    total = []
    names = []
    ipss = []
    lines = buff.split('\r\n')
    for cnt,line in enumerate(lines):
        if cnt < 6:
            continue
        #result =  [s.strip() for s in line.split('  ') if s.strip()]
        list_ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line)
        list_names = line.split(' ', 1)[0]
        
        
        
        if line.__len__()>30 and list_ips.__len__()>0:
            print ("Client name: " + str(list_names) + " have the ip address of " + str(list_ips))
            
            
            
        
            
        #if result.__len__()> 9:
        #    names.append(result[0].rstrip())
        #    ipss.append(result[1].rstrip())
    
   # print ipss
    

#     
#     #go fuck you python
#     list_ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(total))
#     
#     newlist = []
#     for i in list_ips:
#         newlist.append(i.split('\t')[0])
#     
#     for i in newlist:
#         print i
#         
#     

    ssh.close()
   
  
        
   
   
    exit()
    
    
#required line to declare main 
if __name__ == '__main__': main()    
    