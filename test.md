# Analytics API

`Base URL: https://salmakhalill.pythonanywhere.com`

Both dashboard endpoints require an active authenticated user. Inactive users get empty objects back even with a valid token.

---

### `GET /analytics/recent/` — recent dashboard

The main dashboard view. Returns KPI cards with trend comparisons and a time-bucketed bar chart.

**Query params:**

| Param | Default | Options |
|---|---|---|
| `period` | `daily` | `daily` · `weekly` · `monthly` |
| `year` | — | Filter by year |
| `location` | — | Case-insensitive substring match |

**Response:**
```json
{
  "kpis": {
    "total_reports":    { "value": 401, "change": 100.0, "trend": "زيادة" },
    "new_reports":      { "value": 68,  "change": 100.0, "trend": "زيادة" },
    "under_review":     { "value": 122, "change": 0,     "trend": "لا تغيير" },
    "critical_reports": { "value": 29,  "change": 0,     "trend": "لا تغيير" }
  },
  "charts": {
    "bar_chart": {
      "الاثنين": 12, "الثلاثاء": 8, "الأربعاء": 15,
      "الخميس": 9,  "الجمعة": 6,  "السبت": 11, "الأحد": 7
    },
    "status_distribution": { "تم استلام البلاغ": 14, "قيد المراجعة": 22 },
    "heatmap": [{ "latitude": 30.0444, "longitude": 31.2357 }]
  }
}
```

`trend` is one of: `زيادة` · `انخفاض` · `لا تغيير`

Bar chart keys change with the period:
- `daily` → Arabic day names, last 7 days
- `weekly` → الأسبوع 4 through الأسبوع 1
- `monthly` → Arabic month names, last 12 months

---

### `GET /analytics/stats/` — statistics tab

Filterable by year. Returns all-time KPIs and full distribution charts instead of the recent-period view.

**Response:**
```json
{
  "kpis": {
    "total_reports": 401,
    "top_report_type": "تحرش",
    "solved_percentage": 18.5,
    "top_region": "القاهرة"
  },
  "charts": {
    "monthly_reports": { "يناير": 28, "فبراير": 35 },
    "report_type_distribution": { "تحرش": 130, "اعتداء": 98 },
    "case_status_distribution": { "تم استلام البلاغ": 68, "قيد المراجعة": 122 },
    "heatmap": [{ "latitude": 30.0444, "longitude": 31.2357 }]
  }
}
```

---

### `GET /analytics/site_stats/` — public stats

No authentication. Used by the public portal landing page.

```json
{
  "site_stats": {
    "received_reports": 68,
    "in_progress_reports": 94,
    "closed_reports": 43,
    "collaborating_entities": 20
  }
}
```

`collaborating_entities` is a fixed value for now.
