# Description
This is a dicord bot designed to aid in the playing of TTRPGs directly from discord.

# Commands

## General

`/hello [name]` - says hello to user

| arguments | example values | optional |
| - | - | - |
| name | bob<br>john | true |

`/ping` - **Admin only**. Prints latentcy in ms

## Dice

`/20` - generates a random number between 1 and 20 (inclusive), as if you were rolling a 20-sided die

`/r roll roll_type` - rolls dice from the formula provided by the user

| arguments | example values | optional |
| - | - | - |
| roll | 2d6<br>1d20+3+1d4 | false |
| roll_type | `select from list` | false |

## Cards

`/draw-card` - simulates drawing a random card from a standard deck (exluding Jokers)

## Random Generators

`/bdgen` - allows you to choose a generator for a random result to use in your *Blades in the Dark* game

> **Note**: This command has the `whisper` option, so the results only show up for the one generating it if set to `True` (*default behavior*)

| arguments | example values | optional |
| - | - | - |
| generator | `select from list` | false |
| whisper | `True` or `False` | true |

## Owner Only
<details>
<summary>These commands are owner-only.</summary>

`.sync` - syncs commands globally

`.sync ~` - syncs commands to current guild (server)

`.sync ^` - clears commands from current guild and syncs
</details>