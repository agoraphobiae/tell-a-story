from __future__ import print_function
MAX_LINES = 10000
LINES_AT_ONCE = 5
# lol stackoverflow lol
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def PressAndReleaseKey(hexKeyCode):
	extra = ctypes.c_ulong(0)
	ii_ = Input_I()
	ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
	x = Input( ctypes.c_ulong(1), ii_ )
	SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
	ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
	x = Input( ctypes.c_ulong(1), ii_ )
	SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def AltTab():
    '''
    Press Alt+Tab and hold Alt key for 2 seconds in order to see the overlay
    '''

    PressKey(0x012) #Alt
    PressKey(0x09) #Tab
    ReleaseKey(0x09) #~Tab

    time.sleep(2)
    ReleaseKey(0x012) #~Alt

def main():
	print("Prepare your body.")
	[print(9-i, end="\r") or time.sleep(1) for i in xrange(9)]
	i = MAX_LINES

	with open("shakespeare.txt", 'r') as text:
		for line in text:
			if i < 0: return
			i -= 1
			for c in line:
				if c not in ". abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
					continue
				if c == " ":
					PressAndReleaseKey(0x20) # spacebar
					# for some reason, spacebar makes 2 spaces, so delete one
					PressAndReleaseKey(0x08)
				elif c == ".":
					PressKey(0x6E)

				if c.upper() == c:
					PressKey(0xA0)
					PressAndReleaseKey(ord(c))
					ReleaseKey(0xA0)
				else:
					PressAndReleaseKey(ord(c.upper()))
			PressKey(0x0D) # enter

			if i % LINES_AT_ONCE == 0:
				# don't overload kbd input
				time.sleep(1)
	print(":)")

if __name__ =="__main__":
    main()
