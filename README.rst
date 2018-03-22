###############
Utilize Project
###############

`README中文文档 <https://github.com/copyrighthero/Utilize/blob/master/README.zh-CN.md>`_

About the Utilize Library
=========================

This is a collection/resource class for managing project configs and provide users with common resources like:

 - redis instance using [redis-py](https://github.com/andymccurdy/redis-py), memcached instance using [pymemcache](https://github.com/pinterest/pymemcache).
 - application config storage using Python `configparser`.
 - K-V store using [KVS](https://www.github.com/copyrighthero/KVS).
 - message broker using [Msgr](https://www.github.com/copyrighthero/Msgr).
 - url-safe integer<->string base converter using [BaseCon](https://www.github.com/copyrighthero/BaseCon).
 - serialize+compressor using [SeCo](https://www.github.com/copyrighthero/SeCo).
 - database manager using [Decibel](https://www.github.com/copyrighthero/Decibel).

 By invoking `python -m utilize --init [config.ini]`, it will create a default config file to your current directory, users can easily modify the config file to their needs.

 By using this class, user will have a centralized resource manager that can help you build your project faster without the need to worry about configuring and resource management.

 Users can also subclass the `Utilize` class to create their own resource manager, simply add more methods or override existing ones.

How to Use Msgr Library
=======================

After installation using `pip install Utilize`, create an config file in your working directory by calling `python -m utilize -i [file_path]`, modify the created config file to your needs and then use the library: pass in the created config file path when instantiating the Utilize class as the first argument.

.. code-block:: python

  # >>> python -m utilize --init config.ini
  from utilize import Utilize

  utilize = Utilize() # default to read './config.ini'
  utilize = Utilize('./config.ini') # or pass in config file path

  # access and update configs
  utilize.config # configparser instance, the configs
  utilize.update('./new_config.ini') # update configs using new file
  utilize.update({'section': {'key': 'value'}}) # update configs using dict

  ##  all instance created are singleton to save memory ##

  utilize.seco # SeCo instance, used for serialize + compress or the revert

  utilize.kvs # KVS instance, used K-V pair storage

  utilize.decibel # decibel instance, used for sqlite/mysql management

  utilize.redis # redis instance, used for in-memory cache
  utilize.memcached # memcached instance, used for in-memory cache

  utilize.message_broker # message broker, used for cross-process message passing

Utilize Class API References
============================

 The package provide `Utilize` class and a simple CLI program. The CLI program is only used to create config files, simply call `python -m utilize --init [config_file_path]`, the file path is defaulted to './config.ini'.

Utilize Class
-------------

The Utilize class is a config and resource manager, all helper resources are created on first access and further more request for the same request will get the same instance created (singleton resources). To make users feel less stressed, the instances are created automatically according to the config file, so the users don't have to worry about instantiating the instance by themselves.

Signature: `Utilize(config = './config.ini')`

- `instance.config` property: access the read configs, please refer to Python's Docs on `configparser` for more info, but essentially it is a `dict`-like object and configs can be accessed using subscripting (`config['section]`, ie. `config['global']['timeout']`). Remember all things are stored as strings, so cast them before use.
- `instance.update(config)` method: used to update configs, takes in either a string as file path or a dict in the format: `{'section': {'key': 'value', 'key2': 'value2'}, 'section...}`.
- `instance.seco` property: access the SeCo serialize+compress|deserialize+decompress library, for more information please refer to [SeCo Project](https://www.github.com/copyrighthero/Seco).
- `instance.redis`, `instance.memcached` property: acquire a connected redis/memcached in-memory database instance. Please refer to [redis-py Project](https://github.com/andymccurdy/redis-py) and [pymemcache Project](https://github.com/pinterest/pymemcache) for more information and documentations.
- `instance.kvs` property: access the KVS kv-store library, can be config to use `dict` (':memory:'), `redis`, `memcached` or `dbm`. This library automatically initialize the KV-store with supplied key value pair set in the config file, please read the generated config file. The KVS library actually supports more databases like `plyvel` refer to [KVS Project](https://www.github.com/copyrighthero/KVS) for more info.
- `instance.decibel` property: access the Decibel SQLite/MySQL database manager, this library automatically initialize the database with provided init statements and will register regular statements provided in the config files for easy access and execution. Decibel supports any database instances that conforms with Python DB-API 2.0 interfaces, please refer to [Decibel Project](https://www.github.com/copyrighthero/Decibel) for more information.
- `instance.message_broker` property: acquire a `msgr.MessageBroker` instance with `msgr.MessageQueue` instances as `job`, `resolve`, `reject` and `service` queues. The `msgr` message queue supports many other queue types like [`redistr.Queue`](https://www.github.com/copyrighthero/Redistr) besides the default `multiprocessing.Queue`, see [Msgr Project](https://www.github.com/copyrighthero/Msgr) for more details.

Licenses
========

This project is licensed under two permissive licenses, please chose one or both of the licenses to your like. Although not necessary, bug reports or feature improvements, attributes to the author(s), information on how this program is used are welcome and appreciated :-) Happy coding

[BSD-2-Clause License]

Copyright 2018 Hansheng Zhao

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[MIT License]

Copyright 2018 Hansheng Zhao

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
