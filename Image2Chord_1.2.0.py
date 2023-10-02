"""Image to Chord 1.2.0 - Convert images to chords.
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
from PIL import ImageTk, Image
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
    octave=4
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
    img=b'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'

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
    chord_display_label.place(x=25,y=268,width=200)
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

#Convert Image
def convert_image():
    global color
    global img_display
    imgfile=Image.open(imgfilename)
    w,h=imgfile.size
    ratio=w/h
    height=198
    width=int(height*ratio)
    img=imgfile.resize((width,height),Image.Resampling.BICUBIC)
    im2=imgfile.resize((1,1),Image.Resampling.BICUBIC)
    px = im2.load()
    img_display = ImageTk.PhotoImage(image=img)
    ColorDisplayFrame.create_image(0,0, image = img_display, anchor = tk.NW)
    ColorDisplayFrame.update()
    RGBcolor=px[0,0]
    generate_chord(RGBcolor[0],RGBcolor[1],RGBcolor[2])

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

def generate_chord(R,G,B):
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
    chord_play=[]
    scales=[]    
    cmyk=rgb_to_cmyk(R,G,B)
    r=R/255
    g=G/255
    b=B/255
    H,L,S=colorsys.rgb_to_hls(r, g, b)
    H=H*255
    chord=[]
    rootvalue=int(H/21.25)
    #print (rootvalue)
    root=notes[rootvalue]
    chord.append(root)
    chordsteps.append(notes[rootvalue])
    chord_play.append(notes[rootvalue]+'2')
    notevalue=rootvalue
    #print (notevalue,root)
    counter=1
    octave=4
    for value in cmyk:
        try:
            interval=int(value/16.66)+3
        except:
            interval=3
        notevalue=notevalue+interval

        if notevalue>11:
            notevalue=notevalue-11
            octave=octave+1
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
