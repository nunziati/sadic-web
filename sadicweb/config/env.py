import environ

ENV = environ.Env()
PROJECT_ROOT = environ.Path(__file__) - 3

# Default paths to environment files
env_paths = [
    PROJECT_ROOT.path('.env'),
    environ.Path('/etc/sadicweb/sadic.env'),
]

if ENV.str('SADIC_ENV', default='') != '':
    env_paths.insert(0, environ.Path(ENV.str('SADIC_ENV')))

# Read in any environment files
for e in env_paths:
    try:
        e.file('')
        ENV.read_env(e())
    except FileNotFoundError:
        pass