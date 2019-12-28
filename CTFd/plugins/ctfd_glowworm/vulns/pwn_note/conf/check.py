from pwn import *
from sys import *
import time

host = argv[1]
port = int(argv[2])
timeout = 30

context.log_level = 'critical'

def add(p, size, content):
	try:
		p.recvuntil('choice> ', timeout = 1)
		p.sendline('1')
		p.recvuntil('length> ', timeout = 1)
		p.sendline(str(size))
		p.recvuntil('content> ', timeout = 1)
		p.sendline(content)
		return p.recvline(timeout = 1)
	except Exception as e:
		raise Exception, "add error, "+str(e)

def show(p, idx):
	try:	
		p.recvuntil('choice> ', timeout = 1)
		p.sendline('2')
		p.recvuntil('index> ', timeout = 1)
		p.sendline(str(idx))
		return p.recvline(timeout = 1)
	except Exception as e:
		raise Exception, "add error, "+str(e)

def remove(p, idx):
	try:
		p.recvuntil('choice> ', timeout = 1)
		p.sendline('3')
		p.recvuntil('index> ', timeout = 1)
		p.sendline(str(idx))
		return p.recvline(timeout = 1)
	except Exception as e:
		raise Exception, "add error, "+str(e)

def getIO():
    return remote(host, port, timeout=timeout)

#normal I/O check
def check1():
	try:
		p = getIO()

		info = add(p, 0x108, 'aaaa')
		if info != 'done[010]\n':
			raise Exception, "returnInfo1 no same"
		info = add(p, 0x100, 'bbbb')
		if info != 'done[120]\n':
			raise Exception, "returnInfo2 no same"
		info = show(p, 0)
		if info != 'aaaa\n':
			raise Exception, "returnInfo3 no same"
		info = show(p, 1)
		if info != 'bbbb\n':
			raise Exception, "returnInfo4 no same"
		info = remove(p, 1)
		if info != 'done\n':
			raise Exception, "returnInfo5 no same"
		info = add(p, 0x20, 'cccc')
		if info != 'done[120]\n':
			raise Exception, "returnInfo6 no same"
		p.close()
	except Exception as e:
		p.clise()
		raise Exception, "check1 error, "+str(e)
	return True

#check the allocation size
def check2():
	try:
		p = getIO()

		info = add(p, 0x10, 'a'*0x10)
		if info != "done[010]\n":
			raise Exception, "returnInfo7 no same"
		info = add(p, 0x200, 'a'*0x200)
		if info != "done[030]\n":
			raise Exception, "returnInfo8 no same"
		info = show(p, 0)
		if info != ('a'*0x10 + '\n'):
			raise Exception, "returnInfo9 no same"
		info = show(p, 1)
		if info != ('a'*0x200 + '\n'):
			raise Exception, "returnInfo10 no same"
		p.close()
	except Exception as e:
		p.close()
		raise Exception, "check2 error, "+str(e)
	return True
	
		
def check3():
	try:
		p = getIO()

		info = add(p, 0x100, p64(0x7f1186557ba0))
		if info != "done[010]\n":
			raise Exception, "may use a all-defend script"
		info = show(p, 0)
		if info != '\xa0\x7b\x55\x86\x11\x7f\n':
			raise Exception, "may use a all-defend script"
		info = add(p, 0x100, p64(0x556ac6b4d010))
		if info != "done[120]\n":
			raise Exception, "may use a all-defend script"
		info = show(p, 1)
		if info != '\x10\xd0\xb4\xc6\x6a\x55\n':
			raise Exception, "may use a all-defend script"
		info = add(p, 0x100, 'cat')
		if info != "done[230]\n":
			raise Exception, "may use a all-defend script"
		info = show(p, 2)
		if info != 'cat\n':
			raise Exception, "may use a all-defend script"
		info = add(p, 0x100, 'ls')
		if info != "done[340]\n":
			raise Exception, "may use a all-defend script"
		info = show(p, 3)
		if info != "ls\n":
			raise Exception, "may use a all-defend script"
		p.close()
	except Exception as e:
		p.close()
		raise Exception, "check3 error, "+str(e)
	return True


def checker():
	try:
		# add your check function name
		if check1() and check2() and check3():
			pass
		else:
			print "team" + str(port)[1:3]
	except Exception as e:
		print "team" + str(port)[1:3]

if __name__ == '__main__':
    checker()

