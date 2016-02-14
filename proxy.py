import _winreg as wreg
import os

def set_proxy(proxy):
	
	destination = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	wreg.SetValueEx(key, 'ProxyServer' ,0, wreg.REG_SZ, proxy)
	key.Close()



def current_proxy():
	destination = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	pro =  wreg.QueryValueEx(key, 'ProxyServer')
	return pro[0]


def create_folder():
	destination = r"SOFTWARE"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	wreg.SetValue(key, 'Proxy_Servers' , wreg.REG_SZ, 'none')

def initialise_count():
	destination =r"SOFTWARE\Proxy_Servers"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	try:
		count = wreg.QueryValueEx(key, 'count')
	except :
		wreg.SetValueEx(key, 'count' ,0, wreg.REG_SZ, "0")

def change_count(n):
	
	destination =r"SOFTWARE\Proxy_Servers"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	count = wreg.QueryValueEx(key, 'count')
	wreg.SetValueEx(key, 'count' ,0, wreg.REG_SZ, str(int(count[0]) + n ) ) 


def add_proxy(proxy):

	destination =r"SOFTWARE\Proxy_Servers"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	try :
		wreg.QueryValueEx(key, proxy)
	except:
		wreg.SetValueEx(key, proxy , 0 , wreg.REG_SZ , proxy)
		change_count(1)


def delete_proxy(proxy):
	
	destination =r"SOFTWARE\Proxy_Servers"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	try: 
		wreg.DeleteValue(key , proxy)
		change_count(-1)
	except:
		pass


def print_all():
	destination =r"SOFTWARE\Proxy_Servers"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	print "\n#######################################"
	
	print "##   Saved Proxies"
	try: 
		i = 0
		count=1
		while True:
			x = wreg.EnumValue(key, i)
			i+=1
			if x[0]=='':
				continue
			if x[0]=='count':
				continue
			print "##    " , count , " =>  " ,x[0] 
			count+=1
	except:
		pass
	print "#######################################\n"
	

def delete_this(n):
	if(n==0):
		return

	destination =r"SOFTWARE\Proxy_Servers"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	try: 
		x = wreg.EnumValue(key, n+1)
		if x[0]=='count':
			pass
		else:
			delete_proxy(x[0])
		print "Deleted !"
	except:
		print "Not Found"

def set_this(n):
	destination =r"SOFTWARE\Proxy_Servers"
	key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, destination,0,wreg.KEY_ALL_ACCESS)
	try: 
		x = wreg.EnumValue(key, n+1)
		if x[0]=='count':
			pass
		else:
			set_proxy(x[0])
		print "\nProxy " , x[0] , "   Set !"
	except:
		print "Not Found"






if __name__ == "__main__":
	create_folder()
	initialise_count()
	create_folder()
	print_all()


	while True:
		print "\n######################################"
		print "##                                   ##"
		print "    Current Proxy => " , current_proxy()
		print "##                                   ##"
		print "##         Commands                  ##"
		print "##   1 : to set proxy                ##"
		print "##   2 : to add another proxy        ##"
		print "##   3 : to delete proxy             ##"
		print "##   0 : to exit                     ##"
		print "#######################################\n"
		inp = raw_input("Enter a Number ===>")
		if inp=="1":
			print_all()
			i = raw_input("Enter a Number to set proxy ===> ")
			set_this(int(i))
			os.system('control inetcpl.cpl,,4')


		if inp=="2":
			print "Enter proxyin this format Proxy:Port and 0 to exit"
			proxy = raw_input("  Enter Proxy  ===> ")
			add_proxy(proxy)
			print_all()
			
		if inp=="3":
			print_all()
			i = raw_input("Enter a Number to delete proxy and 0 to return   ===> ")
			delete_this(int(i))
			print_all()
		if inp=="0":
			break
		