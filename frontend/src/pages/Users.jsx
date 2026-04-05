import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom';

const Users = () => {
  const [usersList, setUsersList] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const res = await api.get('/users/');
      setUsersList(res.data);
    } catch (err) {
      if (!err.response) {
        setError('Network Error: Could not connect to the backend server.');
      } else {
        setError(err.response?.data?.error || 'Failed to fetch users');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = async (userId, newRole) => {
    try {
      await api.put(`/users/${userId}`, { role: newRole });
      fetchUsers();
    } catch (err) {
      alert("Failed to update user role");
    }
  };

  const toggleStatus = async (userId, currentState) => {
    try {
      await api.put(`/users/${userId}`, { is_active: !currentState });
      fetchUsers();
    } catch (err) {
      alert("Failed to update user status");
    }
  };

  if (user?.role !== 'admin') {
    return <Navigate to="/dashboard" />;
  }

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1 style={{ marginBottom: '24px' }}>User Management</h1>
      {error && <div style={{ color: 'var(--danger)', marginBottom: '16px' }}>{error}</div>}
      
      <div className="glass-panel" style={{ overflow: 'hidden' }}>
        <table className="glass-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {usersList.map((u) => (
              <tr key={u._id}>
                <td style={{ fontWeight: 500 }}>{u.username}</td>
                <td>{u.email}</td>
                <td>
                  <select 
                    className="glass-input" 
                    value={u.role} 
                    onChange={(e) => handleRoleChange(u._id, e.target.value)}
                    style={{ padding: '6px 12px', width: 'auto' }}
                  >
                    <option value="viewer">Viewer</option>
                    <option value="analyst">Analyst</option>
                    <option value="admin">Admin</option>
                  </select>
                </td>
                <td>
                  <span className={`badge ${u.is_active ? 'income' : 'expense'}`}>
                    {u.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>
                  <button 
                    className={`glass-button ${u.is_active ? 'danger' : ''}`} 
                    style={{ padding: '6px 12px', fontSize: '0.8rem' }}
                    onClick={() => toggleStatus(u._id, u.is_active)}
                  >
                    {u.is_active ? 'Disable' : 'Enable'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Users;
