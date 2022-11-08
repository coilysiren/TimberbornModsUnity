"""
invoke entrypoint

docs: https://www.pyinvoke.org/
"""

# 3rd party
import invoke

# local
from . import mac, windows


namespace = invoke.Collection()
namespace.add_collection(mac)
