import util.temp.RenderRequest as RenderRequest
import util.temp.RenderArchive as RenderArchive


testRequest = RenderRequest.RenderRequest(uuid="12345")
testRequest.save_self()

testArchive = RenderArchive.RenderArchive(uuid="12345")
testArchive.save_self()

res = RenderRequest.RenderRequest.read_all()
print(res)