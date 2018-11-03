# SteMeL

A music notation format inspired by step sequencers and [MML](https://en.wikipedia.org/wiki/Music_Macro_Language).

Write music in a format both **human readable** and **code-exploitable**.

SteMeL makes it easy to write long sequences of melodies. You can write chords. You can counterpoint.

## Syntax

| what you write | what it means |
| ---------------| ------------- |
| `<n>`            | play note n   |
| `<n>_`           | play note n over two steps |
| `<n>_<m>`        | play note n over m steps |
| `<n>/<o>`        | play notes n and o at the same time |
| `,`              | move to next step |
| `f50`            | play subsequent notes relative to midi note 50 |
| `l<n>`           | make each step of 1/<n> note length, where n is 1 for full notes, 2 for half notes, 0.25, etc.|
| `>`              | increase volume of current note by one increment |
| `>>`             | increase volume of current note by two increments |
| `a1.1`           | amplitude change increment: change subsequent note amplitudes by multiplying/dividing by factor 1.1 |
| `>n`             | increase volume of current note by n increments |
| `<`              | decrease volume of current note by one increment |
| `<<`              | decrease volume of current note by two increments |     
| `<n`              | decrease volume of current note by n increments |

## SteMeL by example

| SteMeL | Explanation |
| -------| ------------|
| `f50 l2 0,,0,,` | play midi note 50 twice in half-notes with a half-note rest between each note |
| `0/4` | play a chord with notes 0 and 4 |
| `0_4/7,,,` | play a chord with notes 0 and 7, with note 0 sounding for 4 beats and note 7 sounding only one beat |
| `0>5,7<5` | play note 0 very loud (5 increments of volume), then note 5 softly (5 decrements of volume) |
| `0>>>>>,7<<<<<` | same as above |
