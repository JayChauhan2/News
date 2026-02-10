from ddgs import DDGS
import time
import ssl
import certifi

def create_ssl_context():
    return ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = create_ssl_context

LEGIT_SOURCES = ["SpaceX", "elonmusk"]

def debug_scan():
    print("DEBUG: Testing timelimit=None...")
    
    with DDGS(verify=False, timeout=20) as ddgs:
        for source in LEGIT_SOURCES:
            query = f'site:x.com "{source}" /status/'
            print(f"\nScanning {source}...")
            print(f"Query: {query}")
            
            results = []
            try:
                # Try with NO timelimit
                results = list(ddgs.text(query, max_results=5, timelimit=None))
                print(f"  -> Found {len(results)} results (No Timelimit)")
                for r in results:
                    print(f"     - Body: {r.get('body')[:50]}...")
                    print(f"       URL: {r.get('href')}")
            except Exception as e:
                print(f"  -> Error: {e}")
                
            time.sleep(2)

if __name__ == "__main__":
    debug_scan()
