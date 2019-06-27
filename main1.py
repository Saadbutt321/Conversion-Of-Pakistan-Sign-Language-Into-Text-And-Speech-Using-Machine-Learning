# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 22:38:14 2018
"""

import os
import subprocess
import ann_match

from pygame import mixer # for sound

from tkinter import Tk
from tkinter import Label

import errno, stat, shutil
import sys, signal

def signal_handler(signal, frame):
    shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)
    p.kill()
    root.destroy()
    print( 'All done')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise Exception

shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)

"""
Tkinter window
"""
root = Tk()
root.geometry("300x300+1600+100") #Width x Height
l = Label(root, text= "‬")
l.config(font=("Courier", 100))
l.pack()
root.update()


print('Starting OpenPose')
os.chdir('openpose')
p = subprocess.Popen('build\\x64\\Release\\OpenPoseDemo.exe --hand  --write_json ..\\Keypoints --net_resolution 128x128  --number_people_max 1', shell=True)
os.chdir('..')

dirName = 'Keypoints'
fileName = '000000000000_keypoints.json'
 
try:
    # Create target Directory
    os.mkdir(dirName)
    shutil.copy(fileName, dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

lastLabel = ''
while True:
    try:
        fileNames = []
        for entry in os.scandir('Keypoints'):
            if entry.is_file():
                if os.path.splitext(entry)[1] == ".json":
                    fileNames.append(entry.name)
                    fileName = entry.name
                    
        try:
            label = ann_match.match_ann('Keypoints\\'+fileName) 
        except:
            pass
        
        if label != 'no match' and label != 'no confidence' and label != lastLabel:
            lastLabel = label  
            
            l[ "text" ]=label
            root.update()
            
            print("matched Reference =  (" + label + ")" )
            
            mp3 = "speech\\"+label+".mp3"
            mixer.init()
            mixer.music.load(mp3)
            mixer.music.play()
            

    except UnboundLocalError:
        print("UnboundLocalError")
    
 
root.mainloop()







    
    
    
    
    
    
    
    
    
    
    
    
    
