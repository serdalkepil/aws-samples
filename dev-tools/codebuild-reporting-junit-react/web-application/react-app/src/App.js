import './App.css';
import PageHeader from './PageHeader'
import SupportInfo from './SupportInfo'
import GameBoard from './GameBoard'

let App = () =>(
  <div className="App">
    <header>
      <PageHeader />
    </header>
    <section>
      <div className='container'>
          <GameBoard />
      </div>
    </section>
    <SupportInfo />
  </div>
);
export default App