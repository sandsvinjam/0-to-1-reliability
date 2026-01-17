# Alert quality metrics
class AlertQualityTracker:
    def track_alert(self, alert):
        """Track alert outcomes to identify noise"""
        outcome = self.get_alert_outcome(alert)
        
        self.metrics.increment(
            'alert.outcomes',
            tags={
                'alert_name': alert.name,
                'outcome': outcome,  # actionable, false_positive, info_only
                'severity': alert.severity
            }
        )
    
    def identify_noisy_alerts(self):
        """Find alerts with low actionability"""
        alerts = self.get_all_alerts()
        
        noisy = []
        for alert in alerts:
            outcomes = self.get_outcomes_last_30_days(alert)
            actionable_rate = outcomes['actionable'] / outcomes['total']
            
            if actionable_rate < 0.7:  # <70% actionable
                noisy.append({
                    'alert': alert.name,
                    'actionable_rate': actionable_rate,
                    'recommendation': 'Tune thresholds or remove'
                })
        
        return noisy
