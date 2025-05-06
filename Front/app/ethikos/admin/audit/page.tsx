import { PageContainer, ProTable } from '@ant-design/pro-components';
import { Tag } from 'antd';
import { useRequest } from 'ahooks';
import usePageTitle from '@/hooks/usePageTitle';
import { fetchAuditLogs } from '@/services/admin';

type LogRow = {
  id: string;
  actor: string;
  action: string;
  target: string;
  severity: 'info' | 'warn' | 'critical';
  ts: string;
};

export default function AuditLogs() {
  usePageTitle('Admin · Audit Logs');

  const { data, loading } = useRequest(fetchAuditLogs);

  const columns = [
    { title: 'Time', dataIndex: 'ts', valueType: 'dateTime', width: 180, sorter: true },
    { title: 'Actor', dataIndex: 'actor', width: 120 },
    { title: 'Action', dataIndex: 'action', width: 200 },
    { title: 'Target', dataIndex: 'target', ellipsis: true },
    {
      title: 'Severity',
      dataIndex: 'severity',
      width: 120,
      render: (v: LogRow['severity']) => (
        <Tag color={v === 'critical' ? 'red' : v === 'warn' ? 'orange' : 'blue'}>{v}</Tag>
      ),
      filters: [
        { text: 'Info', value: 'info' },
        { text: 'Warn', value: 'warn' },
        { text: 'Critical', value: 'critical' },
      ],
      onFilter: (val: any, row: LogRow) => row.severity === val,
    },
  ];

  return (
    <PageContainer ghost loading={loading}>
      <ProTable<LogRow>
        rowKey="id"
        columns={columns}
        dataSource={data?.items}
        pagination={{ pageSize: 15 }}
        search={false}
      />
    </PageContainer>
  );
}
