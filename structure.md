```mermaid
graph TD
    subgraph "Content Generation"
        A[Content Generator] --> B[Content Expander]
        B --> C[Content Reviewer]
    end

    subgraph "Version Management"
        D[Version Selector] --> E[Version Comparator]
        E --> F[Version Ranker]
    end

    subgraph "Content Enhancement"
        G[Revision Agent] --> H[Citation Editor]
        H --> I[Content Publisher]
    end

    B --> D
    F --> G
    I --> J[Final Output]