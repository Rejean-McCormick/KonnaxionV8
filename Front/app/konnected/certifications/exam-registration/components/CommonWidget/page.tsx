// pages/pageTemplate/components/CommonWidget.tsx
import React from 'react';
import styles from './CommonWidget.module.css';

interface CommonWidgetProps {
  title: string;
  description: string;
}

const CommonWidget: React.FC<CommonWidgetProps> = ({ title, description }) => {
  return (
    <div className={styles.widget}>
      <h2 className={styles.widgetTitle}>{title}</h2>
      <p className={styles.widgetDescription}>{description}</p>
    </div>
  );
};

export default CommonWidget;
