# Contributing to 0-to-1 Reliability Framework

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to uphold:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior** vs. actual behavior
- **Environment details** (OS, Python version, dependencies)
- **Code samples** or error messages if applicable

**Example bug report:**
```markdown
**Title:** Circuit breaker fails to open after 5 consecutive failures

**Description:**
The circuit breaker does not transition to OPEN state after reaching the failure threshold.

**Steps to Reproduce:**
1. Configure circuit breaker with failure_threshold=5
2. Trigger 5 consecutive failures
3. Observe circuit breaker state remains CLOSED

**Expected:** Circuit breaker should open after 5 failures
**Actual:** Circuit breaker remains closed

**Environment:**
- Python 3.9
- 0-to-1-reliability v1.0.0
- Ubuntu 20.04
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear, descriptive title**
- **Provide detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful** to most users
- **Include code examples** if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding standards** (see below)
3. **Add tests** for any new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass** before submitting
6. **Write clear commit messages**

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed my code
- [ ] Commented complex code sections
- [ ] Updated documentation
- [ ] Added tests
- [ ] All tests pass
```

## Development Setup

### Local Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/0-to-1-reliability.git
cd 0-to-1-reliability

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=patterns tests/

# Run specific test file
pytest tests/test_detection.py

# Run tests with output
pytest -v

# Run integration tests only
pytest tests/integration/
```

### Code Style

We follow PEP 8 with some modifications:

```python
# Good
def check_permission(self, user: User, resource: Resource) -> bool:
    """
    Check if user has permission for resource.
    
    Args:
        user: User requesting access
        resource: Resource being accessed
        
    Returns:
        True if permission granted, False otherwise
    """
    if not self.is_authenticated(user):
        return False
    
    return self.has_access(user, resource)


# Bad
def check_permission(self,user,resource):
    if not self.is_authenticated(user): return False
    return self.has_access(user,resource)
```

**Key points:**
- Type hints for function parameters and return values
- Docstrings for all public functions and classes
- Max line length: 100 characters
- Use descriptive variable names
- Follow existing patterns in the codebase

### Linting

```bash
# Run flake8
flake8 patterns/ tests/

# Run black formatter
black patterns/ tests/

# Run mypy for type checking
mypy patterns/
```

## Contribution Areas

### High Priority

1. **Additional Monitoring Backends**
   - Splunk integration
   - Elastic APM integration
   - AWS CloudWatch native integration

2. **Framework Integrations**
   - Django middleware for automatic instrumentation
   - FastAPI dependency injection patterns
   - Express.js/Node.js port

3. **Mitigation Playbooks**
   - More common failure scenarios
   - Industry-specific playbooks (e-commerce, fintech)
   - Multi-region failure scenarios

4. **Infrastructure as Code**
   - Terraform modules
   - CloudFormation templates
   - Helm charts for Kubernetes

### Medium Priority

5. **Additional Chaos Scenarios**
   - Memory pressure testing
   - Disk I/O saturation
   - Certificate expiration simulation

6. **Dashboards**
   - Additional Grafana dashboards
   - Datadog dashboard templates
   - New Relic dashboard configs

7. **Documentation**
   - More detailed case studies
   - Video tutorials
   - Interactive examples

### Getting Started

**Good first issues** are labeled with `good-first-issue` tag. These are:
- Well-defined scope
- Clear acceptance criteria
- Guidance provided
- Lower complexity

**Example good first issues:**
- Add support for Slack alerting
- Create dashboard for specific metric
- Write documentation for specific pattern
- Add unit tests for existing code

## Documentation Style

### Code Documentation

```python
class TrustMonitor:
    """
    Monitor service health and determine trust level.
    
    Trust levels indicate system health and determine which operations
    are allowed. Lower trust levels restrict high-risk operations.
    
    Attributes:
        current_level: Current trust level (NORMAL, DEGRADED, CONSTRAINED, NO_TRUST)
        metrics_service: Service for collecting metrics
        
    Example:
        >>> monitor = TrustMonitor()
        >>> metrics = TrustMetrics(auth_latency_p99=250, error_rate=2.0)
        >>> level = monitor.evaluate_trust_level(metrics)
        >>> print(level)
        TrustLevel.DEGRADED
    """
    
    def evaluate_trust_level(self, metrics: TrustMetrics) -> TrustLevel:
        """
        Determine trust level based on current metrics.
        
        Args:
            metrics: Current system metrics
            
        Returns:
            Appropriate trust level for current metrics
            
        Raises:
            ValueError: If metrics are invalid or incomplete
        """
        pass
```

### README/Markdown Documentation

- Use clear, descriptive headings
- Include code examples for concepts
- Provide both simple and advanced usage
- Link to related documentation
- Include troubleshooting section

## Testing Guidelines

### Unit Tests

```python
import pytest
from patterns.detection import CriticalPathMonitor


class TestCriticalPathMonitor:
    """Test suite for CriticalPathMonitor"""
    
    @pytest.fixture
    def monitor(self):
        """Fixture providing configured monitor instance"""
        return CriticalPathMonitor(
            metrics_backend='prometheus',
            critical_paths=TEST_PATHS
        )
    
    def test_tracks_request_success(self, monitor):
        """Should record successful request"""
        monitor.track_request('payment', duration_ms=150, success=True)
        
        # Verify metrics recorded
        assert monitor.get_success_count('payment') == 1
    
    def test_alerts_on_threshold_violation(self, monitor):
        """Should alert when success rate drops below threshold"""
        # Trigger failures
        for _ in range(10):
            monitor.track_request('payment', duration_ms=150, success=False)
        
        # Verify alert triggered
        alerts = monitor.get_triggered_alerts()
        assert len(alerts) == 1
        assert alerts[0].severity == 'P0'
```

### Integration Tests

```python
@pytest.mark.integration
def test_end_to_end_detection_flow():
    """Test complete detection flow from request to alert"""
    # Setup
    monitor = setup_monitor()
    alerter = setup_alerter()
    
    # Execute
    simulate_service_degradation(duration=300)
    
    # Verify
    assert monitor.detected_incident_within_minutes(5)
    assert alerter.sent_page_to_oncall()
```

### Test Coverage Requirements

- **Minimum 80% code coverage** for new features
- **100% coverage for critical paths** (circuit breakers, rollback, etc.)
- Integration tests for key user flows
- Chaos tests for resilience patterns

## Commit Message Guidelines

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples:**

```
feat(detection): add support for custom SLI definitions

Allows users to define custom SLIs beyond the provided defaults.
Includes configuration validation and documentation updates.

Closes #123
```

```
fix(mitigation): correct rollback threshold calculation

Rollback was triggering too aggressively due to incorrect
percentage calculation. Changed to compare absolute values.

Fixes #456
```

## Review Process

1. **Automated checks** run on all PRs:
   - Unit tests
   - Code coverage
   - Linting (flake8, black)
   - Type checking (mypy)

2. **Manual review** by maintainers:
   - Code quality and style
   - Test coverage
   - Documentation
   - Backward compatibility

3. **Approval requirements:**
   - At least one maintainer approval
   - All automated checks passing
   - No unresolved conversations

4. **Merge:**
   - Squash and merge preferred for feature branches
   - Merge commit for larger features
   - Rebase for simple bug fixes

## Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

**Release checklist:**
- [ ] Update version in `setup.py`
- [ ] Update CHANGELOG.md
- [ ] Create release notes
- [ ] Tag release
- [ ] Publish to PyPI
- [ ] Update documentation

## Community

### Getting Help

- **GitHub Discussions:** Ask questions, share ideas
- **GitHub Issues:** Report bugs, request features
- **Twitter:** [@svinjam](https://twitter.com/svinjam) for announcements

### Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Annual contributor spotlight

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Search closed issues
3. Ask in GitHub Discussions
4. Reach out to maintainers

Thank you for contributing to making distributed systems more reliable!
