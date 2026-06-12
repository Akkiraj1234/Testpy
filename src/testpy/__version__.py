from importlib.metadata import version, PackageNotFoundError


try :
    VERSION = version("testpy")
    
except PackageNotFoundError:
    VERSION = "0.0.0"