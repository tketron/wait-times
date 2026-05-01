# 📡 Time-Series Polling Service (Python + AWS)

## 🎯 Goals

Build a service that:

* Polls an external API every 5–15 minutes
* Stores results in a database
* Supports time-range queries by name
* Is deployed and managed in AWS
* Uses Infrastructure as Code (IaC)
* Incorporates multiple AWS services for learning

---

# 🧱 Final Architecture (Target State)

```
EventBridge (schedule)
        ↓
      SQS (queue)
        ↓
     Lambda (consumer)
        ↓
     RDS Postgres
```

### Optional Extensions

* ECS worker (alternative consumer)
* Dead Letter Queue (DLQ)
* RDS Proxy
* Observability (CloudWatch dashboards/alarms)

---

# 🧩 Core Data Model

## Table: `wait_times`

```sql
CREATE TABLE wait_times (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    polled_at TIMESTAMP NOT NULL,
    wait_time INTEGER NOT NULL
);
```

## Index (critical)

```sql
CREATE INDEX idx_name_time
ON wait_times (name, polled_at DESC);
```

## Optional (deduplication)

```sql
CREATE UNIQUE INDEX uniq_name_time
ON wait_times (name, polled_at);
```

---

# 🛣️ Implementation Roadmap

This is broken into phases with clear stopping points for testing.

---

# 🟢 Phase 1 — Local Polling + Persistence (Foundation)

## Goal

Prove you can:

* Call the API
* Transform data
* Store in Postgres

## Tasks

### 1. Create local Python poller

* Use `requests`
* Fetch API data
* Normalize into:

  * name
  * datetime
  * wait_time

### 2. Set up local Postgres

* Use Docker or local install
* Create schema

### 3. Insert data

* Start with single inserts
* Then switch to batch inserts

```python
# pseudo-example
rows = [(name, timestamp, wait)]
cursor.executemany(...)
```

### 4. Add basic querying

Test queries like:

* range queries
* latest value per name

## ✅ Exit Criteria

* You can run a script locally that polls + writes to DB
* You can query results successfully

---

# 🟡 Phase 2 — Structure + Abstraction

## Goal

Separate concerns so your code works in multiple environments

## Tasks

### 1. Define interfaces

```python
class Poller:
    def poll(self) -> list[dict]:
        pass

class Storage:
    def save(self, data: list[dict]):
        pass
```

### 2. Implement concrete classes

* `HttpPoller`
* `PostgresStorage`

### 3. Add config layer

* env variables
* API URL, DB URL

## ✅ Exit Criteria

* Same logic runs locally with clean separation
* Easy to swap implementations later

---

# 🟠 Phase 3 — Containerization

## Goal

Prepare for cloud deployment

## Tasks

### 1. Add Dockerfile

* Python base image
* install dependencies
* run script

### 2. Run locally in Docker

## ✅ Exit Criteria

* Service runs via Docker and still writes to DB

---

# 🔵 Phase 4 — AWS Infrastructure (IaC)

## Goal

Provision cloud resources using Terraform

## Tasks

### 1. Set up Terraform project

Structure:

```
/infra
  main.tf
  variables.tf
  outputs.tf
```

### 2. Create:

* VPC (or use default)
* RDS Postgres instance
* Security groups

### 3. Connect from local machine to RDS

## ✅ Exit Criteria

* Local script writes to AWS-hosted Postgres

---

# 🟣 Phase 5 — Introduce Scheduling + Queue

## Goal

Move from local cron → event-driven architecture

## Tasks

### 1. Create SQS queue

### 2. Create EventBridge rule

* schedule: `rate(5 minutes)`
* sends message to SQS

### 3. Define message schema

Example:

```json
{
  "triggered_at": "timestamp"
}
```

## ✅ Exit Criteria

* Messages appear in SQS on schedule

---

# 🔴 Phase 6 — Lambda Consumer

## Goal

Process queued jobs in AWS

## Tasks

### 1. Create Lambda function (Python)

* triggered by SQS
* calls poller
* writes to Postgres

### 2. Handle batch processing

* iterate over SQS records

### 3. Add retry behavior

* let failures throw exceptions

## Important Considerations

* connection reuse (global DB connection)
* timeout handling

## ✅ Exit Criteria

* End-to-end flow works:
  EventBridge → SQS → Lambda → RDS

---

# 🟤 Phase 7 — Reliability Enhancements

## Goal

Make system production-like

## Tasks

### 1. Add Dead Letter Queue (DLQ)

* attach to SQS

### 2. Add idempotency

* use unique index
* `ON CONFLICT DO NOTHING`

### 3. Add logging

* structured logs in Lambda

## ✅ Exit Criteria

* Failures are retried safely
* Bad messages go to DLQ

---

# ⚫ Phase 8 — Performance + Scaling

## Goal

Handle growing data efficiently

## Tasks

### 1. Add table partitioning

* monthly partitions by `polled_at`

### 2. Benchmark queries

* large time ranges
* multiple names

### 3. Optional: normalize `name` → `location_id`

## ✅ Exit Criteria

* Queries remain fast with large datasets

---

# ⚪ Phase 9 — Advanced AWS Add-ons (Optional)

## Choose based on interest:

### Option A — RDS Proxy

* manage DB connections from Lambda

### Option B — ECS Worker

* add second consumer implementation

### Option C — Observability

* CloudWatch dashboards
* alarms on DLQ depth

### Option D — TimescaleDB

* convert table to hypertable
* compare performance

---

# 🧠 Key Learning Concepts by Phase

| Phase | Concept                         |
| ----- | ------------------------------- |
| 1     | Data modeling, API integration  |
| 2     | Abstraction, clean architecture |
| 3     | Containerization                |
| 4     | Infrastructure as Code          |
| 5     | Event-driven systems            |
| 6     | Serverless compute              |
| 7     | Reliability + fault tolerance   |
| 8     | Scaling + performance           |
| 9     | Advanced AWS patterns           |

---

# 🚀 Suggested Order of Execution

1. Local script (poll + store)
2. Add schema + indexes
3. Abstract poller/storage
4. Dockerize
5. Provision RDS via Terraform
6. Connect local → RDS
7. Add SQS + EventBridge
8. Add Lambda consumer
9. Add DLQ + retries
10. Add partitioning + optimizations

---

# 🧭 Guiding Principle

At every step:

> “Can I run and verify this piece independently?”

Avoid building multiple layers at once — each phase should be:

* testable
* observable
* reversible

---

# ✅ Final Outcome

You’ll end up with:

* a production-style event-driven system
* real experience with AWS primitives
* a scalable time-series data pipeline
* clean, reusable Python architecture

---
