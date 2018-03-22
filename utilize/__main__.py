# Author: Hansheng Zhao <copyrighthero@gmail.com> (https://www.zhs.me)


from configparser import RawConfigParser
from argparse import ArgumentParser


def create_config(file_path):
  # create config parser instance
  configparser = RawConfigParser(allow_no_value = True)
  # create required sections
  configparser.add_section('global')
  configparser.add_section('basecon')
  configparser.add_section('seco')
  configparser.add_section('redis')
  configparser.add_section('memcached')
  configparser.add_section('kvs')
  configparser.add_section('kvs:init')
  configparser.add_section('decibel')
  configparser.add_section('sqlite:init')
  configparser.add_section('sqlite:stmt')
  configparser.add_section('mysql')
  configparser.add_section('mysql:init')
  configparser.add_section('mysql:stmt')
  # add comments to sections
  configparser.set('global', '; global settings')
  configparser.set('basecon', '; choose base from (2 <= base <= 65)')
  configparser.set('seco', "; choose `serialize` in ('json', 'msgpack', 'pickle')")
  configparser.set('seco', "; chose `compress` in ('zlib', 'bz2')")
  configparser.set('kvs', "; `engine` in (':memory:', 'redis', 'memcached', 'dbm')")
  configparser.set('kvs', "; `path` is only used when `engine` is set to 'dbm'")
  configparser.set('kvs:init', '; `key = value` format, value can be valid JSON string')
  configparser.set('decibel', "; choose decibel `engine` in ('sqlite', 'mysql')")
  configparser.set('decibel', "; `path` is only used when `engine` is set to 'sqlite'")
  configparser.set('sqlite:init', '; `stmt_id = stmt` format, initialize statements')
  configparser.set('sqlite:stmt', '; `stmt_id = stmt` format, regular statements')
  configparser.set('mysql:init', '; `stmt_id = stmt` format, initialize statements')
  configparser.set('mysql:stmt', '; `stmt_id = stmt` format, regular statements')
  # read in default configs
  configparser.read_dict({
    'global': {},
    'basecon': {'base': 62},
    'seco': {
      'serialize': 'msgpack', 'compress': 'zlib'
    },
    'redis': {
      ';unix_socket_path': '',
      'host': 'localhost',
      'port': '6379',
      'password': '',
      'db': '0',
    },
    'memcached': {
      'host': 'localhost', 'port': '11211'
    },
    'kvs': {
      'initialize': 'false',
      'engine': ':memory:',
      'path': './database.kvs'
    },
    'kvs:init': {},
    'decibel': {
      'initialize': 'false',
      'engine': 'sqlite',
      'path': './database.sqlite'
    },
    'sqlite:init': {},
    'sqlite:stmt': {},
    'mysql': {
      'host': 'localhost', 'port': '3306',
      'user': '', 'password': '', 'database': ''
    },
    'mysql:init': {},
    'mysql:stmt': {}
  })
  # write default configs to file
  with open(file_path, 'w', encoding = 'UTF8') as fp:
    configparser.write(fp)


# create argument parser instance
argparse = ArgumentParser(
  prog='python[2|3] -m utilize', description='''
    Initailize default config file for Utilize class.
  ''', epilog='Happy coding :-)'
)

# add positional argument
argparse.add_argument(
  'file_path', metavar='file_path',
  type=str, nargs='?', default='config.ini',
  help="The config file path, default 'config.ini'"
)
# add program execute option
argparse.add_argument(
  '-i', '--init',
  dest='create_config', action='store_const',
  const=create_config, required = True,
  default=lambda _: argparse.print_help(),
  help='Create default config file at [file_path].'
)

# parse argv vector into args
args = argparse.parse_args()

# execute depend on the args
args.create_config(args.file_path)
