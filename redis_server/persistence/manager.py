import time
import threading
from typing import Optional, Dict, Any
from .config import PersistenceConfig
from .aof import AOFWriter
from .recovery import RecoveryManager

class  PersistenceManager:
    
    def __init__(self, config: Optional[PersistenceConfig] = None):
        
        self.config = config or PersistenceConfig()
        
        self.config.ensure_directories()
        
        self.aof_writer = None
        self.recovery_manager = None
        self.last_aof_sync_time = time.time()
        
        self._lock =  threading.Lock()
        
        self._initialize_components()
        
    
    def _initialize_components(self) -> None:
        
     if self.config.aof_enabled:
         self.aof_writer = AOFWriter(
             self.config.aof_filename,
             self.config.aof_sync_policy
         )
         
     self.recovery_manager = RecoveryManager(
         self.config.aof_filename
     )
     
    def start(self) -> None:
        """start  persistence operations"""
        if self.aof_writer:
           self.aof_writer.open()
           
        print(f"Persistence manager started  with   AOF enabled:{self.config.aof_enabled}")
        
    def stop(self) -> None:
     if self.aof_writer:
         self.aof_writer.open()
     print("Persistence manager stopped")   
     
    def recover_data(self, data_store, command_handler = None) -> bool:
       if not self.config.get('recovery_on_startup', True):
           print("Recovery on startup disabled")
           return True
       if self.recovery_manager:
           return self.recovery_manager.recover_data(data_store, command_handler)
           
       return True
       
    def log_write_command(self, command: str, *args) ->  None:  
        """"
        Log a write command (FOR AOF)
        
        Args:
        command: Command Name
        *args : Command arguments
        """
        if self.aof_writer and self._is_write_command(command):
          self.aof_writer.log_command(command,  *args)
        
    def periodic_tasks(self) -> None:
    
      """"
      This is for periodic  persistence  tasks
      Should be called from the main event loop
      """
      current_time = time.time()
      
      if self.aof_writer:
          if self.aof_writer.should_sync():
               self.aof_writer.sync_to_disk()
               self.last_aof_sync_time  = current_time
     
    def rewrite_aof_background(self, data_store) -> bool:
          if not  self.aof_writer:
              return False
          
          try:
              def background_rewrite():
                  
                  temp_filename = self.config.get_aof_temp_filename()
                  success = self.aof_writer.rewrite_aof(data_store, temp_filename)
                  if success:
                      print("Background AOF rewrite completed")
                  else:
                      print("Background AOF rewrite failed")
                  
              thread = threading.Thread(target=background_rewrite, daemon = True)
              thread.start()
              return True
          except Exception as e:
              print(f"Error starting background AOF rewrite: {e}")
              return False
      
    def get_stats(self) -> Dict[str, Any]:
        """Get persistence statistics"""
        return{
            'aof_enabled':self.config.aof_enabled,
            'last_aof_sync_time' : int(self.last_aof_sync_time),
             'aof_filename' :   self.config.aof_filename  if self.config.aof_enabled else None
           }
      
        
    def _is_write_command(self, command : str) -> bool:
        """" 
        Check if command is a write command that should be logged
        """
        write_commands = {
            'SET', 'DEL',  'EXPIRE' , 'EXPIREAT', 'PERSIST', 'FLUSHALL', 'SETEX', 'SETNX', 'MSET', 'MSETNX', 'APPEND', 'INCR',
             'DECR', 'INCRBY', 'DECRBY', 'LPUSH', 'RPUSH', 'LPOP', 'RPOP', 'SADD',
             'SREM', 'SPOP', 'HSET', 'HDEL', 'HINCRBY', 'ZADD', 'ZREM'
        }
        
        return command.upper() in write_commands