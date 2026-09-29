import ipaddress,socket
from urllib.parse import urljoin,urlparse,urldefrag
import httpx
from bs4 import BeautifulSoup
from .config import REQUEST_TIMEOUT,MAX_PAGES

def _public(host):
    if not host:return False
    try:
        for info in socket.getaddrinfo(host,None):
            ip=ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:return False
    except Exception:return False
    return True

def validate_url(url):
    p=urlparse(url)
    if p.scheme not in {'http','https'}:raise ValueError('Only http and https URLs are allowed.')
    if p.username or p.password:raise ValueError('URLs containing credentials are not allowed.')
    if not _public(p.hostname):raise ValueError('The target host is not a public address.')
    return url

def crawl(start_url,max_pages=None):
    start_url=validate_url(start_url); limit=max_pages or MAX_PAGES
    host=urlparse(start_url).hostname.lower(); queue=[start_url]; seen=set(); pages=[]
    headers={'User-Agent':'AI-Ads-Readiness-Bot/1.0'}
    with httpx.Client(timeout=REQUEST_TIMEOUT,follow_redirects=False,headers=headers) as client:
        while queue and len(pages)<limit:
            url=urldefrag(queue.pop(0))[0]
            if url in seen:continue
            seen.add(url)
            try:
                validate_url(url); r=client.get(url)
                if r.status_code in {301,302,303,307,308}:
                    loc=r.headers.get('location'); target=urljoin(url,loc) if loc else None
                    if target and urlparse(target).hostname==host:validate_url(target);queue.append(target)
                    continue
                if r.status_code>=400 or 'text/html' not in r.headers.get('content-type',''):continue
                html=r.text[:2000000]; soup=BeautifulSoup(html,'html.parser')
                title=soup.title.get_text(' ',strip=True) if soup.title else ''
                meta=soup.find('meta',attrs={'name':'description'}); desc=meta.get('content','').strip() if meta else ''
                text=soup.get_text(' ',strip=True)
                links=[]
                for a in soup.find_all('a',href=True):
                    target=urldefrag(urljoin(url,a['href']))[0]; p=urlparse(target)
                    if p.scheme in {'http','https'} and p.hostname==host and target not in seen and target not in queue:queue.append(target)
                    if p.hostname==host:links.append(target)
                pages.append({'url':url,'status':r.status_code,'title':title,'description':desc,'text':text[:100000],'html':html,'links':links[:100]})
            except Exception:continue
    return pages
