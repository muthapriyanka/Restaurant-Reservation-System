import React from "react";
import { useNavigate } from "react-router-dom";
import { useForm, useFieldArray, Controller } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import {
  managerAddOperatingHours,
  managerAddRestaurant,
  managerAddTables,
} from "./api/auth";

// Constants
const COST_RATINGS = [1, 2, 3, 4, 5];
const CUISINES = [
  "italian","chinese","indian","japanese","mexican",
  "french","american","thai","mediterranean","other"
];
const DAYS = [
  "Monday","Tuesday","Wednesday","Thursday",
  "Friday","Saturday","Sunday"
];
const TIMES = Array.from({ length: 48 }, (_, i) => {
  const hour = Math.floor(i / 2), min = i % 2 === 0 ? "00" : "30";
  return `${String(hour).padStart(2,"0")}:${min}`;
});

// Validation schema
const schema = yup.object({
  name: yup.string().required(),
  description: yup.string().required(),
  cuisine_type: yup.string().oneOf(CUISINES).required(),
  address_line1: yup.string().required(),
  city: yup.string().required(),
  state: yup.string().required(),
  zip_code: yup.string().required(),
  email: yup.string().email().required(),
  phone_number: yup
    .string()
    .matches(/^\d{10}$/, "Must be 10 digits")
    .required(),
  cost_rating: yup.number().oneOf(COST_RATINGS).required(),
  availability: yup.array().of(yup.string()).min(1),
  operating_hours: yup
    .array()
    .of(
      yup.object({
        day_of_week: yup.string().oneOf(DAYS).required(),
        opening_time: yup.string().oneOf(TIMES).required(),
        closing_time: yup.string().oneOf(TIMES).required(),
      })
    )
    .min(1, "Add at least one operating hours entry"),
  tables: yup
    .array()
    .of(
      yup.object({
        table_number: yup.string().required(),
        capacity: yup.number().min(1).required(),
      })
    )
    .min(1, "Add at least one table"),
});

export default function AddRestaurantForm() {
  const navigate = useNavigate();
  const {
    register,
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      name: "",
      description: "",
      cuisine_type: "italian",
      address_line1: "",
      address_line2: "",
      city: "",
      state: "",
      zip_code: "",
      email: "",
      phone_number: "",
      cost_rating: "",
      availability: [],
      operating_hours: [{ day_of_week: "", opening_time: "", closing_time: "" }],
      tables: [{ table_number: "", capacity: 1 }],
    },
  });

  const { fields: hours, append: addHour, remove: removeHour } =
    useFieldArray({ control, name: "operating_hours" });
  const { fields: tables, append: addTable, remove: removeTable } =
    useFieldArray({ control, name: "tables" });

  const onSubmit = async (data) => {
    try {
      const { operating_hours, tables: tbls, ...basic } = data;
      const { restaurant_id } = await managerAddRestaurant(basic);
      await Promise.all([
        managerAddOperatingHours(restaurant_id, operating_hours),
        managerAddTables(restaurant_id, {
          tables: tbls.map(({ table_number, capacity }) => ({
            table_number,
            capacity: Number(capacity),
            is_active: true,
          })),
        }),
      ]);
      alert("Restaurant submitted successfully!");
      navigate("/managerDashboard");
    } catch {
      alert("Something went wrong while submitting the form.");
    }
  };

  return (
    <div className="add-restaurant-container">
      <h2>Add New Restaurant</h2>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        {/* Basic Info */}
        {[
          { name: "name", placeholder: "Name" },
          { name: "description", placeholder: "Description", as: "textarea" },
        ].map(({ name, placeholder, as = "input" }) => (
          <div key={name} className="form-group">
            {as === "textarea" ? (
              <textarea {...register(name)} placeholder={placeholder} />
            ) : (
              <input {...register(name)} placeholder={placeholder} />
            )}
            {errors[name] && <span className="error">{errors[name].message}</span>}
          </div>
        ))}

        {/* Cuisine */}
        <div className="form-group">
          <select {...register("cuisine_type")}>
            {CUISINES.map((c) => (
              <option key={c} value={c}>
                {c.charAt(0).toUpperCase() + c.slice(1)}
              </option>
            ))}
          </select>
        </div>

        {/* Address */}
        {["address_line1","address_line2","city","state","zip_code"].map((field) => (
          <div key={field} className="form-group">
            <input {...register(field)} placeholder={field.replace(/_/g," ")} />
            {errors[field] && <span className="error">{errors[field].message}</span>}
          </div>
        ))}

        {/* Contact */}
        {[
          { name: "email", type: "email" },
          { name: "phone_number", type: "text", placeholder: "Phone (10 digits)" },
        ].map(({ name, type, placeholder }) => (
          <div key={name} className="form-group">
            <input
              {...register(name)}
              type={type}
              placeholder={placeholder || name}
            />
            {errors[name] && <span className="error">{errors[name].message}</span>}
          </div>
        ))}

        {/* Cost Rating */}
        <div className="form-group">
          <select {...register("cost_rating")}>
            <option value="">-- Cost Rating --</option>
            {COST_RATINGS.map((i) => (
              <option key={i} value={i}>
                {"$".repeat(i)}
              </option>
            ))}
          </select>
          {errors.cost_rating && <span className="error">{errors.cost_rating.message}</span>}
        </div>

        {/* Availability */}
        <div className="form-group">
          <label>Available Time Slots</label>
          <Controller
            control={control}
            name="availability"
            render={({ field }) => (
              <select {...field} multiple size={6}>
                {TIMES.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            )}
          />
          {errors.availability && (
            <span className="error">{errors.availability.message}</span>
          )}
        </div>

        {/* Operating Hours */}
        <fieldset className="form-group">
          <legend>Operating Hours</legend>
          {hours.map((item, idx) => (
            <div key={item.id} className="hours-row">
              <select
                {...register(`operating_hours.${idx}.day_of_week`)}
              >
                <option value="">Day</option>
                {DAYS.map((d) => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
              <input
                type="time"
                {...register(`operating_hours.${idx}.opening_time`)}
              />
              <input
                type="time"
                {...register(`operating_hours.${idx}.closing_time`)}
              />
              <button type="button" onClick={() => removeHour(idx)}>
                Remove
              </button>
              {(errors.operating_hours?.[idx]) && (
                <span className="error">
                  {Object.values(errors.operating_hours[idx])[0]?.message}
                </span>
              )}
            </div>
          ))}
          <button type="button" onClick={() => addHour({ day_of_week:"", opening_time:"", closing_time:"" })}>
            + Add Hours
          </button>
        </fieldset>

        {/* Tables */}
        <fieldset className="form-group">
          <legend>Tables</legend>
          {tables.map((item, idx) => (
            <div key={item.id} className="table-row">
              <input
                {...register(`tables.${idx}.table_number`)}
                placeholder="Table #"
              />
              <input
                type="number"
                min="1"
                {...register(`tables.${idx}.capacity`)}
                placeholder="Capacity"
              />
              <button type="button" onClick={() => removeTable(idx)}>
                Remove
              </button>
              {(errors.tables?.[idx]) && (
                <span className="error">
                  {Object.values(errors.tables[idx])[0]?.message}
                </span>
              )}
            </div>
          ))}
          <button type="button" onClick={() => addTable({ table_number:"", capacity:1 })}>
            + Add Table
          </button>
        </fieldset>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Submitting…" : "Add Restaurant"}
        </button>
      </form>
    </div>
  );
}
