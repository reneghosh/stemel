# stemel

_polyphonic score player for FoxDot and Sonic Pi_

**NOTE**: stemel is very much a work in progress 
at the moment as the syntax and scope are changing.
I'm not yet sure what form it will take when I 
release it.

A music notation format inspired by 
step sequencers and 
[MML](https://en.wikipedia.org/wiki/Music_Macro_Language), to write music in a format that's both **human readable** and **code-exploitable**. Stemel makes it easy to write long sequences of melodies. Chords. Counterpoint.

## stemel in a nutshell

Stemel represents notes in the form a step
sequencer does.

Let's start with an example. This is a 
two-voice socre, with one voice inputting midi
note 0 twice, once with a two-step duration and 
once with a one-step duration. The other voice
is inputting midi note 7, then resting for 
two steps.

Here's what it looks like:
  
```
0 - 0 / 7 * * 
```

## User Guide

Stemel is a musical notation format inspired by 
step sequencers that supports polyphony.

The gist of it is this:

| operator | description |
| ----| ----|
| `(number)` | add note of midi pitch (number) |
| `-` | carry previous note's duration one step |
| `*` | rest for a step |
| `>` | shift next notes up an octave |
| `<` | shift next notes down an octave |
| `/` | start a new voice |

- whitespace is optional, except after a note
pitch (you have to be able to separate numbers)
- any operator can be repeated multiple times 

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
