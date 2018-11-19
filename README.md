# Connect4AI
Backend to a Connect4 AI computer player which looks 6 moves ahead

##Background: 
The AI player uses a classical artificial intellgence approach, evaluating all outcomes 6 moves ahead with a heuristic function.
Heuristic function is the number of possible 4 in a rows for player minus the possible 4 in a rows for opponent. 
A possible 4 in a row is defined as a 4 in a row with one blank (i.e. X X _ X or X X X _)
The AI player chooses one of the moves that the heuristic function has determined to be the best move.

Without alpha-beta pruning, computer player could look 4 moves ahead and play next move almost instantly on a 7 x 6 board. 
With alpha-beta pruning, computer player could look 6 moves ahead and play almost instantly.
