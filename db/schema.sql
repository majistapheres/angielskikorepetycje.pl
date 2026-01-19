-- D1 Schema for Blog View Counter
-- Run: wrangler d1 execute blog-views --file=./db/schema.sql

CREATE TABLE IF NOT EXISTS page_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    views INTEGER DEFAULT 0,
    first_view DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_view DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create index for fast URL lookups
CREATE INDEX IF NOT EXISTS idx_url ON page_views(url);
