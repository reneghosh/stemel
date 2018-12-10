# stemeL

_polyphonic score player for FoxDot and Sonic Pi_

**NOTE**: stemel is very much a work in progress 
at the moment as the syntax and scope are changing.
I'm not yet sure what form it will take when I 
release it.

A music notation format inspired by 
step sequencers and 
[MML](https://en.wikipedia.org/wiki/Music_Macro_Language), to write music in a format that's both **human readable** and **code-exploitable**. Stemel makes it easy to write long sequences of melodies. Chords. Counterpoint.

## stemel in a nutshell

```
0 - 0 / 7 * * 
```

## User Guide

Stemel is a musical notation format inspired by 
step sequencers that supports polyphony.

The gist of it is this:

- write a series of notes as midi numbers
- a '-' character extends the length of the 
previously entered note b one step
- a '/' character is to start a new voice (track).
- rests are represented by a '*' character.
- a '>' character sends the base range up an octave (all sucessive notes 
will be higher pitched by one octave)
- a '<' characters sends the base range down one octave
- Any character can be repeated any number of times ('>>' to go 
up two octaves, '<<' to go down two octaves, '**' for two rests, 
'---' to carry the preceding note to spawn four sequence steps)

## Roadmap

- Add filters to support array operations on lists
of notes such as randomization, extension, concatenation
- Add grouping, variables, references

## Supported platforms

Stemel has two implementations in python in ruby.
It has helpers to use it on FoxDot (python version)
and Sonic Pi (ruby version).

## Stemel in Python

TO DO

## Stemel in Ruby

TO DO
.
