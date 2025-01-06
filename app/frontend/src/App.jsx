import LoginPage from "./pages/LoginPage"
import Mainpage from "./pages/Mainpage"
import ContactPage from "./pages/ContactPage"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar"
import CalendarLoginPage from "./pages/CalendarLoginPage"

function App() {

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background">
        <Navbar />
        <Routes>
          <Route path="/" element={<Mainpage />}/>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/calendar/login" element={<CalendarLoginPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App