# stemel

_step sequencer expression language_

stemel is a music notation format inspired by
step sequencers and
[MML](https://en.wikipedia.org/wiki/Music_Macro_Language),
to write music in a format that's both **human readable**
and **code-exploitable**.
stemel makes it easy to write long sequences of melodies, with a simple syntax to
support polyphony.

## Supported platforms

At the moment, stemel has a helper class to support integration with FoxDot.
More helpers are planned in the future.

## stemel in a nutshell

stemel represents notes in the same way a step
sequencer does.

Let's start with an example. This is a
two-voice score, with one voice inputting midi
note 0 twice, once with a two-step duration and
once with a one-step duration. The other voice
is inputting midi note 7, then resting for
two steps.

Here's what it looks like:

```
0 - 0 / 7 * *
```
On a step sequencer, this example would look like this:

```
|x| | |x| | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| x |x| x |x|
```
what stemel does is generate data structures to represent
a pattern's pitches, sustains and durations. This example
would generate the following structures:

```
  pitches: [[0.0, 7.0], [-1, -1], [0.0, -1]],
  durations: [[1, 1], [{'rest': 1}, {'rest': 1}], [1, {'rest': 1}]],
  sustains: [[2, 1], [1, 1], [1, 1]]
```

## Usage in FoxDot

To use it in FoxDot code, import stemel within the current script.
```
from stemel import *
```

There are two way of using stemel patterns in FoxDot:

1. Create patterns through the `S|` builder and send them to a FoxDot player through the
`smlp` function, providing the instrument to use, the pattern and the step size to fit the pattern to the desired tempo:

```
Scale.default = "chromatic"
Clock.bpm = 100

bass_pattern = S|"> (0 0 0-) :1 :1 < 5 5 7 10 | amp 1.9 1.5 | lpf 120 720 120 250"
b1 >> smlp(bass, bass_pattern, step=0.5, formant=4)
```

2. Send the pattern directly as a string to the `smls` function. This saves the step of building the pattern, but precludes using the pattern's modification functions such as shifting the pitch or concatenating
patterns together. As with `smlp`, the function is called with the instrument to use, the pattern and the step size to fit the pattern to the desired tempo:
```
Scale.default = "chromatic"
Clock.bpm = 100

bass_pattern = ">(0 0 0-) :1 :1 < 5 5 7 10 | amp 1.9 1.5 | lpf 120 720 120 250"
b1 >> smls(bass, bass_pattern, step=0.5, formant=4)
```
Notice that the `smlp` and `smls` functions accept all arguments that you normally
provide to a FoxDot player. Additionally, these arguments can be embedded in the
stemel pattern through filters.

## Building a modifying patterns

stemel Patterns are built by sending a string representing the pattern, either to the `Stemel()` class constructor or the `S|` operator.
```
from stemel import *

# these two methods of building a pattern are equivalent:
pattern = Stemel("0 0 5")
pattern = S|"0 0 5"
```
Patterns can be modified by the `Stemel` class methods. Any modification to a stemel
pattern gives rise to a new pattern. Certain methods have operator shorthand versions.


| method | description | example (with pattern = S\|"0-0/7")|
|--------|-------------|--------------------|
| shift  | shift pattern pitch | `pattern.shift(2)`|
| >>     | shift pattern pitch | `pattern >> 2`|
| <<     | negative shift pattern pitch | `pattern << 2` |







## Language Guide

### Basic operators
stemel describes a musical pattern with pitches and operators
that inform a note's duration and sustain.

The basic operators are:

| operator | description |
| -------- | ----------- |
| `(number)` | add note of midi pitch (number) |
| `-` | carry previous note's duration one step |
| `*` | rest for a step |
| `>` | shift next notes up an octave |
| `<` | shift next notes down an octave |
| `/` | start a new voice |

- whitespace is optional, except after a note
pitch, because pitch is expressed as a number
- any operator can be repeated multiple times

### Grouping
Patterns can be grouped into variables and used as a reference
further down the pattern. This allows for a more succinct
expression of the overall pattern when one ore more patterns
are repeated verbatim.

To create a group, enclose it in round brackets `()`. The order
of grouping determines the variable's reference number and can
be used by prefixing the reference with the `:` operator.

For example, the following two stemel patterns are equivalent,
the second one using groups to express the first one more succinctly:

```
0 0 5  0 0 5  0 0 5  7 7 12  7 7 12  7 7 12

(0 0 5) :1 :1 (7 7 12) :2 :2
```

Groups can contain other groups. This allows for making
super-patterns that deference in cascade. For instance, the
following two expressions are equivalent:

```
0 7 0 7 0 8 0 7 0 7 0 8

((0 7) :1 0 8) :2
```

### Filters

Filters allow for adding patterns that qualify the musical
pattern. A filter is added to a pattern by apposing an `|` operator,
then the filter name, then a new pattern. Filters are information
to be used by the player that will eventually execute the pattern.

For example, adding amplitude information to a music pattern
might be written as follows:

```
0 0 7 | amp 0.8 0.3 0.3
```
When the player encounters the pattern and receives the additional
information provided by the amplitude filter, it might choose to
affect each note played by the given amplitude.

## A note on polyphonic pattern repetition

When a pattern comprises multiple voices, certain voices
might contain more steps than others. stemel will repeat
a voice within the current pattern buffer to compensate,
effectively looping it.

For instance, the following two patterns are equivalent:
```
7 7 5 7 5 7 4 4/0 0 0 0 0 0 0 0

7 7 5 7 5 7 4 4/0
```
