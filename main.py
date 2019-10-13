from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from PIL import Image, ImageGrab, ImageDraw
from collections import defaultdict
from sklearn.cluster import KMeans
import numpy, cv2, time,os, win32gui
from collections import Counter
from pynput.keyboard import Key, Controller

def detCol(img):
    return_List = []
    lower_green = numpy.array([0,200,0])
    upper_green = numpy.array([102,255,102])
    if numpy.any(cv2.inRange(img,lower_green,upper_green)):
        return_List.append('a')
    lower_red = numpy.array([204,0,0])
    upper_red = numpy.array([255,102,102])
    if numpy.any(cv2.inRange(img,lower_red,upper_red)):
        return_List.append('s')
    lower_yellow = numpy.array([200,200,0])
    upper_yellow = numpy.array([255,255,102])
    if numpy.any(cv2.inRange(img,lower_yellow,upper_yellow)):
        return_List.append('j')
    lower_blue = numpy.array([0,0,170])
    upper_blue = numpy.array([102,102,255])
    if numpy.any(cv2.inRange(img,lower_blue,upper_blue)):
        return_List.append('k')
    lower_orange = numpy.array([170,102,0])
    upper_orange = numpy.array([255,128,0])
    if numpy.any(cv2.inRange(img,lower_orange,upper_orange)):
        return_List.append('l')
    return return_List

def screenGrab():
    box = (668,887,1268,950)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
'.png','PNG')
    return 'full_snap__' + str(int(time.time()))+'.png'

def deleteFile(name):
    os.remove(name)

def isNote():
    name= screenGrab()
    result = readImgSame(name)
    deleteFile(name)
    return result

def readImgSame(img):
    master_file = cv2.imread("master.png")
    compare_file = cv2.imread(img)
    difference = cv2.subtract(master_file,compare_file)
    r,g,b = cv2.split(difference)
    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        return True
    else:
        img = cv2.cvtColor(compare_file,cv2.COLOR_BGR2RGB)
        guitar_strum(detCol(img))    
    return True    

def bringWinFront(application):
    app_dialog = application.top_window()
    app_dialog.minimize()
    app_dialog.restore()
    return True
## MAIN GAME FUNCS
keyboard = Controller()
def guitar_strum(letter_list):
    releaseAll(keyboard)
    for i in letter_list:
        keyboard.press(i)
    send_keys("{UP}")

def releaseAll(keyboard):
    keyboard.release('a')
    keyboard.release('s')
    keyboard.release('j')
    keyboard.release('k')
    keyboard.release('l')
    
app = Application().connect(process=19760)
keyboard = Controller()
bringWinFront(app)
time.sleep(1)
while True:
    try:
        isNote()
    except KeyboardInterrupt:
        raise
    except Exception as msg:
        print(msg)
        pass
        

