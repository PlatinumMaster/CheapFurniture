# CheapFurniture - DS Generation Event Editing Made Easy!
Allows for furniture, warp, trigger, and NPC editing in Pokémon Black 2 and White 2.

***Very experimental. While most of the struct is figured out, the warps are the one thing which are not certainly finished. You have been warned.***

### Instructions for usage:
* Extract the overworld NARC `a/1/2/6`.
* Feed the script one of the files: 

`python CheapFurniture.py dump <file from a126> <output>`

* Make your changes.
* Recompile (Make sure you have the b2w2.s in the same directory): 

`python CheapFurniture.py make <decompiled event file> <output>`

* Reinsert to NARC, reinsert NARC into ROM.
* Profit!

### Credits
* [KazoWAR](https://twitter.com/KazoWAR) and [Kaphotics](https://github.com/kwsch) for their research thus far.
