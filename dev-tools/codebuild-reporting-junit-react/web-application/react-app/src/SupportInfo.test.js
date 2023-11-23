import { render, screen } from '@testing-library/react';
import SupportInfo from './SupportInfo';
const footerText = 'Example Corp 2021'

describe('SupportInfo.test.js', () =>{
  test('confirm that the footer renders', () => {
      render(<SupportInfo />);
      expect(screen.getByText(footerText)).toBeInTheDocument();
  });
});