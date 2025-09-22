import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse

def crawl_website(start_url, max_pages=200):
    urls_to_visit = {start_url}
    visited_urls = set()
    scraped_data = []
    
    domain = urlparse(start_url).netloc
    
    print(f"--- Starting Crawl on {domain} ---")

    while urls_to_visit and len(visited_urls) < max_pages:
        url = urls_to_visit.pop()
        
        if url in visited_urls:
            continue

        print(f"\n---> Visiting: {url}")
        visited_urls.add(url)

        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"  -> Failed to fetch {url}: {e}")
            continue
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        page_title = soup.title.string if soup.title else "No Title"
        
        main_content = soup.find("div", class_="elementor-page")
        if not main_content:
            main_content = soup.body
        
        for script_or_style in main_content(['script', 'style', 'header', 'footer', 'nav']):
            script_or_style.decompose()

        page_text = main_content.get_text(separator='\n', strip=True)

        if page_text:
            print(f"  -> Scraped '{page_title}' ({len(page_text)} chars)")
            scraped_data.append({
                "url": url,
                "title": page_title.strip(),
                "content": page_text
            })
        
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            full_url = urljoin(url, link)
            parsed_url = urlparse(full_url)
            
            clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            
            if (
                parsed_url.netloc == domain and
                clean_url not in visited_urls and
                clean_url not in urls_to_visit and
                not clean_url.endswith(('.pdf', '.jpg', '.png', '.zip'))
            ):
                urls_to_visit.add(clean_url)

    return scraped_data

if __name__ == '__main__':
    start_url = "https://amadisglobal.com/"
    all_content = crawl_website(start_url)
    file_json = 'scraped_content.json'

    with open(file_json, 'w', encoding='utf-8') as f:
        json.dump(all_content, f, indent=4, ensure_ascii=False)
        
    print(f"\n\nCrawling complete. Scraped {len(all_content)} pages.")
    print(f"Full site content saved to {file_json}")
