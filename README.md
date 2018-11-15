# SteMeL

**NOTE**: SteMeL is very much a work in progress at the moment as the syntax and scope are changing. I'm not
yet sure what form it will take when I release it and this repository might even contain nothing but the spec, should
there we different implementations.

A music notation format inspired by step sequencers and [MML](https://en.wikipedia.org/wiki/Music_Macro_Language).

Write music in a format both **human readable** and **code-exploitable**.

SteMeL makes it easy to write long sequences of melodies. You can write chords. You can counterpoint.
teMeL User Guide

SteMel is a musical notation format inspired by step sequencers that supports polyphony and encourages code reeuse.

## Directives, Commands, Variables

A SteMeL flow is made of constructs separated by spaces. 

SteMeL constructs are either  **directives**,. **commands** or  **variables**.

**Directives** Do not produce sound, but instead inform commands. For instance, the frequency directive `f50` informs the interpreter that all subsequent notes will be expressed in a number of half-tones relative to midi note `50`. the `,` directive tells the interpreter to move forward one time segment.

**Commands** produce sound. A command starts with a number  representing a note's pitch. This number represents a number of half-tones above a base frequency. Notes are generally integer (whole) numbers, but they don't _have_ to be: to produce a pitch that's slightly off-key, a note can be expressed as a frequency with decimals after the 0. For instance, `10` or `10.1` are both valid commands.

  **Variables** are used to store series of notes for later reuse, to promote terser code and make it easier to modify them in one place while propagating them across the entire score. To store a variable, a series of notes are encloded in parentheses `(` `)` and given a variable name. They are used by referering to them by a `$` reference.

  ## Directives

Directives are expressed by a letter followed by a number.
   
| Directive | Meaning | Example |
| ----------- | ---------- | ------------|
| `f` or  `F`   | Change base pitch of current line | `f50` |
| `a` or `A`.  | Change amplification factor for note volume increments/decrements | `a1.1`. |
| `l` or `L`.   | Change base note length. Note that the note length will be 1/l, so a higher value indicates a shorter note length | `l4` (quarter-note), `l0.25` (full note) |
| `,` or. `;` | Move interpreter forward one time segment. Without this, all notes will be played simultaneously! | `,` (move forward one segment), `,4` (move forward 4 segments) | 

## Commands

A command is a note pitch. A command is expressed by a number representing the pitch, followed by a series of optional modifiers for length and volume

### Command modifiers

| Modifier |Meaning | Example |
|----------- |-----------| ----------- |
| `_` | Note length | `0_4`
| `>` | Increase amplitude by one increment | `0>` (one increment), `0>4` (four increments) |
| `<` | Decrease amplitude by one increment | `0<` (one increment), `0<4` (four increments) |

## Bars and loops



## Variables

Variables are stored series of notes that can be resused. A variable is defined by enclosing a series of notes in parentheses and then giving the variable a name by prefixing it with a colon `:`. The variable can then be used in following constructs by expressing the variable name prefixed with `$`.

Example: ` ( 0 , 4 , 5 ) :pattern1 $pattern1 $pattern1`
