# coding=utf-8
# This is a script for automating content release activities
# Refer confluence https://confluence-euc.eng.vmware.com/display/EQE/Release+Process+Automation for more details

# Install python 3.4 for enum support as 
# pip install enum34
# Refer https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python


import os
import sys
import subprocess
import fileinput
from subprocess import call
from enum import Enum
import subprocess
import fnmatch, re
import urllib2


class ACTION(Enum):
	NEW_RELEASE_BRANCH = 1
	BETA_ARTIFACT = 2
	GA_ARTIFACT = 3
	BETA_OSL = 4
	GA_OSL = 5

class PROJECT(Enum):
	CONTENT_APP = 1
	CONTENT_SDK = 2
	CONTENT_UI_FW = 3
	CONTEN_VIEWER = 4
	WS1_SEND = 5
	GREETINGS = 6

class ERRORS(Enum):
	INVALID_PARAMETERS = -120
	RELEASE_BRANCH_DOES_NOT_EXIST = -121

def createNewReleaseBranch() :
	print "Create new release branch release1/",releaseVersion

def createBetaArtifact() :
	print "Create Beta artifact for release1/",releaseVersion

def createGAArtifact() :
	print "Create GA artifact for release1/",releaseVersion

def updateOSL() :
	print "Update GA OSL for release1/",releaseVersion
	#Check if release branch exists
	try:
		releaseBranch = releaseBranchPrefix + releaseVersion
		call(['git', 'branch'])
		call(['git', 'checkout', 'development'])
		call(['git', 'pull'])
		#call(['git', 'checkout', '-b', releaseBranch, "origin/" + releaseBranch])
		call(['git', 'checkout', '-b', 'release/3.19.0', "origin/release/3.19.0"])
		call(['git', 'rev-parse', '--verify',  releaseBranch])
		print "Release branch exists proceed with new branch to make changes"
		for root, dirnames, filenames in os.walk('.'):
			for filename in fnmatch.filter(filenames, '*open_source_license*.txt'):
				print "Found file -------- ", os.path.join(root, filename)
				updateOSLInFile(root, filename)
	except:
		print """
		========================================================
			ERROR : Release branch does not exists
		========================================================
		"""
		sys.exit(ERRORS.RELEASE_BRANCH_DOES_NOT_EXIST)

def updateOSLInFile(parent, filename) :
	print "Update OSL for ", releaseBranchPrefix , releaseVersion
	versionSections = releaseVersion.split('.')
	versionForOSL = versionSections[0] + "." + versionSections[1]
	oslLink = ""
	if (ACTION(actionType) == ACTION.BETA_OSL and PROJECT(project) == PROJECT.CONTENT_APP) :
		oslLink = oslUrlLinkPrefix + gaOSLLinks[projectIndex] + "3.19" + oslFileBetaSuffix + oslUrlLinkSuffix
	elif (ACTION(actionType) == ACTION.GA_OSL and PROJECT(project) == PROJECT.CONTENT_APP) :
		oslLink = oslUrlLinkPrefix + gaOSLLinks[projectIndex] + "3.19" + oslFileGASuffix + oslUrlLinkSuffix
	else :
		print "Invalid action"

	if (len(oslLink) > 0 ) :
		print "Download OSL file URL : " + oslLink
		#for pythons 3 wget.download(oslLink, os.path.join(parent, filename))
		filedata = urllib2.urlopen(oslLink)
		datatowrite = filedata.read()
		with open(os.path.join(parent, filename), 'w') as f:
			f.write(datatowrite)

def performAction(actionType) :
	# Referred link https://data-flair.training/blogs/python-switch-case/
	switcher={
		ACTION.NEW_RELEASE_BRANCH : createNewReleaseBranch,
		ACTION.BETA_ARTIFACT : createBetaArtifact,
		ACTION.GA_ARTIFACT : createGAArtifact,
		ACTION.BETA_OSL : updateOSL,
		ACTION.GA_OSL : updateOSL,
	}
	func=switcher.get(actionType, lambda : "Invalid action")
	return func()

def printHelp() :
	print """
	======================================================================================================
	|	Usage: """ , sys.argv[0] , """ <Project> <Action Type> <Release version>                    
	|	example: to create new release branch 3.18.0 and artifact of content locker use below command		
	|	******  """ , sys.argv[0] , """ 1 1 3.18.0   *******                                                        
	|	Below actions are possible                                                                  
	|	1. Create new release versions                                                              
	|	2. Create BETA release artifact                                                             
	|	3. Create GA release artifact																
	|	4. Update BETA OSL																			
	|	5. Update GA OSL																			
	|																								
	|	Valid projects are Below 																	
	|	1. Content App																				
	|	2. Content SDK																				
	|	3. Content UI Framework																		
	|	4. Content Viewer																			
	|	5. WS1 Send																					
	======================================================================================================\n"""


###############################################################
#	Main Script starts here
###############################################################

gitStashLinkPrefix = "ssh://git@stash.air-watch.com:7999/ascl/"
gitStashLinkSuffix = ".git"
# Locations need to match the index from enum PROJECT
projectLocations = ["android-scl", "contentsdk", "content-ui-framework", "contentviewer", "vmware-send---android", "csdkconsumer"]

oslUrlLinkPrefix = "https://www.air-watch.com/downloads/"
oslUrlLinkSuffix = ".txt"
oslFileGASuffix  = "_GA"
oslFileBetaSuffix  = "_Beta"
# OSL urls need to match the index from enum PROJECT
# Complete OSL link would be
gaOSLLinks = ["open_source_license_VMware_Workspace_ONE_Content_for_Android_",
				"", "", "", "", ""]
releaseBranchPrefix = "release/"

if (len(sys.argv) < 4) :
	printHelp()
	sys.exit(ERRORS.INVALID_PARAMETERS)

project = int(sys.argv[1])
projectIndex = project - 1
actionType = int(sys.argv[2])
releaseVersion = sys.argv[3]

#if (ACTION(actionType) is None) :
#	print "Error: Invalid action type\n"
#	printHelp()
#	sys.exit(0)

print "Project - ", project
print "Action type - ", actionType
print "Release Version - ", releaseVersion , "\n"
print "Current working directory - " , os.getcwd()

# Check if project directory already exists if not clone it
if not os.path.exists(projectLocations[projectIndex]) and os.path.isdir(projectLocations[projectIndex]) :
	projectGitRepoPath = gitStashLinkPrefix + projectLocations[projectIndex] + gitStashLinkSuffix
	subprocess.check_output(['git', 'clone', projectGitRepoPath])
	print "Project repo path" , projectGitRepoPath

print "Cloning repository step completed"
call(['cd', projectLocations[projectIndex]])
os.chdir(projectLocations[projectIndex])
print "Project working directory - " , os.getcwd()
performAction(ACTION(actionType))


#print "Argument List:", str(sys.argv)
#print "OS home directory " , os.getenv("HOME")
#os.chdir(os.getenv("HOME"))
#print "Current Working Directory " , os.getcwd()


#versions = ['version', 'version =']
#file = fileinput.input(files=fileName, inplace=1)
#for line in file:
#    if 'version' in line:
#        line = 'version = ' + releaseBranchName
#        print line,
#file.close()

#call('git add .', shell = True)
#call('git commit -m "Updating release branch version"', shell = True)
#call('push --set-upstream origin', shell = True) # This is not working, we need to fix this
#call('git push origin', shell = True)
