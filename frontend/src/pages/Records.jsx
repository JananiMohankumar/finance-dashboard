import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const Records = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ amount: '', type: 'expense', category: '', date: '', notes: '' });

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    try {
      const res = await api.get('/records/');
      setRecords(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/records/', {
        ...formData,
        date: new Date(formData.date).toISOString()
      });
      setShowModal(false);
      fetchRecords();
      setFormData({ amount: '', type: 'expense', category: '', date: '', notes: '' });
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to create');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure?")) return;
    try {
      await api.delete(`/records/${id}`);
      fetchRecords();
    } catch (err) {
      alert("Failed to delete");
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Financial Records</h1>
        {user?.role === 'admin' && (
          <button className="glass-button" onClick={() => setShowModal(true)}>+ Add Record</button>
        )}
      </div>

      <div className="glass-panel" style={{ overflow: 'hidden' }}>
        <table className="glass-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Type</th>
              <th>Category</th>
              <th>Notes</th>
              <th>Amount</th>
              {user?.role === 'admin' && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {records.map(r => (
              <tr key={r._id}>
                <td>{new Date(r.date).toLocaleDateString()}</td>
                <td><span className={`badge ${r.type}`}>{r.type}</span></td>
                <td>{r.category}</td>
                <td>{r.notes}</td>
                <td style={{ fontWeight: 600 }}>₹{r.amount.toFixed(2)}</td>
                {user?.role === 'admin' && (
                  <td>
                    <button className="glass-button danger" style={{ padding: '6px 12px', fontSize: '0.8rem' }} onClick={() => handleDelete(r._id)}>
                      Delete
                    </button>
                  </td>
                )}
              </tr>
            ))}
            {records.length === 0 && (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>No records found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 50, backdropFilter: 'blur(4px)' }}>
          <div className="glass-panel" style={{ padding: '32px', width: '100%', maxWidth: '500px', backgroundColor: 'var(--bg-dark)' }}>
            <h2 style={{ marginBottom: '24px' }}>Add New Record</h2>
            <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <select className="glass-input" value={formData.type} onChange={e => setFormData({...formData, type: e.target.value})}>
                <option value="income">Income</option>
                <option value="expense">Expense</option>
              </select>
              <input type="number" step="0.01" placeholder="Amount" className="glass-input" required value={formData.amount} onChange={e => setFormData({...formData, amount: e.target.value})} />
              <input type="text" placeholder="Category (e.g. Salary, Groceries)" className="glass-input" required value={formData.category} onChange={e => setFormData({...formData, category: e.target.value})} />
              <input type="date" className="glass-input" required value={formData.date} onChange={e => setFormData({...formData, date: e.target.value})} />
              <textarea placeholder="Notes (optional)" className="glass-input" rows={3} value={formData.notes} onChange={e => setFormData({...formData, notes: e.target.value})} />
              <div style={{ display: 'flex', gap: '16px', marginTop: '16px' }}>
                <button type="button" className="glass-button" style={{ background: 'transparent', border: '1px solid var(--border-glass)', flex: 1 }} onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="glass-button" style={{ flex: 1 }}>Save Record</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Records;
