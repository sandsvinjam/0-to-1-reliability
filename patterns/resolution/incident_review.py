class IncidentReview:
    """
    Structured post-incident review process
    """
    def __init__(self, incident_id):
        self.incident = self.load_incident(incident_id)
        
    def conduct_review(self):
        """
        Complete post-incident review
        """
        review = {
            'incident_id': self.incident.id,
            'severity': self.incident.severity,
            'timeline': self.reconstruct_timeline(),
            'impact': self.calculate_impact(),
            'root_cause': self.perform_five_whys(),
            'contributing_factors': self.identify_contributing_factors(),
            'action_items': self.create_action_items(),
            'reviewed_by': self.get_participants(),
            'review_date': datetime.utcnow()
        }
        
        return review
    
    def reconstruct_timeline(self):
        """
        Build accurate timeline of events
        """
        events = []
        
        # Collect events from multiple sources
        events.extend(self.incident.logged_events)
        events.extend(self.get_deployment_events())
        events.extend(self.get_alert_events())
        events.extend(self.get_mitigation_events())
        
        # Sort chronologically
        events.sort(key=lambda e: e.timestamp)
        
        return [
            {
                'timestamp': e.timestamp,
                'event': e.description,
                'source': e.source,
                'actor': e.actor
            }
            for e in events
        ]
    
    def calculate_impact(self):
        """
        Quantify incident impact
        """
        return {
            'duration': self.incident.duration_minutes,
            'affected_users': self.estimate_affected_users(),
            'failed_requests': self.count_failed_requests(),
            'revenue_impact': self.estimate_revenue_impact(),
            'user_experience': self.categorize_ux_impact()
        }
    
    def perform_five_whys(self):
        """
        Root cause analysis using five whys
        """
        whys = []
        current_symptom = self.incident.initial_symptom
        
        for i in range(5):
            why = f"Why {i+1}: {current_symptom}"
            answer = self.ask_why(current_symptom)
            whys.append({
                'question': why,
                'answer': answer
            })
            current_symptom = answer
            
            # Stop if we've reached root cause
            if self.is_root_cause(answer):
                break
        
        return {
            'analysis': whys,
            'root_cause': whys[-1]['answer'] if whys else None
        }
    
    def create_action_items(self):
        """
        Generate specific, actionable items
        """
        action_items = []
        
        # Immediate fixes (< 1 week)
        action_items.extend(self.identify_immediate_fixes())
        
        # Short-term improvements (1-4 weeks)
        action_items.extend(self.identify_short_term_improvements())
        
        # Long-term investments (1-3 months)
        action_items.extend(self.identify_long_term_investments())
        
        # Prioritize by impact
        prioritized = self.prioritize_action_items(action_items)
        
        return [
            {
                'description': item.description,
                'owner': item.owner,
                'due_date': item.due_date,
                'priority': item.priority,
                'estimated_effort': item.effort_days,
                'expected_impact': item.impact_score
            }
            for item in prioritized
        ]
