# Validation Questions

## Question 1

If the CIDR 10.10.2.0/24 runs out of available IPs, which subnets are affected according to our architecture map?

### Expected answer

The affected subnet is `private-app-subnet-a`.

Its CIDR block is `10.10.2.0/24` and it is located in `eu-west-1a`.

According to the infrastructure context, this subnet is used by:

- `eks-node-group`
- `eks-pods`
- `internal-services`

The impact would be on workloads scheduled in `eu-west-1a`, especially EKS nodes, pods and internal services using `private-app-subnet-a`.

The directly affected database subnets are not `database-subnet-a` or `database-subnet-b`, because they use different CIDR blocks: `10.10.10.0/24` and `10.10.11.0/24`.

---

## Question 2

Which subnets are used by the EKS cluster?

### Expected answer

The EKS cluster `production-eks-cluster` uses these private application subnets:

- `private-app-subnet-a`, with CIDR `10.10.2.0/24`, in `eu-west-1a`
- `private-app-subnet-b`, with CIDR `10.10.3.0/24`, in `eu-west-1b`

These subnets are used by the EKS node group, EKS pods and internal services.

---

## Question 3

Can the PostgreSQL database be accessed directly from the public subnets?

### Expected answer

No.

The database `postgres-database` is not publicly accessible.

The JSON indicates:

- `publicly_accessible`: `false`
- It is accessible only from `private-app-subnet-a` and `private-app-subnet-b`
- Its security group allows inbound traffic from `eks-node-security-group` on port `5432`

Therefore, public subnets should not have direct access to PostgreSQL.

---

## Question 4

If nat-gateway-a fails, which subnet is affected?

### Expected answer

The affected subnet is `private-app-subnet-a`.

According to the routing map, `private-app-subnet-a` is attached to `private-route-table-a`, whose default route is `nat-gateway-a`.

The affected resources are:

- `eks-node-group`
- `eks-pods`
- `internal-services`

These resources may lose outbound internet access through NAT in `eu-west-1a`.

---

## Question 5

Which components depend on postgres-database?

### Expected answer

The workloads that depend on `postgres-database` are:

- `api-service`
- `worker-service`

Both are running in the `production` namespace inside the `production-eks-cluster`.