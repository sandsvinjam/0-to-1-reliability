# Business metrics monitoring
BUSINESS_METRICS = {
    'transactions_per_minute': {
        'baseline': 150,  # Normal rate
        'alert_threshold': 0.7,  # Alert if <70% of baseline
        'severity': 'P0'
    },
    'conversion_rate': {
        'baseline': 0.18,  # 18% conversion
        'alert_threshold': 0.8,  # Alert if <80% of baseline
        'severity': 'P1'
    },
    'average_order_value': {
        'baseline': 45.0,  # $45 average
        'alert_threshold': 0.75,
        'severity': 'P2'
    },
    'support_tickets_per_hour': {
        'baseline': 5,
        'alert_threshold': 2.0,  # Alert if >2x baseline
        'severity': 'P1'
    }
}

class BusinessMetricsMonitor:
    def __init__(self, analytics_db):
        self.db = analytics_db
        
    def detect_anomalies(self):
        """Detect business metric anomalies"""
        for metric_name, config in BUSINESS_METRICS.items():
            current = self.get_current_value(metric_name)
            baseline = config['baseline']
            threshold = config['alert_threshold']
            
            if metric_name == 'support_tickets_per_hour':
                # Inverse metric—alert if too high
                anomaly = current > (baseline * threshold)
            else:
                # Normal metrics—alert if too low
                anomaly = current < (baseline * threshold)
            
            if anomaly:
                self.alert_business_anomaly(
                    metric_name=metric_name,
                    current=current,
                    baseline=baseline,
                    severity=config['severity']
                )
