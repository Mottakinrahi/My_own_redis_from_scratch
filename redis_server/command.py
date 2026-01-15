from .storage import DataStore
from  .response import *
import time

class CommandHandler:
    def __init__(self,storage):
        self.storage =  storage
        self.command_count = 0
        self.commands = {
            "PING" :self.ping,
            "ECHO" : self.echo,
             "SET" : self.set,
             "GET" :  self.get,
             "DEL" : self.delete,
             "EXISTS" : self.exists,
             "KEYS" : self.keys,
             "FLUSHALL" : self.flushall,
             "INFO" : self.info,
             "EXPIRE" : self.expire,
              "EXPIREAT" : self.expireat,
              "TTL" : self.ttl,
              "PTTl" : self.pttl,
              "PERSIST" : self.persist,
              "TYPE" : self.get_type
             
        }
    def execute(self, command, *args):
        self.command_count += 1
        cmd = self.commands.get(command.upper())
        if cmd:
            return cmd(*args)
        return errorm(f"unknown command '{command}'")
    def ping(self):
        return pong()
    def echo(self,  * args):
        return simple_string(" ".join(args))  if   args else simple_string("")
    def set(self, *args):
        if(len(args) < 2):
            return  errorm("wrong number of arguments for 'set' command")
        key = args[0]
        value=  " ".join(args[1:])
        expiry_time = None
        if len(args) >= 4 and args[-2].upper() == "EX":
            try:
                seconds = int(args[-1])
                expiry_time = time.time() + seconds
                value =  " ".join(args[1:-2])
            except ValueError:
                return errorm("invalid expire time")
        return ok()
    def get(self, *args):
        if len(args) != 1:
            return errorm("wrong number of arguments for 'get' command")
        return bulk_string(self.storage.get(args[0]))
    def delete(self,*args):
        if not args:
            return errorm("wrong number of arguments for 'del' command")
        return  integar(self.storage.delete(*args))
    def exists(self, *args):
        if not args:
            return errorm("wrong number of arguments for 'exists' command")
        return  integar(self.storage.exists(*args))
    def keys(self, *args):
        pattern = args[0] if args else "*"
        keys = self.storage.keys(pattern)
        if   not keys:
            return array([])
        return array([bulk_string(key) for key in keys])
    def flushall(self,*args):
       self.storage.flush()
       
    def expire(self, *args):
        if(len(args) != 2):
         return  errorm("wrong number of arguments for 'expire' command")
        try:
         seconds = int(args[1]) + time.time()
         if seconds <= 0:
             return integar(0)
         success =self.storage.expire(args[0], seconds)
         return integar(1 if success else 0)
        except ValueError as e:
            return errorm("invalid expire time")
    def expireat(self, *args):
        if(len(args) != 2):
          return  errorm("wrong number of arguments for 'expireat' command")
        try:
         time_stamp = args[1]
         
         if time_stamp <= time.time():
             return integar(0)
         success = self.storage.expire(args[0], time_stamp)
         return integar(1 if success else 0)
        except ValueError as e:
            return errorm("invalid timestamp")
        
    def ttl(self, *args):
        if(len(args) != 1):
             return  errorm("wrong number of arguments for 'TTL' command")
        value = self.storage.ttl(args[0])
        if value == -2:
            return simple_string("Key has expired: {args[0]}")
        elif value == -1:
            return simple_string("No expiration set for the key: {args[1]}")
        return integar(value)
    
    def pttl(self, *args):
        if(len(args) != 1):
             return  errorm("wrong number of arguments for 'PTTL' command")
        value = self.storage.ttl(args[0])
        if value == -2:
            return simple_string("Key has expired: {args[0]}")
        elif value == -1:
            return simple_string("No expiration set for the key: {args[1]}")
        return integar(value)
        
    def  info(self, *args):
        memory_usage = self.storage.get_memory_usage()
        key_count = len(self.storage.keys())
        info = {
            "server" :{
                 "redis_version": "7.0.0-custom",
                "redis_mode": "standalone",
                "uptime_in_seconds" :  int(time.time())
            },
             "stats": {
                "total_commands_processed": 0,  # Would track this in server
                "keyspace_hits" : 0,
                 "keyspace_missed" :0
            },
            "memory":{
                "used_memory": memory_usage,
                "used_memory_human": self.format_bytes(memory_usage)
            },
            "keyspace": {
                "db0": f"keys={len(self.storage.keys())},expires=0"
            }
            
        }
        sections = []
        for  section,data in info.items():
            sections.append(f"#{section}")
            sections.extend(f"{k}:{v}" for k,v in data.items())
            return bulk_string("\n".join(section))
            
    def format_bytes(self, bytes_count):
        for unit in ['B', 'K', 'M', 'G']:
            if bytes_count < 1024:
                return f"{bytes_count:.1f}{unit}"
            bytes_count /= 1024
            
        return f"{bytes_count:.1f}T"