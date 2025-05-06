'use client'

// pages/ethikos/decide/public.tsx
import { PageContainer, ProTable } from '@ant-design/pro-components';
import {
  Radio,
  Segmented,
  Slider,
  Popconfirm,
  Progress,
  Select,
  Space,
  Result,
} from 'antd';
import { useRequest } from 'ahooks';
import { useMemo, useState } from 'react';
import usePageTitle from '@/hooks/usePageTitle';

import {
  fetchPublicTopics,
  submitPublicVote,
  PublicTopic,
  Category,
  VotingFormat,
} from '@/services/decide.mock';

type Row = PublicTopic & { _selected?: string | number };

export default function PublicVotePage() {
  usePageTitle('Decide · Public Voting');

  /* ------------------------------------------------------------ */
  /*  Fetch data                                                  */
  /* ------------------------------------------------------------ */
  const {
    data,
    loading,
    mutate: refresh,
  } = useRequest(fetchPublicTopics);

  const [activeCat, setActiveCat] = useState<string | 'all'>('all');
  const [submitting, setSubmitting] = useState<string | null>(null);

  const categories = data?.categories ?? [];
  const topics = useMemo(() => {
    if (!data?.topics) return [];
    return activeCat === 'all'
      ? data.topics
      : data.topics.filter(t => t.categoryId === activeCat);
  }, [data, activeCat]);

  /* ------------------------------------------------------------ */
  /*  Submit / mutate                                             */
  /* ------------------------------------------------------------ */
  const vote = async (topic: Row) => {
    if (topic._selected == null) return;
    setSubmitting(topic.id);
    await submitPublicVote(topic.id, topic._selected);
    await refresh(); // update turnout
    setSubmitting(null);
  };

  /* ------------------------------------------------------------ */
  /*  Column helpers                                              */
  /* ------------------------------------------------------------ */
  const renderVoteInput = (row: Row) => {
    const commonProps = {
      disabled: submitting === row.id,
      onChange: (val: any) =>
        (row._selected =
          val?.target?.value ?? // Radio
          val), // Slider / Segmented
    };

    switch (row.format as VotingFormat) {
      case 'binary':
        return (
          <Radio.Group
            options={(row.options ?? ['Yes', 'No']).map(v => ({
              label: v,
              value: v,
            }))}
            {...commonProps}
          />
        );

      case 'multiple':
        return (
          <Radio.Group
            options={(row.options ?? []).map(v => ({ label: v, value: v }))}
            {...commonProps}
          />
        );

      case 'scale': {
        // 0-based numeric values
        const labels = row.scaleLabels ?? [
          '1',
          '2',
          '3',
          '4',
          '5',
        ];
        return (
          <Space direction="vertical" size={4}>
            <Segmented
              options={labels}
              {...commonProps}
              block
            />
            {/* fallback slider for keyboard / mobile users */}
            <Slider
              min={0}
              max={labels.length - 1}
              step={1}
              tooltip={{ formatter: idx => labels[idx as number] }}
              {...commonProps}
            />
          </Space>
        );
      }

      default:
        return null;
    }
  };

  const columns = [
    { title: 'Question', dataIndex: 'question', width: 340 },
    {
      title: 'Vote',
      dataIndex: 'vote',
      render: (_: any, row: Row) =>
        submitting === row.id ? (
          <Result status="info" title="Submitting…" />
        ) : (
          <Popconfirm
            title="Confirm your vote?"
            okText="Yes"
            cancelText="No"
            onConfirm={() => vote(row)}
          >
            {renderVoteInput(row)}
          </Popconfirm>
        ),
    },
    {
      title: 'Turnout',
      dataIndex: 'turnout',
      width: 140,
      render: (v: number) => <Progress percent={v} size="small" />,
    },
    { title: 'Closes', dataIndex: 'closesAt', valueType: 'datetime' },
  ];

  /* ------------------------------------------------------------ */
  /*  UI                                                          */
  /* ------------------------------------------------------------ */
  return (
    <PageContainer ghost loading={loading}>
      <Space style={{ marginBottom: 16 }}>
        <b>Category:</b>
        <Select
          value={activeCat}
          onChange={setActiveCat}
          options={[
            { label: 'All', value: 'all' },
            ...categories.map((c: Category) => ({
              label: c.name,
              value: c.id,
            })),
          ]}
          style={{ width: 260 }}
        />
      </Space>

      <ProTable<Row>
        rowKey="id"
        columns={columns as any}
        dataSource={topics}
        pagination={{ pageSize: 6 }}
        search={false}
      />
    </PageContainer>
  );
}
