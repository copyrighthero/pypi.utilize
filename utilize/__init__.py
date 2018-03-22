# Author: Hansheng Zhao <copyrighthero@gmail.com> (https://www.zhs.me)


# import directive
__all__ = (
  '__author__', '__license__',
  '__version__', 'Utilize'
)
# package metadata
__author__ = 'Hansheng Zhao'
__license__ = 'BSD-2-Clause + MIT'
__version__ = '1.0.1'


class Utilize(object):
  """ Utilize class for common resources """

  __slots__ = (
    '_config',
    '_basecon', '_seco', '_kvs', '_decibel',
    '_redis', '_memcached', '_message_broker'
  )

  def __init__(self, config = './config.ini'):
    """
    Resource class constructor
    :param config: mixed, the config resource
    """
    # import ini file config parser
    from configparser import RawConfigParser
    # read config from config resource
    self._config = RawConfigParser()
    self.update(config)
    # initialize attributes
    self._basecon = None
    self._seco = None
    self._kvs = None
    self._decibel = None
    self._redis = None
    self._memcached = None
    self._message_broker = None

  def update(self, config, string = False):
    """
    Update config with file, string or dict
    :param config: mixed, config resource
    :param string: bool, whether read string
    :return: None
    """
    # type check and decide how to update
    if isinstance(config, (str, bytes, bytearray)):
      config = config if isinstance(config, str) \
        else config.decode(encoding = 'UTF8')
      self._config.read(config) if not string \
        else self._config.read_string(config)
    # update content from a dict
    elif isinstance(config, dict):
      self._config.read_dict(config)

  @staticmethod
  def _boolean(keyword):
    """
    Boolean-ize a string
    :param keyword: str|bytes|bytearray, keyword
    :return: bool
    """
    # convert keyword into string
    keyword = keyword.decode(encoding = 'UTF8') \
      if isinstance(keyword, (bytes, bytearray)) \
      else keyword
    return keyword.lower() in (
      '1', 't', 'y', 'true', 'yes',
      'on', 'ok', 'okay', 'confirm'
    )

  @property
  def config(self):
    """
    Acquire the ConfigParse instance
    :return: configparse, the ConfigParse instance
    """
    return self._config

  @property
  def basecon(self):
    """
    Acquire a singleton base_convert instance
    :return: base_convert, a base_convert instance
    """
    # return if exists
    if self._basecon is not None: return self._basecon
    # else instantiate and return
    from basecon import BaseCon
    base = int(self._config['basecon']['base']) \
      if 'basecon' in self._config else 62
    self._basecon = BaseCon(base = base)
    return self._basecon

  @property
  def seco(self):
    """
    Acquire a singleton SeCo instance
    :return: seco, a SeCo instance
    """
    # return if exists
    if self._seco is not None: return self._seco
    # else instantiate and return
    from seco import SeCo
    if 'seco' in self._config:
      self._seco = SeCo(**self._config['seco'])
    else:
      self._seco = SeCo()
    return self._seco

  @property
  def kvs(self):
    """
    Acquire a singleton k-v store instance

    DO NOT INVOKE BEFORE MULTI-PROC FORKING

    :return: kvs, a KVS instance
    """
    # return only one instance of database instance
    if self._kvs is not None: return self._kvs
    # else instantiate and return
    from kvs import KVS
    # acquire config and serialize instance
    config = self._config
    seco = self.seco
    # attempts to get the kvs configs
    kvs_config = config['kvs'] \
      if 'kvs' in config else {}
    kvs_init = 'initialize' in kvs_config \
      and self._boolean(kvs_config['initialize'])
    kvs_engine = kvs_config['engine'].lower() \
      if 'engine' in kvs_config else ':memory:'
    kvs_path = kvs_config['path'] \
      if 'path' in kvs_config else './database.kvs'
    # instantiate kvs according to configs
    if kvs_engine == ':memory:':
      engine = KVS(serialize = seco)
    elif kvs_engine in ('dbm', 'gdbm', 'ndbm'):
      engine = KVS(kvs_path, seco)
    elif kvs_engine == 'redis':
      engine = KVS(self.redis, seco)
    elif kvs_engine == 'memcached':
      engine = KVS(self.memcached, seco)
    else:
      raise NotImplementedError(
        'Other databases not supported yet.'
      )
    # initialize kv-store
    if kvs_init and 'kvs:init' in config:
      # import json for decoding
      import json
      for key, value in config['kvs:init'].items():
        # try to decode value as json
        try: engine.set(key, json.loads(value))
        except (json.JSONDecodeError, ValueError):
          engine.set(key, value)
    # preserve and return kv-store instance
    self._kvs = engine
    return self._kvs

  @property
  def decibel(self):
    """
    Acquire a singleton decibel instance

    DO NOT INVOKE BEFORE MULTI-PROC FORKING

    :return: decibel, a Decibel instance
    """
    # return only one instance of database instance
    if self._decibel is not None: return self._decibel
    from decibel import Decibel
    # set config shorthand
    config = self._config
    # attempts to acquire decibel configs
    db_config = config['decibel'] \
      if 'decibel' in config else {}
    db_init = 'initialize' in db_config \
      and self._boolean(db_config['initialize'])
    db_engine = db_config['engine'].lower() \
      if 'engine' in db_config else 'sqlite'
    db_path = db_config['path'] \
      if 'path' in db_config else './database.sqlite'
    # initialize database instance, acquire statements
    if db_engine in ('sqlite', 'sqlite3'):
      import sqlite3
      engine = sqlite3.connect(db_path)
      init = tuple(config['sqlite:init'].values()) \
        if db_init and 'sqlite:init' in config else ()
      stmt = dict(config['sqlite:stmt']) \
        if 'sqlite:stmt' in config else {}
    elif db_engine == 'mysql':
      from mysql.connector import connect
      engine = connect(**(
        config['mysql'] if 'mysql' in config else {}
      ))
      init = tuple(config['mysql:init'].values()) \
        if db_init and 'mysql:init' in config else ()
      stmt = dict(config['mysql:stmt']) \
        if 'mysql:stmt' in config else {}
    else:
      raise NotImplementedError(
        'Other databases not supported yet.'
      )
    # initialize sql database
    if db_init and init:
      cursor = engine.cursor()
      for init_stmt in init:
        cursor.execute(init_stmt)
      else:
        cursor.close()
        engine.commit()
    # preserve and return decibel instance
    self._decibel = Decibel(engine, stmt)
    return self._decibel

  @property
  def redis(self):
    """
    Acquire a singleton redis instance

    DO NOT INVOKE BEFORE MULTI-PROC FORKING

    :return: redis, a Redis instance
    """
    # return if exists
    if self._redis is not None: return self._redis
    # else instantiate and return
    from redis import Redis
    # acquire config
    config = self._config['redis'] \
      if 'redis' in self._config else {}
    # preserve and return
    self._redis = Redis(**config)
    return self._redis

  @property
  def memcached(self):
    """
    Acquire a singleton memcached instance

    DO NOT INVOKE BEFORE MULTI-PROC FORKING

    :return: memcached, the instance
    """
    # return if exists
    if self._memcached is not None:
      return self._memcached
    # else instantiate and return
    from pymemcache.client.base \
      import Client as Memcached
    # acquire config
    host, port = 'localhost', 11211
    if 'memcached' in self._config:
      config = self._config['memcached']
      host = config['path'] \
        if 'path' in config else 'localhost'
      port = int(config['port']) \
        if 'port' in config else 11211
    # preserve and return
    self._memcached = Memcached((host, port))
    return self._memcached

  @property
  def message_broker(self):
    """
    Acquire a singleton message broker instance
    :return: message_broker, a message broker
    """
    # return only one instance of broker
    if self._message_broker is not None:
      return self._message_broker
    # else instantiate and return
    from msgr import MessageQueue, MessageBroker
    # initialize and return message broker instance
    self._message_broker = \
      MessageBroker(
        job = MessageQueue(), res = MessageQueue(),
        rej = MessageQueue(), ser = MessageQueue()
      )
    return self._message_broker
