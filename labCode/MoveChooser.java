import java.util.ArrayList;  


public class MoveChooser {


    public static int evaluateValue(BoardState board) {
    // The static function was used to evaluate the value of each square on the whole game board.

        int[][] valuesArray = {
                {120,-20,20,5,5,20,-20,120},
                {-20,-40,-5,-5,-5,-5,-40,-20},
                {20,-5,15,3,3,15,-5,20},
                {5,-5,3,3,3,3,-5,5},
                {5,-5,3,3,3,3,-5,5},
                {20,-5,15,3,3,15,-5,20},
                {-20,-40,-5,-5,-5,-5,-40,-20},
                {120,-20,20,5,5,20,-20,120}
        };
        // The above array of values was taken from a textbook by Peter Norvig.

        int whiteWeight = 0;
        // According to the lab instruction, the weight was always counted from the view of white.

        for(int i= 0; i< 8; i++)
            for(int j= 0; j < 8; j++) {
                if(board.getContents(i,j)==1) {
                    whiteWeight+=valuesArray[i][j];  // white piece
                }
                else if(board.getContents(i,j)==-1) {
                    whiteWeight-=valuesArray[i][j];  // black piece
                }
            }
        return whiteWeight;
        // The value of all white points was counted and the current score was derived through subtracting all black points.
    }


    public static int alpha_beta(boolean MaxOrMin, BoardState board, int searchDepth, int alpha, int beta) {
    // The core algorithm was designed here and the first boolean paramete was called to consider the layer, 
    // which was asking for the maximum or minimum layer. 

        ArrayList<Move> moves= board.getLegalMoves();
        // All the legal move could be checked by getLegalMoves() at the current situation.

        if(moves.size()==0 || searchDepth==0) return evaluateValue(board);
        // The static score would be returned if checked one was the Terminal Node.

        if(MaxOrMin) {
        // The maximum layer.
        // This situation was that a maximum value should be caught copying many game board duplicates, through alpha-beta pruning.

            for (Move move : moves) {
                BoardState temp = board.deepCopy();
                temp.makeLegalMove(move.x, move.y);
                alpha = Math.max(alpha, alpha_beta(false, temp, searchDepth - 1, alpha, beta));
                // According to lecture materials, the most classic part of the algorithm was designed here, 
                // which was supported by a series of BF-recursive searches.
                
                if (alpha > beta) break; // PRUN!!!
                // The node would be terminated when alpha > beta, which meant a better value would never be caught in this situation.
            }
            return alpha;
        }

        else {
        // The minimum layer was just a reverse of the maximum situation.
            for (Move move : moves) {
                BoardState temp = board.deepCopy();
                temp.makeLegalMove(move.x, move.y);
                beta = Math.min(beta, alpha_beta(true, temp, searchDepth - 1, alpha, beta));
                if (alpha > beta) break;  // PRUN!!!
            }
            return beta;
        }
    }
  

    public static Move chooseMove(BoardState boardState) {
        int searchDepth= Othello.searchDepth;
        ArrayList<Move> moves= boardState.getLegalMoves();
        if(moves.isEmpty()){
            return null;
        } // default null

        boolean MaxOrMin = true;  // true -> max, false -> min.
        Move max_move = moves.get(0);  // default one
        int current_value = 0;  
        int max_value = Integer.MIN_VALUE; 

        // The most valuable move would be found by traversing the whole MOVE arraylist.
        for (Move move : moves) {
            BoardState temp = boardState.deepCopy();
            temp.makeLegalMove(move.x, move.y);
            current_value = alpha_beta(true, temp, searchDepth, Integer.MIN_VALUE, Integer.MAX_VALUE);
            // The Integer.MIN_VALUE and Integer.MAX_VALUE were used to represented the negative infinity and positive infinity。

            if(current_value >= max_value) {
                max_value = current_value;
                max_move = move;
            }
        }
        return max_move;
    }


}
