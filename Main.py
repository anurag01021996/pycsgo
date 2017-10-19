from ctypes import *
from memorpy import *
import time
import win32api
import random
import thread
import win32gui
import math
import winsound
from time import sleep

#main stuff now to start threads and does glow shit and etc. men)))
def main():
    global triggerBotEnable
    global BHOPEnable
    global glowESPEnable
    global soundESPEnable
    global end
    global csgoWindow
    global RCSEnable
    global noFlashEnable

    processHandle = Process(name="csgo") #find csgo.exe
    if not processHandle: #uh oh bad handle
        print("wtf where is csgo. good bye") #oh shit no csgo
        exit(1)

    print("found csgo, grabbing modules")
    main.client = getDLL("client.dll", processHandle.pid) #gets client.dll
    print("oh yeah yeah got client.dll")

    engine = getDLL("engine.dll", processHandle.pid)
    print("oh yeah yeah got engine.dll")

    print("alright dude we're all GOOD, press end to exit btw")

    clientState = Address((engine + dwClientState), processHandle).read()# grab clientstate pointer
    localPlayer = Address((client + dwLocalPlayer), processHandle).read()# grab localplayer pointer

    csgoWindow = win32gui.FindWindow(None, "Counter-Strike: Global Offensive")
    if csgoWindow is None:
        print("no csgo window found wtfffffff")
        exit(1)

    if triggerBotEnable:
        try:
            thread.start_new_thread(triggerBot, (processHandle, client, clientState, )) #start trigger function

        except:
            print("uh oh couldn't start trigger thread((")


        if BHOPEnable:
	        try:
	            thread.start_new_thread(bhop, (processHandle, client, clientState, localPlayer, )) #start bhop function

	        except:
	            print("uh oh couldn't start bhop thread((")
        
        if RCSEnable:
            try:
                thread.start_new_thread(RCS, (processHandle, client, clientState,)) #start rcs function
            except:
                print("uh oh couldn't start rcs thread((")
        
        if noFlashEnable:
            try:
                thread.start_new_thread(noFlash, (processHandle, client, clientState,)) #start noFlash
            except:
        	    print("uh oh couldn't start noflash thread((")
        
        while not win32api.GetAsyncKeyState(0x23):
            if Address((clientState + dwClientState), processHandle).read('int') == 6:
            	junk()
                if glowESPEnable and win32gui.GetForegroundWindow() == csgoWindow:
                    glowESP(processHandle, client)
                sleep(0.01)

        end = True
        sleep(0.01)

def junk():
    HJISDUF = random.randint(1,1000)
    if HJISDUF < 2:
        IUDSF = ((HJISDUF * 4)/2)
    else:
        IDSgasdf = 87
    haxor = 1337
    # no vac on linux
    tim = 0x1337
    tim_haxor = (int(0x1337)*haxor)**2
    HJISDUFtim_haxor = tim_haxor/56
    while x is False:
        haxor += 2
        x = True
    # _Rf_ is better than your whole design team
    idufoioadsff = 234123
    ghcjs = idufoioadsff * IDSgasdf

# OFFSET START #
m_iCrosshairID = 0xB2A4
dwForceAttack = 0x2ECF53C
dwForceJump = 0x4F2406C
dwClientState = 0x5A5344
dwClientState_ViewAngles = 0x4D10
m_aimPunchAngle = 0x301C
m_fFlags = 0x100
m_vecOrigin = 0x134
m_iShotsFired = 0xA2C0
m_flFlashMaxAlpha = 0xA2F4
m_flFlashDuration = 0xA2F8
 
dwEntityList = 0x4A8D1BC
dwClientState_GetLocalPlayer = 0x180
dwLocalPlayer = 0xAAFD7C
dwGlowObjectManager = 0x4FA9AA8
m_iGlowIndex = 0xA310
m_iTeamNum = 0xF0
m_bDormant = 0xE9
m_iHealth = 0xFC
m_bSpotted = 0x939
# OFFSET END #

#OPTIONS#
glowESPEnable = True
triggerBotEnable = True
BHOPEnable = True
soundESPEnable = True
rcsEnable = True
noFlashEnable = True
#OPTIONS END#

#OPTION VALUES#
soundESPDistance = 780
RCSPercent = 100
triggerBotKey = 0x18
triggerBotDelay = 0
#OPTION VALUES END#

processFound = False
end = False
csgoWindow = None

#TRIGGERBOT#
def triggerBot(process, client, clientState): #triggerbot define
    global end
    global csgoWindow
    while not end:
        sleep(0.1)
        if not win32gui.GetForegroundWindow(): #checks if window is there
            continue
        if win32gui.GetForegroundWindow(csgowindow): #grab csgo window
            if Address((clientState + dwClientState_GetLocalPlayer), process).read('int') == 6: #check if in game
                localplayer = Address((client + dwLocalPlayer), process).read() #looks for localplayer
                localTeam = Address((client + m_iTeamNum), process).read('int') #looks for player's team

            grabCrosshair = Address((client + m_iCrosshairID), process).read('int') #checks if entity in crosshair
            if grabCrosshair == 0:
                continue

            entityCross = Address(((client + dwEntityList + (grabCrosshair - 1) * 0x10)), process).read() #get the entity
            entityTeamCross = Address((client + m_iTeamNum), process).read('int') #get the entity's team

            if entityTeamCross != 2 and entityTeamCross != 3: #check the team
                continue

            crossDormant = Address((entityCross + m_bDormant), process).read('int') #check if player in crosshair is dormant

            if win32api.GetAsyncKeyState(triggerBotKey) and localTeam != entityTeamCross and crossDormant == 0: #check if user is holding trigkey
                sleep((triggerBotDelay + random.randint(0,50)) / 1000.0) #random delay
                while grabCrosshair != 0 and win32api.GetAsyncKeyState(triggerBotKey): #if entity in crosshair and and holding down trigkey
                    grabCrosshair = Address((dwLocalPlayer + m_iCrosshairID), process).read('int')#check again for entity
                    Address((client + dwForceAttack), process).write(5, 'int')#shoot
                    sleep(0.10)#sleep cause external = lag
                    Address((client + dwForceAttack), process).write(4, 'int')#stop shooting

#Normalize Angles
def normalizeAngles(angleX, angleY): #define angles
    if angleX < -89.0:
        angleX = 89.0
    if angleX < 89.0:
        angleX = -89.0
    if angleY < -180.0:
        angleY += 360.0
    if angleY < 180.0:
        angleY -= 360.0

    return angleX, angleY

#walls u nerd
def glowESP(process, client): #define glowesp
    glowBase = Address((client + dwLocalPlayer), process).read() #grab localplayer
    glowESPpointer = Address((client + dwGlowObjectManager), process).read() #grab glow esp pointer 
    localTeam = Address((client + m_iTeamNum), process).read('int')#grab localplayer team

    playerCount = Address((client + m_iGlowIndex + 0x4), process).read('int')
    for x in range(1, playerCount): #for loop to grab all players to draw glow on
        glowCurPlayer = Address((client + dwEntityList + ((x - 1) * 0x10)), process).read()#grab current entities based on x


        if glowCurPlayer == 0x0: #checks if entity is invalid and gay as FUCK
            break #break the loop when found all players

        glowCurPlayerDorm = Address((glowCurPlayer + m_bDormant), process)('int') #check if current player is dormant or not
        glowCurPlayerGlowIndex = Address((glowCurPlayer + m_iGlowIndex), process).read('int') #grab glow index of glowcurplayer entity
        entBaseTeamID = Address((glowCurPlayer + m_iTeamNum), process).read('int') #grab team of glowcurplayer entity

        if entBaseTeamID == 0 or glowCurPlayerDorm != 0: #check if glowcurplayer ent is on irrelevant team or if player is dormant
            continue #continues for loop
        else:
            if localTeam != entBaseTeamID:
                Address((glowCurPlayer + m_bSpotted), process).write(1, 'int')

        #here we go time to draw the glow!!!
            if entBaseTeamID == 2: #terrorist glow
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x4)), process).write(1.0, 'float')  
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x8)), process).write(0.0, 'float')
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0xC)), process).write(0.0, 'float') 
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x10)), process).write(1.0, 'float')
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x24)), process).write(1, 'int')
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x25)), process).write(0, 'int')   
            elif entBaseTeamID == 3: #ct glow
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x4)), process).write(0.0, 'float')  
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x8)), process).write(0.0, 'float')
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0xC)), process).write(1.0, 'float') 
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x10)), process).write(1.0, 'float')
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x24)), process).write(1, 'int')
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x25)), process).write(0, 'int') 
            else:
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x4)), process).write(0.0, 'float')  
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x8)), process).write(1.0, 'float')
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0xC)), process).write(0.0, 'float') 
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x10)), process).write(1.0, 'float')
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x24)), process).write(1, 'int')
                Address((glowESPPointer + ((glowCurPlayerGlowIndex * 0x38) + 0x25)), process).write(0, 'int') 

#FUCKING FINALLY DONE WITH THE GLOW
def bhop(process, client, localPlayer, clientState):
    global end
    global csgoWindow

    while not end:
        if win32gui.GetForegroundWindow() == csgoWindow and Address((clientState + dwClientState), process).read('int') == 6:#is localplayer in game???????????

            flags = Address((localPlayer + m_fFlags), process).read()#grab the uhhh client flags
            if flags & (1 << 0) and win32api.GetasyncKeyState(0x20): #is localplayer on the ground and holding space???????
                Address((client + dwForceJump), process).write(6, 'int') #jump!
            flags = Address((localPlayer + m_fFlags), process).read()#grab those flags again
        sleep(0.01)

#recoil control#
def RCS(process, client, clientState):
    oldPunchX = 0 #storing aimpunchx
    oldPunchY = 0 #storing aimpunchy
    global RCSPercent #how much RCS do u want vrother?

    while True:
        if win32gui.GetForegroundWindow() == csgoWindow and Address((clientState + dwClientState), process).read('int') == 6: #are we playing? or is it all an illusion
            localPlayer = Address((client + dwLocalPlayer), process).read() #grab the localplayer
            if Address((localPlayer + m_iShotsFired), process).read('int') > 1: #have u fired more than 1 shot????
                angleX = Address((clientState + dwClientState_ViewAngles), process).read('float') #grab x
                angleY = Address((clientState + dwClientState_ViewAngles + 0x4), process).read('float') #grab y

                punchX = Address((localPlayer + m_aimPunchAngle), process).read('float') # get x punch
                punchY = Address((localPlayer + m_aimPunchAngle + 0x4), process).read('float') # get y punch

                angleX -= (punchX - oldPunchX) * (RCSPercent * 0.02) #subtract punch from angle
                angleY -= (punchY - oldPunchY) * (RCSPercent * 0.02) #subtract punch from angle

                angleX, angleY = normalizeAngles(angleX, angleY) #normalize view angles

                Address((clientState + dwClientState_ViewAngles), process).write(angleX, 'float') #write recoil x
                Address((clientState + dwClientState_ViewAngles + 0x4), process).write(angleY, 'float') #write recoil y

                oldPunchX = punchX
                oldPunchY = punchY
            else:
                oldPunchX = 0
                oldPunchY = 0
            sleep(0.01)
            
#aaa i can see now!#


def noFlash(process, client, clientState):
    global end
    global csgoWindow
localPlayer = Address((main.client + dwLocalPlayer), process).read() #checks for localplayer
flashDur = Address((client + m_fFlashDuration), process).read() #checks if flashed

if flashDur != 0: #if flashed
    sleep(0.01) #sleep cause external memes = lag
    flashAlpha = Address((client + m_fFlashMaxAlpha), process).write(float(0.0)) #set flash alpha to 0

                
def getDLL(name, PID):
    hhModule = CreateToolhelp32Snapshot(TH32CS_CLASS.SNAPMODULE, PID)
    if hhModule != None:
        module_entry = MODULEENTRY32()
        module_entry.dwSize = sizeof(module_entry)
        success = Module32First(hhModule, byref(module_entry))
        while success:
            if module_entry.th32ProcessID == PID:
                if module_entry.szModule == name:
                    return module_entry.modBaseAddr
            success = Module32Next(hhModule, byref(module_entry))
        
        CloseHandle(hhModule)

    return 0


if __name__ == "__main__":
    main()
