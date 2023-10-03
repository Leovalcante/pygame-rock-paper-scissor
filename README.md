# Pygame - Rock, paper, scissor

Code from [Python Online Multiplayer Game Development Tutorial](https://youtu.be/McoDjOCb2Zo)

I made a few additions:

- Secure Socket connection using TLS ([Read this before running the code](./ssl/README.md))
- Safer pickle deserialization (this scares the shit out of me in any case)
- Clearer code (thus the client can still be improved a lot)
- TODO: Fix frontrunning: If client B picks before client A, client A knows what to play to win as the server sends the current state of the Game, which held the users' moves, to both players
