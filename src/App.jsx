import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import ArticlePage from './pages/ArticlePage';
import WritersPage from './pages/WritersPage'; // Keeping this if it exists, or will create/stub it

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="category/:category" element={<HomePage />} />
          <Route path="article/:id" element={<ArticlePage />} />
          <Route path="writers" element={<WritersPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
