# SteMeL

A music notation format inspired by step sequencers and [MML](https://en.wikipedia.org/wiki/Music_Macro_Language).

Its purpose is to store a musical score in format that's both human readable and usable in code.

SteMeL makes it easy to write long sequences of melodies, chords, and counterpoint.

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

```
|0|-|0|-|0|-|0|-|0|-|0|-|0|-|0|-|
```

You'd write: `0,,0,,0,,0,,0,,0,,0,,0,`. This means, _play note 0, then move to the next step, then play nothing,
then move to the next step and play 0 again, etc._
