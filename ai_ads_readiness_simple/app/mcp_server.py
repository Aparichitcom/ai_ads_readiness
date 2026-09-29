from mcp.server.fastmcp import FastMCP
from .analyzer import analyze_website
from .generator import save_analysis,load_analysis,generate_assets,list_files,read_file,make_zip
mcp=FastMCP('AI Ads Readiness Generator',stateless_http=True,json_response=True)
@mcp.tool()
def analyze_website_tool(url:str,max_pages:int=10)->dict:
    """Analyze a public website and return deterministic readiness scores."""
    a=analyze_website(url,max_pages);save_analysis(a);return a
@mcp.tool()
def get_analysis(project_id:str)->dict:return load_analysis(project_id)
@mcp.tool()
def get_report(project_id:str)->dict:
    a=load_analysis(project_id);return {'project_id':project_id,'scores':a['scores'],'recommendations':a['recommendations'],'commercial_intents':a['commercial_intents']}
@mcp.tool()
def get_recommendations(project_id:str)->list[str]:return load_analysis(project_id)['recommendations']
@mcp.tool()
def get_commercial_intents(project_id:str)->list[dict]:return load_analysis(project_id)['commercial_intents']
@mcp.tool()
def generate_assets_tool(project_id:str)->list[str]:return generate_assets(project_id)
@mcp.tool()
def list_generated_files(project_id:str)->list[str]:return list_files(project_id)
@mcp.tool()
def read_generated_file(project_id:str,filename:str)->str:return read_file(project_id,filename)
@mcp.tool()
def download_package(project_id:str)->str:return str(make_zip(project_id))
