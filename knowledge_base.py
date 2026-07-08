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

        1. Run the complete test suite
           - Run unit tests
           - Run integration tests
           - Verify code quality

        2. Build the application
           - Create the release package
           - Verify the build completed successfully

        3. Update application configuration
           - Review environment settings
           - Validate configuration values

        4. Deploy to the staging environment
           - Perform smoke testing
           - Verify application functionality
           - Check database connectivity

        5. Deploy to production
           - Deploy the approved release
           - Keep the previous version available for rollback

        6. Monitor the application
           - Watch error rates
           - Verify response times
           - Ensure application health

        Always verify each step before continuing.
        If any step fails, stop the deployment and investigate.
        """
    },

    {
        "id": "deploy_process_2",
        "title": "Pre-Deployment Checklist",
        "content": """
        Before deployment, ensure:

        - All planned changes are complete
        - Code review is approved
        - All automated tests pass
        - Database changes are validated
        - Configuration values are verified
        - Security checks are completed
        - Performance testing is satisfactory
        - Release notes are prepared
        - Stakeholders are informed

        Never deploy if critical issues remain unresolved.
        """
    },

    {
        "id": "rollback_procedure",
        "title": "Rollback Procedure",
        "content": """
        If deployment causes issues:

        1. Restore the previous stable version.
        2. Verify the application is functioning correctly.
        3. Notify the support team.
        4. Investigate the root cause.
        5. Document the incident.
        6. Fix the issue before attempting another deployment.

        A rollback should be quick and well documented.
        """
    },

    {
        "id": "deployment_monitoring",
        "title": "Post-Deployment Monitoring",
        "content": """
        Monitor the application for at least 30 minutes after deployment.

        Check:
        - Error rates
        - Response times
        - Memory usage
        - CPU utilization
        - Database performance
        - User-reported issues

        Compare current metrics with the normal baseline.

        If abnormal behavior is detected, investigate immediately and
        prepare for rollback if necessary.
        """
    },

    {
        "id": "deployment_tools",
        "title": "Deployment Tools",
        "content": """
        Common deployment activities include:

        - Running automated tests
        - Building release packages
        - Executing deployment pipelines
        - Reviewing deployment logs
        - Monitoring application health
        - Tracking release history
        - Reviewing performance dashboards

        Use the tools approved by your organization for these tasks.
        """
    },

    {
        "id": "troubleshooting_deployment",
        "title": "Troubleshooting Deployment Issues",
        "content": """
        Common deployment issues:

        Application fails to start
        - Review application logs
        - Verify configuration
        - Check required services

        High error rate
        - Review recent changes
        - Check database connectivity
        - Validate external service availability

        Slow performance
        - Identify slow operations
        - Review resource utilization
        - Compare with previous releases

        Memory usage increasing
        - Look for memory leaks
        - Review recent code changes
        - Restart the application if necessary

        Deployment timeout
        - Check deployment logs
        - Verify deployment steps
        - Retry after resolving the underlying issue

        Always investigate the root cause before attempting another deployment.
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