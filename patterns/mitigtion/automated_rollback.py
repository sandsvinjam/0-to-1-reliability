class AutomatedRollback:
    def __init__(self, deployment_service, health_checker):
        self.deployment = deployment_service
        self.health = health_checker
        
    def deploy_with_auto_rollback(self, service_name, new_version):
        """
        Deploy with automatic rollback if health degrades
        """
        # Record current metrics
        baseline_metrics = self.health.get_baseline(service_name)
        
        # Deploy new version
        self.deployment.deploy(service_name, new_version)
        
        # Monitor for 10 minutes
        for minute in range(10):
            time.sleep(60)
            
            current_metrics = self.health.get_current(service_name)
            
            # Check if metrics degraded
            if self._metrics_degraded(baseline_metrics, current_metrics):
                logger.error(
                    f"Health degradation detected for {service_name}",
                    baseline=baseline_metrics,
                    current=current_metrics
                )
                
                # Automatic rollback
                previous_version = self.deployment.get_previous_version(service_name)
                self.deployment.deploy(service_name, previous_version)
                
                self.alert(
                    severity='P0',
                    title=f"Auto-rollback triggered for {service_name}",
                    message=f"Rolled back {new_version} → {previous_version} due to health degradation"
                )
                
                return RollbackResult(
                    success=False,
                    rolled_back=True,
                    reason="Health degradation detected"
                )
        
        return RollbackResult(success=True, rolled_back=False)
    
    def _metrics_degraded(self, baseline, current):
        """Check if current metrics are significantly worse than baseline"""
        # Error rate increased by >50%
        if current['error_rate'] > baseline['error_rate'] * 1.5:
            return True
        
        # Latency increased by >100%
        if current['latency_p95'] > baseline['latency_p95'] * 2.0:
            return True
        
        # Success rate dropped by >5%
        if current['success_rate'] < baseline['success_rate'] - 5.0:
            return True
        
        return False
