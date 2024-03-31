import pymem
import customtkinter
import keyboard
import threading
from time import sleep as wait
import subprocess
 
subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 730")
wait(25)

 
app = customtkinter.CTk()
app.geometry("250x300")
app.title("Cheat")
app.wm_attributes('-topmost', True)
 
pm = pymem.Pymem("csgo.exe")
client = pymem.pymem.process.module_from_name(pm.process_handle, 'client.dll').lpBaseOfDll
 
triggerBot = True
triggerBotThread = True
 
espOn = True
espThread = True
 
chamsOn = True
chamsThread = True
 
bhopOn = True
bhopThread = True
 
noFlashOn = True
noFlashThread = True
 
radarOn = True
radarThread = True
 
crosshair = 0x11838
 
plr = pm.read_uint(client + 0xDEA964)
 
def triggerBotFunc():
    while True:
        plr = pm.read_uint(client + 0xDEA964)
        if plr:
            if pm.read_uint(plr + 0x100) >= 0:
                cross = pm.read_uint(plr + crosshair)
                localTeam = pm.read_uint(plr + 0xF4)
                team = pm.read_uint(client + 0x4DFFEF4 + (cross - 1) * 0x10)
                if team:
                    crosshairTeam = pm.read_uint(team + 0xF4)
                if localTeam != crosshairTeam:
                    if cross >= 1 and cross <= 15:
                        pm.write_int(client + 0x322DCFC, 6)
                        wait(.2)
 
def changeFov(value):
    plr = pm.read_uint(client + 0xDEA964)
    if plr:
        pm.write_int(plr + 0x333C, int(value))
        fovDisplay.configure(text = pm.read_uint(plr + 0x333C))
 
def glowEsp():
    global espOn
    glowManager = pm.read_uint(client + 0x535A9C8)
    
    while True:
        plr = pm.read_uint(client + 0xDEA964)
 
        for x in range(33):
            entity = pm.read_uint(client + 0x4DFFEF4 + x * 0x10)
 
            if entity:
                entityTeam = pm.read_uint(entity + 0xF4)
                localTeam = pm.read_uint(plr + 0xF4)
                health = pm.read_uint(entity + 0x100)
                
 
                if int(health) >= 1: 
                    if entityTeam != localTeam:
 
                        glowIndx = pm.read_uint(entity + 0x10488)
                        pm.write_float(glowManager + (glowIndx * 0x38) + 0x8, 0.25)
                        pm.write_float(glowManager + (glowIndx * 0x38) + 0xC, 0.0)
                        pm.write_float(glowManager + (glowIndx * 0x38) + 0x10, 1.0)
                        pm.write_float(glowManager + (glowIndx * 0x38) + 0x14, 1.0)
 
                        pm.write_bool(glowManager + (glowIndx * 0x38) + 0x27, espOn)
                        pm.write_bool(glowManager + (glowIndx * 0x38) + 0x28, espOn)
 
                    else:
                        
                        glowIndx = pm.read_uint(entity +0x10488)
                        pm.write_float(glowManager + (glowIndx * 0x38) + 0x8, 0.0)
                        pm.write_float(glowManager + (glowIndx * 0x38) + 0xC, 1.0)
                        pm.write_float(glowManager + (glowIndx * 0x38) + 0x10, 0.0)
                        pm.write_float(glowManager + (glowIndx * 0x38) + 0x14, 1.0)
 
                        pm.write_bool(glowManager + (glowIndx * 0x38) + 0x27, espOn)
                        pm.write_bool(glowManager + (glowIndx * 0x38) + 0x28, espOn)
 
def chams():
    while True:
        plr = pm.read_uint(client + 0xDEA964)
        for x in range(33):
            entity = pm.read_uint(client + 0x4DFFEF4 + x * 0x10)
 
            if entity:
                entityTeam = pm.read_uint(entity + 0xF4)
                localTeam = pm.read_uint(plr + 0xF4)
                if entityTeam != localTeam:
                    pm.write_int(entity + 0x70, (50))
                    pm.write_int(entity + 0x71, (0))
                    pm.write_int(entity + 0x72, (255))
                else:
                    pm.write_int(entity + 0x70, (0))
                    pm.write_int(entity + 0x71, (255))
                    pm.write_int(entity + 0x72, (0))
 
 
 
def runEsp():
    global espOn
    global espThread
 
    if espOn:
        espOn = False
    else:
        espOn = True
 
    if not espThread:
        espThread = True
        func = threading.Thread(target=glowEsp)
        func.start()
 
def runChams():
    global chamsOn
    global chamsThread
 
    if chamsOn:
        chamsOn = False
    else:
        chamsOn = True
 
    if not chamsThread:
        chamsThread = True
        chamss = threading.Thread(target=chams)
        chamss.start()
 
def runTriggerBot():
    global triggerBot
    global triggerBotThread
 
    if triggerBot:
        triggerBot = False
    else:
        triggerBot = True
 
    if not triggerBotThread:
        triggerBotThread = True
        trig = threading.Thread(target=triggerBotFunc)
        trig.start() 
 
 
def radarFunc():
    global radarOn
    while True:
        plr = pm.read_uint(client + 0xDEA964)
        if plr:
            for x in range(33):
                entity = pm.read_uint(client + 0x4DFFEF4 + x * 0x10)
                if entity:
                    pm.write_uchar(entity + 0x93D, 1)
 
def runRadar():
    global radarOn
    global radarThread
 
    if radarOn:
        radarOn = False
    else:
        radarOn = True
 
    if not radarThread:
        radarThread = True
        radarr = threading.Thread(target=radarFunc)
        radarr.start() 
 
 
def bhopFunc():
    global bhopOn
    while True:
        if bhopOn:
 
            if keyboard.is_pressed("space"):
                force_jump = client + 0x52BBC7C
                plr = pm.read_uint(client + 0xDEA964)
                if plr:
                    on_ground = pm.read_uint(plr + 0x104)
                    if on_ground and on_ground == 257:
                        pm.write_int(force_jump, 5)
                        wait(0.01)
                        pm.write_int(force_jump, 4)
        wait(0.001)
 
 
def noFlashFunc():
    global noFlashOn
    while True:
        if noFlashOn:
 
            plr = pm.read_uint(client + 0xDEA964)
            if plr:
                if pm.read_uint(plr +  0x1046C) > 0.0:
                    pm.write_float(plr +  0x1046C, float(0))
 
            
        wait(.001)
 
def runBhop():
    global bhopOn
    global bhopThread
 
    if bhopOn:
        bhopOn = False
    else:
        bhopOn = True
 
    if not bhopThread:
        bhopThread = True
        bhopp = threading.Thread(target=bhopFunc)
        bhopp.start()  
 
def runNoFlash():
    global noFlashOn
    global noFlashThread
 
    if noFlashOn:
        noFlashOn = False
    else:
        noFlashOn = True
 
    if not noFlashThread:
        noFlashThread = True
        fThread = threading.Thread(target=noFlashFunc)
        fThread.start()  
try:
    fovDisplay = customtkinter.CTkLabel(master=app, text=f"Fov: {pm.read_uint(plr + 0x333C)}", font=('Arial', 25))
    fovDisplay.pack(pady=0, padx=0)
except:
    pass
 
fovSlider = customtkinter.CTkSlider(master=app, command=changeFov, from_=60, to=150)
fovSlider.pack(pady=10, padx=10)
 
 
 
espBtn = customtkinter.CTkButton(master=app, command=runEsp, text='Esp', width=50, height=25)
espBtn.pack(pady=5, padx=0)
 
ChamsBtn = customtkinter.CTkButton(master=app, command=runChams, text='Chams', width=50, height=25)
ChamsBtn.pack(pady=5, padx=0)
 
TriggerBotBtn = customtkinter.CTkButton(master=app, command=runTriggerBot, text='Trigger Bot', width=50, height=25)
TriggerBotBtn.pack(pady=5, padx=0)
 
BhopBtn = customtkinter.CTkButton(master=app, command=runBhop, text='Bhop', width=50, height=25)
BhopBtn.pack(pady=5, padx=0)
 
NoFlashBtn = customtkinter.CTkButton(master=app, command=runNoFlash, text='No Flash', width=50, height=25)
NoFlashBtn.pack(pady=5, padx=0)
 
RadarBtn = customtkinter.CTkButton(master=app, command=runRadar, text='Radar', width=50, height=25)
RadarBtn.pack(pady=5, padx=0)
 
 
app.mainloop()