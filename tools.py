"""
Tools Module

This module defines the tools that the agentic AI can call.
Each tool represents an action that can be taken (e.g., running tests, deploying).

In production, these would call real APIs and infrastructure tools.
For this demo, they simulate the behavior.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Callable
import time


# ============================================================================
# Tool Input Schemas (using Pydantic for validation)
# ============================================================================

class RunTestsInput(BaseModel):
    """Run the test suite."""
    test_scope: str = Field(
        default="all",
        description="Scope: 'unit', 'integration', or 'all'",
        pattern="^(unit|integration|all)$"
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose output"
    )


class BuildArtifactsInput(BaseModel):
    """Build Docker artifacts."""
    version: str = Field(
        description="Version to build (e.g., '2.5.0')",
        min_length=1
    )
    push_to_registry: bool = Field(
        default=True,
        description="Push to container registry after building"
    )
    registry: str = Field(
        default="gcr.io/myproject",
        description="Container registry URL"
    )


class DeployToStagingInput(BaseModel):
    """Deploy to staging environment."""
    version: str = Field(
        description="Version to deploy",
        min_length=1
    )
    wait_for_health: bool = Field(
        default=True,
        description="Wait for health checks to pass"
    )
    replicas: int = Field(
        default=3,
        description="Number of replicas to deploy",
        ge=1,
        le=10
    )


class CheckMonitoringInput(BaseModel):
    """Check monitoring metrics post-deployment."""
    duration_minutes: int = Field(
        default=5,
        description="How long to monitor (in minutes)",
        ge=1,
        le=60
    )
    metrics: list = Field(
        default=["error_rate", "latency", "memory", "cpu"],
        description="Metrics to check"
    )


# ============================================================================
# Tool Implementations (Simulated for demo)
# ============================================================================

def run_tests(test_scope: str = "all", verbose: bool = False) -> str:
    """
    Simulate running the test suite.
    
    In production, this would:
    1. Execute: pytest tests/ -v
    2. Parse results
    3. Return detailed report
    
    Args:
        test_scope: Which tests to run
        verbose: Whether to show detailed output
        
    Returns:
        Test results summary
    """
    print(f"    [Simulating] Running {test_scope} tests...")
    time.sleep(1)  # Simulate test execution time
    
    results = []
    if test_scope in ["unit", "all"]:
        results.append("✓ Unit tests: 147 passed, 0 failed, 0 skipped")
    if test_scope in ["integration", "all"]:
        results.append("✓ Integration tests: 42 passed, 0 failed, 0 skipped")
    
    if verbose:
        results.append("\nDetailed output:")
        results.append("  - Database connection tests: PASS")
        results.append("  - API endpoint tests: PASS")
        results.append("  - Authentication tests: PASS")
    
    return "\n".join(results)


def build_artifacts(
    version: str,
    push_to_registry: bool = True,
    registry: str = "gcr.io/myproject"
) -> str:
    """
    Simulate building Docker artifacts.
    
    In production, this would:
    1. Execute: docker build -t myapp:VERSION .
    2. Create Docker image
    3. Optionally push to registry
    4. Return build summary
    
    Args:
        version: Version to build
        push_to_registry: Whether to push to registry
        registry: Registry URL
        
    Returns:
        Build results summary
    """
    print(f"    [Simulating] Building Docker image for version {version}...")
    time.sleep(2)  # Simulate build time
    
    results = []
    results.append(f"✓ Built Docker image: myapp:{version}")
    results.append(f"  Image size: 245MB")
    results.append(f"  Layers: 12")
    results.append(f"  Base image: python:3.11-slim")
    
    if push_to_registry:
        print(f"    [Simulating] Pushing to {registry}...")
        time.sleep(1)
        results.append(f"\n✓ Pushed to registry: {registry}/myapp:{version}")
        results.append(f"  Registry URL: {registry}/myapp:{version}")
        results.append(f"  Digest: sha256:abcd1234...")
    
    return "\n".join(results)


def deploy_to_staging(
    version: str,
    wait_for_health: bool = True,
    replicas: int = 3
) -> str:
    """
    Simulate deploying to staging environment.
    
    In production, this would:
    1. Update Kubernetes deployment
    2. Wait for pods to start
    3. Run health checks
    4. Return deployment status
    
    Args:
        version: Version to deploy
        wait_for_health: Whether to wait for health checks
        replicas: Number of replicas
        
    Returns:
        Deployment results summary
    """
    print(f"    [Simulating] Deploying {version} to staging ({replicas} replicas)...")
    time.sleep(2)  # Simulate deployment time
    
    results = []
    results.append(f"✓ Deployed {version} to staging environment")
    results.append(f"  Replicas: {replicas}")
    results.append(f"  Namespace: staging")
    results.append(f"  Deployment: myapp-staging")
    
    if wait_for_health:
        print(f"    [Simulating] Waiting for health checks...")
        time.sleep(1)
        results.append(f"\n✓ Health checks passed")
        results.append(f"  All {replicas} pods ready")
        results.append(f"  Endpoints responding: http://staging.myapp.internal")
        results.append(f"  Readiness probes: PASS")
        results.append(f"  Liveness probes: PASS")
    
    return "\n".join(results)


def check_monitoring(
    duration_minutes: int = 5,
    metrics: list = None
) -> str:
    """
    Simulate checking monitoring metrics post-deployment.
    
    In production, this would:
    1. Query Prometheus for metrics
    2. Check error rates, latency, resource usage
    3. Compare against baseline
    4. Return assessment
    
    Args:
        duration_minutes: How long to monitor
        metrics: Which metrics to check
        
    Returns:
        Monitoring results summary
    """
    if metrics is None:
        metrics = ["error_rate", "latency", "memory", "cpu"]
    
    print(f"    [Simulating] Checking monitoring metrics for {duration_minutes} minutes...")
    time.sleep(2)  # Simulate monitoring time
    
    results = []
    results.append(f"✓ Monitoring check completed ({duration_minutes} minutes):")
    
    if "error_rate" in metrics:
        results.append(f"  - Error rate: 0.05% (✓ normal, baseline: 0.03%)")
    
    if "latency" in metrics:
        results.append(f"  - P50 latency: 120ms (✓ normal)")
        results.append(f"  - P95 latency: 245ms (✓ normal, baseline: 250ms)")
        results.append(f"  - P99 latency: 890ms (✓ normal, baseline: 900ms)")
    
    if "memory" in metrics:
        results.append(f"  - Memory usage: 65% (✓ healthy)")
        results.append(f"  - Memory trend: Stable (no leak detected)")
    
    if "cpu" in metrics:
        results.append(f"  - CPU usage: 42% (✓ healthy)")
        results.append(f"  - CPU trend: Normal variation")
    
    results.append(f"\n  Overall assessment: ✅ HEALTHY")
    
    return "\n".join(results)


def simulate_rollback(version: str) -> str:
    """
    Simulate rolling back to a previous version.
    
    In production, this would:
    1. Execute: kubectl rollout undo deployment/prod
    2. Wait for pods to restart
    3. Verify deployment
    
    Args:
        version: Version to rollback from
        
    Returns:
        Rollback results summary
    """
    print(f"    [Simulating] Rolling back from {version}...")
    time.sleep(2)
    
    results = []
    results.append(f"✓ Rollback completed")
    results.append(f"  Previous version: 2.4.0")
    results.append(f"  Bad version: {version}")
    results.append(f"  Status: All pods healthy")
    
    return "\n".join(results)


# ============================================================================
# Tool Registry
# ============================================================================

tool_registry: Dict[str, Dict[str, Any]] = {
    "run_tests": {
        "function": run_tests,
        "input_schema": RunTestsInput,
        "description": "Run the test suite to verify code quality"
    },
    "build_artifacts": {
        "function": build_artifacts,
        "input_schema": BuildArtifactsInput,
        "description": "Build Docker artifacts and push to container registry"
    },
    "deploy_to_staging": {
        "function": deploy_to_staging,
        "input_schema": DeployToStagingInput,
        "description": "Deploy to staging environment and verify health"
    },
    "check_monitoring": {
        "function": check_monitoring,
        "input_schema": CheckMonitoringInput,
        "description": "Check monitoring metrics post-deployment (error rate, latency, resources)"
    }
}


def get_tool_registry() -> Dict[str, Dict[str, Any]]:
    """
    Get the tool registry.
    
    Returns:
        Dictionary of available tools
    """
    return tool_registry


def get_tool_names() -> list:
    """
    Get list of available tool names.
    
    Returns:
        List of tool names
    """
    return list(tool_registry.keys())


def get_tool_description(tool_name: str) -> str:
    """
    Get description of a specific tool.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Tool description or None if not found
    """
    if tool_name in tool_registry:
        return tool_registry[tool_name]["description"]
    return None


def test_tools():
    """
    Test all tools independently.
    """
    print("\n" + "="*70)
    print("Testing Tools")
    print("="*70 + "\n")
    
    # Test run_tests
    print("Testing run_tests():")
    result = run_tests("all")
    print(result)
    
    # Test build_artifacts
    print("\n" + "-"*70)
    print("Testing build_artifacts():")
    result = build_artifacts("2.5.0")
    print(result)
    
    # Test deploy_to_staging
    print("\n" + "-"*70)
    print("Testing deploy_to_staging():")
    result = deploy_to_staging("2.5.0")
    print(result)
    
    # Test check_monitoring
    print("\n" + "-"*70)
    print("Testing check_monitoring():")
    result = check_monitoring(5)
    print(result)


if __name__ == "__main__":
    test_tools()
