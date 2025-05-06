'use client'

// pages/ekoh/overview-analytics/current-ekoh-score/index.tsx
import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import type { NextPage } from 'next';
import { Card, Row, Col, Alert, Timeline, Table } from 'antd';
import MainLayout from '@/components/layout-components/MainLayout';
import {
  PieChart as RePieChart,
  Pie,
  Cell,
  Legend,
  Tooltip as ReTooltip,
  ResponsiveContainer,
  LineChart as ReLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

const CurrentEkohScore: NextPage & { getLayout?: (page: React.ReactElement) => React.ReactNode } = () => {
  // Données pour le donut chart
  const [pieData, setPieData] = useState([
    { name: 'Expertise', value: 40 },
    { name: 'Community Feedback', value: 35 },
    { name: 'Ethics', value: 25 },
  ]);

  // Données pour le graphique en ligne (historical trend)
  const [trendData, setTrendData] = useState<Array<{ date: string; score: number }>>([
    { date: '2023-08-01', score: 60 },
    { date: '2023-08-02', score: 62 },
    { date: '2023-08-03', score: 65 },
    { date: '2023-08-04', score: 67 },
    { date: '2023-08-05', score: 70 },
    { date: '2023-08-06', score: 72 },
    { date: '2023-08-07', score: 75 },
  ]);

  // Timeline : événements clés influençant le score
  const timelineData = [
    { key: '1', time: '2023-08-02', event: 'Achieved Expert Level 3' },
    { key: '2', time: '2023-08-04', event: 'Received high community feedback' },
    { key: '3', time: '2023-08-06', event: 'Ethics audit improved rating' },
  ];

  // Colonnes et données simulées pour la table des évaluations récentes
  const tableColumns = [
    { title: 'Date', dataIndex: 'date', key: 'date' },
    { title: 'Contribution Detail', dataIndex: 'detail', key: 'detail' },
  ];

  const tableData = [
    { key: '1', date: '2023-08-02', detail: 'Expert review added +4 points' },
    { key: '2', date: '2023-08-04', detail: 'Community vote increased score by +3 points' },
    { key: '3', date: '2023-08-06', detail: 'Ethics audit contributed +2 points' },
  ];

  // Optionnel : mise à jour dynamique du graphique historique
  useEffect(() => {
    const interval = setInterval(() => {
      const newDate = new Date().toISOString().split('T')[0];
      const newScore = 60 + Math.floor(Math.random() * 20);
      setTrendData(prev => [...prev.slice(-6), { date: newDate, score: newScore }]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <Head>
        <title>Current Ekoh Score – Overview & Analytics</title>
        <meta name="description" content="Detailed breakdown of your Ekoh score with charts, timeline, and evaluation details." />
      </Head>
      <div className="container mx-auto p-5">
        {/* Page header */}
        <h1 className="text-2xl font-bold mb-4">Current Ekoh Score – Overview & Analytics</h1>

        {/* Donut Chart Section */}
        <Card className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Score Breakdown</h2>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <RePieChart>
                <ReTooltip />
                <Legend verticalAlign="bottom" height={36} />
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  dataKey="value"
                  paddingAngle={5}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
              </RePieChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Historical Trend Chart */}
        <Card className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Historical Trend</h2>
          <div style={{ width: '100%', height: 250 }}>
            <ResponsiveContainer>
              <ReLineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <ReTooltip />
                <Line type="monotone" dataKey="score" stroke="#82ca9d" />
              </ReLineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Timeline of Influencing Events */}
        <Card className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Key Events Influencing Your Score</h2>
          <Timeline>
            {timelineData.map(item => (
              <Timeline.Item key={item.key}>
                <strong>{item.time}</strong> - {item.event}
              </Timeline.Item>
            ))}
          </Timeline>
        </Card>

        {/* Explanation Panel */}
        <Card className="mb-6">
          <h2 className="text-xl font-semibold mb-4">How Your Score is Calculated</h2>
          <Alert
            message="Score Calculation Explained"
            description="Your Ekoh score is derived from a weighted combination of your expertise level, community feedback, and ethical evaluations. This transparent approach ensures that every contribution is fairly recognized."
            type="info"
            showIcon
          />
        </Card>

        {/* Recent Evaluations Table */}
        <Card>
          <h2 className="text-xl font-semibold mb-4">Recent Evaluations Impacting Your Score</h2>
          <Table columns={tableColumns} dataSource={tableData} pagination={false} />
        </Card>
      </div>
    </>
  );
};

CurrentEkohScore.getLayout = (page: React.ReactElement) => <MainLayout>{page}</MainLayout>;

export default CurrentEkohScore;
