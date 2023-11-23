import { render, screen } from '@testing-library/react';
import App from './App';

jest.mock("./GameBoard", () => { 
  return function GameBoard(props) { 
    return (
      <div data-testid="GameBoard">Gameboard</div>
    )};
});
jest.mock("./SupportInfo", () => { 
  return function SupportInfo(props) { return (
    <div data-testid="SupportInfo">SupportInfo</div>
  )};
});
jest.mock("./PageHeader", () => { 
  return function PageHeader(props) { return (
    <div data-testid="PageHeader">PageHeader</div>
  )};
});

describe('App.test.js', () =>{
  test('renders App component', () => {
    render(<App />);
  });
});