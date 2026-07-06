"""
Knowledge Base Module

This module contains the company's deployment documentation and best practices.
In a production system, this would be loaded from a database or external source.

Each document has an ID, title, and content. These documents are indexed
and searchable via the RAG retriever.
"""

KNOWLEDGE_BASE = [
    {
        "id": "deploy_process_1",
        "title": "Deployment Process Overview",
        "content": """
        The recommended deployment process consists of these steps:
        
        1. Run the complete test suite to ensure code quality
           - Run all unit tests
           - Run all integration tests
           - Ensure code coverage is above 80%
        
        2. Build Docker artifacts and push to registry
           - Build Docker image with version tag
           - Push to container registry (gcr.io)
           - Verify image is accessible
        
        3. Update configuration files in staging environment
           - Update environment variables
           - Update ConfigMaps
           - Verify configurations are valid
        
        4. Run smoke tests in staging
           - Test critical user journeys
           - Verify database connections
           - Check external API integrations
        
        5. If all tests pass, deploy to production
           - Use blue-green deployment strategy
           - Monitor for errors during deployment
           - Keep previous version as rollback point
        
        6. Monitor logs for 30 minutes after deployment
           - Watch error rates
           - Monitor latency metrics
           - Check resource utilization
        
        Always verify each step completes successfully before moving to the next.
        If any step fails, stop and investigate before retrying.
        Never force a deployment if tests are failing.
        """
    },
    {
        "id": "deploy_process_2",
        "title": "Pre-Deployment Checklist",
        "content": """
        Before deployment, ensure:
        
        ✓ All code is merged to main branch
          - No pending PRs for this release
          - All commits are signed
        
        ✓ Code review approved by at least 2 senior developers
          - Requires approval from tech leads
          - Security review completed
          - Architecture review completed
        
        ✓ No failing tests
          - Unit tests: 100% pass rate
          - Integration tests: 100% pass rate
          - End-to-end tests: 100% pass rate
        
        ✓ Database migrations run successfully
          - Migrations tested on staging
          - Rollback plan documented
          - Data backup verified
        
        ✓ Environment variables are configured
          - All required vars set
          - No hardcoded secrets
          - Secrets stored in vault
        
        ✓ Security scan passed
          - SAST scan completed
          - Dependency audit passed
          - No critical vulnerabilities
        
        ✓ Load testing passed (for production)
          - Can handle 2x peak traffic
          - Response times acceptable
          - No memory leaks detected
        
        ✓ Release notes prepared
          - Feature list documented
          - Breaking changes noted
          - Migration guide provided
        
        ✓ Stakeholders notified
          - Product team informed
          - Customer success notified
          - Support team briefed
        """
    },
    {
        "id": "rollback_procedure",
        "title": "Rollback Procedure (Emergency)",
        "content": """
        If deployment causes issues or outages:
        
        IMMEDIATE ACTIONS (Within 2 minutes):
        1. Immediately revert to previous stable version
           Command: kubectl rollout undo deployment/prod
           This reverts to the previous working version instantly
        
        2. Verify previous version is healthy
           - Check pod status: kubectl get pods
           - Verify endpoints responding: curl http://service/health
           - Check error rates in logs
        
        3. Notify on-call team in Slack
           - Post in #incidents channel
           - Tag on-call engineer
           - Include brief description of issue
        
        POST-ROLLBACK ACTIONS (Within 30 minutes):
        4. Investigate root cause
           - Check logs from failed deployment
           - Review changes in the bad version
           - Identify what went wrong
        
        5. Communicate status to stakeholders
           - Post status update in #incidents
           - Notify customers if needed
           - Set expectations for investigation time
        
        6. Document the incident
           - Create incident report
           - Record timeline
           - Note what warning signs were missed
        
        BEFORE NEXT DEPLOYMENT:
        7. Fix issue and test thoroughly
           - Fix the bug
           - Test locally
           - Test in staging
           - Get code review
        
        8. Analyze what went wrong
           - Was the issue caught by tests?
           - Why didn't tests catch it?
           - How can we prevent this in future?
        
        9. Implement preventative measures
           - Add tests for this scenario
           - Update deployment checklist
           - Add monitoring for this condition
        
        ROLLBACK COMMANDS:
        - Rollback last deployment: kubectl rollout undo deployment/prod
        - Rollback to specific version: kubectl rollout undo deployment/prod --to-revision=3
        - View rollout history: kubectl rollout history deployment/prod
        - Pause deployment: kubectl rollout pause deployment/prod
        
        NOTE: Rollback should take less than 5 minutes total.
        If rollback is slow, something is wrong with your infrastructure.
        """
    },
    {
        "id": "deployment_monitoring",
        "title": "Post-Deployment Monitoring",
        "content": """
        After deployment, monitor these metrics for at least 30 minutes:
        
        ERROR METRICS:
        - Error rate: Should remain < 0.1% (or within 0.1% of baseline)
          - 5xx errors: Must be 0 or declining
          - 4xx errors: Should match previous baseline
          - Check logs for patterns of errors
        
        PERFORMANCE METRICS:
        - Response times (latency):
          - p50 (median): Should match baseline ± 5%
          - p95 (95th percentile): Should be < 500ms
          - p99 (99th percentile): Should be < 2000ms
          - Track if latency is trending up
        
        RESOURCE METRICS:
        - Database connection pool
          - Should not be maxed out
          - Monitor if connections trending up
          - Alert if > 80% utilization
        
        - Memory usage on pods
          - Should not exceed 80% of limits
          - Watch for memory leaks (gradual increase)
          - If memory trending up, prepare to rollback
        
        - CPU usage
          - Should match previous baseline
          - Spikes are normal, but should return to baseline
          - If sustained high CPU, investigate
        
        BUSINESS METRICS:
        - Request rate: Should match expected traffic
        - Transaction success rate: Should be > 99%
        - User reports: Monitor Slack/Support for complaints
        
        AUTOMATED ALERTING:
        Set up Prometheus alerts for:
        - Error rate > 1% for 5 minutes → Page on-call
        - p95 latency > 1000ms for 10 minutes → Page on-call
        - Pod memory > 90% for 5 minutes → Page on-call
        - Pod CPU > 95% for 10 minutes → Notify
        
        MANUAL CHECKS:
        - At 5 minutes: Quick health check
        - At 15 minutes: Detailed metrics review
        - At 30 minutes: Full assessment and sign-off
        
        SIGN-OFF CHECKLIST:
        ✓ Error rate normal
        ✓ Response times normal
        ✓ No memory leaks detected
        ✓ Resource utilization normal
        ✓ No reported issues from users
        ✓ All automated alerts passing
        
        If ALL above are true → Deployment successful ✓
        If ANY are concerning → Prepare to rollback
        """
    },
    {
        "id": "deployment_tools",
        "title": "Deployment Tools and Commands",
        "content": """
        Common deployment tools and their usage:
        
        DOCKER COMMANDS:
        - Build: docker build -t myapp:2.5.0 .
        - Push: docker push gcr.io/myproject/myapp:2.5.0
        - Run locally: docker run -p 8000:8000 myapp:2.5.0
        
        KUBERNETES COMMANDS:
        - Get pods: kubectl get pods -n production
        - View logs: kubectl logs deployment/prod -n production
        - Describe pod: kubectl describe pod POD_NAME -n production
        - Update deployment: kubectl set image deployment/prod myapp=gcr.io/myproject/myapp:2.5.0
        - Rollback: kubectl rollout undo deployment/prod
        - Scale: kubectl scale deployment prod --replicas=5
        
        TESTING TOOLS:
        - Run tests: pytest tests/ -v
        - Run coverage: pytest --cov=src tests/
        - Run integration tests: pytest tests/integration/ -v
        - Load testing: locust -f locustfile.py --host=http://staging
        
        MONITORING:
        - Prometheus: http://prometheus.internal:9090
        - Grafana: http://grafana.internal:3000
        - ELK Stack (Elasticsearch, Logstash, Kibana): http://kibana.internal:5601
        
        CI/CD:
        - GitHub Actions: See .github/workflows/deploy.yml
        - Run manual CI: gh workflow run deploy.yml
        - View CI logs: gh run view
        
        DEPLOYMENT PLATFORMS:
        - Staging: GKE (Google Kubernetes Engine)
        - Production: GKE with multi-region setup
        - Database: Cloud SQL for PostgreSQL
        - Secrets: Google Secret Manager
        """
    },
    {
        "id": "troubleshooting_deployment",
        "title": "Troubleshooting Deployment Issues",
        "content": """
        Common deployment issues and how to fix them:
        
        ISSUE: Pods not starting
        Symptoms: Pods stuck in Pending or ImagePullBackOff
        Fix:
        1. Check image exists: docker pull gcr.io/myproject/myapp:VERSION
        2. Check resource requests: kubectl describe pod POD_NAME
        3. Check PVC availability: kubectl get pvc
        4. View pod logs: kubectl logs POD_NAME
        
        ISSUE: High error rate after deployment
        Symptoms: 5xx errors spike to > 1%
        Fix:
        1. Check logs: kubectl logs deployment/prod --tail=100
        2. Look for exceptions or panics
        3. Verify database connectivity
        4. Check if migrations ran successfully
        5. If unclear, rollback immediately
        
        ISSUE: High latency after deployment
        Symptoms: p95 latency > 1000ms
        Fix:
        1. Check database query performance
        2. Look for N+1 queries
        3. Check for blocking operations
        4. Review recent code changes
        5. Consider scaling up pods
        
        ISSUE: Memory leak
        Symptoms: Memory usage trending up over time
        Fix:
        1. Review recent code changes
        2. Check for circular references or not releasing resources
        3. Look at Go heap dumps or Python memory profiles
        4. Consider rolling pods (graceful restart)
        5. If serious, rollback and fix
        
        ISSUE: Database connection pool exhausted
        Symptoms: "too many connections" errors
        Fix:
        1. Check database queries are closing connections
        2. Look for long-running transactions
        3. Increase pool size (if possible)
        4. Scale up database if needed
        5. Consider connection pooling (PgBouncer)
        
        ISSUE: Deployment timeout
        Symptoms: Deployment hangs, doesn't complete
        Fix:
        1. Check pod readiness probes
        2. Increase deployment timeout
        3. Check if migrations are hanging
        4. Kill hanging pods: kubectl delete pod POD_NAME
        5. Check logs for what's blocking
        
        DEBUG COMMANDS:
        - Port forward to pod: kubectl port-forward pod/NAME 8000:8000
        - Exec into pod: kubectl exec -it pod/NAME -- /bin/bash
        - Stream logs: kubectl logs deployment/prod -f
        - Get metrics: kubectl top nodes / kubectl top pods
        """
    }
]


def get_knowledge_base():
    """
    Get the knowledge base.
    
    Returns:
        list: List of knowledge base documents
    """
    return KNOWLEDGE_BASE


def get_document_by_id(doc_id: str):
    """
    Get a specific document by ID.
    
    Args:
        doc_id: Document ID to retrieve
        
    Returns:
        dict: Document if found, None otherwise
    """
    for doc in KNOWLEDGE_BASE:
        if doc["id"] == doc_id:
            return doc
    return None


def get_all_titles():
    """
    Get all document titles.
    
    Returns:
        list: List of document titles
    """
    return [doc["title"] for doc in KNOWLEDGE_BASE]
