class CapacityPlanner:
    """
    Predict and prevent capacity issues
    """
    def predict_capacity_needs(self, service_name, horizon_days=30):
        """
        Forecast capacity requirements
        """
        # Get historical usage data
        historical = self.get_usage_history(service_name, days=90)
        
        # Fit growth model
        growth_model = self.fit_growth_model(historical)
        
        # Project future usage
        forecast = growth_model.predict(horizon_days)
        
        # Compare to current capacity
        current_capacity = self.get_current_capacity(service_name)
        
        # Calculate headroom
        headroom_days = self.calculate_headroom(forecast, current_capacity)
        
        if headroom_days < 14:
            self.alert_capacity_warning(
                service=service_name,
                headroom_days=headroom_days,
                action="Scale up capacity in next 2 weeks"
            )
        
        return CapacityForecast(
            service=service_name,
            current_usage=historical[-1],
            forecast=forecast,
            current_capacity=current_capacity,
            headroom_days=headroom_days
        )
