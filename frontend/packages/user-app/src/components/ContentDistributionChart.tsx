import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

type DistItem = { id?: string; title: string; minutes: number; percent?: number };
interface Props { data: DistItem[]; }

export const ContentDistributionChart: React.FC<Props> = ({ data }) => {
  const labels = data.map((d) => d.title);
  const values = data.map((d) => d.minutes);
  const total = values.reduce((a, b) => a + b, 0);
  const colors = ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"];
  const backgroundColor = labels.map((_, i) => colors[i % colors.length]);
  const options: any = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: "right" } },
  };
  const dataChart = {
    labels,
    datasets: [ {
      data: values,
      backgroundColor,
    } ],
  };
  return (
    <div className="chart-container" style={{ height: 260 }}>
      <Pie data={dataChart} options={options} />
    </div>
  );
};
