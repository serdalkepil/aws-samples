import { render, screen } from '@testing-library/react';
import PageHeader from './PageHeader';
const titleText = 'Tic-Tac-Toe!'

describe('PageHeader.test.js', () =>{
  test('confirm that the header renders', () => {
      render(<PageHeader />);
      expect(screen.getByText(titleText)).toBeInTheDocument();
  });
});