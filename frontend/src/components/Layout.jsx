import React from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Receipt, Users, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Layout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="app-layout">
      <aside className="sidebar glass-panel">
        <div style={{ padding: '0 16px', marginBottom: '24px' }}>
          <h2 style={{ color: 'var(--text-main)', margin: 0 }}>FinancePro</h2>
          <small style={{ color: 'var(--text-muted)' }}>Role: {user?.role}</small>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
          <NavLink to="/dashboard" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
            <LayoutDashboard size={20} /> Dashboard
          </NavLink>
          {(user?.role === 'admin' || user?.role === 'analyst') && (
            <NavLink to="/records" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              <Receipt size={20} /> Records
            </NavLink>
          )}
          {user?.role === 'admin' && (
            <NavLink to="/users" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              <Users size={20} /> Users
            </NavLink>
          )}
        </nav>

        <button onClick={handleLogout} className="glass-button danger" style={{ display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}>
          <LogOut size={18} /> Logout
        </button>
      </aside>
      
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
