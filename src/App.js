import './App.css';
import CustomNavbar from './components/CustomNavbar';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Home from './components/Home';
import Login from './components/UserMangement/Login';
import Signup from './components/UserMangement/Signup';
import Chatbot from './components/Chatbot';
import DataProcessing from './components/DataProcessing';
import ThirdFactorAuthentication from './components/UserMangement/ThirdFactorAuthentication';
import SecondFactorAuthentication from './components/UserMangement/SecondFactorAuthentication';
import RestaurateurLogin from './components/UserMangement/RestaurateurLogin';
import Visualization from './components/Visualization/Visualization';
import Chat from './components/Chat'
import Polarity from './components/Machine Learning/Polarity';
import Similarity from './components/Machine Learning/Similarity';
import User from './components/User';

function App() {
  return (
    <div className="App">
      <Router>
        <CustomNavbar />
        <Routes>
          <Route path='/' element={<Home />}/>
          <Route path='/login' element={<Login />}/>
          <Route path='/signup' element={<Signup />} />
          <Route path='/ThirdFactorAuthentication' element={<ThirdFactorAuthentication />} />
          <Route path='/SecondFactorAuthentication' element={<SecondFactorAuthentication />} />
          <Route path='/chatbot' element={<Chatbot />}/>
          <Route path='/data-processing' element={<DataProcessing />}/>
          <Route path='/RestaurateurLogin' element={<RestaurateurLogin />}/>
          <Route path='/Visualization' element={<Visualization />}/>
          <Route path='/chat' element={<Chat/>}/>
          <Route path='/polarity' element={<Polarity/>}/>
          <Route path='/similarity' element={<Similarity/>}/>
          <Route path='/user' element={<User/>}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
