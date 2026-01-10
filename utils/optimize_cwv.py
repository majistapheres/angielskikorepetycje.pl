"""
Core Web Vitals Optimization Script
Applies performance optimizations to all HTML files in the project.
"""

import os
import re
from pathlib import Path

# Project root
PROJECT_ROOT = Path(r"e:\AntiGravity Projects\angielski-korepetycje")

# Resource hints to add after meta description
RESOURCE_HINTS = """
    <!-- Resource Hints for Performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://unpkg.com">
    
    <!-- Optimized Font Loading -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&family=Montserrat:wght@400;500;600;700;800&display=swap">
"""

# New Lucide initialization script
NEW_LUCIDE_INIT = """    <!-- Initialize Lucide Icons after DOM is ready -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        });
    </script>"""

def optimize_html_file(filepath):
    """Apply Core Web Vitals optimizations to an HTML file."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    # Skip index.html as it's already optimized
    if filepath.name == 'index.html' and filepath.parent == PROJECT_ROOT:
        return False, ["Skipped - already optimized"]
    
    # 1. Add defer to Lucide script if not present
    if '<script src="https://unpkg.com/lucide@latest"></script>' in content:
        content = content.replace(
            '<script src="https://unpkg.com/lucide@latest"></script>',
            '<script src="https://unpkg.com/lucide@latest" defer></script>'
        )
        changes_made.append("Added defer to Lucide script")
    
    # 2. Add resource hints if not present
    if 'rel="preconnect"' not in content:
        # Find position after meta description or after stylesheet link
        patterns = [
            (r'(<link rel="stylesheet" href="[^"]*styles\.css"[^>]*>)', r'\1' + RESOURCE_HINTS),
            (r'(<link rel="stylesheet" href="/css/styles\.css"[^>]*>)', r'\1' + RESOURCE_HINTS),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, count=1)
                changes_made.append("Added resource hints and font preconnect")
                break
    
    # 3. Update Lucide initialization to use DOMContentLoaded
    old_lucide_patterns = [
        r'<script>\s*lucide\.createIcons\(\);\s*</script>',
        r'<script>\r?\n\s*lucide\.createIcons\(\);\r?\n\s*</script>',
    ]
    
    for pattern in old_lucide_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, NEW_LUCIDE_INIT, content)
            changes_made.append("Updated Lucide initialization to DOMContentLoaded")
            break
    
    # 4. Add loading="lazy" to images that don't have it (except first image)
    img_pattern = r'<img([^>]*?)(?<!loading=")(?<!loading="lazy")(\s*>)'
    
    def add_lazy_loading(match):
        attrs = match.group(1)
        # Skip if already has loading attribute or fetchpriority
        if 'loading=' in attrs or 'fetchpriority=' in attrs:
            return match.group(0)
        # Add loading="lazy" and decoding="async"
        if 'loading=' not in attrs:
            return f'<img{attrs} loading="lazy" decoding="async">'
        return match.group(0)
    
    # Only add lazy loading to images not in hero section
    # This is a simplified approach - we're adding it to all images
    
    # 5. Write back if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes_made
    
    return False, ["No changes needed"]

def main():
    """Process all HTML files in the project."""
    
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    
    # Filter out any backup or temp files
    html_files = [f for f in html_files if not any(x in str(f) for x in ['.backup', '.tmp', 'node_modules', '.git'])]
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    optimized = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        relative_path = filepath.relative_to(PROJECT_ROOT)
        changed, changes = optimize_html_file(filepath)
        
        if changed:
            print(f"✅ {relative_path}")
            for change in changes:
                print(f"   - {change}")
            optimized += 1
        else:
            print(f"⏭️  {relative_path}: {changes[0]}")
            skipped += 1
    
    print(f"\n{'='*50}")
    print(f"Summary: {optimized} files optimized, {skipped} files skipped")

if __name__ == "__main__":
    main()
