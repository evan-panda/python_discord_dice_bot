# Description
This is a dicord bot designed to aid in the playing of TTRPGs directly from discord.

# Setup
Open the [bot invite link](https://discord.com/api/oauth2/authorize?client_id=1015631326424072232&permissions=2112&scope=bot%20applications.commands) in your browswer or discord and invite to the server you want it to join.

Set up permissions on your channels so bot can view the channel(s) you want to use it in.

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
