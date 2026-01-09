<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
    <xsl:output method="html" encoding="UTF-8" />
    <xsl:template match="/">
        <html>
            <head>
                <title>XML Sitemap</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
                        color: #333;
                        margin: 0;
                        padding: 2rem;
                        background: #f8fafc;
                    }
                    .container {
                        max-width: 1000px;
                        margin: 0 auto;
                        background: #fff;
                        padding: 2rem;
                        border-radius: 8px;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                    }
                    h1 {
                        color: #0f172a;
                        margin-bottom: 0.5rem;
                    }
                    p.desc {
                        color: #64748b;
                        margin-bottom: 2rem;
                    }
                    a {
                        color: #2563eb;
                        text-decoration: none;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 1rem;
                    }
                    th {
                        background: #f1f5f9;
                        text-align: left;
                        padding: 1rem;
                        font-weight: 600;
                        color: #475569;
                        border-bottom: 1px solid #e2e8f0;
                    }
                    td {
                        padding: 1rem;
                        border-bottom: 1px solid #e2e8f0;
                        color: #334155;
                    }
                    tr:hover {
                        background: #f8fafc;
                    }
                    .badge {
                        display: inline-block;
                        padding: 0.25rem 0.5rem;
                        border-radius: 4px;
                        font-size: 0.85rem;
                        font-weight: 500;
                    }
                    .badge-high { background: #dcfce7; color: #166534; }
                    .badge-med { background: #e0f2fe; color: #075985; }
                    .badge-low { background: #f1f5f9; color: #64748b; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>XML Sitemap</h1>
                    <xsl:if test="count(s:sitemapindex/s:sitemap) &gt; 0">
                        <p class="desc">
                            This is a <strong>Sitemap Index</strong>. It points to other sitemaps containing the actual URLs.
                        </p>
                        <table>
                            <thead>
                                <tr>
                                    <th>Sitemap URL</th>
                                    <th>Last Modified</th>
                                </tr>
                            </thead>
                            <tbody>
                                <xsl:for-each select="s:sitemapindex/s:sitemap">
                                    <tr>
                                        <td><a href="{s:loc}"><xsl:value-of select="s:loc"/></a></td>
                                        <td><xsl:value-of select="s:lastmod"/></td>
                                    </tr>
                                </xsl:for-each>
                            </tbody>
                        </table>
                    </xsl:if>

                    <xsl:if test="count(s:urlset/s:url) &gt; 0">
                        <p class="desc">
                            This is a <strong>URL Set</strong>. It lists the actual pages on the website.
                        </p>
                        <table>
                            <thead>
                                <tr>
                                    <th>Location</th>
                                    <th>Last Modified</th>
                                    <th>Change Freq</th>
                                    <th>Priority</th>
                                </tr>
                            </thead>
                            <tbody>
                                <xsl:for-each select="s:urlset/s:url">
                                    <tr>
                                        <td><a href="{s:loc}"><xsl:value-of select="s:loc"/></a></td>
                                        <td><xsl:value-of select="s:lastmod"/></td>
                                        <td><xsl:value-of select="s:changefreq"/></td>
                                        <td>
                                            <xsl:variable name="p" select="s:priority"/>
                                            <span>
                                                <xsl:attribute name="class">
                                                    <xsl:choose>
                                                        <xsl:when test="$p &gt;= 0.8">badge badge-high</xsl:when>
                                                        <xsl:when test="$p &gt;= 0.5">badge badge-med</xsl:when>
                                                        <xsl:otherwise>badge badge-low</xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:attribute>
                                                <xsl:value-of select="$p"/>
                                            </span>
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </tbody>
                        </table>
                    </xsl:if>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
