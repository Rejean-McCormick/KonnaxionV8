// pages/dashboard.tsx
import React from 'react';
import MainLayout from '@/components/MainLayout';

const Dashboard: React.FC = () => {
  return (
    <MainLayout>
      <h1>Bienvenue sur le Dashboard de Konnaxion</h1>
      <p>
        Ceci est une page de test intégrée dans le layout global pour vérifier la navigation, la sidebar,
        la topbar avec barre de recherche, notifications et le menu dropdown du logo.
      </p>
    </MainLayout>
  );
};

export default Dashboard;
