import csv
import paramiko
import re
import time
import io
#delcare all the variable as list
hostnames = []
sitenames = []
macaddresses =[]
passwords = []
ips = []

class SSHClient():
    """SSH CLient version 1.0"""
    
    def __init__(self):
        self.SERVER_IP = '192.168.31.2'
        self.SERVER_USERNAME = 'sbaruffi' 
        self.SERVER_PASSWORD = 'foreignguy'
        self.SERVER_PORT = 22
        self.SSH_CONNECTION_TIME_OUT = 120
        self.SSH_SHELL_RECV_BUFFER_SIZE = 9999
        
    def sshConnect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #self.transport = self.ssh.get_transport()
        self.ssh.connect(self.SERVER_IP, username=self.SERVER_USERNAME, password=self.SERVER_PASSWORD,
                         port=self.SERVER_PORT, timeout=self.SSH_CONNECTION_TIME_OUT)
    
    def sshClose(self):
        self.ssh.close()
    
    def sshInvokeShell(self):
        self.channel = self.ssh.invoke_shell()    
    
    #this will flush the output buffer to make sure we are empty and waiting at the command prompt
    #do this before you send a shell command
    def sshFlushShell(self, endswith = '# '):
        self.sshSendShellCommand(cmd = '\n', endswith = endswith)
    
    def sshSendShellCommand(self, cmd = 'show clients\n', endswith = '# '):
        
        timer = time.time()
        self.channel.settimeout(self.SSH_CONNECTION_TIME_OUT)
        
        
        try:
            # Execute the given command

            self.channel.sendall(cmd)#'ls\n')
            #self.channel.send(cmd)#'ls\n')
            contents = io.BytesIO()#StringIO()
            error = io.BytesIO()#StringIO()
            
            #endswith takes a tuple which is what SSH_RESPONSE is sometimes if there is more than one possible expect
            while not contents.getvalue().endswith(endswith.encode(encoding='UTF-8')) \
                or self.channel.recv_ready() or self.channel.recv_stderr_ready():   
                
                if self.channel.recv_ready():
                    data = self.channel.recv(self.SSH_SHELL_RECV_BUFFER_SIZE)
                    while data:
                        contents.write(data)
                        data = None
                        if self.channel.recv_ready():
                            data = self.channel.recv(self.SSH_SHELL_RECV_BUFFER_SIZE)
                
                if self.channel.recv_stderr_ready():
                    error_buff = self.channel.recv_stderr(self.SSH_SHELL_RECV_BUFFER_SIZE)
                    while error_buff:
                        error.write(error_buff)
                        error_buff = None
                        if self.channel.recv_stderr_ready():
                            error_buff = self.channel.recv_stderr(self.SSH_SHELL_RECV_BUFFER_SIZE)
                
                #this could happen before recv_ready() is ready
                #if self.channel.exit_status_ready():
                #    break        
                
            exit_status = -1    #the ssh socket is still active
            if self.channel.exit_status_ready():
                exit_status = self.channel.recv_exit_status()
            
        
        except OSError as e: #socket.timeout:
            #should attempt to reconnect on socket error here because this usually means server timed us outs
            raise e #socket.timeout
        
        output = contents.getvalue()
        print(output)
        error_value = error.getvalue()
        
        timer = time.time() - timer
        
        print(timer)
        
        return output,error_value,exit_status,timer

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
    
    
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect('192.168.31.2', username='sbaruffi', password='foreignguy')
    
    #chan = ssh.invoke_shell()
    
     
#     sshClient.sshConnect()
#     
#     buff = ''
#     
#     while not buff.endswith('# '):
#         resp = chan.recv(9999)
#         buff += str.encode(resp)
#     
#     # Ssh and wait for the password prompt.
#     chan.send('show clients\n')
#     buff = ''
#     
#     while not buff.endswith('# '):
#         resp = chan.recv(9999)
#         buff += resp
#         print ('buff', buff)
    
    sshClient = SSHClient()
    sshClient.sshConnect()
    sshClient.sshInvokeShell()
    #send a dummy command to make sure we are at the command prompt after connecting
    sshClient.sshFlushShell()
    (output,error_value,exit_status,timer) = sshClient.sshSendShellCommand()
    sshClient.sshClose()
    
    total = []
    names = []
    ipss = []
    lines = output.decode(encoding='UTF-8')
    lines = lines.split('\r\n')
    
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

    #ssh.close()
   
  
        
   
   
    #exit()
    
    
#required line to declare main 
if __name__ == '__main__': main()    
    