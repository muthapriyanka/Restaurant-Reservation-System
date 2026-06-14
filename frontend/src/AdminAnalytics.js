import React, { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import Header from "./Header";
import { getAllAdminRestaurants } from "./api/auth";

const StatCard = ({ title, value }) => (
  <div className="stat-card">
    <h3>{value}</h3>
    <p>{title}</p>
  </div>
);

const formatDate = (value) => {
  if (!value) {
    return "Unknown";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "Unknown";
  }

  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
};

const buildDailyCounts = (restaurants) => {
  const counts = restaurants.reduce((acc, restaurant) => {
    const key = formatDate(restaurant.created_at);
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  return Object.entries(counts).map(([date, count]) => ({ date, count }));
};

const buildTopCities = (restaurants) => {
  const counts = restaurants.reduce((acc, restaurant) => {
    const city = restaurant.city || "Unknown";
    acc[city] = (acc[city] || 0) + 1;
    return acc;
  }, {});

  return Object.entries(counts)
    .map(([city, count]) => ({ city, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);
};

const DailyChart = ({ data }) => (
  <div className="chart-container">
    <h4>Daily Additions</h4>
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis
          dataKey="date"
          tick={{ fill: "white" }}
          axisLine={{ stroke: "white" }}
        />
        <YAxis tick={{ fill: "white" }} axisLine={{ stroke: "white" }} />
        <Tooltip />
        <Bar dataKey="count" fill="#007bff" />
      </BarChart>
    </ResponsiveContainer>
  </div>
);

const AdminAnalytics = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await getAllAdminRestaurants();
        setRestaurants(Array.isArray(data) ? data : []);
        setError(null);
      } catch (err) {
        console.error("Error fetching admin analytics:", err);
        setError("Unable to load analytics right now.");
      }
    };

    fetchAnalytics();
  }, []);

  const dailyCounts = useMemo(
    () => buildDailyCounts(restaurants),
    [restaurants]
  );
  const topCities = useMemo(() => buildTopCities(restaurants), [restaurants]);
  const recent = useMemo(
    () =>
      [...restaurants]
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 5),
    [restaurants]
  );

  const approvedCount = restaurants.filter(
    (restaurant) => restaurant.is_approved
  ).length;
  const pendingCount = restaurants.length - approvedCount;

  return (
    <>
      <Header />
      <div className="analytics-bg">
        <main className="admin-analytics">
          <h1 className="analytics-title">Admin Analytics</h1>

          {error ? <p className="error-text">{error}</p> : null}

          <section className="analytics-cards">
            <StatCard title="Total Restaurants" value={restaurants.length} />
            <StatCard title="Approved" value={approvedCount} />
            <StatCard title="Pending Approval" value={pendingCount} />
          </section>

          <DailyChart data={dailyCounts} />

          <section className="chart-container">
            <h4>Top Cities</h4>
            {topCities.length > 0 ? (
              <ul>
                {topCities.map(({ city, count }) => (
                  <li key={city}>
                    {city}: {count}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No city data available.</p>
            )}
          </section>

          <section className="chart-container">
            <h4>Recent Restaurants</h4>
            {recent.length > 0 ? (
              <ul>
                {recent.map((restaurant) => (
                  <li key={restaurant.restaurant_id}>
                    {restaurant.name} - {formatDate(restaurant.created_at)}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No restaurants available.</p>
            )}
          </section>
        </main>
      </div>
    </>
  );
};

export default AdminAnalytics;
