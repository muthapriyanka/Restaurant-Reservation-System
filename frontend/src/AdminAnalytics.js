// src/pages/AdminAnalytics.jsx
import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import {
  ResponsiveContainer,
  BarChart,
  XAxis,
  YAxis,
  Tooltip,
  Bar,
} from "recharts";
import axios from "axios";

const StatCard = ({ title, value }) => (
  <div className="stat-card">
    <h3>{value}</h3>
    <p>{title}</p>
  </div>
);

const DailyChart = ({ data }) => (
  <div className="chart-container">
    <h4>📅 Daily Additions</h4>
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="date" tick={{ fill: "white" }} axisLine={{ stroke: "white" }} />
        <YAxis tick={{ fill: "white" }} axisLine={{ stroke: "white" }} />
        <Tooltip />
        <Bar dataKey="count" fill="#007bff" />
      </BarChart>
    </ResponsiveContainer>
  </div>
);

const AdminAnalytics = () => {
  const [recent, setRecent] = useState([]);
  const [dailyCounts, setDailyCounts] = useState([]);
  const [topCities, setTopCities] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAndProcess = async () => {
      try {
        // 👉 swap in real endpoint when ready:
        // const { data: all } = await axios.get("/api/restaurants");
        // dummy data for n
