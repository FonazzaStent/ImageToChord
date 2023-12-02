"""Image to Chord 1.3.3 - Convert images to chords.
Copyright (C) 2023  Fonazza-Stent

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

import random
from random import randint
from PIL import ImageTk, Image, ImagePalette
import tkinter as tk
from tkinter import colorchooser
import tkinter.ttk as ttk
import musicpy
from shutil import copyfile
from os import remove
import colorsys
from tkinter.filedialog import askopenfilename

notes=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
rgb_scale = 255
cmyk_scale = 100
steps=[[0, 1, 3, 4, 6, 8, 10, 0], [0, 1, 3, 5, 6, 8, 10, 0], [0, 1, 3, 5, 7, 8, 10, 0], [0, 1, 3, 5, 7, 9, 10, 0], [0, 2, 3, 5, 6, 8, 10, 0], [0, 2, 3, 5, 7, 8, 10, 0], [0, 2, 3, 5, 7, 9, 10, 0], [0, 2, 3, 5, 7, 9, 11, 0], [0, 2, 4, 5, 7, 8, 10, 0], [0, 2, 4, 5, 7, 9, 10, 0], [0, 2, 4, 5, 7, 9, 11, 0], [0, 2, 4, 6, 7, 9, 10, 0], [0, 2, 4, 6, 7, 9, 11, 0], [0, 2, 4, 6, 8, 9, 11, 0]]
stepsitem=[]
stepscale=[]
stepscales=[]
chord_play=[]
scales=[]
validate_count=1

def init():
    global chordnotes
    global counter
    global chord
    global chordstring
    global notelist
    global occurrences
    global chordsteps
    global scale
    global stepstransposed
    global chordn
    global scalecombo

    chordnotes=[]
    chord=[]
    chordsteps=[]
    counter=1
    octave=3
    chordstring=""
    notelist=[]
    occurrences=[]
    clash_occ=[0,0,0,0,0,0,0,0,0,0,0,0]
    random.seed()
    scale=[]
    scalecombo=[]
    stepstransposed=[]

#Create app window
def create_app_window():
    global top
    global rootw
    img=b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TtVIrDlYQcchQXbSLijiWKhbBQmkrtOpgcukXNGlIUlwcBdeCgx+LVQcXZ10dXAVB8APE1cVJ0UVK/F9SaBHrwXE/3t173L0DhHqZqWZXBFA1y0jGomImuyr6XuFHD/owgSGJmXo8tZhGx/F1Dw9f78I8q/O5P0e/kjMZ4BGJI0w3LOIN4tlNS+e8TxxkRUkhPieeNOiCxI9cl11+41xwWOCZQSOdnCcOEouFNpbbmBUNlXiGOKSoGuULGZcVzluc1XKVNe/JXxjIaSsprtMcRQxLiCMBETKqKKEMC2FaNVJMJGk/2sE/4vgT5JLJVQIjxwIqUCE5fvA/+N2tmZ+ecpMCUaD7xbY/xgDfLtCo2fb3sW03TgDvM3CltfyVOjD3SXqtpYWOgIFt4OK6pcl7wOUOMPykS4bkSF6aQj4PvJ/RN2WBwVvAv+b21tzH6QOQpq6Wb4CDQ2C8QNnrHd7d297bv2ea/f0AnppyuCZ8qSgAAAAGYktHRAD/AP8A/6C9p5MAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAHdElNRQfnCgYLLiCUcgDiAAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAABvdJREFUWMONl3+MVFcVxz/n3DczO7Prilhqd3VX3VpIagNp0gqJaULUWBsE0tDERIrWKpEfUsAiReVHhZYfbQKFCoX+Ev9QUmNFYltp+BXB+DvWGP9oi0s1Eajt0lba7uzMvHuPf7w3b9/sbFte8ua9ue/ec879nnO+51w5NXjGGHuF9iFUEAOT1uG2sfHWvsNlApr9MWtR1nbTqigEx4Jld7NgxT2IgUhiICTvbU+VNvliIKcGzxjBMCETkE0yHbPdwFfu2Ehvd4nayDCPr1/A3HU/ob8EZ+vK/p1rIQiGtqxpblBEkmdOj5w6PWgtSoOxYOW9eAPRBgHBhQhLhTiL8Q7EHMEJkfd4ETQEvBPUOzAjiCACuMDmby/lY32XjeuiKFOc80vBPGd+uRsTQ8wQIBAQIPlRAjbqRwNjFEWHw4shIfDc2Tc4+ed/MNA3CW+pjNQtZkYkIlhI4Um/ekAk0WXJbBSXwEeyUFNR2X/RTA6AhmSxiOCDT8YQDAMVLF0b5YOv+Z4fawocL7hePP86Ax+aQKSt4zWEa+YsIcYx+Youbpx146jcMWhnLrD8bsYG33gpZMZN39xAsJjBp/ag1hwPfPLm5bzw1ENcvPgmfz83zMLVm5hx7dUJymNSd1xNXrgkA0wCqHDlF5dgElLkBBl5i18d/yOfn7+Mrk7h1lvmsmHjdkRG46aZCTo+ecglGBBSCB2o8PHZSxBRRITTv/4RN0ydwtM/vg9QKp0Rg0NVfN23uVszgmkx4r3Z7K77HqHghOO77ySSIiKOK2d/I7N/4sRuJnV/AFHFgue6Kb00QkBJCSuNBW3SaQtToe8J/89/f5qdq2+nr7+fFw9uR1Uh6qBeb4wGZHp771n8rcW8TZFbl63H1CEWcpp0LOThXQ3wgGqdqb0fxFJUnz+4B1Xlwn9fHp2nCRpOi+zevpMnH9vLX/bdzm0r1xFJNAaBpgveIQMMw+MJKUGIGLiQ1AAR8A0kfgNzo5tRS2TH3vOf8y9z2+xPMWPRYzx0z7osBqIsBpr5Lu27995z1c3LU2aE4IwSDhGXCZo5/w6O7l1PT09vy9rDR47w+JPHMHH87ZUiu7d+j66OdJ3kEciDn0PBzJg8bxXWTCEU8Y5nd6+nt6cvQ+C3Bx4ksnKW4AHPVbOX8rkZMzi5/auYKtOu/gSdlTIeS9wDRCaAWYaAAqKt7CfhbZDCKLROEKqtiStCT08PANseOcC+Q7/hn8/sY/KshVwzZYBH711NR0eRMIYNtT0D2q/Thx6mKEIkSaE99eCdTKi8rz1OvDEwZznz5t7Ec7sWMGXOIo7ev5SZN3yaUqVMEG1raKJL6VxE4PmDD1JvNLgwNJTttDUzjIF5K+l0nlkLV6Mac+T+FQwVr8DsYlvHlVXDjAlVsoASCeRqYVLHJFAqFunt7R2XF4brgU5XpeYLPLNjFQHHuUI3EhTFEupOXd2svIK09gPNIqEEXq8OEyOICT6EZIplGhEVRB0BQQj4oBzZv4NXhy5wwZUIodkbNHClMg7Dp8UoK+syjgtEBG9w/S3LwBwNC2AyymyW60ZpspkDPKIu+y4qhBAQB3FU5ont3weSNLacK6IW6hdJMiIyVs+ZThxiIldHiRgejql0KKVSATNHI/ZAjCj4RkwthnrN4yKlEBUpRYoRaPjAtsMvMDxSpdRRygpd5o7xekI15X/VEYooBGPRmk0cu3smFsMXthxl15aNeDUK5/7Koh2H2bN5DYvXbuPZtTOIvPLZrb/j4c3fxYJlrRsuUKlUEEmQaepTtL2FNjW6O0t0dBYodRXwhYj+a+fSd3k3ddeFaExn2fHRaZ8B8biSQ8Xom76Qj0x6P1vmT0eKBcrdHZS7SsldLmOWGJTvsrTZkptZVg9McmcAjZg5tZ/w7xOoBTTUqMWBWt1RLig+wEgcs2rp14nCCBAx6/oPs+iuTaN1Ine2IFhLy6ctJx6VNqL42op1PPqDjYjBa9UGogUiJ8SNBq+eHyRokQgY6LucXfufAIyy1ahagVqt+u78YrlynIclb6kF4KWfYSq89maMWZ3uSicdZWXemr049RRdRKkS8cChU8QUMDNObv4ScUPayKfNiPzJSGlFwHD0T6jQN3QcMcefXmnw1mXX0VFMqlm9VscHT7FYpBBFfHnFBv51cAf20nG8KZNXPc2BBzYQp+3b2PavjQcCCUE0Jx45cZKfHjxBLAVc7Syl8kR+uHUaIhFmlqZVOl3ACfzi6B/4zs5jqA6DKNVqlUJuXjPTskLXRCBPRHlrm7DF9TpxPaAOiuWObE4WP6nLaiMhLdpGqaSIOIK0noiBpIXLiEhHycGwpCdJI9dS46JikajYfgy3HJGJCOVK1EI0wayNabPvZvwf3s9Xdk/SRwYAAAAASUVORK5CYII='
    rootw= tk.Tk()
    top= rootw
    top.geometry("470x548")
    top.resizable(0,0)
    top.title("Image to Chord")
    favicon=tk.PhotoImage(data=img) 
    rootw.wm_iconphoto(True, favicon)

    #Create settings entries

    global ColorDisplayFrame
    ColorDisplayFrame= tk.Canvas(top)
    ColorDisplayFrame.place(x=25, y=20, height=198, width=265)
    ColorDisplayFrame.configure(relief='groove')
    ColorDisplayFrame.configure(borderwidth="2")
    ColorDisplayFrame.configure(relief="groove")
    ColorDisplayFrame.bind("<Button-1>",open_file)
    #ColorDisplayFrame.pack()
 
    #chord display
    global chord_display
    global chord_display_entry
    global chord_display_label
    chord_display=tk.Text(top)
    chord_display.place(x=25,y=243,height=25,width=420)
    chord_display.configure(state='disabled')    
    chord_display_label=tk.Label(top)
    chord_display_label.place(x=25,y=268,width=420)
    chord_display_label.configure(text="Chord",anchor="w", justify="left",font=("Arial",12))
    #scales display
    global scales_display
    scales_display=ttk.Combobox(top)
    scales_display.place(x=25,y=298,height=25,width=420)
    scales_display.configure(state="readonly",values=[" "])    
    scales_display_label=tk.Label(top)
    scales_display_label.place(x=25,y=323,width=200)
    scales_display_label.configure(text="Scale",anchor="w", justify="left",font=("Arial",12))
    #history display
    global history_display
    global history_display_entry
    history_display = tk.Text(top)
    history_display.place(x=25, y=358, height=160, width=405)
    scroll_1=tk.Scrollbar (top)
    scroll_1.place(x=440, y=358, height=160, anchor='n')
    history_display.configure(yscrollcommand=scroll_1.set)
    scroll_1.configure(command=history_display.yview)    
    #generate chord button
    """global generate_chord_button
    generate_chord_button=tk.Button(top)
    generate_chord_button.place(x=310,y=20,height=40,width=140)
    generate_chord_button.configure(text="Generate chord",font=("Arial",12))
    generate_chord_button.bind("<Button-1>",generate_chord_hotkey)"""
    #play chord button
    global play_chord_button
    play_chord_button=tk.Button(top)
    play_chord_button.place(x=310,y=20,height=40,width=140)
    play_chord_button.configure(text="Play chord",font=("Arial",12))
    play_chord_button.bind("<Button-1>",play_chord_hotkey)
    #play scale button
    global play_scale_button
    play_scale_button=tk.Button(top)
    play_scale_button.place(x=310,y=70,height=40,width=140)
    play_scale_button.configure(text="Play scale",font=("Arial",12))
    play_scale_button.bind("<Button-1>",play_scale_hotkey)
    #Load Image button
    global load_image_button
    load_image_button=tk.Button(top)
    load_image_button.place(x=310,y=120,height=40,width=140)
    load_image_button.configure(text="Load image",font=("Arial",12))
    load_image_button.bind("<Button-1>",open_file)    
    #notes number
    global notes_number
    global notes_number_entry
    notes_number=4
    nn=tk.StringVar()
    nn.set(notes_number)
    notes_number_entry=tk.Entry(top, textvariable=nn,justify="right",font=("Arial",12))
    notes_number_entry.place(x=310,y=170,width=45,height=25)
    notes_number_label=tk.Label(top)
    notes_number_label.place(x=310,y=205,width=189,height=15)
    notes_number_label.configure(text="Number of notes (4-11)",anchor="w", justify="left",font=("Arial",10))

#get notes number
def get_notes_number():
    global notes_number
    notes_number=notes_number_entry.get()
    if notes_number.isdigit()==True:
        notes_number=int(notes_number)
        #print (notes_number)
        if int(notes_number)<4:
            notes_number=4
        if int(notes_number)>11:
            notes_number=11
    else:
        notes_number=4
    notes_number_entry.delete(0,tk.END)
    notes_number_entry.insert(0,str(notes_number))
    notes_number=notes_number-1

#Convert Image
def convert_image():
    global color
    global img_display
    global indexed_img
    global onepix_color
    imgfile=Image.open(imgfilename)
    w,h=imgfile.size
    ratio=w/h
    height=198
    width=int(height*ratio)
    img=imgfile.resize((width,height),Image.Resampling.BICUBIC)
    get_notes_number()
    #notes_number=notes_number-1
    indexed_img=img.convert("P").quantize(colors=notes_number,method=Image.Quantize.MEDIANCUT,kmeans=2,dither=Image.Dither.FLOYDSTEINBERG)
    img_display = ImageTk.PhotoImage(image=img)
    ColorDisplayFrame.create_image(0,0, image = img_display, anchor = tk.NW)
    ColorDisplayFrame.update()
    onepix=imgfile.resize((1,1),Image.Resampling.BICUBIC)
    px = onepix.load()
    onepix_color=px[0,0]
    get_palette()
    generate_chord()
    #remove("indexed.png")

#get palette
def get_palette():
    global lightness_values
    global hue_values
    palcol=indexed_img.palette.colors
    #pal.save("palette.png",format="png")
    palcol2 = {}
    for k, v in palcol.items():
        palcol2[v] = palcol2.get(v, ()) + k
    lightness_values=[]
    #print (palcol2)
    palettelen=len(palcol2)
    for n in range (0,palettelen):
        R,G,B= (palcol2[n])
        lightness=int((R+G+B)/3)
        lightness_values.append(lightness)

    hue_values=[]    
    for n in range (0,palettelen):
        r,g,b,=palcol2[n]
        H,L,S=colorsys.rgb_to_hls(r, g, b)
        H=int(H*255)
        hue_values.append(H)
    
    lightness_values.reverse()
    #print (lightness_values)
    #print (hue_values)

#Open File
def open_file(event):
    global imgfile
    global imgfilename
    data=[('Image', '*.bmp *.jpg *.png')]
    imgfilename=askopenfilename(filetypes=data)
    if str(imgfilename)!='':
        imgfile=open(imgfilename,'rb')
    convert_image()

def pick_color_frame(event):
    pick_color()
    
#convert Hex to RGB
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    
def play_chord():
    global chord_play
    #print (chord_play)
    if chord_play!=[]:
        c_one=musicpy.chord(notes=chord_play,interval=0, duration=2)
        #print (c_one)
        musicpy.play(c_one,100)
        copyfile("temp.mid","chord.mid")
        remove("temp.mid")

def play_chord_hotkey(event):
    play_chord()

def play_scale():
    global scales_display
    global scales
    if scales!=[]:
        index=scales_display.current()
        octave=5
        c=musicpy.chord(scales[index],interval=0.3,duration=0.3)
        musicpy.play(c,100)
        copyfile("temp.mid","scale.mid")
        remove ("temp.mid")

def play_scale_hotkey(event):
    play_scale()



#Name Chord
def name_chord():
    global chordname_string
    chord_length=len(chord)
    chordname=[]
    chord_notes=[]
    chordname_string=''
    for n in range (0,12):
        if chord[0]==notes[n]:
            index=n
            for i in range (0,12):
                chord_notes.append(notes[index])
                index=index+1
                if index>11:
                    index=0
    #print (chord_notes)

    chordname.append(chord[0])

    sus=False
    sus_index=999
    ninth=False
    ninth_index=999
    seventh_maj=False
    seventh_maj_index=999
    seventh=False
    seventh_index=999
    sixth=False
    sixth_index=999
    eleventh=False
    eleventh_index=999
    ninth_maj=False
    ninth_maj_index=999
    thirteenth=False
    maj=False
    minr=False
    plusninth=False
    mincheck=False
    bfive=False
    fifth=False
    dim=False
    aug=False
    add_fifth=False
    minr_index=999
    for n in range (1,chord_length):
        step=chord_notes.index(chord[n])+1
        #print (step)
        if step==5:
            maj=True
            minr=False
        if step==4:
            minr=True
            maj=False
        if maj==True and minr==True and plusninth==False:
            plusninth=True
            minr=False
            chordname.append(" 9+")
            plusninth_index=len(chordname)
        elif minr==True and mincheck==False:
            chordname.append("m ")
            minr_index=len(chordname)
            mincheck=True
        if step==8:
            fifth=True

    for n in range (1,chord_length):
        step=chord_notes.index(chord[n])+1
        if step==6 and sus==False:
            sus=True
            chordname.append(" Sus")
            sus_index=len(chordname)
        if minr==True and step==7 and dim==False and fifth==False:
            dim=True
            chordname.append(" Dim")
            dim_index=len(chordname)
            if minr_index!=999:
                chordname[minr_index-1]='delete'
        if dim==False and step==7 and bfive==False:
            bfive=True
            chordname.append(" Add5b")
            bfive_index=len(chordname)
        if step==9 and fifth==False and aug==False:
            aug=True
            chordname.append(" Aug")
            aug_index=len(chordname)-1
        if step==9 and fifth==True and add_fifth==False:
            add_fifth_plus=True
            chordname.append(" Add5+")
            add_fifth_plus_index=len(chordname)
        if step==10:
            sixth=True
            chordname.append(" 6")
            sixth_index=len(chordname)
        if step==11:
            seventh=True
            chordname.append(" 7")
            seventh_index=len(chordname)
            #print (seventh_index)
        if step==12:
            seventh_maj=True
            chordname.append(" 7maj")
            seventh_maj_index=len(chordname)
        if step==3 and seventh==True:
            ninth=True
            chordname.append(" 9")
            ninth_index=len(chordname)
            if seventh_index!=999: 
                chordname[seventh_index-1]='delete'
        if step==3 and sus==False and seventh_maj==True:
            ninth_maj=True
            chordname.append(" 9maj")
            ninth_maj_index=len(chordname)
            if seventh_maj_index!=999:
                chordname[seventh_maj_index-1]='delete'
        if step==3 and seventh_maj==False and seventh==False:
            add_ninth=True
            chordname.append(" Add9")
            ninth_maj_index=len(chordname)
            if seventh_maj_index!=999:
                chordname[seventh_maj_index-1]='delete'        
        if step==2:
            ninthb=True
            chordname.append(" Add9b")
            ninthb_index=len(chordname)
        if ninth==True and sus==True and sixth==False and(seventh==True or seventh_maj==True):
            eleventh=True
            chordname.append(" 11")
            eleventh_index=len(chordname)
            #print (eleventh_index)
            chordname[ninth_index-1]='delete'
            chordname[sus_index-1]='delete'

        if ninth==True and sus==True and sixth==True and(seventh==True or seventh_maj==True):
            thirteenth=True
            chordname.append(" 13")
            thirteenth_index=len(chordname)
            if ninth_index!=999:
                chordname[ninth_index-1]='delete'
            if sixth_index!=999:
                chordname[sixth_index-1]='delete'
            if sus_index!=999:
                #print (sus_index)
                chordname[sus_index-1]='delete'
            if seventh_index!=999:
                #print (seventh_index)
                chordname[seventh_index-1]='delete'
            if eleventh_index!=999:
                chordname[eleventh_index-1]='delete'
            

    length=len(chordname)           
    for x in range(0,length):
        #print (x)
        if chordname[x]!='delete':
            chordname_string=chordname_string+chordname[x]

def rgb_to_cmyk(r,g,b):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / float(rgb_scale)
    m = 1 - g / float(rgb_scale)
    y = 1 - b / float(rgb_scale)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) 
    m = (m - min_cmy) 
    y = (y - min_cmy) 
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    cmyk=[ int(c*cmyk_scale), int(m*cmyk_scale), int(y*cmyk_scale), int(k*cmyk_scale)]
    return cmyk

#GenerateChord

def generate_chord():
    global notesnumber
    global counter
    global chordnotes
    global counter
    global chord
    global chordstring
    global chord_play
    global notelist
    global occurrences
    global clash_occ
    global chordsteps
    global scale
    global scales
    global stepstransposed
    global root
    global trycheck
    global chordok
    global chordmem
    global rootvalue
    global Hvalue
    global notevalue
    global octave
    chord_play=[]
    scales=[]
    R,G,B=onepix_color
    #cmyk=rgb_to_cmyk(R,G,B)
    r=R/255
    g=G/255
    b=B/255
    H,L,S=colorsys.rgb_to_hls(r, g, b)
    H=int(H*239)
    if H<=239 and H>=228:
        Hvalue=0
    if H<=227 and H>=217:
        Hvalue=1
    if H<=216 and H>=198:
        Hvalue=2
    if H<=197 and H>=179:
        Hvalue=3
    if H<=178 and H>=103:
        Hvalue=4
    if H<=102 and H>=76:
        Hvalue=5
    if H<=75 and H>=50:
        Hvalue=6
    if H<=49 and H>=42:
        Hvalue=7
    if H<=41 and H>=34:
        Hvalue=8
    if H<=33 and H>=23:
        Hvalue=9
    if H<=22 and H>=13:
        Hvalue=10
    if H<=12 and H>=0:
        Hvalue=11
    chord=[]
    rootvalue=int(Hvalue)
    #print (rootvalue)
    root=notes[rootvalue]
    chord.append(root)
    chordsteps.append(notes[rootvalue])
    chord_play.append(notes[rootvalue]+'2')
    notevalue=rootvalue
    #print (notevalue,root)
    counter=1
    octave=3
    for value in hue_values:
        try:
            interval=int(value/42.5)+3
        except:
            interval=3
        notevalue=notevalue+interval

        if notevalue>11:
            notevalue=notevalue-11
            octave=octave+1
        validate_note()
        chord.append(notes[notevalue])
        chordsteps.append(notevalue)
        chord_play.append(notes[notevalue]+str(octave))          
        counter=counter+1

    counter =1
    
    name_chord()        
    chorddisplay=''
    for item in chord:
        chorddisplay= chorddisplay+item+" "
    #print ("\n"+"Chord: "+chorddisplay+"\n")
    history_display.configure(state='normal')
    history_display.insert(tk.END,"\n"+chorddisplay+"\n")
    chord_display.configure(state="normal")
    chord_display.delete(1.0,tk.END)
    chord_display.insert(tk.END,chorddisplay)
    history_display.yview('end')
    chord_display.configure(state="disabled")
    chord_display_label.configure(text="Chord: "+chordname_string,anchor="w", justify="left",font=("Arial",12))    
    guess_scale()
    init()
    ColorDisplayFrame.create_image(0,0, image = img_display, anchor = tk.NW)
    ColorDisplayFrame.update()



def generate_chord_hotkey(event):
    generate_chord(RGBcolor[0],RGBcolor[1],RGBcolor[2])

def validate_note():
    global notevalue
    global octave
    global validate_count
    for chordnote in chord:
        if notes[notevalue]==chordnote:
            notevalue=notevalue+2
            validate_count=validate_count+1
            if notevalue>11:
                notevalue=notevalue-11
                octave=octave+1
            if validate_count<=3:
                validate_note()
            else:
                validate_count=1

def guess_scale():
    global match
    global matchlist
    global scale
    global scales
    global stepstransposed
    global stepsitem
    global root
    global stepscale
    global stepscales
    match=0
    matchlist=[]
    stepscale=[]
    stepscales=[]
    chordlen=len(chordsteps)
    stepslen=len(steps)
    for n in range (0, stepslen):
        for m in range (0,7):
            transpose=steps[n][m]+rootvalue
            if transpose>11:
                transpose=transpose-12
            stepsitem.append(transpose)
            transpose=0
        stepstransposed.append(stepsitem)
        stepsitem=[]
    #print (stepstransposed)
    #print (chord)
    for n in range (0, stepslen):
        for m in range (0,7):
            for o in range (0,chordlen):
                #print (chordsteps[o],steps[n][m])
                if chordsteps[o]==stepstransposed[n][m]:
                    match=match+1
                    
        matchlist.append(match)
        match=0


    for n in range (0,stepslen):
        if matchlist[n]==max(matchlist):
            #print (steps[n])
            #print (stepstransposed[n])
            for x in range (0,7):
                noteindex=stepstransposed[n][x]
                scalenote=notes[noteindex]
                scale.append(scalenote)
                stepscale.append(noteindex)
        if scale!=[]:
            scales.append(scale)
            stepscales.append(stepscale)
        scale=[]
        stepscale=[]
    scalestring=''
    #print ("Scales:")
    history_display.configure(state='normal')
    history_display.insert(tk.END,"\nScales:\n")
    guess=1
    for item in scales:
        for note in item:
            scalestring=scalestring+note+" "
        #print ("Match",str(guess)+": ",scalestring)
        scalecombo.append(scalestring)
        history_display.insert(tk.END,"Match"+str(guess)+": "+str(scalestring)+"\n")
        guess=guess+1
        scalestring=''
    scales_display.configure(value=scalecombo)
    scales_display.current(0)
    guess=0
    #print ("\n")
    #history_display.insert(tk.END,"\n")
    history_display.yview('end')
    history_display.configure(state="disabled")
    #print (scales)

#CopyContextMenu
def create_context_menu():
    global menu
    menu = tk.Menu(rootw, tearoff = 0)
    menu.add_command(label="Copy", command=copy_text)
    rootw.bind("<Button-3>", context_menu)

def context_menu(event): 
    try: 
        menu.tk_popup(event.x_root, event.y_root)
    finally: 
        menu.grab_release()
        
def copy_text():
        history_display.event_generate(("<<Copy>>"))

def main():
    init()
    create_app_window()
    create_context_menu()
    
main()
rootw.mainloop()
