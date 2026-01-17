# Testing requirements before any deployment
class PreDeploymentGate:
    def __init__(self):
        self.requirements = {
            'unit_tests': {
                'coverage_threshold': 80,  # 80% code coverage
                'required': True
            },
            'integration_tests': {
                'required_scenarios': [
                    'happy_path',
                    'error_handling',
                    'timeout_handling',
                    'dependency_failure'
                ],
                'required': True
            },
            'load_tests': {
                'target_rps': 'peak_traffic * 2',  # 2x peak capacity
                'duration_minutes': 30,
                'success_criteria': {
                    'error_rate': '<1%',
                    'latency_p95': '<500ms',
                    'throughput': '>= target_rps'
                },
                'required': True
            },
            'chaos_tests': {
                'scenarios': [
                    'database_unavailable',
                    'dependency_timeout',
                    'high_latency',
                    'partial_deployment'
                ],
                'required_for_critical_services': True
            }
        }
    
    def can_deploy(self, service_name, test_results):
        """
        Check if service passes all deployment gates
        """
        failures = []
        
        # Check unit test coverage
        if test_results['unit_coverage'] < self.requirements['unit_tests']['coverage_threshold']:
            failures.append(
                f"Unit test coverage {test_results['unit_coverage']}% < "
                f"required {self.requirements['unit_tests']['coverage_threshold']}%"
            )
        
        # Check integration test scenarios
        required_scenarios = set(self.requirements['integration_tests']['required_scenarios'])
        tested_scenarios = set(test_results['integration_scenarios'])
        missing = required_scenarios - tested_scenarios
        
        if missing:
            failures.append(f"Missing integration test scenarios: {missing}")
        
        # Check load test results
        load_test = test_results['load_test']
        criteria = self.requirements['load_tests']['success_criteria']
        
        if load_test['error_rate'] >= float(criteria['error_rate'].strip('<%')):
            failures.append(f"Load test error rate too high: {load_test['error_rate']}%")
        
        if load_test['latency_p95'] >= int(criteria['latency_p95'].strip('<ms')):
            failures.append(f"Load test p95 latency too high: {load_test['latency_p95']}ms")
        
        # Check chaos test results for critical services
        if service_name in CRITICAL_SERVICES:
            required_chaos = set(self.requirements['chaos_tests']['scenarios'])
            tested_chaos = set(test_results.get('chaos_scenarios', []))
            missing_chaos = required_chaos - tested_chaos
            
            if missing_chaos:
                failures.append(f"Missing chaos test scenarios: {missing_chaos}")
        
        if failures:
            return DeploymentGateResult(
                can_deploy=False,
                failures=failures,
                recommendation="Fix failing tests before deployment"
            )
        
        return DeploymentGateResult(can_deploy=True, failures=[])
