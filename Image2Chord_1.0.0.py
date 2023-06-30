"""Image to Chord 1.0.0 - Convert images to chords.
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
import sys
import tkinter as tk
import tkinter.ttk as ttk

notes=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
rgb_scale = 255
cmyk_scale = 100
steps=[[0, 1, 3, 4, 6, 8, 10, 0], [0, 1, 3, 5, 6, 8, 10, 0], [0, 1, 3, 5, 7, 8, 10, 0], [0, 1, 3, 5, 7, 9, 10, 0], [0, 2, 3, 5, 6, 8, 10, 0], [0, 2, 3, 5, 7, 8, 10, 0], [0, 2, 3, 5, 7, 9, 10, 0], [0, 2, 3, 5, 7, 9, 11, 0], [0, 2, 4, 5, 7, 8, 10, 0], [0, 2, 4, 5, 7, 9, 10, 0], [0, 2, 4, 5, 7, 9, 11, 0], [0, 2, 4, 6, 7, 9, 10, 0], [0, 2, 4, 6, 7, 9, 11, 0], [0, 2, 4, 6, 8, 9, 11, 0]]
stepsitem=[]
stepscale=[]
stepscales=[]
stepstransposed=[]
scale=[]
scales=[]
chordsteps=[]

def convert_image():
    global color
    imgfilename=str(sys.argv[1])
    imgfile=Image.open(imgfilename)
    im2=imgfile.resize((1,1),Image.Resampling.BICUBIC)
    #img2=im2.convert("P", palette=Image.Palette.ADAPTIVE, dither=Image.Dither.FLOYDSTEINBERG, colors=256)
    px = im2.load()
    color=px[0,0]
    print ("R:",color[0],"\nG:",color[1],"\nB:",color[2])
    GenerateChord(color[0],color[1],color[2])
    

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

def GenerateChord(R,G,B):
    global chord
    global rootvalue
    global chordsteps
    cmyk=rgb_to_cmyk(R,G,B)
    chord=[]
    rootvalue=int(((R+G+B)/3)/21.25)
    root=notes[rootvalue]
    chord.append(root)
    chordsteps.append(rootvalue)
    notevalue=rootvalue
    #print (notevalue,root)
        
    for value in cmyk:
        try:
            interval=int(value/16.66)+3
        except:
            interval=3
        notevalue=notevalue+interval
        if notevalue>11:
            notevalue=notevalue-11
        chord.append(notes[notevalue])
        chordsteps.append(notevalue)
    chorddisplay=''
    for item in chord:
        chorddisplay= chorddisplay+item+" "
    print ("\n"+"Chord: "+chorddisplay+"\n")

    #return chord

def guess_scale(chord):
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
    chordlen=len(chord)
    stepslen=len(steps)
    for n in range (0, stepslen):
        scalelen=len(steps[n])
        for m in range (0,scalelen):
            transpose=steps[n][m]+rootvalue
            if transpose>11:
                transpose=transpose-12
            stepsitem.append(transpose)
            transpose=0
        stepstransposed.append(stepsitem)
        stepsitem=[]
    #print (stepstransposed)
    for n in range (0, stepslen):
        scalelen=len(steps[n])
        for m in range (0,scalelen):
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
    print ("Scales:")
    guess=1
    for item in scales:
        for note in item:
            scalestring=scalestring+note+" "
        print ("Match",str(guess)+": ",scalestring)
        guess=guess+1
        scalestring=''
    guess=0
    print ("\n")

#main
def main():
    convert_image()
    guess_scale(chord)
    e=input("press Enter to close")
main()
