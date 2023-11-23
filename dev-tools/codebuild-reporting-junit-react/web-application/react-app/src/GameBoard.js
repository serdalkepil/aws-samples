import React from 'react';
import './GameBoard.css';

class GameBoard extends React.Component {
    
    //default state for a fresh game
    freshState = {
      square: [0,1,2],
      board: new Array(9),
      xMoves: [],
      oMoves: [],
      player: 'X',
      winner: null
    };

    //array with all possible winning combinations
    wins = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6]
    ];

    constructor(props){
      //initialize, set the starting state to a fresh game and initialize 
      //button clicks in state
      super(props);
      this.state = JSON.parse(JSON.stringify(this.freshState));
      this.playSquare = this.playSquare.bind(this);
    }
    
    resetGame(e) {
      //prevent default click behaviour and reset state to a fresh game
      e.preventDefault();
      this.setState(JSON.parse(JSON.stringify(this.freshState)));
    }
    
    checkForWin() {
      //This function checks to see if any player has a winning combination
      // make sure that a enough turns have been played to win
      if (this.state.xMoves.length + this.state.oMoves < 5) {return false};
      //build array of players to check
      const players = [
        {name: 'X', moves: this.state.xMoves},
        {name: 'O', moves: this.state.oMoves}
      ];
      //loop through players
      for(let player of players){
        //loop through all winning combinations
        for (let line of this.wins) {
          let currMoves = player.moves
          //check if all moves for each winning combination if present
          if (currMoves.includes(line[0]) && currMoves.includes(line[1]) && currMoves.includes(line[2])){
            //set the winner in state if a winning combination is found and exit
            this.setState({winner: player.name + " is the Winner!"});
            return true;
          }
        }
      }
      return false;
    }

    gameOver() {
      // see if 9 moves have been made without a winner
      if (!this.state.winner && this.state.xMoves.length + this.state.oMoves.length == 9) {
        this.setState({winner: "It's a Draw!"});
        return true;
      } else {
        return false;
      }
    }
    
    playSquare(loc, e) {
      //prevent default html button action
      e.preventDefault();
      //confirm that the board location is still playable
      if (this.state.board[loc] || this.state.winner) {
        return;
      }
      //get the current play and existing moves from state and
      //load them into working variables
      let player = this.state.player
      let moves = this.state[player.toLowerCase() + 'Moves'];
      let board = this.state.board;
      //add the move to working variables 
      moves.push(loc);
      board[loc] = player;
      //set the the move to state and change
      //the active player
      this.setState({
        [player.toLowerCase() + 'Moves']: moves,
        player: (player == 'X') ? 'O' : 'X',
        board: board
      });
      //check if that move won or ended the game
      if(!this.checkForWin()){
        this.gameOver();
      }
    }
    
    render()
    {
      //build the board with 9 squares by looping through the array for rows and columns
      let board = this.state.square.map(x => {
        return(
          <div key={x} className="boardRow">
            {
              this.state.square.map(y => {
                const loc = (x * 3) + y;
                return(
                  //create a button for each square, bind it to the playSquare function
                  //and show the move that is in the board array of state
                  <button onClick={this.playSquare.bind(this,loc)} key={loc} aria-label={loc} id={loc} className="boardSquare">
                    {(this.state.board[loc]) ? this.state.board[loc] : "-"}
                  </button>
                );
              })
            }
          </div>
        );
      });
      
      return (
        <div>
          {(this.state.winner) ? (
            <h2 id="status" className="result">{this.state.winner}</h2>
          ):(
            <h2 id="status" className="result">{this.state.player}'s Turn...</h2>
          )}
          {board}
          <button id="reset" className="resetButton" onClick={this.resetGame.bind(this)}>Start a new game</button>
        </div>  
      );
    }
}
export default GameBoard;