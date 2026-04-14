import React from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

type Datum = { date: string; minutes: number };
interface Props {
  data: Datum[];
  periodLabel?: string;
  height?: number;
}

export const PlayTimeChart: React.FC<Props> = ({ data, periodLabel = "Period", height = 260 }) => {
  const labels = data.map((d) => d.date);
  const values = data.map((d) => d.minutes);
  const options: any = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      title: { display: false },
    },
    scales: {
      x: { grid: { display: false } },
      y: {
        beginAtZero: true,
        ticks: {
          callback: function (value: number) {
            const h = Math.floor(value / 60);
            const m = value % 60;
            if (h > 0) return `${h}h ${m}m`;
            return `${m}m`;
          },
        },
      },
    },
  };
  const chartData = {
    labels,
    datasets: [
      {
        label: "Play Time",
        data: values,
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };
  return (
    <div className="chart-container" style={{ height }}>
      <Bar options={options} data={chartData} />
    </div>
  );
};
