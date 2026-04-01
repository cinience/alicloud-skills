# ECS Cloud Assistant (RunCommand)

Use Cloud Assistant to execute shell or PowerShell scripts on ECS instances.

## Key requirements

- Instance must be in `Running` state.
- Cloud Assistant agent must be installed and online.
- Use the correct command type for OS (shell for Linux, PowerShell for Windows).

## Typical flow

1) (Optional) Install agent: `InstallCloudAssistant`.
2) Execute command: `RunCommand`.
3) Query execution: `DescribeInvocations` and `DescribeInvocationResults`.

## References

- RunCommand API: https://www.alibabacloud.com/help/en/ecs/developer-reference/runcommand
