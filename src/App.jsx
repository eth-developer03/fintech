import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Topbar from './scenes/global/Topbar';
import Sidebar from './scenes/global/Sidebar';
import Dashboard from './scenes/dashboard';
import PortfolioOptimization from './scenes/portfolio/portfolioOptimization';
import Invoices from './scenes/invoices';
import Contacts from './scenes/contacts';
import Bar from './scenes/bar';
import Form from './scenes/form';
import Line from './scenes/line';

import FAQ from './scenes/faq/index';
import { CssBaseline, ThemeProvider, Button } from '@mui/material';
import { ColorModeContext, useMode } from './theme';
import Calendar from './scenes/calendar/calendar';
import Chatbot from './components/Chatbot';
import {
  SignedIn,
  SignedOut,
  SignIn,
  SignUp,
  RedirectToSignIn,
  UserButton,
  useClerk,
  useUser,
} from '@clerk/clerk-react';
import MutualTear from './scenes/mutualfunds';
import GdpDashboard from './scenes/gdp';
import CrossBorder from './scenes/crossborder';

function App() {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(false);
  const { signOut } = useClerk();
  const { user } = useUser();

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          <SignedIn>
            <Sidebar isSidebar={isSidebar} />
            <main className="content">
              <Topbar setIsSidebar={setIsSidebar} />
              <div style={{ display: 'flex', justifyContent: 'flex-end', padding: '10px' }}>
                <UserButton />
                <Button onClick={signOut} variant="contained" color="secondary" style={{ marginLeft: '10px' }}>
                  Sign Out
                </Button>
              </div>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/contacts" element={<Contacts />} />
                <Route path="/invoices" element={<Invoices />} />
                <Route path="/portfolio" element={<PortfolioOptimization />} />
                <Route path="/mutualfunds" element={<MutualTear/>} />
                <Route path="/gdp" element={<GdpDashboard/>} />
                <Route path="/crossborder" element={<CrossBorder/>} />




                <Route path="/form" element={<Form />} />
                <Route path="/bar" element={<Bar />} />
                <Route path="/pie" element={<Chatbot />} />
                <Route path="/line" element={<Line />} />
                <Route path="/faq" element={<FAQ />} />
                <Route path="/calendar" element={<Calendar />} />
              </Routes>
            </main>
          </SignedIn>

          <SignedOut>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
              <Routes>
                <Route path="/sign-in/*" element={<SignIn />} />
                <Route
                  path="/sign-up/*"
                  element={
                    <SignUp
                      path="/sign-up"
                      signUpFields={[
                        { name: 'name', type: 'text', label: 'Full Name' },
                        { name: 'email_address', type: 'email', label: 'Email' },
                        { name: 'password', type: 'password', label: 'Password' },
                        { name: 'age', type: 'number', label: 'Age' },
                        { name: 'gender', type: 'select', label: 'Gender', options: ['Male', 'Female', 'Other'] },
                      ]}
                    />
                  }
                />
                <Route path="*" element={<RedirectToSignIn />} />
              </Routes>
            </div>
          </SignedOut>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;

