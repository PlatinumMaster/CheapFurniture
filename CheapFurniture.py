#!/usr/bin/python3.8

import struct
import sys
import subprocess
import os
import pathlib

# CheapFurniture

# devkitARM setup
DEVKIT = pathlib.Path(os.environ.get('DEVKITARM'), 'bin')
AS = (DEVKIT / 'arm-none-eabi-as')
OBJCOPY = (DEVKIT / 'arm-none-eabi-objcopy')

def overworld_to_asm(overworld, output):
    overworld = pathlib.Path(overworld)
    output = pathlib.Path(output)
    
    with open(output, 'w') as out:
        out.write(".align 4\n")
        out.write(".include \"B2W2.s\"\n\n")
        out.write('.word Extra - 4\n\n')
        with overworld.open('rb') as ow:
            fileSize, nFurniture, nNPC, nWarps, nTriggers = struct.unpack("<LBBBB", ow.read(8))
            out.write('.byte %s     @ Furniture Count\n' % hex(nFurniture))
            out.write('.byte %s     @ NPC Count\n' % hex(nNPC))
            out.write('.byte %s     @ Warp Count\n' % hex(nWarps))
            out.write('.byte %s     @ Trigger Count\n\n' % hex(nTriggers))
            
            out.write("Furniture:\n")
            for x in range(0, nFurniture):
                out.write("  furniture {0[0]}, {0[1]}, {0[2]}, {0[3]}, {0[4]}, {0[5]}, {0[6]}\n".format(struct.unpack("<HHHHLLL", ow.read(0x14))))
            out.write('\n')
            
            out.write("NPCs:\n")
            for x in range(0, nNPC):
                out.write("  npc {0[0]}, {0[1]}, {0[2]}, {0[3]}, {0[4]}, {0[5]}, {0[6]}, {0[7]}, {0[8]}, {0[9]}, {0[10]}, {0[11]}, {0[12]}, {0[13]}, {0[14]}, {0[15]}, {0[16]}, {0[17]}\n".format(struct.unpack("<HHHHHHHHHHHHHHHHHH", ow.read(0x24))))
            out.write('\n')
            
            out.write("Warps:\n")
            for x in range(0, nWarps):
                out.write("  warp {0[0]}, {0[1]}, {0[2]}, {0[3]}, {0[4]}, {0[5]}, {0[6]}, {0[7]}, {0[8]}\n".format(struct.unpack("<HHBBLLHHH", ow.read(0x14))))
            out.write('\n')
            
            out.write("Triggers:\n")
            for x in range(0, nTriggers):
                out.write("  trigger {0[0]}, {0[1]}, {0[2]}, {0[3]}, {0[4]}, {0[5]}, {0[6]}, {0[7]}, {0[8]}, {0[9]}, {0[10]}\n".format(struct.unpack("<HHHHHHHHHHH", ow.read(0x16))))
            out.write('\n')
            
            out.write("Extra:\n")
            while True:
                try:
                    out.write("  extra {0[0]}, {0[1]}\n".format(struct.unpack("<HL", ow.read(0x6))))
                except struct.error:
                    break
            out.write('\n')
    return

def asm_to_overworld(file, output):
    path = pathlib.Path(file)
    output = pathlib.Path(output)
    subprocess.run([AS.as_posix(), '-mthumb', '-c', path, '-o', (output.parent / (output.stem + '.o'))])
    subprocess.run([OBJCOPY.as_posix(), '-O', 'binary', (output.parent / (output.stem + '.o')), (output.parent / (output.stem + '.bin'))])
    (output.parent / (output.stem + '.o')).unlink()

def main():
    if sys.argv[1].lower() == 'dump':
        overworld_to_asm(sys.argv[2], sys.argv[3])
    elif sys.argv[1].lower() == 'make':
        asm_to_overworld(sys.argv[2], sys.argv[3])
    else:
        print('Trouble')
    return

main()
