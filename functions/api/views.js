/**
 * Cloudflare Pages Function: View Counter API
 * 
 * Endpoints:
 * - GET /api/views?url=/path/to/page  -> Returns view count
 * - POST /api/views { url: "/path/to/page" } -> Increments and returns view count
 */

export async function onRequest(context) {
    const { request, env } = context;
    const url = new URL(request.url);

    // CORS headers for all responses
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    };

    // Handle preflight requests
    if (request.method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders });
    }

    try {
        // Check if D1 is bound
        if (!env.DB) {
            return new Response(
                JSON.stringify({ error: 'Database not configured' }),
                { status: 500, headers: corsHeaders }
            );
        }

        if (request.method === 'GET') {
            // GET: Retrieve view count for a URL
            const pageUrl = url.searchParams.get('url');

            if (!pageUrl) {
                return new Response(
                    JSON.stringify({ error: 'Missing url parameter' }),
                    { status: 400, headers: corsHeaders }
                );
            }

            const result = await env.DB.prepare(
                'SELECT views FROM page_views WHERE url = ?'
            ).bind(pageUrl).first();

            return new Response(
                JSON.stringify({ url: pageUrl, views: result?.views || 0 }),
                { headers: corsHeaders }
            );

        } else if (request.method === 'POST') {
            // POST: Increment view count
            const body = await request.json().catch(() => ({}));
            const pageUrl = body.url || url.searchParams.get('url');

            if (!pageUrl) {
                return new Response(
                    JSON.stringify({ error: 'Missing url in request body' }),
                    { status: 400, headers: corsHeaders }
                );
            }

            // Upsert: Insert or increment view count
            await env.DB.prepare(`
                INSERT INTO page_views (url, views, first_view, last_view)
                VALUES (?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(url) DO UPDATE SET
                    views = views + 1,
                    last_view = CURRENT_TIMESTAMP
            `).bind(pageUrl).run();

            // Get updated count
            const result = await env.DB.prepare(
                'SELECT views FROM page_views WHERE url = ?'
            ).bind(pageUrl).first();

            return new Response(
                JSON.stringify({ url: pageUrl, views: result?.views || 1, incremented: true }),
                { headers: corsHeaders }
            );
        }

        return new Response(
            JSON.stringify({ error: 'Method not allowed' }),
            { status: 405, headers: corsHeaders }
        );

    } catch (error) {
        console.error('View counter error:', error);
        return new Response(
            JSON.stringify({ error: 'Internal server error', message: error.message }),
            { status: 500, headers: corsHeaders }
        );
    }
}
