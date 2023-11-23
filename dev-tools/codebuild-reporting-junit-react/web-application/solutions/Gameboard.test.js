import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import GameBoard from './GameBoard';

const allSquares = [0, 1, 2, 3, 4, 5, 6, 7, 8]

describe('Challenge.test.js', () => {
  test('all elements render for a new game.', () => {
    /*render the component*/
    render(<GameBoard />);
    /*make sure all of the game squares are there and at the correct starting position*/
    for (let i of allSquares) { expect(screen.getByRole('button', { name: i })).toHaveTextContent('-') };
    /*confirm reset button*/
    expect(screen.getByRole('button', { name: 'Start a new game' })).toBeInTheDocument();
    /*confirm the game output is at the correct starting text*/
    expect(screen.getByRole('heading', { name: /X's Turn/i })).toBeInTheDocument();

  });

  test('the players trade moves and the outputs are correct', () => {
    // render the game board
    render(<GameBoard />);

    //confirm that the game output shows players X's turn
    expect(screen.getByRole('heading', { name: "X's Turn..." })).toBeInTheDocument();
    /*Click the the top left square*/
    userEvent.click(screen.getByRole('button', { name: 0 }));
    //confirm that the square is taken by player X
    expect(screen.getByRole('button', { name: 0 })).toHaveTextContent("X");

    //confirm that the game output shows players O's turn
    expect(screen.getByRole('heading', { name: "O's Turn..." })).toBeInTheDocument();
    //Click the the top left square
    userEvent.click(screen.getByRole('button', { name: 1 }));
    //confirm that the square is taken by player O
    expect(screen.getByRole('button', { name: 1 })).toHaveTextContent("O");
  });

  test('the game can be reset', () => {

    //function that verifies everything has been reset
    let test = () => {
      for (let i of allSquares) { expect(screen.getByRole('button', { name: i })).toHaveTextContent('-') };
      expect(screen.getByRole('heading', { name: /X's Turn/i })).toBeInTheDocument();
    };
    
    render(<GameBoard />);
    //test that the button can be clicked before any moves are taken
    userEvent.click(screen.getByRole('button', { name: 'Start a new game' }));
    test();

    //test that the game is reset with moves on the board
    var i = 0;

    let clicks = [0, 1]
    for (let i of clicks) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('button', { name: "0" })).toHaveTextContent('X');
    expect(screen.getByRole('button', { name: "1" })).toHaveTextContent('O');

    userEvent.click(screen.getByRole('button', { name: 'Start a new game' }));
    test();
  });

  test('a button can only by clicked once', () => {
    render(<GameBoard />);
    let game = [0, 0]
    for (let i of game) {
      userEvent.click(screen.getByRole('button', { name: i }))
      expect(screen.getByRole('button', { name: i })).toHaveTextContent('X')
    };
  });

  test('the game can be won by X', () => {
    // winning moves [0,3,6]
    render(<GameBoard />);
    let game = [0, 4, 8, 2, 6, 7, 3]
    for (let i of game) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('heading', { name: 'X is the Winner!' })).toBeInTheDocument();
  });

  test('the game can be won by O', () => {
    // winning moves [2,4,6]
    render(<GameBoard />);
    let game = [0, 4, 8, 2, 3, 6]
    for (let i of game) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('heading', { name: 'O is the Winner!' })).toBeInTheDocument();
  });
  
  test('the game can be a draw', () => {
    render(<GameBoard />);
    let game = [4, 2, 8, 0, 1, 7, 3, 5, 6]
    for (let i of game) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('heading', { name: "It's a Draw!" })).toBeInTheDocument();
  });
  
  test('the game can be won by [0, 1, 2]', () => {
    render(<GameBoard />);
    let game = [0, 4, 1, 6, 2]
    for (let i of game) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('heading', { name: 'X is the Winner!' })).toBeInTheDocument();
  });

  test('the game can be won by [3, 4, 5]', () => {
    render(<GameBoard />);
    let game = [0, 3, 1, 4, 6, 5]
    for (let i of game) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('heading', { name: 'O is the Winner!' })).toBeInTheDocument();
  });

  test('the game can be won by [6, 7, 8]', () => {
    render(<GameBoard />);
    let game = [6, 0, 7, 1, 8]
    for (let i of game) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('heading', { name: 'X is the Winner!' })).toBeInTheDocument();
  });

  test('the game can be won by [1, 4, 7]', () => {
    render(<GameBoard />);
    let game = [3, 1, 6, 4, 2, 7]
    for (let i of game) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('heading', { name: 'O is the Winner!' })).toBeInTheDocument();
  });

  test('the game can be won by [2, 5, 8]', () => {
    render(<GameBoard />);
    let game = [2, 4, 5, 0, 8]
    for (let i of game) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('heading', { name: 'X is the Winner!' })).toBeInTheDocument();
  }); 

  test('the game can be won by [0, 4, 8]', () => {
    render(<GameBoard />);
    let game = [2, 0, 1, 4, 3, 8]
    for (let i of game) { userEvent.click(screen.getByRole('button', { name: i })) };
    expect(screen.getByRole('heading', { name: 'O is the Winner!' })).toBeInTheDocument();
  });
});