from .fast_unfolding import *
from .em import *
from .LPA import *
from .GN import *
from .cpm import *

_method = FastUnfolding()
_verbose = False

def get_method(name=None, verbose=False):
  if not name:
    name = 'Fast Unfolding'
  if name == 'Fast Unfolding':
    return FastUnfolding(verbose=verbose)
  if name == 'EM':
    return EM(verbose=verbose)
  if name == 'LPA':
    return LPA(verbose=verbose)
  if name == 'GN':
    return GN(verbose=verbose)
  if name == 'CPM':
    return CPM(verbose=verbose)
  else:
    raise NotImplementedError

def methods():
  return [
    'Fast Unfolding',
    'EM',
    'LPA',
    'GN',
    'CPM'
  ]

def set_params(verbose=False, *args, **kwargs):
  global _verbose
  _verbose = verbose
  if args or kwargs:
    global _method
    _method.set_params(*args, **kwargs)

def use(name=None):
  global _method
  _method = get_method(name)
  global _verbose
  if _verbose:
    print(f'mode change to {_method}')

def process(*args, **kwargs):
  global _method
  return _method.process(*args, **kwargs)