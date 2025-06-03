import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  getRestaurantDetailForManager,
  managerUpdateOperatingHours,
  managerUpdateTables,
  updateRestaurantForManager,
} from "./api/auth";

const CostRatingEnum = Object.freeze({ 1: 1, 2: 2, 3: 3, 4: 4, 5: 5 });
const daysOfWeek = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];
const generateTimeOptions = () => {
  const times = [];
  for (let hour = 0; hour < 24; hour++) {
    for (let min = 0; min < 60; min += 30) {
      times.push(
        `${String(hour).padStart(2, "0")}:${String(min).padStart(2, "0")}`
      );
    }
  }
  return times;
};

const UpdateRestaurant = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [restaurant, setRestaurant] = useState(null);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getRestaurantDetailForManager({ id });
        if (!Array.isArray(res.operating_hours)) {
          res.operating_hours = [
            { day_of_week: "", opening_time: "", closing_time: "" },
          ];
        }
        if (!Array.isArray(res.tables)) {
          res.tables = [{ table_number: "", capacity: "" }];
        }
        setRestaurant(res);
      } catch (err) {
        console.error("Error fetching details:", err);
      }
    };
    fetchData();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newValue =
      name === "cost_rating" ? CostRatingEnum[value] ?? "" : value;
    setRestaurant((prev) => ({ ...prev, [name]: newValue }));
    setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleAvailabilityChange = (e) => {
    const selected = Array.from(e.target.selectedOptions).map((o) => o.value);
    setRestaurant((prev) => ({ ...prev, availability: selected }));
  };

  const handleHoursChange = (idx, field, value) => {
    setRestaurant((prev) => {
      const hrs = prev.operating_hours.map((h, i) =>
        i === idx ? { ...h, [field]: value } : h
      );
      return { ...prev, operating_hours: hrs };
    });
    setErrors((prev) => {
      const copy = { ...prev };
      delete copy[`operating_hours.${idx}.${field}`];
      return copy;
    });
  };

  const addOperatingHour = () => {
    setRestaurant((prev) => ({
      ...prev,
      operating_hours: [
        ...prev.operating_hours,
        { day_of_week: "", opening_time: "", closing_time: "" },
      ],
    }));
  };

  const removeOperatingHour = (idx) => {
    setRestaurant((prev) => ({
      ...prev,
      operating_hours: prev.operating_hours.filter((_, i) => i !== idx),
    }));
  };

  const handleTableChange = (idx, field, value) => {
    setRestaurant((prev) => {
      const newTables = prev.tables.map((t, i) =>
        i === idx ? { ...t, [field]: value } : t
      );
      return { ...prev, tables: newTables };
    });
  };

  const addTable = () => {
    setRestaurant((prev) => ({
      ...prev,
      tables: [...prev.tables, { table_number: "", capacity: "" }],
    }));
  };

  const removeTable = (idx) => {
    setRestaurant((prev) => ({
      ...prev,
      tables: prev.tables.filter((_, i) => i !== idx),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // 1) Update basic restaurant info
      const { operating_hours, tables, ...basicInfo } = restaurant;
      const updated = await updateRestaurantForManager({
        id,
        restaurant: basicInfo,
      });
      const rstId = updated.restaurant_id;

      // 2) Prepare payloads
      const tablesPayload = tables.map((t) => ({
        table_number: t.table_number,
        capacity: Number(t.capacity),
        is_active: true
      }));

      // 3) Run follow-up updates in parallel
      const [hrsRes, tblsRes] = await Promise.all([
        managerUpdateOperatingHours(rstId, operating_hours),
        managerUpdateTables(rstId, { tables: tablesPayload }),
      ]);

      console.log("hours updated", hrsRes);
      console.log("tables updated", tblsRes);

      alert("Restaurant updated successfully!");
      navigate("/managerDashboard");
    } catch (err) {
      console.error("Update failed:", err);
      alert("Error updating restaurant.");
    }
  };

  if (!restaurant) return <div>Loading...</div>;

  return (
    <div className="add-restaurant-bg">
      <div className="add-restaurant-overlay">
        <div className="add-restaurant-container">
          <h2>Update Restaurant</h2>
          <form onSubmit={handleSubmit} className="restaurant-form" noValidate>
            {/* Name */}
            <div className="form-group">
              <input
                name="name"
                value={restaurant.name}
                onChange={handleChange}
                placeholder="Name"
              />
            </div>

            {/* Description */}
            <div className="form-group">
              <textarea
                name="description"
                value={restaurant.description}
                onChange={handleChange}
                placeholder="Description"
                className="selectDescription"
              />
            </div>

            {/* Cuisine Type */}
            <div className="form-group">
              <select
                name="cuisine_type"
                value={restaurant.cuisine_type}
                onChange={handleChange}
                className="selectDescription"
              >
                <option value="italian">Italian</option>
                <option value="chinese">Chinese</option>
                <option value="indian">Indian</option>
                <option value="japanese">Japanese</option>
                <option value="mexican">Mexican</option>
                <option value="french">French</option>
                <option value="american">American</option>
                <option value="thai">Thai</option>
                <option value="mediterranean">Mediterranean</option>
                <option value="other">Other</option>
              </select>
            </div>

            {/* Address */}
            <div className="form-group">
              <input
                name="address_line1"
                value={restaurant.address_line1}
                onChange={handleChange}
                placeholder="Address Line 1"
              />
            </div>
            <div className="form-group">
              <input
                name="address_line2"
                value={restaurant.address_line2}
                onChange={handleChange}
                placeholder="Address Line 2"
              />
            </div>

            {/* City, State, Zip */}
            <div className="form-group">
              <input
                name="city"
                value={restaurant.city}
                onChange={handleChange}
                placeholder="City"
              />
            </div>
            <div className="form-group">
              <input
                name="state"
                value={restaurant.state}
                onChange={handleChange}
                placeholder="State"
              />
            </div>
            <div className="form-group">
              <input
                name="zip_code"
                value={restaurant.zip_code}
                onChange={handleChange}
                placeholder="Zip Code"
              />
            </div>

            {/* Contact */}
            <div className="form-group">
              <input
                name="email"
                value={restaurant.email}
                onChange={handleChange}
                placeholder="Email"
              />
            </div>
            <div className="form-group">
              <input
                name="phone_number"
                value={restaurant.phone_number}
                onChange={handleChange}
                placeholder="Phone Number"
              />
            </div>

            {/* Cost Rating */}
            <div className="form-group">
              <select
                name="cost_rating"
                value={restaurant.cost_rating}
                onChange={handleChange}
                className="selectDescription"
              >
                <option value="">-- Cost Rating --</option>
                <option value="1">$</option>
                <option value="2">$$</option>
                <option value="3">$$$</option>
                <option value="4">$$$$</option>
                <option value="5">$$$$$</option>
              </select>
            </div>

            {/* Availability */}
            <div className="form-group">
              <label>Available Time Slots (30-minute intervals)</label>
              <select
                multiple
                value={restaurant.availability}
                onChange={handleAvailabilityChange}
                className="selectDescription"
                size={6}
              >
                {generateTimeOptions().map((time) => (
                  <option key={time} value={time}>
                    {time}
                  </option>
                ))}
              </select>
            </div>

            {/* Operating Hours */}
            <div className="form-group">
              <label>Operating Hours</label>
              {restaurant.operating_hours.map((h, idx) => (
                <div key={idx} className="hours-row">
                  <select
                    value={h.day_of_week}
                    onChange={(e) =>
                      handleHoursChange(idx, "day_of_week", e.target.value)
                    }
                    className="selectDescription"
                  >
                    <option value="">Day of Week</option>
                    {daysOfWeek.map((d) => (
                      <option key={d} value={d}>
                        {d}
                      </option>
                    ))}
                  </select>
                  <input
                    type="time"
                    value={h.opening_time}
                    onChange={(e) =>
                      handleHoursChange(idx, "opening_time", e.target.value)
                    }
                  />
                  <input
                    type="time"
                    value={h.closing_time}
                    onChange={(e) =>
                      handleHoursChange(idx, "closing_time", e.target.value)
                    }
                  />
                  <button
                    type="button"
                    className="remove-hour-btn"
                    onClick={() => removeOperatingHour(idx)}
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button
                type="button"
                className="add-hour-btn"
                onClick={addOperatingHour}
              >
                + Add Hours
              </button>
            </div>

            {/* Tables Configuration */}
            <div className="form-group">
              <label>Tables Configuration</label>
              {restaurant.tables.map((tbl, idx) => (
                <div key={idx} className="table-row">
                  <input
                    placeholder="Table No."
                    value={tbl.table_number}
                    onChange={(e) =>
                      handleTableChange(idx, "table_number", e.target.value)
                    }
                  />
                  <input
                    type="number"
                    min="1"
                    placeholder="Capacity"
                    value={tbl.capacity}
                    onChange={(e) =>
                      handleTableChange(idx, "capacity", e.target.value)
                    }
                  />
                  <button
                    type="button"
                    className="remove-table-btn"
                    onClick={() => removeTable(idx)}
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button
                type="button"
                className="add-table-btn"
                onClick={addTable}
              >
                + Add Table
              </button>
            </div>

            {/* Submit */}
            <button type="submit" className="submit-button">
              Save
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default UpdateRestaurant;
