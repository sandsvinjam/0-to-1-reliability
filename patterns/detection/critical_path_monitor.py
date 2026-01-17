# Week 1: Monitor the money-making paths
CRITICAL_PATHS = {
    'user_signup': {
        'endpoint': '/api/v1/signup',
        'success_rate_threshold': 99.5,
        'latency_p95_threshold': 500,  # milliseconds
        'alert_severity': 'P0'  # Page immediately
    },
    'service_booking': {
        'endpoint': '/api/v1/bookings',
        'success_rate_threshold': 99.5,
        'latency_p95_threshold': 1000,
        'alert_severity': 'P0'
    },
    'payment_processing': {
        'endpoint': '/api/v1/payments',
        'success_rate_threshold': 99.9,  # Higher threshold for payments
        'latency_p95_threshold': 2000,
        'alert_severity': 'P0'
    },
    'order_confirmation': {
        'endpoint': '/api/v1/confirmations',
        'success_rate_threshold': 99.0,
        'latency_p95_threshold': 500,
        'alert_severity': 'P1'  # Page during business hours
    }
}

class CriticalPathMonitor:
    def __init__(self, metrics_backend):
        self.metrics = metrics_backend
        
    def track_request(self, path_name, duration_ms, success):
        """Track every request on critical paths"""
        # Record latency
        self.metrics.histogram(
            f'critical_path.{path_name}.latency_ms',
            duration_ms
        )
        
        # Record success/failure
        self.metrics.increment(
            f'critical_path.{path_name}.requests',
            tags={'success': str(success)}
        )
        
        # Check thresholds
        self._check_thresholds(path_name)
    
    def _check_thresholds(self, path_name):
        """Alert if critical path degrades"""
        config = CRITICAL_PATHS[path_name]
        
        # Get current metrics (5-minute window)
        current_success_rate = self.metrics.get_success_rate(
            f'critical_path.{path_name}.requests',
            window='5m'
        )
        
        current_p95 = self.metrics.get_percentile(
            f'critical_path.{path_name}.latency_ms',
            percentile=95,
            window='5m'
        )
        
        # Alert if thresholds violated
        if current_success_rate < config['success_rate_threshold']:
            self.alert(
                severity=config['alert_severity'],
                title=f"{path_name} success rate below threshold",
                message=f"Current: {current_success_rate:.2f}%, Threshold: {config['success_rate_threshold']}%",
                runbook=f"https://runbooks.example.com/{path_name}/low-success-rate"
            )
        
        if current_p95 > config['latency_p95_threshold']:
            self.alert(
                severity=config['alert_severity'],
                title=f"{path_name} latency above threshold",
                message=f"P95: {current_p95}ms, Threshold: {config['latency_p95_threshold']}ms",
                runbook=f"https://runbooks.example.com/{path_name}/high-latency"
            )
