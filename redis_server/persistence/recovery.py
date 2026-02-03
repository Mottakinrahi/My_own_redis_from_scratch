
"""
Data Recovery management
it recovers data from AOF file in startup
"""
import os
import time
from typing import Optional, Dict
from .aof import AOFWriter


class  RecoveryManager:
    
    def __init__(self, aof_filename:str):
        self.aof_filename = aof_filename
        self.aof_handler = None
        
    def recover_data(self, data_store, command_handler = None) -> bool:
        
        try:
            aof_exists = os.path.exists(self.aof_filename)
            if not aof_exists:
                print("No AOF file found, starting with empty database")
                return  True
            print(f"Loading datafrom AOF file: {self.aof_filename}")
            return self._replay_aof(data_store,  command_handler)
        except Exception as e:
            print(f"Error during data recovery {e}")
            return self._handle_corruption(e)
        
    def _replay_aof(self, data_store, command_handler) -> bool:
         
         
         try:
             commands_replayed = 0
             with open(self.aof_filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f,1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                       parts = line.split(' ',2)
                       if len(parts) < 2:
                           continue
                       timestamp = parts[0]
                       command = parts[1]
                       args = parts[2].split() if len(parts) > 2 else []
                       
                       #execute command direct on data store.
                       
                       self._execute_recovery_command(data_store,command, args)
                       commands_replayed += 1
                       
                    except Exception as e:
                        print(f"Error replaying command at line {line_num} : {e}")
                        print(f"Problematic line: {line}")
                        continue
                print(f"Replayed {commands_replayed} commands from  AOF")
                    
         except Exception as e:
             print("Error replay AOF file: {e}")
             return False
    def _execute_recovery_command(self, data_store, command: str, args: list) -> None:
        
        try:
          if command == 'SET':
             if len(args) >= 2:
                 key = args[0]
                 value = ' '.join(args[1:])
                 data_store.set(key, value)
                 
          elif command == 'DEL':
               if args:
                   data_store.delete(*args)
          elif command == 'EXPIRE':
               if len(args) == 2:
                   key = args[0]
                   seconds = int(args[1])
                   data_store.expire(key, seconds)
          elif command =='EXPIREAT':
               if len(args) == 2:
                    key = args[0]
                    timestamp = int(args[1])
                    data_store.expire(key, timestamp)
          elif command == 'PERSIST':
              if len(args) == 1:
                  key = args[0]
                  data_store.persist(key)
          elif command == 'FLUSHALL':
              data_store.flush()
          else:
              #unknown command - ignore during startup
              pass
        except Exception as e:
            print(f"Error executing recovery command {command}: {e}")
    def _handle_corruption(self, e) -> bool:
        """This is for handling corrupted persistence files
        
           it returns true if recovery should continue with empty database
        """
        print(f"Persistence file corruption detected: {e}")
        print("Starting with an empty database. Consider restoring from backup")
        #In production, we might want to:
        # 1.Create backup of corrupted files
        # Attempt partial recovery
        # Send alerts to administrators
        
        return True # Continue with empty database
    def validate_files(self) -> Dict[str, bool]:
        """"
        Validate AOF file without loading it
        
        """
        results = {
            'aof_exists' : os.path.exists(self.aof_filename),
            'aof_valid' : False
        }
        if results ['aof_exists'] :
            try:
                with open(self.aof_filename, 'r', encoding='utf-8') as f:
                    #try to read first 5 lines
                    for i, line in enumerate(f):
                        if i >= 5:
                             break
                        parts = line.strip.split(' ',2)
                         
                        if len(parts) >= 2:
                             try:
                                 int(parts[0])
                             except:
                                 break
                    else:
                        results['aof_valid'] = True
            except  Exception:
                  results['aof_valid'] = False
        return results