#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime


def createOutputFilename(filename, presetName):
    baseFilename, extension = os.path.splitext(filename)
    baseFilename = baseFilename + " - " + presetName + " converted for Synth - " + datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    return baseFilename

def modifyPresetNameMessage(message):
    presetName = message[11:25].decode('ascii')
    presetName = presetName.replace('\x00', '')
    presetName = presetName.rstrip()
    message = message[:11]
    message[7] = 0x23
    message.pop(6)
    message.extend(presetName.encode('ascii'))
    message.append(0xF7)
    return message, presetName

def main():
    if not (len(sys.argv) == 2):
    	print("This app converts a SysEx file containing a single preset\nas emitted by the Uno Synth Pro (backup) so it can be\nsent back to the synth (Restore).\nWARNING: Sequencer data won't be included.\nUsage: %s UnoSynthProBackup.syx" % (sys.argv[0]))
    	sys.exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename) and os.access(filename, os.R_OK):
        print("Cannot access file.")
        sys.exit(1)

    with open(filename, mode='rb') as file:
        fileContent = bytearray(file.read())

    if len(fileContent) < 1100:
        print("The file is rather small for preset data of the synth.")
        sys.exit(1)

    if fileContent[0] != 240 or fileContent[len(fileContent)-1] != 247:
        print("Please provide a SysEx file. This appearently is none.")
        sys.exit(1)

    if not fileContent[1] == 0x00 and fileContent[2] == 0x21 and fileContent[3] == 0x1A and fileContent[4] == 0x02 and fileContent[5] == 0x03:
        print("This appearently is no data of the Uno Synth Pro.")
        sys.exit(1)

    SYSEX_BEGIN = bytes([0xF0])
    messages = [ SYSEX_BEGIN + part for part in fileContent.split(SYSEX_BEGIN)[1:] ]
    if len(messages) != 6:
        print("Expected 6 SysEx packages, but found", len(messages))
        sys.exit(1)

    for i, message in enumerate(messages):
        message = bytearray(message)
        print(i)
        if i == 0 and len(message) != 43:
            print("Expected first SysEx package to be 43 bytes long, but found", len(message))
            sys.exit(1)
        elif i == 0 and len(message) == 43:
            print("Modifying name")
            message, presetName = modifyPresetNameMessage(message)
            messages[i] = message
            continue

        if not i == 1 and len(message) == 305 and message[6] != 0x00 and message[7] != 0x29:
            print("Expected second SysEx package to contain patch data, but it doesn't")
            sys.exit(1)
        else:
            message[7] = 0x28
            message.pop(6)
            print("One byte altered, one removed")

        if message[9] != 0x00:
            print("Expected null byte in package", i)
            sys.exit(1)
        else:
            message[9] = 0x20
            print("0x00 replaced by 0x20")
            messages[i] = message
            messages = messages[:2]
            break

    SysExCommand = bytearray.fromhex("F0 00 21 1A 02 03 11 01 0A F7")
    messages.insert(0, SysExCommand)

    filename = createOutputFilename(filename, presetName)

    # ToDo: Some basic checks
    with open(filename+".syx", "wb") as file:
        for currentArray in messages:
            file.write(currentArray)


if __name__ == "__main__":
    main()


