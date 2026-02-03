import os
import  time
from typing import List,Tuple, Dict,Any

class   PersistenceConfig:
    
    def __init__(self, config_dict : Dict[str, Any] = None):
        """"
        initialize default persistence configuration first
        Then if custom config given update the config
        """
        
        self._config = self._get_default_config()
        
        #Update provided config
        if  config_dict:
            self._config.update(config_dict)
            
        self._validate_config()
        
    def _get_default_config(self) -> Dict[str, Any] :
        return {
            #AOF configuration
            'aof_enabled': True,
            'aof_filename': 'appendonly.aof',
            'aof_sync_policy' : 'everysec',
             'aof_rewrite_percentage' : 100,
             'aof_rewrite_min_size' : 1024  * 1024,
             
             #Directory Configuration
            'data_dir' : './data',
            'temp_dir' : './data/temp',
            
            #General Settings
            'persistence_enabled' : True,
            'recovery_on_startup' : True,
            'max_memory_usage' : 100 * 1024 * 1024,
             
            
        }
    
    def  _validate_config(self) -> None: 
        
      valid_sync_policies = ['always', 'everysecond', 'no']
      if self._config['aof_sync_policy'] not in valid_sync_policies:
          raise ValueError("Invalid sync policy. Must be one of {valid_sync_policies}") 
             
      if not self._config['aof_filename'] :
          raise ValueError("AOF filename cannot be empty")
    
    def get(self, key: str, default = None):
        return self._config.get(key, default)
    
    def set (self, key : str, value : Any) -> None:
        self._config[key] = value
        self._validate_config()
    def update(self, config_dict:  Dict[str, Any]) -> None:
        self._config.update(config_dict)
        self._validate_config()
        
    
    def get_all(self) -> Dict[str, Any]:
        return self._config.copy()
    
    @property
    def aof_enabled(self) -> bool:
        return self._config['aof_enabled']
    
    @property
    def aof_filename(self) -> str:
        return os.path.join(self._config['data_dir'], self._config['aof_filename'])
    
    @property
    def aof_sync_policy(self) -> str:
        return self._config['aof_sync_policy']
    
    @property 
    def data_dir(self) ->   str:
        return self._config['data_dir']
    
    def temp_dir(self) -> str:
        return self._config['temp_dir']
    
    def ensure_directories(self) -> None:
        
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.temp_dir,exist_ok=True)

    def get_aof_temp_filename(self) -> str:
           
        return os.path.join(self.temp_dir, f"temp-rewrite-aof-{int(time.time())}.aof")
    def __repr__(self):
        
        return f"PersistenceConfig({self._config})"
        