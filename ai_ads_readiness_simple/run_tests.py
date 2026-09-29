import unittest
class Smoke(unittest.TestCase):
 def test_imports(self):
  from app.main import app
  from app.mcp_server import mcp
  self.assertIsNotNone(app);self.assertIsNotNone(mcp)
if __name__=='__main__':unittest.main()
