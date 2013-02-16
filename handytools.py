#!/usr/bin/python
from fabric.api import *
from fabric.contrib.files import comment, uncomment, contains, exists, append, sed
from os import system;
import string
import csv
import paramiko
import socket

from string import whitespace
env.hosts = []
env.warn_onl=True

def main():
	
	'''Python parses the entire script and once it reaches 'if __name__ == '__main__':' section and the bottom it calls 
	this main function.'''

	loop = 1
	choice = 0

	

	while loop == 1:
	
		print hilite("=================================== ",3,0)
		print hilite("      Support - Handy Tools       ",3,1)
		print hilite("=================================== ",3,0)
		print hilite("=================================== ",3,0)
		print hilite("           HOST SELECTION           ",3,1)
		print hilite("=================================== ",3,0)
		print "1) Import list of hosts from file"
		print "2) Display set of currently selected hosts"
		print "3) Add Hosts Manually - Not Implemented"
		print "4) Clear set of currently selected hosts"
		print "\n"
		print hilite("=================================== ",1,0)
		print hilite("              TASKS                 ",1,1)
		print hilite("=================================== ",1,0)
		print "11) Get Host Type"
		print "12) Get Uptime"
		print "13) Check NFS Mounts"
		print "14) Add CONS Admin Group to /etc/sudoers"
		print "15) Add CONS Admin Group to /etc/security/access.conf"
		print "16) Create Data Volume at /data and use 100% of disk space - Not Implemented"
		print "17) Add iptables firewall rules - Not Implemented"
		print "\n"
		print hilite("=================================== ",2,0)
		print hilite("       Miscellaneous / System       ",2,1)
		print hilite("=================================== ",2,0)
		print "100) Clear Terminal"
		print "0) Quit Handytools"
		print ""

		try:
			choice = int(raw_input("Choose your option: "))
			if choice == 1:
				env.hosts = get_hosts()
			elif choice == 2:
				show_hosts()
			elif choice == 3:
				execute(add_hosts)
			elif choice == 4:
				env.hosts = ""
				env.host_string = ""
			elif choice == 11:
				env.host_string = None
				if action_confirm()==1:
					execute(host_type)
			elif choice == 12:
				env.host_string = None
				if action_confirm()==1:
					execute(get_uptime)
			elif choice == 13:
				env.host_string = None
				if action_confirm()==1:
					execute(compare_nfs)
			elif choice == 14:
				env.host_string = None
				if action_confirm()==1:
					execute(sudoers)
			elif choice == 15:
				env.host_string = None
				if action_confirm()==1:
					execute(accessconf)
			elif choice == 69:
				env.host_string = None
				if action_confirm()==1:
					password = str(raw_input("Enter the password:"))
					if password==("Password1"):
						global command
						command = str(raw_input("Enter some bash commands:"))
					execute(becareful)		
			elif choice == 0:
				loop = 0
			elif choice == 9:
				print env.hosts
			elif choice == 100:
				system('clear')
			elif choice :
				print hilite("Invalid Choice",2,0)
		except ValueError:
			print hilite("Bad Value. Try Again.",2,0)
	print "Bye."

def get_hosts():
	
	'''This function imports hosts from a file in csv format. It only imports names from the first column and checks for any 
	bad syntax'''
	
	fileLoc = raw_input("Enter the path to your CSV:")
	try:
		ifile  = open(fileLoc, "r")
		hostnames = csv.reader(ifile)
		i=0
		hostlist=[]
		for names in hostnames:
			hostlist.append(names[0])
			i+=1
		print hilite("File Found and Parsed Successfully",1,1)
		return hostlist	
		
	except IOError:
		print hilite("File doesn't exist. Check your path.",3,1)
		
def show_hosts():
	
	'''Display the current working set of hosts. Iterate's through env.hosts and print out.'''
	
	print hilite("=================================================================================================",4,1)
	print hilite("                               Hosts Currently Selected                                          ",3,0)
	print hilite("=================================================================================================",4,1)
	for i in env.hosts:
		print hilite("                               %s									  " % i,1,1)

def add_hosts():
	
	''' Not implemented yet. The plan is to be able to add hosts to the current working set of hosts via the menu.'''
	
	hostadd = raw_input("Input the name of the host you would like appended to the current working set.")
	env.hosts.append(hostadd)
	return env.hosts

def action_confirm():

	'''This function's purpose is to prompt the user for confirmation of action against the set of currently selected hosts.
	Every menu item should call this function first before calling a task type of function. The menu check's the return value of this function 
	and proceeds with the task if the return value is 1. Any other value will exit the menu 'if' statement and display the menu again.'''
	
	with hide('running', 'output'):
		print hilite("=================================================================================================",2,0)
		print hilite("You are about to execute tasks on the following hosts. Are you CERTAIN that you want to do this ?",3,0)
		print hilite("=================================================================================================",2,0)
		show_hosts()
		menuloop = 1
		choice = 0
		while menuloop == 1:
			try:
				print hilite("1 to continue, 2 to abort: ",3,0)
				choice = int(raw_input(": "))
				if choice == 1:
					return 1
					menuloop = 2
				if choice == 2:
					print "Aborting Job"
					return 2	
					menuloop = 2
				elif choice:
					print hilite("Bad value. Try again.",3,1)
			except ValueError:
				print hilite("Bad value. Try again.",3,1)
				
def host_type():
	
	'''Checks what type of host we are connecting to by running simple bash 'uname' command on host.'''
	
	if _is_host_up(env.host, int(env.port)) is True:
		with hide('running'):
			run('uname -s')
	else:
		print hilite("Connection to %s is not available. Continuing to next host." % env.host, 3,0)

def becareful():
	
	
		
			if _is_host_up(env.host, int(env.port)) is True:
					'''with hide('running'):'''
					'''run('%s' % command)'''
					sudo ('%s' % command)
			else:
				print hilite("Connection to %s is not available. Continuing to next host." % env.host, 3,0)				
			
def hilite(string, status, bold):
	
	"""This function is used to change the color of ascii text. It takes 3 arguments, 'string', 'status', 'bold'. 
	It returns your input string in the color and boldnes you specify with the 'status' and 'bold' arguments. Taken from stackoverflow.com"""
	
	attr = []
	if status == 1:
		# green
		attr.append('32')
	elif status == 2:
		# yellow 
		attr.append('33')
	elif status == 3:
	# red
		attr.append('31')
	elif status == 4:
	# information
		attr.append('34')
	if bold:
		attr.append('1')
	return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

def sudoers():
	
	'''Add the 'CONS' user groups to sudoers file. Get's project acronym from hostname using bash 'cut' command.'''
	
	acronym = run('echo $HOSTNAME | cut -c 3-5')
	domacronym = str(r'%ACME')
	sudo (r'sed -i "/## Allow root to run any commands anywhere/a %s\\\\\\\%s_cons_admins ALL=(ALL)    ALL" /etc/sudoers' % (domacronym,acronym),shell=False)

def accessconf():
	
	'''Add the 'CONS' user groups to the access.conf file. Get's project acronym from hostname using bash 'cut' command.'''
	
	acronym = run('echo $HOSTNAME | cut -c 3-5')
	sudo (r'sed -i "/linux_users/a + : ACME\\\\%s_cons_admins : ALL" /etc/security/access.conf' % acronym,shell=False)
	sudo (r'sed -i "/linux_users/a + : ACME\\\\%s_cons_app_admins : ALL" /etc/security/access.conf' % acronym,shell=False)
	sudo (r'sed -i "/linux_users/a + : ACME\\\\%s_cons_users : ALL" /etc/security/access.conf' % acronym,shell=False)
	
def get_uptime():
	
	'''This function gets the uptime of the host and then returns that value with a particular color depending on the duration of that uptime value.'''
	
	with hide('running', 'output'): #  Hide console output
		oktime = 15
		warntime = 60
		errortime = 1
		uptime = run ('cat /proc/uptime')
		splituptime = uptime.split(" ")
		minutes = float(splituptime[0]) / 60
		hours = minutes / 60
		if minutes < oktime:
			print hilite("has recently rebooted and has been up for %f minutes" %(minutes),3,0)
		elif minutes < warntime:
			print hilite("has rebooted within the last hour and has been up for %f minutes" %(minutes),2,0)
		elif hours > errortime:
			print hilite("HASN'T rebooted recently and has been up for %f hours" %(hours),1,0)
		else:
			print "Good bye"

def check_fstab():
	
	'''This is the first of three functions used to check a server for all NFS mounts being in a mounted state. This function is called by the function 
	'compare_nfs'. It returns a value based on the number of NFS filesystems configured in the /etc/fstab.'''
	
	with hide('running', 'output'):
		nfscounter = int(0)
		counter = int(0)
		fstabfile = run('cat /etc/fstab')
		lines = fstabfile.split("\n")
		for a in lines:
			columns = lines[counter].split()
			#print "Found %d columns in fstab line %d" % (len(columns),counter)
			if len(columns)<2:
				#print "Found bad line"
				counter+=1
				continue
			elif columns[0].count("#")>0:
				#print "found a commented line"
				counter+=1
				continue
			if columns[2]=="nfs4":
				#print "Found a NFS filesystem"
				nfscounter+=1
			counter+=1
		howManyFstabNfs = "INFO: Found %d NFS file system entries in /etc/fstab" %(nfscounter)
	print hilite(howManyFstabNfs,4,1)
	return nfscounter

def check_mounts():
	
	'''This is the second of three functions used to check a server for all NFS mounts being in a mounted state. This function is called by the function 
	'compare_nfs'. It returns a value based on the number of NFS filesystems actually mounted on the system by running the bash 'mount'
	command and checking the output.'''
	
	with hide('running', 'output'):
		NFSmounts = int(0)
		mountCounter = int(0)
		mountFile = run('/bin/mount')
		mountLines = mountFile.split("\n")
		for a in mountLines:
			mountCol = mountLines[mountCounter].split()
			if len(mountCol)<=3:
				mountCounter+=1
				continue
			elif mountCol[4]=="nfs4":
				NFSmounts+=1
			mountCounter+=1
	howManyNfsMounted = "INFO: Found %d NFS file system currently mounted" %(NFSmounts)
	print hilite(howManyNfsMounted,4,1)
	return NFSmounts

def compare_nfs():
	
	'''This is the third of three functions used to check a server for all NFS mounts being in a mounted state. This function calls 'check_fstab'
	then calls 'check_mounts' and compares their returned values. If the values are the same then we can assume that all NFS exports are mounted.
	If the values differ, then we can assume there is a problem with the NFS mounts.
	'''
	
	a = check_fstab()
	b = check_mounts()
	if a==b:
		printmountsok = "Mounts look ok"
		print hilite(printmountsok,1,1)
	elif a!=b:
		printmountsbad = "Looks like there is a problem with NFS mounts"
		print hilite(printmountsbad,3,1)

def _is_host_up(host, port):
	
	'''This function performs a quick check on the host to see if it is available before continuing with running remote ssh commands. If the
	host is unavailable fabric api will skip the host and move onto the next host in the list. If this function isn't used fabric api's default 
	behaviour is to exit the program if there is a connection error. Obviously this isn't great if you are running a job against 100's of hosts
	and fabric quits half way through because it couldn't connect to one single host.
	'''
	
	# Set the timeout
	original_timeout = socket.getdefaulttimeout()
	new_timeout = 3
	socket.setdefaulttimeout(new_timeout)
	host_status = False
	try:
		paramiko.Transport((host, port))
		host_status = True
	except:
		print('***Warning*** Host {host} on port {port} is down.'.format(
    		host=host, port=port)
		)
	socket.setdefaulttimeout(original_timeout)
	return host_status

if __name__ == '__main__':
	main()
