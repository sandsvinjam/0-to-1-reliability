class ProgressiveRollout:
    """
    Gradually roll out changes to minimize blast radius
    """
    ROLLOUT_STAGES = [
        {'name': 'canary', 'percentage': 1, 'duration_minutes': 30},
        {'name': 'small', 'percentage': 10, 'duration_minutes': 60},
        {'name': 'medium', 'percentage': 50, 'duration_minutes': 120},
        {'name': 'full', 'percentage': 100, 'duration_minutes': 0}
    ]
    
    def deploy(self, service_name, new_version):
        """
        Deploy with progressive rollout
        """
        for stage in self.ROLLOUT_STAGES:
            logger.info(
                f"Deploying {service_name} {new_version} to {stage['percentage']}%"
            )
            
            # Update traffic routing
            self.set_traffic_split(service_name, new_version, stage['percentage'])
            
            # Monitor health during this stage
            if not self.monitor_health(service_name, stage['duration_minutes']):
                logger.error(f"Health degradation detected at {stage['name']} stage")
                self.rollback(service_name, new_version)
                return DeploymentResult(success=False, stage=stage['name'])
            
            logger.info(f"Stage {stage['name']} completed successfully")
        
        return DeploymentResult(success=True, stage='full')
    
    def monitor_health(self, service_name, duration_minutes):
        """
        Monitor service health during rollout stage
        """
        baseline = self.get_baseline_metrics(service_name)
        
        end_time = datetime.utcnow() + timedelta(minutes=duration_minutes)
        
        while datetime.utcnow() < end_time:
            current = self.get_current_metrics(service_name)
            
            # Check for degradation
            if current['error_rate'] > baseline['error_rate'] * 1.5:
                return False
            
            if current['latency_p95'] > baseline['latency_p95'] * 2.0:
                return False
            
            time.sleep(60)  # Check every minute
        
        return True
