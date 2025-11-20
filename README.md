# Overview

The Uno Synth Pro by IK Multimedia is an excellent monophonic (resp. paraphonic) synthesizer. I wished more musicians used it and more 3rd party soundsets were available. However it doesn't seem to be a wide spread synth.

## Highlights

- Three oscillators with waveshaping and various cross modulation features.
- Mixer saturation in case the oscillators are fed into the mixer at higher volumes.
- Two different dual filters with various modes and routings.
- Post filter drive circuit with dedicated control.
- Built in effects.
- Modulation matrix.
- Preset memory.
- Excellent Fatar keybed (for the keyboard version).
- And last, but of course most important: massive analogue sound.

## Drawbacks

There are a couple of drawbacks, e.g. [AudioPilz](https://www.youtube.com/@AudioPilz/videos) mentiones the

* [Software Manager](https://www.youtube.com/watch?v=-QLh7bmfHT4&t=317s) the user is forced to install in order to download further content, like firmware updates with bugfixes, the editor, or additional soundsets.
* [License transfer policy](https://www.youtube.com/watch?v=-QLh7bmfHT4&t=339s). In case someone sells the synth, moving the license to another user requires payment.
* ["impeccable customer support"](https://www.youtube.com/watch?v=-QLh7bmfHT4&start=347). Fortunately I never was in need of it.

There are a couple of further issues, e.g.

* The synth emits noise when connected via USB.
* Backups aren't possible without using the issuer's software.¹
* 1:1 restoration isn't possible since the editor resorts the presets alphanumerically, rendering program changes in your DAW useless.¹
* No support for OS other than macOS or Windows.¹
* Lack of SysEx documentation makes it almost impossible to integrate the synth with 3rd party software.¹
* Factory presets and [additional packs](https://www.ikmultimedia.com/unosounds/) mainly are useful for electronic genres, not showcasing the synth's potential for other genres.
* Knobs instead of encoders for the editing matrix, making sound design a rather challenging experience (several Waldorf synthesizers showcase that the matrix design concept with encoders works quite well).
* The power socket is mini and unsecured. Hope it won't break eventually.
* Micro USB port. Hope it won't break eventually.

## Verdict

In case one accepts the drawbacks, this synth is a great choice. And the price, especially 2nd hand, is unrivaled for what one gets.


# Preset addresses

The synth's memory is divided into two banks. Bank 1 is addressed as 0, bank 2 as 1. The presets in either bank are addressed as 0 through 127. The combination of both allows to address the presets 1-256.

## Preset data format as received from the synth

A preset as returned by the synth consists of 6 SysEx messages:

* One message of 43 bytes, mainly containing the preset's name (14 bytes, all  characters uppercase).

* One message of 305 bytes, probably the sound engine's data.

* Four (and in rare cases, less) messages of variable length, about 204 bytes long. Maybe the sequence data.

* The first can be requested by sending the following request to the synth:
  
  ```
  0xF0 0x00 0x21 0x1A 0x02 0x03 0x24 0x01 bank-Id preset-Id 0xF7
  ```

* The latter 5 can be requested by sending the following request 5 times, incrementing 'chunk-Id' from 0 to 4:
  
  ```
  0xF0 0x00 0x21 0x1A 0x02 0x03 0x29 bank-Id preset-Id chunk-Id 0xF7
  ```

For example, to request all 6 SysEx packages of preset 131, the following requests are necessary:

```
0xF0 0x00 0x21 0x1A 0x02 0x03 0x24 0x01 0x01 0x03 0xF7
0xF0 0x00 0x21 0x1A 0x02 0x03 0x29 0x01 0x03 0x00 0xF7
0xF0 0x00 0x21 0x1A 0x02 0x03 0x29 0x01 0x03 0x01 0xF7
0xF0 0x00 0x21 0x1A 0x02 0x03 0x29 0x01 0x03 0x02 0xF7
0xF0 0x00 0x21 0x1A 0x02 0x03 0x29 0x01 0x03 0x03 0xF7
0xF0 0x00 0x21 0x1A 0x02 0x03 0x29 0x01 0x03 0x04 0xF7
```

# Deltas receiving and sending a particular preset

When receiving a particular preset ("backup"), its data differs from the data that needs to be sent to the synth ("restore"). The following is preset number 250, a personal INIT preset. The first block is the data as received from the synth, the second is converted so it can be used for restoration.

The first message containing the name differs most. Instead of the 43 bytes as received from the synth, it's just 15 bytes long (at least in this case, it differs depending on the length of the preset's name).

* Byte 7 (value 24) is replaced by a value of 23.
* The predecessor byte (00) is dropped.
* All bytes after the preset's name are dropped, except for the terminating F7, of course:

```
                                 I  N  I  T
F0 00 21 1A 02 03 00 24 01 01 79 49 4E 49 54 00 20 20 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 F7
```

```
                                 I  N  I  T
F0 00 21 1A 02 03    23 01 01 79 49 4E 49 54                                                                                  F7
```

In the subsequent 5 messages

* Byte 7 (value of 29) always is replaced by a value of 28.
* The predecessor byte (00) is dropped.

This message is 305 bytes long when received from the synth. Besides the above modification, byte 10 (value 00) is replaced by a value of 20:

```
F0 00 21 1A 02 03 00 29 01 79 00 00 04 00 40 37 00 00 00 00 00 00 00 10 15 00 00 64 00 20 05 00 00 00 00 28 01 00 00 00 00 00 00 00 02 7C 0F 70 1F 00 00 14 00 00 00 00 00 19 00 64 00 00 00 00 00 00 00 00 00 7C 03 40 01 00 00 66 03 00 00 00 00 00 00 64 02 00 00 00 00 00 00 00 00 00 58 20 66 00 74 0B 70 2E 40 7B 03 10 00 0B 64 0C 40 3E 01 6E 05 38 3F 00 02 30 41 0C 0F 1F 00 01 58 20 46 42 0F 40 00 00 08 70 00 00 32 1E 3E 00 0A 70 60 00 00 64 00 60 73 71 03 50 00 07 00 10 73 71 03 10 00 07 06 00 50 0F 40 3E 0F 1F 00 05 38 30 00 00 32 00 70 79 78 01 08 00 00 01 48 75 20 26 40 66 00 17 48 01 60 03 00 0F 00 01 64 00 00 10 20 01 00 01 7E 7F 7F 00 00 00 00 00 0C 44 08 00 00 49 00 26 00 00 0A 50 02 00 01 11 02 00 20 22 20 0A 00 40 04 54 00 20 00 40 0D 00 00 00 60 01 00 43 0A 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 06 04 01 00 08 01 12 00 00 5D 78 00 00 40 0C 11 00 00 00 00 00 00 00 00 00 00 08 00 F7
```

```
F0 00 21 1A 02 03    28 01 79 20 00 04 00 40 37 00 00 00 00 00 00 00 10 15 00 00 64 00 20 05 00 00 00 00 28 01 00 00 00 00 00 00 00 02 7C 0F 70 1F 00 00 14 00 00 00 00 00 19 00 64 00 00 00 00 00 00 00 00 00 7C 03 40 01 00 00 66 03 00 00 00 00 00 00 64 02 00 00 00 00 00 00 00 00 00 58 20 66 00 74 0B 70 2E 40 7B 03 10 00 0B 64 0C 40 3E 01 6E 05 38 3F 00 02 30 41 0C 0F 1F 00 01 58 20 46 42 0F 40 00 00 08 70 00 00 32 1E 3E 00 0A 70 60 00 00 64 00 60 73 71 03 50 00 07 00 10 73 71 03 10 00 07 06 00 50 0F 40 3E 0F 1F 00 05 38 30 00 00 32 00 70 79 78 01 08 00 00 01 48 75 20 26 40 66 00 17 48 01 60 03 00 0F 00 01 64 00 00 10 20 01 00 01 7E 7F 7F 00 00 00 00 00 0C 44 08 00 00 49 00 26 00 00 0A 50 02 00 01 11 02 00 20 22 20 0A 00 40 04 54 00 20 00 40 0D 00 00 00 60 01 00 43 0A 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 06 04 01 00 08 01 12 00 00 5D 78 00 00 40 0C 11 00 00 00 00 00 00 00 00 00 00 08 00 F7
```

The following three messages are not altered except for the two modifications as described above. The length of those messages differ from preset to preset:

```
F0 00 21 1A 02 03 00 29 01 79 01 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 0F 00 00 00 00 00 00 00 00 00 01 00 00 F7
```

```
F0 00 21 1A 02 03    28 01 79 01 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 0F 00 00 00 00 00 00 00 00 00 01 00 00 F7
```

```
F0 00 21 1A 02 03 00 29 01 79 02 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 0F 00 00 00 00 00 00 00 00 00 F7
```

```
F0 00 21 1A 02 03    28 01 79 02 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 0F 00 00 00 00 00 00 00 00 00 F7
```

```
F0 00 21 1A 02 03 00 29 01 79 03 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 0F 00 00 00 00 00 00 00 00 00 F7
```

```
F0 00 21 1A 02 03    28 01 79 03 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 0F 00 00 00 00 00 00 00 00 00 F7
```

In the last message, additionally to the above modification, byte 10 (value 04) is replaced by value 44:

```
F0 00 21 1A 02 03 00 29 01 79 04 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 0F 00 00 00 00 00 00 00 00 00 F7
```

```
F0 00 21 1A 02 03    28 01 79 44 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 4F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7C 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 67 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 3F 7E 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 73 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 1F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 79 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 0F 00 00 00 00 00 00 00 00 00 F7
```

# Sending a particular preset

After the above modifications, a preset can be sent back to the synth. However, the following SysEx command of 10 bytes needs to be prepended:

```
F0 00 21 1A 02 03 11 01 0A F7
``

# Using Python

The editor communicates with the synth via traditional [MIDI Sytem exclusive messages](https://en.wikipedia.org/wiki/MIDI#SysEx) which can be used for backup and restore over USB or MIDI cables. To issue the SysEx requests required for backups via the request script in this repository, Mido and [RtMidi](https://github.com/thestk/rtmidi?tab=readme-ov-file) are required:

```
pip install mido python-rtmidi
```

The script can request one preset at a time, so you have to pass the preset number (1-256) to the script. The synth will answer by dumping the preset. Record this dump using the SysEx recording tool of your choice.

# Remarks

¹ Those issues are a addressed by the contents of this repository.
```
