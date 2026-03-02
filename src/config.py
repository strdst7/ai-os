"""
AI-OS Configuration Layer
Centralized governance for guardrail thresholds
"""

class GuardrailConfig:
    """
    Configurable stability thresholds.
    These can later be moved to environment variables.
    """

    LATENCY_THRESHOLD = 0.3
    DRIFT_THRESHOLD = 0.2
    COST_VOLATILITY_THRESHOLD = 0.4


class MonitoringConfig:
    """
    Monitoring system configuration.
    """

    HISTORY_LIMIT = 20
    MONITOR_INTERVAL_SECONDS = 10
