import React from 'react';
import dynamic from 'next/dynamic';
import styles from './styles.module.css';
import CommonWidget from './components/CommonWidget';

// Utilisation d'un import dynamique pour MainLayout afin de rompre le cycle d'importation
const MainLayout = dynamic(() => import(@/components/layout-components/MainLayout'), { ssr: true });

const PageTemplate: React.FC = () => {
  return (
    <MainLayout>
      <div className={styles.container}>
        <h1 className={styles.title}>Titre de la Page Générique</h1>
        <p className={styles.subtitle}>
          Ceci est un contenu générique qui servira de base pour chaque page. Vous pourrez ensuite personnaliser
          ce contenu par section.
        </p>
        <div className={styles.widgets}>
          <CommonWidget title="Widget 1" description="Description du widget 1" />
          <CommonWidget title="Widget 2" description="Description du widget 2" />
          <CommonWidget title="Widget 3" description="Description du widget 3" />
        </div>
      </div>
    </MainLayout>
  );
};

export default PageTemplate;
