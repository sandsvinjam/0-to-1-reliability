# Week 2: Service-level indicators
SLI_DEFINITIONS = {
    'api_availability': {
        'description': 'Percentage of API requests that succeed',
        'target': 99.5,
        'measurement': 'http_requests_total{status=~"2.."} / http_requests_total'
    },
    'api_latency': {
        'description': 'API request latency at 95th percentile',
        'target': 500,  # milliseconds
        'measurement': 'histogram_quantile(0.95, http_request_duration_ms)'
    },
    'database_health': {
        'description': 'Database query success rate',
        'target': 99.9,
        'measurement': 'db_queries_success / db_queries_total'
    },
    'queue_lag': {
        'description': 'Maximum message age in any queue',
        'target': 60,  # seconds
        'measurement': 'max(queue_message_age_seconds)'
    }
}

class SLIMonitor:
    def __init__(self, prometheus_client):
        self.prometheus = prometheus_client
        
    def check_sli(self, sli_name):
        """Evaluate SLI against target"""
        sli = SLI_DEFINITIONS[sli_name]
        
        # Query Prometheus for current value
        current_value = self.prometheus.query(sli['measurement'])
        
        # Compare against target
        if sli_name.endswith('_availability'):
            # For availability, current should be >= target
            violated = current_value < sli['target']
        else:
            # For latency/lag, current should be <= target
            violated = current_value > sli['target']
        
        if violated:
            return SLIViolation(
                sli_name=sli_name,
                description=sli['description'],
                current_value=current_value,
                target=sli['target']
            )
        
        return None
    
    def continuous_monitoring(self):
        """Check all SLIs every minute"""
        while True:
            for sli_name in SLI_DEFINITIONS:
                violation = self.check_sli(sli_name)
                
                if violation:
                    self.alert_sli_violation(violation)
            
            time.sleep(60)
