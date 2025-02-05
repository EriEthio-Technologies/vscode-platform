# Coding Guidelines

Always follow coding best practices and the following rules.

Comprehensive Rules for High-Quality, Efficient, and Scalable Development
Ensuring UI Consistency with DaisyUI & shadcn/ui
Rule: To maintain a modern and consistent design across the application, all UI components should be implemented using DaisyUI (with a choice of dark, synthwave, or sunset themes) and shadcn/ui.
How:
Apply DaisyUI themes globally: This will ensure that the chosen theme (dark, synthwave, or sunset) is applied consistently across all components, providing a unified visual experience.
Utilize pre-built shadcn/ui components: shadcn/ui provides a range of pre-designed components that align with modern design principles. By using these components wherever possible, you can save development time and ensure that your UI elements adhere to established design standards.
Minimize custom styling: Custom styling should only be used when absolutely necessary to achieve specific design requirements that cannot be met by DaisyUI or shadcn/ui components. Excessive custom styling can lead to inconsistencies and increase maintenance efforts.
Justification:
Accelerated development: Using pre-built components and established design patterns can significantly speed up development time, allowing you to focus on core functionality.
Visual consistency: By adhering to a consistent design system, you can create a cohesive and professional-looking user interface that is easy to navigate and understand.
Reduced maintenance: A standardized UI design with minimal custom styling is easier to maintain and update, as changes can be applied globally and consistently.
Improved collaboration: A clear set of UI guidelines and a shared library of components can improve collaboration among developers, designers, and other stakeholders.
Additional Considerations:
Component library: Consider creating a component library that encapsulates commonly used UI elements based on DaisyUI and shadcn/ui. This can further streamline development and ensure consistency across different parts of the application.
Accessibility: Ensure that the chosen DaisyUI theme and shadcn/ui components meet accessibility standards, making the application usable by people with disabilities.
Testing: Thoroughly test the UI with different DaisyUI themes and shadcn/ui components to ensure that they work correctly and display as expected in various browsers and devices.
Documentation: Document the UI guidelines, including the use of DaisyUI themes, shadcn/ui components, and any custom styling rules. This will help maintain consistency and onboard new team members.

Modular & Reusable UI Components
Rule: To ensure a clean and maintainable codebase, UI elements should be designed to be modular, reusable, and well-structured. This approach not only streamlines development but also enhances the overall user experience.
How:
Break UI into Atomic Components: By decomposing the user interface into smaller, self-contained components, each responsible for a single functionality, you create building blocks that can be easily reused and rearranged.
Avoid Monolithic Files: Large, monolithic files can quickly become unwieldy and difficult to manage. Instead, opt for creating separate files for each reusable component. This promotes code organization and clarity.
Clear and Self-Explanatory Names: Using descriptive names for components makes the codebase more readable and understandable, reducing the cognitive load for developers who are working with the code.
Justification:
Improved Code Maintainability: Modular code is inherently easier to maintain. Changes and updates can be made to specific components without affecting the entire codebase.
Simplified Debugging: Isolating issues becomes less cumbersome when dealing with modular components. The source of a bug can be quickly traced to the relevant component.
Enhanced UI Consistency: Reusable components ensure a consistent look and feel across the application, leading to a more polished and professional user experience.
Accelerated Development: Having a library of reusable UI components speeds up development time, as developers can leverage existing components instead of building everything from scratch.
Facilitates Collaboration: Modular code promotes collaboration among developers, as different team members can work on separate components simultaneously.
By adhering to the principle of modular and reusable UI components, developers can create robust, scalable, and user-friendly applications that are both efficient to develop and easy to maintain.

Component Documentation
Rule: Each UI component must include clear, structured documentation.
How:
Add JSDoc-style comments describing:
Component purpose
Props and state dependencies
Usage instructions
Include examples of expected inputs and outputs.
Document any side effects or potential performance implications.
Keep the documentation up-to-date as the component evolves.
Justification: Prevents confusion, aids in debugging, and streamlines onboarding. Clear documentation also makes it easier to reuse components and understand their behavior.4. Maintain Existing Functionality While Debugging
Rule: Debugging or refactoring should not break existing features.
How:
Implement automated unit and integration tests.
Use feature flags to separate testing environments.
Write clear and concise commit messages.
Use a version control system and track changes.
Communicate with other team members about potential impacts.
Justification: Prevents unexpected issues in production and ensures a smooth user experience.5. Ensure Vercel & GCP Deployment Compatibility
Rule: All code must be optimized for Vercel and GCP deployments.
How:
Test all endpoints locally (localhost:3000) before deployment.
Ensure environment variables are correctly configured for cloud deployment.
Follow Vercel and GCP best practices for deployment.
Use deployment scripts or automation tools.
Monitor deployments and logs for errors.
Justification: Prevents deployment failures and ensures smooth cloud execution.6. Containerization & Orchestration Readiness
Rule: Where necessary, implement Docker & Kubernetes for consistency across environments.
How:
Use Dockerfiles for microservices and APIs.
Utilize Kubernetes/Cloud Run for large-scale applications.
Write clear and concise Dockerfiles.
Use a container registry to store and manage images.
Monitor container health and logs.
Justification: Ensures scalability and deployment flexibility. Containerization also makes it easier to move applications between environments and manage dependencies.7. Optimize API Endpoints for Speed & Scalability
Rule: All API endpoints should be highly efficient and scalable.
How:
Use pagination, indexing, and caching.
Optimize database queries to reduce response times.
Implement rate limiting to prevent abuse.
Profile API performance and identify bottlenecks.
Use a load balancer to distribute traffic.
Scale horizontally by adding more servers.
Justification: Reduces server load and improves performance, resulting in a better user experience.8. Handle Data Asynchronously

Rule: Use asynchronous operations to optimize responsiveness.

How:
Use Promises and async/await for API calls.
Implement WebSockets where real-time updates are needed.
Use a message queue for background tasks.
Avoid blocking the main thread.
Justification: Improves performance and prevents UI freezing, especially for long-running tasks.9. API Response Documentation

Rule: Clearly document API request and response formats.

How:
Include Swagger/OpenAPI specs if necessary.
Provide examples of expected inputs and outputs.
Document status codes and error messages.
Keep the documentation up-to-date as the API evolves.
Make the documentation easily accessible to developers.
Justification: Eases integration and debugging for developers who are using the API.10. Use Supabase with Server-Side Rendering (SSR)

Rule: Database interactions should be secure, efficient, and SSR-optimized.

How:
Fetch data server-side where possible.
Use role-based access control (RBAC).
Optimize database queries for SSR.
Cache data where appropriate.
Consider using a CDN for static assets.
Justification: Enhances security and performance, especially for initial page loads.11. Comprehensive Error Handling & Logging

Rule: Implement structured error handling across all components.

How:
Use try/catch blocks for all async operations.
Log errors with detailed stack traces in a centralized system (e.g., LogRocket, Datadog).
Handle errors gracefully and provide informative feedback to the user.
Monitor error logs and address issues promptly.
Justification: Speeds up debugging and improves system reliability.12. Persistent Project Indexing

Rule: Maintain an up-to-date index of all project components.

How:
Use automated indexing tools to track dependencies.
Document dependencies and relationships between components.
Keep the index up-to-date as the project evolves.
Justification: Prevents outdated dependencies from causing issues and makes it easier to understand the project structure.13. Scalable Caching Strategies

Rule: Implement Redis or in-memory caching to optimize performance.

How:
Identify high-traffic API calls for caching.
Implement cache expiration policies to maintain data accuracy.
Choose an appropriate caching strategy for your application.
Monitor cache hit rates and adjust as needed.
Justification: Reduces database load and improves response times.14. Context-Aware Debugging

Rule: Debugging should consider dependencies to avoid new issues.

How:
Perform impact analysis before changes.
Understand the relationships between components.
Test changes thoroughly in isolation and in context.
Justification: Prevents circular debugging loops and minimizes unintended consequences.15. Continuous Integration & Deployment (CI/CD)

Rule: Automate testing, building, and deployment pipelines.

How:
Use GitHub Actions, Jenkins, or GitLab CI.
Run automated tests before merging.
Deploy to staging environments first.
Monitor deployments and roll back if necessary.
Justification: Ensures stable and error-free deployments.16. Effective Version Control & Branch Management

Rule: Follow structured version control practices.

How:
Use GitFlow or a similar branching strategy.
Enforce code reviews before merging.
Write clear and concise commit messages.
Tag releases and keep a changelog.
Justification: Maintains traceability and reduces integration issues.17. Real-Time Monitoring & Observability

Rule: Implement system-wide monitoring tools.

How:
Use Prometheus, Grafana, or Datadog.
Set up error tracking dashboards.
Monitor key metrics and logs.
Alert on critical issues.
Justification: Prevents downtime and allows quick response to issues.18. User-Centric Design & Accessibility

Rule: Follow Web Content Accessibility Guidelines (WCAG).

How:
Use semantic HTML and accessible UI components.
Conduct accessibility testing (e.g., Axe DevTools).
Consider users with disabilities and different needs.
Justification: Improves usability for all users.19. Data Encryption & Security Best Practices

Rule: Protect user data with encryption and best security practices.

How:
Encrypt sensitive data at rest and in transit.
Implement role-based access control (RBAC).
Follow industry-standard security practices.
Conduct regular security audits.
Justification: Prevents data breaches and enhances security compliance.


or each item, feature, or component you start working on, you should: make sure that it is well-documented, that it is tested, and that it is integrated with the rest of the system. Also, each item, task, feature, or component you start working on, yous should complete it 100% before moving on to the next item where possible and it is done within a way that it is easy to understand and easy to maintain.

As a cash poor startup, our first option is to use a free tier of a cloud provider.
as a cash poor startup, it is preferable for us to find free or low-cost solutions for our needs.

We are currently using GCP or Vercel for deployment


# Some additional rules

- make sure to add comments and descriptions throughout the code files
-makes sure you follow the rules, and ask questions if you need to
- Whenever you are done with each request and ask me "would you like me to: ..." and give a list of items, I would like you to include benefits of each suggestion, whether we havepreviously implemented related items, and the specific item, feature, component it will affect


- I do not accept anything mediocre and I expect you to always develop/implement each of the items, features, components, etc to be built to be advanced, robust, fully integrated with each other.
- give me a confirmation of completion to 100% for each item, feature, component etc you work on
- generate concise summary of completed tasks each time you complete them
