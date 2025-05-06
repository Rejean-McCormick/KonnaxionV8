import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(_req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({
    refreshedAt: new Date().toISOString(),
    kpis: [
      {
        label: 'Active users',
        value: 8421,
        delta: 3.4,
        history: [
          { date: '2025-04-20', value: 7100 },
          { date: '2025-04-21', value: 7300 },
          { date: '2025-04-22', value: 7600 },
          { date: '2025-04-23', value: 7900 },
          { date: '2025-04-24', value: 8200 },
          { date: '2025-04-25', value: 8421 },
        ],
      },
      {
        label: 'Daily posts',
        value: 156,
        delta: -1.2,
        history: [
          { date: '2025-04-20', value: 180 },
          { date: '2025-04-21', value: 170 },
          { date: '2025-04-22', value: 165 },
          { date: '2025-04-23', value: 162 },
          { date: '2025-04-24', value: 158 },
          { date: '2025-04-25', value: 156 },
        ],
      },
      // …add two more KPIs if you like
    ],
  });
}
