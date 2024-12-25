import pyperclip as CLIP
import keyboard
from tkinter import *
from tkinter import ttk
import tempfile as tf
import json
import os.path

ColmSum = 6 # 列数
DataSavePath = tf.gettempdir()+r'\savedata.json'

def createGUI():
    global strVars
    global root
    global CheckColm

    root = Tk()
    root.title('剪贴板助手')
    topFrame = ttk.Frame(root, padding=10)
    topFrame.pack(side='top')

    strVars = [createVars(root) for i in range(ColmSum)]
    [createChildrenFrame(topFrame,strVars[i],index=i) for i in range(ColmSum)]

    bottomFrame = ttk.Frame(root, padding=10)
    bottomFrame.pack(side='bottom')

    CheckColm =  IntVar(value=0) # 当前选中的列号
    # Label(bottomFrame,text='当前选择的配置:',padx=17).pack(side='left')
    [Radiobutton(bottomFrame, text=' 配置 '+str(i)+'  ',value=i,variable=CheckColm,height=2,width=25,relief="raised").pack(side='left') for i in range(ColmSum)]
    
    bottomFrame2 = ttk.Frame(root, padding=10)
    bottomFrame2.pack(side='top')

    Button(bottomFrame2,text='保存配置',command=saveText2File).pack(side='left')
    Button(bottomFrame2,text='加载配置',command=lambda:loadTextFromFile(root)).pack(side='left')

def createChildrenFrame(parentFrame = None,_strVars = None,index = 0):
    if _strVars == None:
        _strVars = createVars()
    frm = ttk.Frame(parentFrame, padding=10)
    frm.pack(side='left')

    Label(frm,text='配置 '+str(index)).pack(side='top')

    frame1 = ttk.Frame(frm)
    frame1.pack(side='top')
    field1 = Entry(frame1,justify='left',textvariable=_strVars[0])
    field1.pack(side='left')
    Label(frame1,text='Alt+1').pack(side='right')

    frame2 = ttk.Frame(frm)
    frame2.pack(side='top')
    field2 = ttk.Entry(frame2,justify='left',textvariable=_strVars[1])
    field2.pack(side='left')
    Label(frame2,text='Alt+2').pack(side='right')

    frame3 = ttk.Frame(frm)
    frame3.pack(side='top')
    field3 = ttk.Entry(frame3,justify='left',textvariable=_strVars[2])
    field3.pack(side='left')
    Label(frame3,text='Alt+3').pack(side='right')

    frame4 = ttk.Frame(frm)
    frame4.pack(side='top')
    field4 = ttk.Entry(frame4,justify='left',textvariable=_strVars[3])
    field4.pack(side='left')
    Label(frame4,text='Alt+4').pack(side='right')

    frame5 = ttk.Frame(frm)
    frame5.pack(side='top')
    field5 = ttk.Entry(frame5,justify='left',textvariable=_strVars[4])
    field5.pack(side='left')
    Label(frame5,text='Alt+5').pack(side='right')

def loadTextFromFile():
    if not os.path.exists(DataSavePath):
        return
    global strVars
    _list = []
    try:
        with open(DataSavePath,'r+',encoding='utf8') as file:
            _list = json.load(file)
            for i,l in enumerate(_list):
                for j,s in enumerate(l):
                    strVars[i][j].set(s)
    except:
        print('read file err or json format err')

def saveText2File():
    global strVars
    temp_dir = tf.gettempdir()
    temp_list = [[s.get() for s in l ]for l in strVars]
    try:
        with open(DataSavePath,'w',encoding='utf8') as file:
            json.dump(temp_list,file)
    except:
        print('save json 2 file err')

def createVars(_master=None):
    t = []
    for i in range(5):
        t.append(StringVar(master=_master,value=''))
    return t

def _paste(numb):
    global strVars
    # CLIP.copy(strVars[CheckColm.get()][numb-1].get())
    # keyboard.send('ctrl+v')
    keyboard.write(strVars[CheckColm.get()][numb-1].get())

def setHotkey():
    keyboard.add_hotkey('ctrl+1',_paste,args=[1],suppress=True,trigger_on_release=True)
    keyboard.add_hotkey('ctrl+2',_paste,args=[2],suppress=True,trigger_on_release=True)
    keyboard.add_hotkey('ctrl+3',_paste,args=[3],suppress=True,trigger_on_release=True)
    keyboard.add_hotkey('ctrl+4',_paste,args=[4],suppress=True,trigger_on_release=True)
    keyboard.add_hotkey('ctrl+5',_paste,args=[5],suppress=True,trigger_on_release=True)

def main():
    createGUI()
    setHotkey()
    loadTextFromFile()
    root.mainloop()

if __name__ == "__main__":
    main()