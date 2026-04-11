# Glasshouse 🔍 
A static privacy and security analysis tool for websites. Paste a URL, get a report.
## Why I Built This
Targeted advertising has always been suspicious. But something shifted when major platforms started introducing “child safety” features that (conveniently) also gave them a cleaner excuse to be less subtle about their tracking infrastructure. The surveillance never stop, it just got rebranded.
As someone who grew up on the internet and genuinely cares about what happens in that space, I wanted a tool that could pull back the curtain a little. Not a VPN ad. Not a cookie banner blocker. Something that actually shows you what a site is doing on the initial load and calls it out plainly.
This is that tool.
## What It Checks
- Trackers: known advertising and analytics scripts embedded in page HTML
- Security Headers: CSP, X-Frame-Options, HTTPS
- Fingerprinting: libraries that build a unique profile of your browser without cookies
- Cookies: whether cookies have proper Secure, HttpOnly and SameSite flags
- Risk Score: Low, Medium or High based on findings
## Findings Worth Mentioning
Notably, a large volunteer-run nonprofit platform scored Low Risk with no findings, while several major corporate sites got flagged with Medium or even High Risk, which suggests that privacy hygiene often correlates more with organizational values than resources.
## Installation
You can access the live version at https://glasshouse-tool.onrender.com/, or if you'd prefer to locally run it:
```bash
git clone https://github.com/mariam-elshoura05/Glasshouse
cd Glasshouse
pip3 install -r requirements.txt --break-system-packages
python3 app.py
```
## Limitations
- This tool only does static analysis, so dynamically loaded scripts via JavaScript are not detected
- Tracker database is manually maintained and not exhaustive
- Cookie analysis only covers cookies set on initial page load
## Planned
- Browser extension (v2)
- Expanded tracker database
- Dynamic analysis via headless browser
