# Tiny Chess Engine in 4 KB of Python

A deterministic chess engine in a single `main.py` of 4,049 bytes (limit: 4,096), written for the make.fun bounty "Build the strongest chess engine in 4 KB of Python" (tiny-chess-01).

## How it plays

- Full legal move generation on a 64-square board: pawn pushes and captures, promotions to queen, castling both sides with rights tracking, and king-safety filtering of every pseudo-legal move.
- Negamax search with alpha-beta pruning and iterative deepening (depths 1-4) under a fixed budget of 12,000 nodes per move — never a clock, so replays are identical.
- Quiescence search over captures and promotions at the leaves.
- Evaluation: material (100/320/330/500/900) plus a pawn-advancement and centrality terms for knights, bishops, rooks, queens and the king.
- Move ordering by MVV-LVA with a promotion bonus.

## Interface

`main.py` is the whole engine (Python 3.13, standard library only). It talks to the trial env at `MAKEFUN_ENV_URL`: it asks for the game in play with `POST /game` and answers with `POST /move` until the env reports the trial is done.
