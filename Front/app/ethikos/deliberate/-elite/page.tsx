import { PageContainer, ProTable } from '@ant-design/pro-components';
import { Tag } from 'antd';
import { useRequest } from 'ahooks';
import usePageTitle from '@/hooks/usePageTitle';
import { fetchEliteTopics } from '@/services/deliberate';
import type { Topic } from '@/types';

export default function EliteAgora() {
  usePageTitle('Deliberate · Elite Agora');

  const { data, loading } = useRequest(fetchEliteTopics);

  const columns = [
    { title: 'Title', dataIndex: 'title', width: 260 },
    { title: 'Category', dataIndex: 'category', width: 160 },
    {
      title: 'Stances',
      dataIndex: 'stanceCount',
      width: 120,
      render: (v: number) => <Tag color="blue">{v}</Tag>,
    },
    {
      title: 'Created',
      dataIndex: 'createdAt',
      valueType: 'date',
      sorter: true,
    },
  ];

  return (
    <PageContainer ghost loading={loading}>
      <ProTable<Topic>
        rowKey="id"
        columns={columns}
        dataSource={data?.list}
        pagination={{ pageSize: 10 }}
        search={false}
      />
    </PageContainer>
  );
}
