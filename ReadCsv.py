import csv

#declare readcsv function and parameters required
def readcsv(csvname,user='admin',port='221'):
    
    #open the csv file
    with open(csvname) as csvfile:
        readcsv = csv.reader(csvfile,delimiter=',')
    
        #delcare all the variable as list
        hostnames = []
        sitenames = []
        macaddresses =[]
        passwords = []
        ips = []
        
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
    
    
    
    
    
    #exit the program
    exit()
    
    
#required line to declare main 
if __name__ == '__main__': main()    
    