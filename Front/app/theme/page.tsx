// File: /pages/theme.tsx
import React from 'react';
import { NextPage } from 'next';
import {
  Button,
  Card,
  Typography,
  Space,
  Input,
  Menu,
  Table,
  Avatar,
  Badge,
  Divider,
  Switch,
} from 'antd';
import { TeamOutlined, SearchOutlined } from '@ant-design/icons';
import PageContainer from '@/components/PageContainer';
import ThemeSwitcher from '@/components/ThemeSwitcher';

const { Title, Paragraph, Text } = Typography;

// Sample table data for demonstration
const tableData = [
  { key: '1', name: 'Alice', age: 28, address: 'Wonderland' },
  { key: '2', name: 'Bob', age: 34, address: 'Builder City' },
  { key: '3', name: 'Charlie', age: 25, address: 'Chocolate Factory' },
];

const tableColumns = [
  { title: 'Name', dataIndex: 'name', key: 'name' },
  { title: 'Age', dataIndex: 'age', key: 'age' },
  { title: 'Address', dataIndex: 'address', key: 'address' },
];

// Sample menu items for demonstration
const demoMenuItems = [
  { key: 'home', label: 'Home' },
  { key: 'about', label: 'About' },
  { key: 'services', label: 'Services' },
  { key: 'contact', label: 'Contact' },
];

const ThemeDemoPage: NextPage = () => {
  return (
    <PageContainer title="Theme Demo & Switcher">
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        
        {/* Typography Demo */}
        <Card title="Typography" bordered>
          <Title>Ant Design Typography</Title>
          <Paragraph>
            This is a paragraph demonstrating the typography settings from your theme.
            Notice the font family and size defined by your tokens.
          </Paragraph>
          <Text>This is some sample text.</Text>
        </Card>

        {/* Buttons Demo */}
        <Card title="Buttons" bordered>
          <Space>
            <Button type="primary">Primary Button</Button>
            <Button type="default">Default Button</Button>
            <Button type="dashed">Dashed Button</Button>
            <Button type="text">Text Button</Button>
            <Button type="link">Link Button</Button>
          </Space>
        </Card>

        {/* Input Elements Demo */}
        <Card title="Inputs & Search" bordered>
          <Space direction="vertical" style={{ width: '100%' }}>
            <Input placeholder="Basic Input" />
            <Input.Search placeholder="Search Input" enterButton icon={<SearchOutlined />} />
          </Space>
        </Card>

        {/* Menu Demo */}
        <Card title="Menu" bordered>
          <Menu mode="horizontal" items={demoMenuItems} />
        </Card>

        {/* Table Demo */}
        <Card title="Table" bordered>
          <Table dataSource={tableData} columns={tableColumns} pagination={false} />
        </Card>

        {/* Avatars & Badges Demo */}
        <Card title="Avatars & Badges" bordered>
          <Space size="large">
            <Avatar size="large" icon={<TeamOutlined />} />
            <Badge count={8}>
              <Avatar shape="square" size="large" style={{ backgroundColor: '#87d068' }} />
            </Badge>
          </Space>
        </Card>

        {/* Miscellaneous Elements */}
        <Card title="Miscellaneous" bordered>
          <Space direction="vertical">
            <Switch defaultChecked />
            <Divider />
            <Text>This text shows the default global text color defined by your theme.</Text>
          </Space>
        </Card>

        {/* Theme Switcher Demo */}
        <Card title="Theme Switcher" bordered>
          <Paragraph>
            Use the button below to cycle between themes (funky, light, dark). All the UI elements above will change accordingly.
          </Paragraph>
          <ThemeSwitcher />
        </Card>
      </Space>
    </PageContainer>
  );
};

export default ThemeDemoPage;
