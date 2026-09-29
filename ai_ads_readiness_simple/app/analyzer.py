import uuid
from datetime import datetime,timezone
from urllib.parse import urlparse
from .crawler import crawl

def analyze_website(url,max_pages=10):
    pages=crawl(url,max_pages); pid=uuid.uuid4().hex[:12]
    home=pages[0] if pages else {'title':'','description':'','text':'','html':''}
    text='\n'.join(p['text'] for p in pages).lower(); html='\n'.join(p['html'] for p in pages).lower()
    has=lambda *xs:any(x in text for x in xs)
    schema=any(x in html for x in ['application/ld+json','schema.org']); faq=has('faq','frequently asked','questions')
    pricing=has('pricing','price','cost'); cta=has('book','buy','demo','trial','get started','contact sales','request')
    trust=sum(x in text for x in ['about','contact','privacy','terms','security','testimonial','case study'])>=2
    audience=sum(x in text for x in ['enterprise','small business','developers','marketers','teams','businesses'])>=2
    product=sum(x in text for x in ['product','products','features','solution','solutions','service','services'])>=2
    commercial=sum(x in text for x in ['buy','price','pricing','cost','quote','demo','trial','order','book','contact sales'])>=3
    scores={
      'ai_readiness':min(100,30+len(pages)*4+(20 if product else 0)+(20 if audience else 0)),
      'ai_search_readiness':min(100,35+(20 if schema else 0)+(20 if faq else 0)+(15 if product else 0)),
      'commercial_intent':min(100,25+(35 if commercial else 0)+(20 if pricing else 0)+(15 if cta else 0)),
      'content_quality':min(100,30+(25 if home['title'] else 0)+(20 if home['description'] else 0)+(20 if len(text)>3000 else 0)),
      'structured_data':85 if schema else 20,'crawler_accessibility':80 if pages else 10,
      'conversion_readiness':min(100,30+(30 if cta else 0)+(20 if pricing else 0)+(15 if trust else 0)),
      'ai_advertising_opportunity':min(100,25+(25 if commercial else 0)+(20 if product else 0)+(15 if audience else 0))}
    rec=[]
    if not schema:rec.append('Add relevant Organization, Product/Service, WebSite, BreadcrumbList and FAQ structured data.')
    if not faq:rec.append('Create a concise FAQ covering customer questions, objections and use cases.')
    if not pricing:rec.append('Make pricing, starting price, quote rules or a clear pricing path easier to understand.')
    if not audience:rec.append('Clearly describe target audiences, industries, roles and use cases.')
    if not cta:rec.append('Add explicit conversion actions such as demo, trial, quote, booking or contact sales.')
    if not trust:rec.append('Strengthen trust information with company details, contact information, security/privacy material or case studies.')
    if not rec:rec.append('Maintain clear product, audience, pricing, trust and structured-data signals and review them regularly.')
    intents=[{'intent':'informational_research','priority':'medium'}]
    if commercial:intents.insert(0,{'intent':'pricing_purchase','priority':'high'})
    if cta:intents.append({'intent':'demo_or_contact','priority':'medium'})
    return {'project_id':pid,'url':url,'title':home['title'],'description':home['description'],'pages_crawled':len(pages),'scores':scores,'signals':{'https':urlparse(url).scheme=='https','structured_data_detected':schema,'faq_detected':faq,'pricing_detected':pricing,'conversion_cta_detected':cta,'trust_signals_detected':trust,'audience_signals_detected':audience,'product_service_signals_detected':product},'recommendations':rec,'commercial_intents':intents,'created_at':datetime.now(timezone.utc).isoformat()}
