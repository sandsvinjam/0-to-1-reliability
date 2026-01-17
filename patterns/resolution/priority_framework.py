def calculate_action_item_priority(action_item):
    """
    Priority = Frequency × Duration × User Impact
    """
    # How often does this type of incident occur?
    frequency_score = {
        'multiple_per_week': 10,
        'weekly': 7,
        'monthly': 4,
        'quarterly': 2,
        'rarely': 1
    }[action_item.frequency]
    
    # How long is typical downtime?
    duration_score = {
        'hours': 10,
        '30_60_min': 7,
        '10_30_min': 4,
        'under_10_min': 2
    }[action_item.typical_duration]
    
    # How severe is user impact?
    impact_score = {
        'revenue_blocking': 10,  # Users can't pay
        'major_degradation': 7,  # Core features broken
        'minor_degradation': 4,  # Slowness, errors
        'cosmetic': 1  # Visual issues only
    }[action_item.user_impact]
    
    priority = frequency_score * duration_score * impact_score
    
    return {
        'priority_score': priority,
        'priority_level': 'P0' if priority >= 300 else 'P1' if priority >= 100 else 'P2'
    }
