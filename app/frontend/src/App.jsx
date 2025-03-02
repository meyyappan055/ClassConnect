import LoginPage from "./pages/LoginPage"
import MainPage from "./pages/MainPage"
import About from "./pages/About"
import DownloadPage from "./pages/DownloadPage"
import TermsPage from "./pages/TermsPage"
import PrivacyPage from "./pages/PrivacyPage"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar"
import {Analytics} from '@vercel/analytics/react';

function App() {

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background">
        <Navbar />
        <Routes>
          <Route path="/" element={<MainPage />}/>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/about" element= {<About />} />
          <Route path="/download" element = {<DownloadPage />} />
          <Route path="/terms" element = {<TermsPage />} />
          <Route path="/privacy" element = {<PrivacyPage />} />
        </Routes>
        <Analytics />
      </div>
    </BrowserRouter>
  )
}

export default App