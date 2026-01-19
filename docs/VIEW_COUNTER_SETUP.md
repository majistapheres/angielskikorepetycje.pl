# Cloudflare D1 View Counter - Setup Guide

This guide explains how to set up the view counter using Cloudflare D1.

## Prerequisites

1. **Wrangler CLI** - Install if not already:
   ```bash
   npm install -g wrangler
   ```

2. **Cloudflare Account** - You need to be logged in:
   ```bash
   wrangler login
   ```

## Step 1: Create the D1 Database

Run this command in the project root:

```bash
wrangler d1 create blog-views
```

This will output something like:
```
Created database 'blog-views' with id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Step 2: Update wrangler.toml

Copy the database ID from the output and update `wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "blog-views"
database_id = "YOUR_DATABASE_ID_HERE"  # <-- Replace with actual ID
```

## Step 3: Initialize the Database Schema

Run the schema migration:

```bash
wrangler d1 execute blog-views --file=./db/schema.sql
```

## Step 4: Deploy to Cloudflare Pages

Push your changes to Git. The Pages Function at `/functions/api/views.js` will automatically be deployed.

```bash
git add .
git commit -m "Add D1 view counter"
git push
```

## Step 5: Bind D1 to Pages Project (Cloudflare Dashboard)

1. Go to **Cloudflare Dashboard** > **Pages** > **Your Project**
2. Click **Settings** > **Functions**
3. Under **D1 database bindings**, click **Add binding**
4. Set:
   - Variable name: `DB`
   - D1 database: `blog-views`
5. Save and redeploy

## Testing Locally

You can test locally with:

```bash
wrangler pages dev ./ --d1=DB=blog-views
```

## File Structure

```
project/
├── wrangler.toml           # D1 configuration
├── db/
│   └── schema.sql          # Database schema
├── functions/
│   └── api/
│       └── views.js        # API endpoint (Cloudflare Pages Function)
└── js/
    └── view-counter.js     # Client-side script
```

## How It Works

1. When a blog page loads, `view-counter.js` runs
2. It checks localStorage to prevent spam (30-min cooldown)
3. If new visit: POST to `/api/views` (increments count)
4. If repeat visit: GET from `/api/views` (just displays count)
5. Count appears next to the date: "19 Sty 2026 • 12 min czytania • 156 wyświetleń"

## Troubleshooting

### "Database not configured" error
- Make sure D1 is bound in Cloudflare Dashboard > Pages > Settings > Functions

### View count not showing
- Check browser console for errors
- Verify the script is loaded: `<script src="/js/view-counter.js" defer></script>`
- Check that the page URL contains `/wiedza/`

### Local development
- Use `wrangler pages dev` with D1 binding for local testing
