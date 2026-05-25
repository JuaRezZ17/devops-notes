# Fundamentals of CI/CD

## Objective
Understanding the modern software development lifecycle. It’s not just about automating commands, but about creating a chain of trust where faulty code is blocked before it reaches production.

### Continuous Integration (CI)
This is the practice whereby developers frequently commit their code to a centralised repository (such as the Git ‘main’ branch). The main aim of CI is to identify and fix bugs as early as possible. Every time someone uploads code (makes a push or opens a Pull Request), an automated server kicks in and performs two key checks:
- **Automated Testing:** Ensures that the new code does not break existing functionality.
    - **Unit Testing:** Validates small, isolated parts of the code.

    - **Integration Testing:** Verifies that different modules of the system work well when connected.

- **Static Code Analysis:** It is like an advanced spellchecker and grammar checker for code. It reviews the source code without actually executing it.
    - **Linting:** Checks that the code follows the team’s style guidelines. It makes the code readable and consistent.

    - **SonarQube (or similar tools):** Looks for deeper-seated issues. Detects code smells (code that works but is poorly structured and will be difficult to maintain), potential bugs and security vulnerabilities.

If all the tests and analyses pass, we know that the code is functional, secure and clean.

### Continuous Delivery (CD) vs Continuous Deployment (CD)
Once the code has passed the CI phase, it needs to be packaged and deployed to the real world. This is where the ‘D’ in CD takes two different paths depending on company policies:
- **Continuous delivery:** The entire process of creating the artifact is automated. The software is packaged, tested in environments identical to production (such as Staging) and ready to go live. The problem is that the move to the actual Production environment requires human intervention. A manager, QA team or the client must press a button, sign off on approval or decide on a release date. This is mainly used by companies with strict compliance controls such as banks, healthcare, mobile apps or traditional businesses.

- **Continuous Deployment:** This is the highest level of automation. If the code passes absolutely all automated tests (CI) and the artifact is generated correctly, it goes directly to production without any human intervention. To do this without causing a disaster, the company needs to have a flawless suite of automated tests and advanced monitoring systems. If something fails in production, the system must detect it and automatically revert to the previous version or roll back. It is mainly used by tech start-ups and modern SaaS companies.

### Usa Mermaid.js en tu archivo Markdown de apuntes para diseñar el diagrama de flujo de un pipeline ideal.
### Dibuja las fases: Checkout -> Linting -> Unit Tests -> Build Docker -> Security Scan (Trivy) -> Push to Registry -> Deploy to Staging.
```mermaid
flowchart LR
    A[Checkout] --> B[Linting]
    B --> C[Unit Tests]
    C --> D[Build Docker]
    D --> E[Security Scan: Trivy]
    E --> F[Push to Registry]
    F --> G[Deploy to Staging]
    
    %% Styling for better visualization
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px