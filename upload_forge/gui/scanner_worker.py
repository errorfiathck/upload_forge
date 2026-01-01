from PySide6.QtCore import QThread, Signal, QObject
import asyncio
from ..core.scanner import Scanner
from ..core.vulnerability_models import ScanResult, VulnerabilityFinding, TrafficLog

class ScannerWorker(QThread):
    """
    Runs the scanner in a separate thread.
    """
    finished = Signal(ScanResult)
    progress = Signal(str) # Log message
    finding_found = Signal(VulnerabilityFinding)
    traffic_log = Signal(TrafficLog)

    def __init__(self, target_url, param, upload_dir, proxies, headers):
        super().__init__()
        self.target_url = target_url
        self.param = param
        self.upload_dir = upload_dir
        self.proxies = proxies
        self.headers = headers
        self.scanner = Scanner()
        self._is_running = True

    def _on_traffic_log(self, log: TrafficLog):
        self.traffic_log.emit(log)

    def _on_finding_found(self, finding: VulnerabilityFinding):
        self.finding_found.emit(finding)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # We need to bridge logger to signals in a real app, 
        # for now we just run it and return result.
        # Ideally we'd hook into scanner callbacks.
        
        try:
            result = loop.run_until_complete(self.scanner.scan(
                target_url=self.target_url,
                file_param=self.param,
                upload_dir=self.upload_dir,
                proxies=self.proxies,
                headers=self.headers,
                on_log_callback=self._on_traffic_log,
                on_finding_callback=self._on_finding_found
            ))
            self.finished.emit(result)
        except Exception as e:
            # Handle error
            print(f"Scanner error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            loop.close()

    def stop(self):
        self.scanner.stop()
        self.quit()
        self.wait()
