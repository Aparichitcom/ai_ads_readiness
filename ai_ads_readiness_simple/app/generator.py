import json,zipfile
from pathlib import Path
from .config import GENERATED_DIR,DATA_DIR

def save_analysis(a): (DATA_DIR/f"{a['project_id']}.json").write_text(json.dumps(a,indent=2),encoding='utf-8')
def load_analysis(pid):
    p=DATA_DIR/f'{pid}.json'
    if not p.exists():raise FileNotFoundError('Project not found.')
    return json.loads(p.read_text(encoding='utf-8'))
def outdir(pid):
    p=GENERATED_DIR/pid;p.mkdir(parents=True,exist_ok=True);return p
def generate_assets(pid):
    a=load_analysis(pid);o=outdir(pid);base={'project_id':pid,'website':a['url'],'title':a['title'],'description':a['description'],'scores':a['scores'],'signals':a['signals']}
    payload={'ai-business.json':{**base,'type':'business'},'ai-products.json':{**base,'type':'products'},'ai-services.json':{**base,'type':'services'},'ai-faq.json':{**base,'type':'faq'},'ai-use-cases.json':{**base,'type':'use_cases'},'ai-pricing.json':{**base,'type':'pricing'},'ai-ad-config.json':{**base,'type':'application_ad_config','note':'Application-level specification; not an official advertising API.','commercial_intents':a['commercial_intents']},'ai-commercial-intents.json':{'project_id':pid,'intents':a['commercial_intents']},'ai-audience.json':{**base,'type':'audience'},'schema.jsonld':{'@context':'https://schema.org','@type':'Organization','name':a['title'],'url':a['url'],'description':a['description']},'report.json':a}
    for n,d in payload.items():(o/n).write_text(json.dumps(d,indent=2),encoding='utf-8')
    rec='\n'.join('- '+x for x in a['recommendations']); llms=f"# {a['title'] or a['url']}\n\nWebsite: {a['url']}\n\n## Description\n{a['description']}\n\n## Readiness\n{json.dumps(a['scores'],indent=2)}\n\n## Recommended improvements\n{rec}\n"
    (o/'llms.txt').write_text(llms,encoding='utf-8');(o/'llms-full.txt').write_text(llms+'\n## Signals\n'+json.dumps(a['signals'],indent=2)+'\n\n## Commercial intents\n'+json.dumps(a['commercial_intents'],indent=2),encoding='utf-8')
    md='# AI Ads Readiness Report\n\n## Website\n'+a['url']+'\n\n## Scores\n'+'\n'.join(f"- **{k}**: {v}/100" for k,v in a['scores'].items())+'\n\n## Recommendations\n'+rec
    (o/'report.md').write_text(md,encoding='utf-8')
    return sorted(p.name for p in o.iterdir() if p.is_file())
def list_files(pid):return sorted(p.name for p in outdir(pid).iterdir() if p.is_file())
def read_file(pid,name):
    p=Path(name)
    if p.name!=name or '..' in p.parts:raise ValueError('Invalid filename.')
    f=outdir(pid)/name
    if not f.exists() or not f.is_file():raise FileNotFoundError('Generated file not found.')
    return f.read_text(encoding='utf-8')
def make_zip(pid):
    o=outdir(pid)
    if not any(o.iterdir()):generate_assets(pid)
    z=GENERATED_DIR/f'{pid}-ai-ads-readiness.zip'
    with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
        for p in o.iterdir():
            if p.is_file():f.write(p,p.name)
    return z
