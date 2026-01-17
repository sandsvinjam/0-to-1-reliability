class TrafficShaper:
    def __init__(self, load_balancer):
        self.lb = load_balancer
        
    def shed_load(self, service_name, percentage):
        """
        Shed a percentage of traffic to protect service
        """
        config = {
            'service': service_name,
            'load_shedding': {
                'enabled': True,
                'reject_percentage': percentage,
                'response_code': 503,
                'retry_after': 60  # seconds
            }
        }
        
        self.lb.update_config(config)
        
        logger.warning(
            f"Load shedding enabled for {service_name}",
            percentage=percentage
        )
    
    def enable_circuit_breaker(self, service_name, dependency):
        """
        Open circuit breaker to failing dependency
        """
        config = {
            'service': service_name,
            'circuit_breaker': {
                'dependency': dependency,
                'state': 'OPEN',
                'timeout': 60
            }
        }
        
        self.lb.update_config(config)
        
        logger.warning(
            f"Circuit breaker opened for {service_name} → {dependency}"
        )
    
    def redirect_traffic(self, service_name, from_region, to_region):
        """
        Redirect traffic from unhealthy region
        """
        config = {
            'service': service_name,
            'traffic_routing': {
                'from': from_region,
                'to': to_region,
                'percentage': 100
            }
        }
        
        self.lb.update_config(config)
        
        logger.critical(
            f"Traffic redirected: {service_name} from {from_region} → {to_region}"
        )
