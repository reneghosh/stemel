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
| `f50`            | play notes relative to midi note 50 |
| `a1.1`           | change amplitudes by multiplying/dividing by factor 1.1 |
| `l<n>`           | play 1/<n> notes, where n is 1 for full notes, 2 for half notes, 0.25, etc.|
| `l1`             | play full notes |
| `>`              | increase volume of current note |
| `>>`             | increase volume of current note twice |
| `>n`             | increase vomume of current note n times |
| `<`              | decrease volume of current note |

## SteMeL by example

| SteMeL | Sequencer | Explanation |
| -------| ----------| ------------|
| `0,,0,,0,,0,,0,,0,,0,,0,` | ```
| 0 | | 0 | | 0 | | 0 | | 0 | | 0 | | 0 | | 0 | 
```| play note 0, then move to the next step, then play nothing, then move to the next step and play 0 again, etc. |
