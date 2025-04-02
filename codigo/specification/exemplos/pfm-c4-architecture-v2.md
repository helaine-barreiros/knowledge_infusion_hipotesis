# AI-Enhanced Personal Finance Management (PFM)
> System architecture & documentation  
> Using C4 Model, doc-as-code style, and Spring Boot as core tech stack

---

## 1. System Requirements

### Functional Requirements

| ID       | Requirement                                                                      | Priority   |
|----------|----------------------------------------------------------------------------------|------------|
| FR-01    | Users must be able to connect and synchronize financial accounts from banks.    | Essential  |
| FR-02    | System must categorize and tag transactions using AI.                           | Essential  |
| FR-03    | Users can create, monitor, and get alerts on budgets.                           | Important  |
| FR-04    | AI must offer personalized saving and investment suggestions.                   | Essential  |
| FR-05    | System should provide visual dashboards and reports.                            | Important  |
| FR-06    | System must track recurring payments and detect anomalies.                      | Important  |
| FR-07    | Users can define personal financial goals and track progress.                   | Desirable  |

### Non-Functional Requirements

| ID       | Requirement                                                                      | Priority   |
|----------|----------------------------------------------------------------------------------|------------|
| NFR-01   | Must support high availability and fault tolerance.                             | Essential  |
| NFR-02   | Must comply with financial data protection laws (e.g., LGPD, GDPR).             | Essential  |
| NFR-03   | API response times must be under 300ms on average.                              | Important  |
| NFR-04   | Must support at least 100,000 users concurrently.                               | Important  |
| NFR-05   | Frontend and backend must support internationalization.                         | Desirable  |

---

## 2. Architecturally Significant Requirements (ASRs)

| ID       | Requirement         | Justification as ASR                                                      | Quality Attribute       | Priority   |
|----------|---------------------|---------------------------------------------------------------------------|--------------------------|------------|
| FR-01    | Bank account sync    | Requires secure integrations with external APIs and tokenized OAuth2     | Interoperability, Security | Essential  |
| FR-02    | AI-based categorization | Demands AI/ML integration, modularity, model updates                     | Modifiability, Performance | Essential  |
| FR-04    | Investment suggestions | Personalized insights require model inference with low latency           | Performance, Accuracy    | Essential  |
| NFR-01   | High availability    | Requires architectural decisions: container orchestration, resilience    | Availability, Reliability | Essential  |
| NFR-02   | Data protection      | Impacts DB encryption, audit logs, secure APIs                           | Security, Compliance     | Essential  |
| NFR-03   | Latency requirement  | Influences DB indexing, caching strategy, async communication             | Performance              | Important  |

**Architectural Decisions**:

- Language: Java
- Framework: Spring Boot, Spring Security, Spring Data, Spring Cloud
- Design Pattern: Hexagonal Architecture (Ports & Adapters)
- AI Engine: Python microservice (via REST gRPC or Kafka event bus)
- API Docs: OpenAPI/Swagger
- Deployment: Docker, Kubernetes (K8s)
- Monitoring: Prometheus + Grafana

**Lifecycle Adherence**:

- CI/CD pipelines: GitHub Actions + SonarQube
- Automated tests: JUnit (REST), Postman (API)
- Architecture reviews + Linting (Checkstyle + ArchUnit)

---

## 3. C1 - Context Diagram

```plantuml
@startuml C1_PFM_Context

!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
LAYOUT_TOP_DOWN()

Person(user, "PFM User", "Manages personal finances")
System(pfmSystem, "AI-Powered PFM", "Provides smart financial insights and automation")

System_Ext(bankAPI, "Open Banking APIs", "Used to retrieve financial account data")
System_Ext(aiEngine, "AI Engine (Python)", "Provides ML-based insights and classifications")
System_Ext(notificationService, "Notification Service (Expo Push)", "Delivers alerts and reminders")

Rel(user, pfmSystem, "Uses", "Mobile/Web App")
Rel(pfmSystem, bankAPI, "Fetches account and transaction data via secure API", "OAuth2/REST")
Rel(pfmSystem, aiEngine, "Sends transactions & goals for classification/suggestions", "HTTP/gRPC/Kafka")
Rel(pfmSystem, notificationService, "Sends alerts to", "Push Notification API")

@enduml
```

### Key Entities & Interactions

- **AI Engine**: External microservice that performs transaction classification, budget alerts, and recommendation generation.
- **Notification Service**: External push platform (e.g., Expo, Firebase) for user engagement.
- **Bank APIs**: External REST APIs (PSD2/Open Finance) for syncing bank account data securely.

---

## 4. C2 - Container Diagram

```plantuml
@startuml C2_PFM_Containers

!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
LAYOUT_WITH_LEGEND()

System_Boundary(pfmSystem, "AI-Enhanced PFM") {

  Container(webApp, "Web/Mobile App", "React Native + REST", "UI for managing finances")
  Container(api, "API Gateway", "Spring Boot", "Handles all external requests, routing, auth")
  Container(bff, "Backend For Frontend", "Spring Boot", "Adapts responses for UI needs")
  Container(appService, "Application Services", "Spring Boot", "Orchestrates business logic")
  Container(persistence, "Data Store", "PostgreSQL", "Stores user, transaction, and goal data")
  Container(aiClient, "AI Client Adapter", "Spring Boot", "Calls external AI Engine")
  Container(authService, "Authentication Service", "Keycloak / Spring Security", "Manages users and tokens")

}

Rel(user, webApp, "Uses")
Rel(webApp, api, "Sends requests")
Rel(api, authService, "Delegates token validation")
Rel(api, bff, "Routes user-level requests")
Rel(bff, appService, "Invokes use cases")
Rel(appService, persistence, "Reads/Writes data")
Rel(appService, aiClient, "Delegates to AI engine")
Rel(aiClient, aiEngine, "Fetches insights", "REST/gRPC")
Rel(appService, notificationService, "Sends notifications", "HTTPS")

@enduml
```

---

## 5. C3 - Component Diagram (Spring Boot AppService Layer)

```plantuml
@startuml C3_AppService_Components

!includeurl https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml
LAYOUT_TOP_DOWN()

Container_Boundary(appService, "Application Services") {

  Component(transactionUseCase, "TransactionUseCase", "Handles transaction flows")
  Component(budgetUseCase, "BudgetUseCase", "Handles budget planning, alerts")
  Component(goalUseCase, "GoalTrackingUseCase", "Tracks financial goals")
  Component(portAI, "AIClientPort", "Adapter for AI integration")
  Component(portRepo, "TransactionRepositoryPort", "Persistence port")

}

Rel(bff, transactionUseCase, "Invokes")
Rel(transactionUseCase, portAI, "Sends to AI for tagging")
Rel(transactionUseCase, portRepo, "Stores result")
Rel(goalUseCase, portRepo, "Reads goal progress")
Rel(budgetUseCase, portRepo, "Triggers alerts based on thresholds")
Rel(budgetUseCase, notificationService, "Sends alerts")

@enduml
```

**Layers & Rules**

- **Controller Layer (REST)**: No business logic. Delegates to use cases.
- **Application Layer (UseCases)**: Contains business logic. Interfaces with AI, repos, notifications.
- **Domain Layer**: Entity definitions, rules, aggregates.
- **Infrastructure Layer**: Repositories, external integrations (AI, notification, bank APIs).

**Naming & Conventions**:

- `...UseCase.java` in `app/usecase`
- `...Service.java` only for orchestration
- `...Port.java` for interfaces
- `...Adapter.java` for implementations
- No controller-to-repository access directly
- Spring Boot annotations (`@Service`, `@Component`, `@Repository`, `@RestController`)

**Restrictions**:

- All external calls go through adapters
- Domain is unaware of infrastructure
- Repositories must implement only ports

---

