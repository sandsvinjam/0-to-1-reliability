class GracefulDegradation:
    """
    Define degradation modes for each service
    """
    DEGRADATION_LEVELS = {
        'inventory_service': {
            'FULL': {
                'description': 'Real-time inventory, accurate counts',
                'latency_target': 100,  # ms
                'data_freshness': 0  # real-time
            },
            'DEGRADED': {
                'description': 'Cached inventory, 5-minute staleness',
                'latency_target': 50,
                'data_freshness': 300,  # 5 minutes
                'fallback_strategy': 'use_cached_inventory'
            },
            'EMERGENCY': {
                'description': 'Static catalog only, no stock info',
                'latency_target': 20,
                'data_freshness': 3600,  # 1 hour
                'fallback_strategy': 'static_catalog'
            }
        },
        'pricing_service': {
            'FULL': {
                'description': 'Dynamic pricing with real-time market data',
                'latency_target': 150,
                'includes': ['surge_pricing', 'personalized_offers']
            },
            'DEGRADED': {
                'description': 'Base pricing only, no dynamic adjustments',
                'latency_target': 50,
                'fallback_strategy': 'base_prices_only'
            },
            'EMERGENCY': {
                'description': 'Cached prices from last successful fetch',
                'latency_target': 10,
                'fallback_strategy': 'cached_prices'
            }
        }
    }
    
    def degrade_service(self, service_name, level):
        """
        Put service into degraded mode
        """
        config = self.DEGRADATION_LEVELS[service_name][level]
        
        # Update service configuration
        self.update_service_mode(service_name, level, config)
        
        # Alert users if necessary
        if level == 'EMERGENCY':
            self.notify_users(
                message="We're experiencing high demand. Some features may be limited.",
                severity='warning'
            )
        
        logger.warning(
            f"Service {service_name} degraded to {level}",
            description=config['description']
        )
