import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import WritersPage from './pages/WritersPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="writers" element={<WritersPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
