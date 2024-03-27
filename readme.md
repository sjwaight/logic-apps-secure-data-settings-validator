# Sample Azure Logic App and Secure Data Settings Validator

This sample repository contains a single Logic Apps Standard project with two simple workflows defined.

One workflow has the default settings for security of triggers and actions, while the other workflow has the security settings configured.

## Run the secure data parser

You will find a Python script in the root of the repository that you can use to determine whether workflows are configured for secure data handling or not.

Pass the current folder and the script will search for all workflows and validate them.

```bash
python validate-secure-data-settings.py .
```

Note: if you want to return a non-zero error code from this script (maybe for CI?) then pass `--exit-code` as an argument.

Your output should look similar to this.

```bash
Processing file: ./InsecureWorkflow/workflow.json

Actions
=======
Name: HTTP
        'runtimeConfiguration' node with 'secureData' child is not present

Triggers
========
Name: When_a_HTTP_request_is_received
        'runtimeConfiguration' node with 'secureData' child is not present

Processing file: ./SecureWorkflow/workflow.json

Actions
=======
Name: HTTP
        'runtimeConfiguration' node with 'secureData' child is present
                'inputs' is present in 'properties'
                'outputs' is present in 'properties'

Triggers
========
Name: When_a_HTTP_request_is_received
        'runtimeConfiguration' node with 'secureData' child is present
                'inputs' is present in 'properties'
                'outputs' is present in 'properties'
```
