# coding=utf-8

# This is a script for automating content release activities


import os
import sys
import subprocess
import fileinput


print "Argument List:", str(sys.argv)
# Starting of actual sript
print "OS home directory " , os.getenv("HOME")
os.chdir(os.getenv("HOME"))
print "Current Working Directory " , os.getcwd()

releaseBranchName = sys.argv[2];
print "Branch name - ", releaseBranchName

print "Path to change to - ", sys.argv[1]
if os.path.exists(sys.argv[1]) :
    # Change the current working Directory    
    os.chdir(sys.argv[1])
else:
    print "Can't switch to given path"
    
print "Changed to path " , os.getcwd()


versions = ['version', 'version =']

file = fileinput.input(files="build.txt", inplace=1)
for line in file:
    if 'version' in line:
        line = 'version = ' + releaseBranchName
        print line,
file.close()
            
# for line in fileinput.input('build.txt', inplace=True):
#   if word in line for word in versions
#       print line.replace('version', 'version = ' + releaseBranchName)

# subprocess.call("cd sys.argv[1]", cwd=os.getcwd(), shell=True)
subprocess.call(["git", "add --all"])
subprocess.call(["git", "commit"])
subprocess.call(["git", "branch", releaseBranchName])
subprocess.call(["git", "checkout", releaseBranchName])
# os.system('cd /AndroidProjects')
