# IAM

## Objetive
Implement the ‘Zero Trust’ principle. In the cloud, the network is no longer your primary perimeter; identities and permissions are.

### Identities
The golden rule in AWS IAM is to understand who or what is going to authenticate and what the lifecycle of their credentials is:
- **IAM users:** An entity representing a real person or a fixed external application. It has long-term (static) credentials and is mainly used by developers, administrators and on-premises services that need to communicate with AWS. Credentials are rotated manually, which carries a high risk if access keys are leaked. 

- **IAM roles:** An identity with temporary permissions that can be ‘assumed’ by trusted entities. It has short-term (dynamic/temporary) credentials generated using AWS STS (Security Token Service). It is used by native AWS services, for cross-account access and for federated users. Rotation is automatic and managed by AWS.

### JSON Policies
These are the documents that define what is permitted and what is not. AWS evaluates these JSON files every time an API call is attempted. They have three main elements:
- **`Effect`:** Only supports two values: ‘Allow’ or ‘Deny’ (default).

- **`Action`:** Defines the API call or calls to the service that are authorised or blocked. It follows the format `service:operation`.
 
- **`Resource`:** Specifies the exact target to which the action applies via its ARN (Amazon Resource Name).

### Principle of Least Privilege
It stipulates that an identity must have only the permissions strictly necessary to perform its task, and no more. Using wildcards such as `‘Action’: ‘*’` or `“Resource”: ‘*’` is a lazy practice that security auditors (and standards such as SOC2, ISO 27001 or PCI-DSS) immediately flag as a serious vulnerability for the following reasons:
- **Increased Blast Radius:** If a Lambda function has `‘Action’: ‘s3:*’` on `“Resource”: ‘*’`, and the Lambda code suffers a code injection, the attacker will not only be able to read the bucket the Lambda required, but also delete all buckets in the account (`s3:DeleteBucket`) or exfiltrate data from other departments.

- **Risk of Privilege Escalation:** Granting broad permissions on certain services (particularly IAM) allows an attacker to become an administrator. For example, if you grant `‘Action’: ‘iam:*’` so that a service ‘runs smoothly’, that service can create a new administrator user with a password and perpetual access to the console.

- **Lack of Traceability and Intent:** In a post-incident forensic audit, a strict policy demonstrates exactly what the service was intended to do. A wildcard negates the ability to audit the intent of the architectural design.

- **Emergence of New Services and APIs:** AWS is constantly adding new actions to its services. If you use `‘Action’: ‘dynamodb:*’`, you are automatically granting permissions for destructive or replication APIs that AWS may introduce in the future, without you having assessed them beforehand.

### Exercise 1: Enable MFA (Multi-Factor Authentication) on your Root account and do not use it again.
Log in to AWS using your Root user account. In the top-right corner, click on your account name and select ‘Security credentials’. In the ‘Multi-factor authentication (MFA)’ section, click on ‘Assign MFA device’:

![security_credentials](img/security_credentials.png)

Choose a name for the device and select the ‘Authenticator App’ option:

![authenticator_app](img/authenticator_app.png)

In the next window, scan the QR code using an authorised app and enter the first two codes in the boxes below:

![qr](img/qr.png)

### Exercise 2: Create an IAM user for day-to-day tasks, add them to the DevOpsAdmins group, and enforce MFA.
First, go to IAM > ‘User Groups’ > ‘Create group’. Set a user name and, in the ‘Attach permissions policies’ section, select the `AdministratorAccess` policy:

![group](img/group.png)

Once the group has been created, return to the IAM menu and go to ‘Users’ > ‘Create user’. Set a username, tick the ‘Provide user access to the AWS Management Console’ box, select ‘I want to create an IAM user’ and choose ‘Custom password’. Also, untick the option to force a password change:

![user_1](img/user_1.png)

On the permissions screen, select ‘Add user to group’ and tick the group we created earlier:

![user_2](img/user_2.png)

Now log out of the Root user and log in with the MFA user. Once logged in, go to the security credentials and enable MFA in the same way as in Exercise 1:

![user_mfa](img/user_mfa.png)

![daily_user_mfa_1](img/daily_user_mfa_1.png)

![daily_user_mfa_2](img/daily_user_mfa_2.png)

### Exercise 3: Write a custom JSON policy that denies any action to delete EC2 instances if the user has not logged in using MFA (‘aws:MultiFactorAuthPresent’: ‘false’).
Using the administrator account, go to IAM > ‘Policies’ > ‘Create policy’. Switch to the ‘JSON’ tab and add the policy code:

![policie_json](img/policie_json.png)

In the next window, choose a name and create the policy:

![policie_name](img/policie_name.png)

Finally, go to ‘Users and groups’ > click on `DevOpsAdmin` > “Permissions” tab > ‘Add permissions’ > ‘Attach policies’. Locate the policy you have just created and click ‘Add permissions’:

![policie_asigned](img/policie_asigned.png)

### Exercise 4: Create a role called EC2-ReadS3-Role that allows a virtual machine to list a specific bucket without needing to store passwords within it.
First, let’s create a new IAM policy for this role:

![role_policie_1](img/role_policie_1.png)

![role_policie_2](img/role_policie_2.png)

Now go to the side menu “Roles” > “Create role”. Leave ‘AWS service’ selected and, in the ‘Service or use case’ drop-down menu, choose ‘EC2’:

![role_1](img/role_1.png)

In the next window, select the policy created earlier: 

![role_2](img/role_2.png)

Choose a name for the role:

![role_3](img/role_3.png)

Now go to the EC2 console > ‘Instances’, select the instance, go to ‘Actions’ > “Security” and ‘Modify IAM role’. Select the role and click ‘Update IAM role’:

![role_4](img/role_4.png)