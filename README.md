# AWS-Object-Storage-Alert-System
This workflow is designed to monitor critical file uploads to an Amazon S3 bucket and automatically trigger a chain of serverless actions that ensure visibility, traceability, and alerting for those uploads. Here’s a description of the AWS event-driven serverless workflow that performs the tasks specified above:
Workflow: Serverless File Monitoring and Notification System on AWS

Step 1: Monitor File Uploads to Amazon S3
Trigger: A user or system uploads a file to a designated S3 bucket (e.g., /critical-uploads/).
Service: Amazon S3 Event Notifications
Action: Configured to trigger a Lambda function when a new object is created (s3:ObjectCreated:*).


Step 2: Process Metadata and Store in DynamoDB
Service: AWS Lambda
Action:
Extracts metadata from the uploaded file (e.g., filename, timestamp, uploader info, file type).
Writes this metadata into a DynamoDB table (e.g., CriticalFileMetadata) using the AWS SDK.


Step 3: Send Alert Notifications to Slack
Service: AWS Lambda (same or separate from Step 2, depending on architecture)
Action:
Formats a message (e.g., "🚨 Critical file uploaded: filename.pdf").
Sends the alert to Slack using a Slack webhook URL or via Amazon EventBridge → API destination.


Step 4: Publish a Notification to an SNS Topic
Service: Amazon SNS (Simple Notification Service)
Action:
The Lambda function (or EventBridge rule) also publishes a message to an SNS topic (e.g., CriticalFileUploadTopic).
The topic can fan out the message to other systems—email, SMS, Lambda, HTTP endpoints, etc.


Key Benefits
Fully serverless: No infrastructure management.
Scalable and event-driven.
Integrated alerts and data storage.
Easily extensible (e.g., add audit logging, downstream processing, etc.).
