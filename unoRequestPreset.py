#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import mido

name_outport = "UNO Synth Pro"
outport = mido.open_output(name_outport)

def delay():
    time.sleep(0.1)


def isValidPresetNumber(argument):
    if argument.isdigit():
        presetNumber = int(argument)
        if presetNumber >=1 and presetNumber <=256:
            return True, presetNumber
    else:
        return False, 0

def presetIds(presetNum):
    bankId = 0
    presetId = presetNum -1

    if presetId > 127:
        bankId = 1
        presetId = presetId -128

    return bankId, presetId

def requestPreset(presetNumber):
    bankId, presetId = presetIds(presetNumber)

    # Request preset header data, including its name. The synth replies with 1 package of 43 bytes.
    print("Use a SysEx tool to record the data emitted by the synth.")
    print("Requesting data of preset", presetNumber, "(bank-id", bankId, "preset-id", presetId, ")\n")
    sysexData = [0xF0, 0x00, 0x21, 0x1A, 0x02, 0x03, 0x24, 0x01, bankId, presetId, 0xF7]
    message = mido.Message('sysex', data = sysexData[1:-1])
    outport.send(message)

    # Request patch data in 5 chunks, First one is 305 bytes, the others are of variable length, about 204 bytes.
    # Remark: A few patches even consist of less than 5 bytes
    for chunkId in range(0,5):
        delay()
        sysexData = [0xF0, 0x00, 0x21, 0x1A, 0x02, 0x03, 0x29, bankId, presetId, chunkId, 0xF7]
        message = mido.Message('sysex', data = sysexData[1:-1])
        outport.send(message)


def main():
    if (len(sys.argv) != 2):
        print("Please pass the preset number (1-256) to request.")
        sys.exit(0)

    if (len(sys.argv) == 2):
        argument = sys.argv[1]
        success, presetNumber = isValidPresetNumber(argument)
        
        if not success:
            print("Please pass the preset number (1-256) to request.")
        
        else:
            requestPreset(presetNumber)

    elif (len(sys.argv) == 3):
        success1, presetNumber1 = isValidPresetNumber(sys.argv[1])
        success2, presetNumber2 = isValidPresetNumber(sys.argv[2])
        if not success1 and success2:
            print("Detected invalid preset number.\n")
            emitUsageHints()
            sys.exit(1)
        elif not presetNumber1 < presetNumber2:
            print("Please first pass the lower, then the higher preset number.")
            sys.exit(1)
        else:
            requestPresets(presetNumber1, presetNumber2)

    elif (len(sys.argv) > 3):
        emitUsageHints()
        sys.exit(1)


if __name__ == "__main__":
    main()
