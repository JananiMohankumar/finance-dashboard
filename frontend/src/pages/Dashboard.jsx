import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip, Legend } from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await api.get('/dashboard/summary');
        setData(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (!data) return <div>Error loading dashboard</div>;

  const expCategories = data.by_category.filter(c => c.type === 'expense');

  return (
    <div>
      <h1 style={{ marginBottom: '24px' }}>Dashboard Overview</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px', marginBottom: '32px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ color: 'var(--text-muted)', margin: '0 0 8px 0', fontWeight: 500 }}>Total Income</h3>
          <h2 style={{ color: 'var(--success)', margin: 0, fontSize: '2rem' }}>₹{data.summary.total_income.toFixed(2)}</h2>
        </div>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ color: 'var(--text-muted)', margin: '0 0 8px 0', fontWeight: 500 }}>Total Expenses</h3>
          <h2 style={{ color: 'var(--danger)', margin: 0, fontSize: '2rem' }}>₹{data.summary.total_expense.toFixed(2)}</h2>
        </div>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ color: 'var(--text-muted)', margin: '0 0 8px 0', fontWeight: 500 }}>Net Balance</h3>
          <h2 style={{ color: data.summary.net_balance >= 0 ? 'var(--text-main)' : 'var(--danger)', margin: 0, fontSize: '2rem' }}>
            ₹{data.summary.net_balance.toFixed(2)}
          </h2>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '24px' }}>Expenses by Category</h3>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={expCategories} dataKey="amount" nameKey="category" cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={5}>
                  {expCategories.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip contentStyle={{ backgroundColor: 'var(--bg-glass)', border: '1px solid var(--border-glass)', borderRadius: '8px' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ marginBottom: '24px' }}>Recent Activity</h3>
          {data.recent_activity.length === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>No recent activity.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {data.recent_activity.map(item => (
                <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '16px', borderBottom: '1px solid var(--border-glass)' }}>
                  <div>
                    <h4 style={{ margin: '0 0 4px 0' }}>{item.category}</h4>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{new Date(item.date).toLocaleDateString()}</span>
                  </div>
                  <span className={`badge ${item.type}`}>
                    {item.type === 'income' ? '+' : '-'}₹{item.amount.toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
