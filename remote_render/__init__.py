from ._version import __version__
import logging
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__).addHandler(logging.NullHandler())

from remote_render.util import ManagerFlaskApp


# Must import views after app
app = ManagerFlaskApp(__name__, template_folder='./manager/templates', static_folder='./manager/static')
CORS(app)
import remote_render.manager.views
