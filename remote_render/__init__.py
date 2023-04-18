from ._version import __version__
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__).addHandler(logging.NullHandler())

from .util import ManagerFlaskApp, datatypes

from remote_render.util import ManagerFlaskApp


# Must import views after app
app = ManagerFlaskApp(__name__, template_folder='./manager/templates', static_folder='./manager/static')
import remote_render.manager.views
