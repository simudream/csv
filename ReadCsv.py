import csv
import paramiko
    
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
        print hostnames
        print sitenames 
        print macaddresses
        print passwords
        print ips
        
#declare the main function    
def main():
    #call the readcsv function
    readcsv('cara.csv')
    
    #start loop for the ssh connection
    for cnt,host in enumerate (hostnames): 
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ips[cnt], username='admin', password=passwords[cnt], port=221 , timeout=120)    
        except Exception as e:
            print "Hostname: "  + hostnames[cnt] + str(e) 
            pass
    #run a command on the ssh connection
    #stdin, stdout ,stderr = ssh.exec_command(cmd[], timeout=cmd[self.SSH_TIMEOUT_INDEX])
    
    
    #exit the program
    exit()
    
    
#required line to declare main 
if __name__ == '__main__': main()    
    