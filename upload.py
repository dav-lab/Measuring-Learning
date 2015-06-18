import os
import paramiko
import time

def detect_change(dirName):
    current=os.getcwd()
    if os.path.isdir(dirName):
        times={}
        beforeFiles=os.listdir(dirName)
        for i in beforeFiles:
            #all files are uploaded first
            upload(current+'/'+dirName+'/'+i,i)
            info=os.stat(dirName+'/'+i)
            times[i]=info.st_mtime
        while 1:
            afterFiles=os.listdir(dirName)
            added=[f for f in afterFiles if f not in beforeFiles]
            #upload added files
            for j in added:
                upload(current+'/'+dirName+'/'+j,j)
                times[j]=os.stat(dirName+'/'+j).st_mtime
            #upload modified files
            for key in times:
                 if os.stat(dirName+'/'+key).st_mtime>times[key]:
                     upload(current+'/'+dirName+'/'+key,key)
                     times[key]=os.stat(dirName+'/'+key).st_mtime
            time.sleep(5)

def upload(localFile,newName):
    host=''
    port=22
    transport=paramiko.Transport((host,port))
    password=''
    username=''
    transport.connect(username=username,password=password)
    sftp=paramiko.SFTPClient.from_transport(transport)
    filepath='/...../'+newName
    sftp.put(localFile,filepath)
    sftp.close()
    transport.close()

#detect_change('test')