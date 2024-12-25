import pyperclip as CLIP
import keyboard
from tkinter import *
from tkinter import ttk
import tempfile as tf
import json
import os.path

ColmSum = 6 # 列数
RowsSum = 5 # 行数
KeyboardWrite = False # 是否键盘输入，默认CV
DataSavePath = tf.gettempdir()+r'\savedata.json'
KeyName = 'Alt' # 快捷键+数字

def createGUI():
    """创建UI
    """
    global strVars
    global root
    global CheckColm
    global KeyboardWrite

    CheckColm =  IntVar(value=0) # 当前选中的列号
    KeyboardWrite = BooleanVar(value=KeyboardWrite)

    # 内容编辑栏
    topFrame = ttk.Frame(root, padding=10)
    topFrame.pack(side='top')
    strVars = createVars(root)
    childrenFrameList = [createChildrenFrame(topFrame,strVars[i],index=i) for i in range(ColmSum)]

    # 复制模式切换栏
    bottomFrame1 = ttk.Frame(root, padding=10)
    bottomFrame1.pack(side='top')
    Radiobutton(bottomFrame1, text='模拟键盘输入',selectcolor='#f28c2c',value=True,variable=KeyboardWrite,indicatoron=False,width=10,pady=5).pack(side='left')
    Radiobutton(bottomFrame1, text='模拟Ctrl+V',selectcolor='#f28c2c',value=False,variable=KeyboardWrite,indicatoron=False,width=10,pady=5).pack(side='left')
    
    # 配置保存加载栏
    bottomFrame2 = ttk.Frame(root, padding=10)
    bottomFrame2.pack(side='top')
    Button(bottomFrame2,text='保存配置',command=saveText2File,relief='raised').pack(side='left')
    Button(bottomFrame2,text='加载配置',command=lambda:loadTextFromFile(),relief='raised').pack(side='left')

def createChildrenFrame(parentFrame = None,_strVars = None,index = 0):
    """创建配置列

    Args:
        parentFrame (_type_, optional):  Defaults to None.
        _strVars (_type_, optional): _description_. Defaults to None.
        index (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    global CheckColm

    if _strVars == None:
        _strVars = createColmVars()
    
    frm = ttk.Frame(parentFrame, padding=10)
    frm.pack(side='left')
    # 底部单选按钮
    Radiobutton(frm, text=f'配置 {index}',selectcolor='#f28c2c',value=index,variable=CheckColm,indicatoron=False,width=15,pady=5,).pack(side='bottom')
    # 创建RowsSum行输入框
    for i in range(RowsSum):
        frame = ttk.Frame(frm)
        frame.pack(side='top')
        Entry(frame, justify='left', textvariable=_strVars[i]).pack(side='left')
        Label(frame, text=f'{KeyName}+{i + 1}').pack(side='right')
    
    return frm

def loadTextFromFile():
    """加载配置
    """
    if not os.path.exists(DataSavePath):
        return
    global strVars
    try:
        with open(DataSavePath,'r+',encoding='utf8') as f:
            [[strVars[i][j].set(s) for j,s in enumerate(l)]for i,l in enumerate(json.load(f))]
    except:
        print('read file err or json format err')
        

def saveText2File():
    """保存配置
    """
    global strVars

    try:
        with open(DataSavePath,'w',encoding='utf8') as f:
            json.dump([[s.get() for s in l ] for l in strVars],f)
    except:
        print('save json 2 file err')

def createColmVars(_master=None):
    """创建每列里的StringVar

    Args:
        _master (_type_, optional): master. Defaults to None.

    Returns:
        List[StringVar]: return StringVar list of len(RowsSum)
    """
    return [StringVar(master=_master, value='') for _ in range(RowsSum)]

def createVars(_master=None):
    """创建所有StringVar

    Args:
        _master (_type_, optional): _description_. Defaults to None.

    Returns:
        List[[StringVar]]: [ColmSum][RowsSum]
    """
    return [createColmVars(_master) for i in range(ColmSum)]

def _paste(numb):
    """复制操作

    Args:
        numb (int): _description_
    """
    global strVars
    global KeyboardWrite

    temp = strVars[CheckColm.get()][numb-1].get()
    if not isinstance(temp,str):
        temp = str(temp)
    # 模拟键盘输入还是CV
    if KeyboardWrite.get():
        keyboard.write(temp,restore_state_after=False)
    else:
        CLIP.copy(temp)
        keyboard.send('ctrl+v')

def setHotkey():
    """设置KeyName+number的快捷键
    """
    for i in range(1, 6):
        keyboard.add_hotkey(f'{KeyName}+{i}', _paste, args=[i], suppress=True,trigger_on_release=True)

def main():
    global root

    root = Tk()
    root.title('剪贴板助手')
    createGUI()
    setHotkey()
    loadTextFromFile()
    root.mainloop()

if __name__ == "__main__":
    main()