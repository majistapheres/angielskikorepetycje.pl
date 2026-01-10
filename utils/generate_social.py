import os
import re
import json
import requests # Requires: pip install requests

# Configuration
BASE_URL = "https://angielskikorepetycje.pl"
HISTORY_FILE = "posted_history.json"

# Secrets (Set these in your environment variables or replace here for testing)
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")

def clean_html(text):
    """Removes HTML tags and extra whitespace."""
    if not text: return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_recent_posted_links():
    """
    Fetches the last 25 posts from the Facebook Page to avoid duplicates.
    Returns a set of URLs that have already been posted.
    """
    if not FB_PAGE_TOKEN or not FB_PAGE_ID:
        return set()

    url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/feed"
    params = {
        'fields': 'link',
        'limit': 25,
        'access_token': FB_PAGE_TOKEN
    }
    
    known_links = set()
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        for post in data.get('data', []):
            if 'link' in post:
                # Normalize link (remove query params, trailing slashes if needed)
                clean_link = post['link'].split('?')[0].rstrip('/')
                known_links.add(clean_link)
                
        print(f"📡 Found {len(known_links)} recent links on Facebook Page.")
        return known_links
    except Exception as e:
        print(f"⚠️ Could not fetch recent posts: {e}")
        return set()

def post_to_facebook(message, link):
    """
    Posts content to Facebook Page via Graph API.
    Returns True if successful, False otherwise.
    """
    if not FB_PAGE_TOKEN or not FB_PAGE_ID:
        print(f"⚠️  [Dry Run] Would post to FB: {link}")
        return True 

    url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/feed"
    payload = {
        'message': message,
        'link': link,
        'access_token': FB_PAGE_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(f"✅ Posted to Facebook: {link}")
        return True
    except Exception as e:
        print(f"❌ Error posting to Facebook: {e}")
        return False

def parse_blog_post(filepath, wiedza_root):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Title
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        title = clean_html(title_match.group(1)) if title_match else "Unknown Title"

        # 2. URL
        rel_path = os.path.relpath(filepath, os.path.join(wiedza_root, ".."))
        rel_path = rel_path.replace("\\", "/")
        if rel_path.endswith(".html"):
            url = f"{BASE_URL}/{rel_path[:-5]}"
        else:
            url = f"{BASE_URL}/{rel_path}"
        
        # 3. Intro Paragraph
        body_match = re.search(r'<div class="blog-article-body">\s*(.*?)\s*(?:<hr|<div class="|<h2>)', content, re.DOTALL) 
        intro = ""
        snippet = ""
        
        if body_match:
            body_content = body_match.group(1)
            paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', body_content, re.DOTALL)
            if paragraphs:
                intro = clean_html(paragraphs[0])
                if len(paragraphs) > 1:
                     snippet = clean_html(paragraphs[1])
        
        # 4. Pro Tip
        pro_tip = ""
        tip_match = re.search(r'<div class="blog-pro-tip"[^>]*>(.*?)</div>', content, re.DOTALL)
        if tip_match:
            raw_tip = tip_match.group(1)
            raw_tip = re.sub(r'<h4.*?>.*?</h4>', '', raw_tip, flags=re.DOTALL)
            pro_tip = clean_html(raw_tip)

        return {
            "title": title,
            "url": url,
            "intro": intro,
            "snippet": snippet,
            "pro_tip": pro_tip
        }

    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None

def generate_post_content(data):
    post = []
    
    # Headline
    post.append(f"🎓 {data['title']}") # Removed bold markdown for FB plaintext compatibility check
    
    # Intro
    if data['intro']:
        post.append(f"\n{data['intro']}")
    
    # Snippet or Pro Tip
    if data['pro_tip']:
        post.append(f"\n💡 Pro Tip: {data['pro_tip']}")
    elif data['snippet']:
        post.append(f"\n👀 {data['snippet']}")
        
    # Hashtags
    tags = ["#Angielski", "#Wrocław", "#NaukaJezyka", "#AdrianEkrem"]
    if "matura" in data['url']: tags.append("#Matura2026")
    if "praca" in data['url']: tags.append("#BusinessEnglish")
    
    post.append("\n" + " ".join(tags))
    
    return "\n".join(post)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    wiedza_dir = os.path.abspath(os.path.join(base_dir, "..", "wiedza"))
    output_path = os.path.join(base_dir, "..", "social_media_drafts.md")
    
    # Check what is already live on Facebook
    already_posted_links = get_recent_posted_links()
    
    new_posts_buffer = []
    
    print(f"🔍 Scanning for UNPUBLISHED posts in: {wiedza_dir}")

    if not os.path.exists(wiedza_dir):
        print(f"ERROR: Directory not found: {wiedza_dir}")
        return

    for root, dirs, files in os.walk(wiedza_dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                
                # We need the URL to check if it's posted
                # Parse minimally just to get URL first? Or full parse?
                # Full parse is cheap for static generator
                data = parse_blog_post(filepath, wiedza_dir)
                
                if not data or not data['url']:
                    continue
                    
                # Duplicate Check logic
                clean_url = data['url'].split('?')[0].rstrip('/')
                if clean_url in already_posted_links:
                    # Already on FB
                    continue
                    
                print(f"🆕 New unposted article found: {file}")
                
                # Generate content
                fb_message = generate_post_content(data)
                
                # Try to Post (or simulate)
                if post_to_facebook(fb_message, data['url']):
                    new_posts_buffer.append(f"### [PUBLISHED/SIMULATED] {file}\n\n{fb_message}\n\n👉 {data['url']}\n\n---\n")

    # Append logs
    if new_posts_buffer:
        with open(output_path, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(new_posts_buffer))
        print(f"✨ Successfully processed {len(new_posts_buffer)} new posts.")
    else:
        print("✅ No new posts found. Facebook is up to date.")

if __name__ == "__main__":
    main()
