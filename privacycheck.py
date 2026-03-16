import requests
from bs4 import BeautifulSoup
import re
import sys

def get_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        sys.exit(1)

TRACKERS = {
    "Google Analytics": ["google-analytics.com", "googletagmanager.com", "gtag/js"],
    "Meta Pixel": ["connect.facebook.net", "fbevents.js"],
    "TikTok": ["analytics.tiktok.com", "tiktok-pixel"],
    "Twitter/X": ["static.ads-twitter.com", "twq.js"],
    "LinkedIn": ["snap.licdn.com", "linkedin.com/px"],
    "Hotjar": ["static.hotjar.com"],
    "Mixpanel": ["cdn.mxpnl.com", "mixpanel.com"],
}

def check_trackers(soup, response_text):
    found = []
    for name, patterns in TRACKERS.items():
        for pattern in patterns:
            if pattern in response_text:
                found.append(name)
                break
    return found

def check_headers(response):
    headers = response.headers
    results = []
    
    if "Content-Security-Policy" not in headers:
        results.append("❌ Missing Content-Security-Policy")
    else:
        results.append("✅ Content-Security-Policy present")
        
    if "X-Frame-Options" not in headers:
        results.append("❌ Missing X-Frame-Options")
    else:
        results.append("✅ X-Frame-Options present")

    if response.url.startswith("https://"):
        results.append("✅ HTTPS enabled")
    else:
        results.append("❌ No HTTPS")
        
    return results

FINGERPRINTERS = {
    "FingerprintJS": ["fingerprintjs", "fpjs", "fingerprint.com"],
    "Canvas Fingerprinting": ["toDataURL", "getImageData"],
    "AudioContext Fingerprinting": ["AudioContext", "OfflineAudioContext"],
    "WebRTC Fingerprinting": ["RTCPeerConnection"],
}

def check_fingerprinting(response_text):
    found = []
    for name, patterns in FINGERPRINTERS.items():
        for pattern in patterns:
            if pattern in response_text:
                found.append(name)
                break
    return found

def check_cookies(response):
    results = []
    cookies = response.cookies
    
    if not cookies:
        results.append("✅ No cookies set on initial load")
        return results
    
    for cookie in cookies:
        if not cookie.secure:
            results.append(f"⚠️  Cookie '{cookie.name}' missing Secure flag")
        if not cookie.has_nonstandard_attr("HttpOnly"):
            results.append(f"⚠️  Cookie '{cookie.name}' missing HttpOnly flag")
        if not cookie.has_nonstandard_attr("SameSite"):
            results.append(f"⚠️  Cookie '{cookie.name}' missing SameSite flag")
    
    if not results:
        results.append(f"✅ {len(cookies)} cookie(s) found with proper security flags")
    
    return results

def calculate_risk(trackers, header_results, fingerprints, cookie_results):
    score = 0
    
    score += len(trackers) * 2
    
    for r in header_results:
        if "❌" in r:
            score += 1
            
    score += len(fingerprints) * 2
    
    for r in cookie_results:
        if "⚠️" in r:
            score += 1
    
    if score == 0:
        return "🟢 Low Risk"
    elif score <= 3:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 privacycheck.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"\n🔍 Scanning {url}...\n")
    response = get_page(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    trackers = check_trackers(soup, response.text)
    if trackers:
        print(f"⚠️  Trackers found: {', '.join(trackers)}")
    else:
        print("✅ No known trackers detected")
    headers_results = check_headers(response)
    for result in headers_results:
        print(result)
    fingerprints = check_fingerprinting(response.text)
    if fingerprints:
        print(f"⚠️  Fingerprinting detected: {', '.join(fingerprints)}")
    else:
        print("✅ No fingerprinting detected")
    cookie_results = check_cookies(response)
    for result in cookie_results:
        print(result)
    risk = calculate_risk(trackers, headers_results, fingerprints, cookie_results)
    print(f"\n── Risk Assessment ──")
    print(f"Overall: {risk}")

if __name__ == "__main__":
    main()