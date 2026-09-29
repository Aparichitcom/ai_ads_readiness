from contextlib import asynccontextmanager
from fastapi import FastAPI,HTTPException,Header
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from .config import HOST,PORT,MCP_API_KEY
from .models import AnalyzeRequest
from .analyzer import analyze_website
from .generator import save_analysis,load_analysis,generate_assets,list_files,read_file,make_zip
from .mcp_server import mcp
@asynccontextmanager
async def lifespan(app:FastAPI):
    async with mcp.session_manager.run():yield
app=FastAPI(title='AI Ads Readiness Generator',version='1.0.0',lifespan=lifespan)

class MCPAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == '/mcp' or request.url.path.startswith('/mcp/'):
            auth=request.headers.get('authorization','')
            if not MCP_API_KEY or MCP_API_KEY == 'change-me' or not auth.startswith('Bearer ') or auth[7:] != MCP_API_KEY:
                return JSONResponse({'detail':'Invalid or missing MCP API key.'},status_code=401)
        return await call_next(request)

app.add_middleware(MCPAuthMiddleware)
app.mount('/mcp',mcp.streamable_http_app())
@app.get('/')
def root():return {'name':'AI Ads Readiness Generator','status':'running','mcp_endpoint':'/mcp','docs':'/docs'}
@app.get('/api/health')
def health():return {'status':'ok'}
@app.post('/api/analyze')
def api_analyze(r:AnalyzeRequest):
    try:a=analyze_website(str(r.url),r.max_pages);save_analysis(a);return a
    except ValueError as e:raise HTTPException(400,str(e))
    except Exception as e:raise HTTPException(502,f'Website analysis failed: {e}')
@app.post('/api/generate')
def api_generate(project_id:str):
    try:return {'project_id':project_id,'files':generate_assets(project_id)}
    except FileNotFoundError:raise HTTPException(404,'Project not found.')
@app.get('/api/projects/{project_id}')
def api_project(project_id:str):
    try:return load_analysis(project_id)
    except FileNotFoundError:raise HTTPException(404,'Project not found.')
@app.get('/api/projects/{project_id}/report')
def api_report(project_id:str):
    try:
        a=load_analysis(project_id);return {'project_id':project_id,'scores':a['scores'],'recommendations':a['recommendations'],'commercial_intents':a['commercial_intents']}
    except FileNotFoundError:raise HTTPException(404,'Project not found.')
@app.get('/api/projects/{project_id}/files')
def api_files(project_id:str):return {'project_id':project_id,'files':list_files(project_id)}
@app.get('/api/projects/{project_id}/files/{filename}')
def api_file(project_id:str,filename:str):
    try:return {'filename':filename,'content':read_file(project_id,filename)}
    except (FileNotFoundError,ValueError) as e:raise HTTPException(404,str(e))
@app.get('/api/packages/{project_id}/download')
def api_download(project_id:str):
    try:
        p=make_zip(project_id);return FileResponse(p,filename=p.name,media_type='application/zip')
    except FileNotFoundError:raise HTTPException(404,'Project not found.')
@app.get('/api/protected-check')
def protected_check(authorization:str|None=Header(default=None)):
    if not authorization or not authorization.startswith('Bearer ') or authorization[7:]!=MCP_API_KEY or MCP_API_KEY=='change-me':raise HTTPException(401,'Invalid MCP API key.')
    return {'authorized':True}
if __name__=='__main__':
    import uvicorn;uvicorn.run('app.main:app',host=HOST,port=PORT,reload=True)
