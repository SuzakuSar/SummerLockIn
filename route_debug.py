# Save this as route_debug.py in your project root

"""
This script loads your Flask app and prints all registered routes.
Run it with: python route_debug.py
"""

from website import create_app

app = create_app()

# Print all registered rules in the app
print("\n===== ALL REGISTERED ROUTES =====")
for rule in app.url_map.iter_rules():
    methods = ','.join(sorted(rule.methods))
    print(f"{rule.endpoint:50s} {methods:20s} {rule}")

# Check specifically for hangman and guessing_game routes
print("\n===== CHECKING FOR CONFLICTS =====")
hangman_routes = []
guessing_routes = []

for rule in app.url_map.iter_rules():
    if 'hangman' in rule.endpoint:
        hangman_routes.append(rule)
    if 'guessing' in rule.endpoint:
        guessing_routes.append(rule)

print(f"\nHangman Routes ({len(hangman_routes)}):")
for rule in hangman_routes:
    print(f"  {rule.endpoint} -> {rule}")

print(f"\nGuessing Game Routes ({len(guessing_routes)}):")
for rule in guessing_routes:
    print(f"  {rule.endpoint} -> {rule}")

# Check for URL pattern conflicts
print("\n===== CHECKING FOR URL PATTERN CONFLICTS =====")
all_urls = {}

for rule in app.url_map.iter_rules():
    # Strip variable parts from the URL pattern
    base_url = str(rule)
    base_url = base_url.split('<')[0].rstrip('/')
    
    if base_url in all_urls:
        all_urls[base_url].append(rule.endpoint)
    else:
        all_urls[base_url] = [rule.endpoint]

print("\nPotential conflicts (same base URL pattern):")
for url, endpoints in all_urls.items():
    if len(endpoints) > 1:
        print(f"  URL: {url}")
        for endpoint in endpoints:
            print(f"    - {endpoint}")

print("\n===== END OF ROUTE ANALYSIS =====")