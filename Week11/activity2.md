# Feasibility Study

## Project

**Peer-to-Peer Bicycle Rental Platform**

## Purpose

This study evaluates whether the proposed bicycle rental platform is practical to develop, deploy, operate, and demonstrate for MSE800 Assessment 2.

The analysis follows the feasibility categories described by GeeksforGeeks: technical, operational, economic, legal, schedule, cultural and political, market, and resource feasibility.

Reference:

- [Types of Feasibility Study in Software Project Development](https://www.geeksforgeeks.org/software-engineering/types-of-feasibility-study-in-software-project-development/)

## Executive Summary

The project is feasible for the assessment scope.

The current implementation already demonstrates the principal technical and operational requirements:

- a React web application;
- a Django REST API;
- PostgreSQL persistence;
- role-based renter, lender, and staff workflows;
- map and nearby bicycle search;
- booking, deposit, handover, return, claim, dispute, and rating flows;
- Amazon S3 media storage;
- Mailgun email delivery;
- Docker-based AWS EC2 deployment;
- Caddy-managed HTTPS;
- automated backend and frontend CI.

The main residual risks are operational rather than architectural. These include database backup automation, external service limits, production monitoring, and keeping the Postman collection aligned with the latest dispute workflow.

| Feasibility area | Assessment | Summary |
| --- | --- | --- |
| Technical | Feasible | The required stack is implemented and deployable |
| Operational | Feasible with controls | Workflows are usable, but backups and monitoring require continued attention |
| Economic | Feasible for assessment | Open-source software and small-scale cloud resources keep costs limited |
| Legal | Feasible with compliance actions | Privacy, uploaded content, evidence access, and software licensing must be managed |
| Schedule | Feasible | Core work is organized across three sprints and largely complete |
| Cultural and organizational | Feasible | Role-based workflows support collaboration between renters, lenders, and staff |
| Market | Feasible as an MVP | The platform addresses local, affordable, lower-carbon transport needs |
| Resource | Feasible | The current team, repository, cloud services, and automation are sufficient |

## 1. Technical Feasibility

### Objective

Determine whether the team has the technology, infrastructure, and technical capability required to build and maintain the platform.

### Current Technical Evidence

| Requirement | Current implementation |
| --- | --- |
| Web interface | React 18 and Vite |
| Backend services | Django 4.2 and Django REST Framework |
| Authentication | Simple JWT access and refresh tokens |
| Relational data | PostgreSQL 16 |
| Mapping | Leaflet, OpenStreetMap tiles, geocoding and reverse geocoding services |
| Media | Amazon S3 through `django-storages` |
| Email | Mailgun SMTP |
| Deployment | Docker Compose on AWS EC2 |
| HTTPS | Caddy automatic certificate management |
| CI/CD | GitHub Actions for backend, frontend, and deployment |
| Automated validation | 69 Django workflow tests and frontend production build checks |

### Architecture Suitability

The application is separated into:

- frontend;
- backend;
- PostgreSQL database;
- reverse proxy;
- external media storage;
- external email delivery.

This separation makes the application maintainable and allows future migration from Docker Compose to Kubernetes without redesigning the complete system.

### Technical Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| EC2 instance failure | Application and local database become unavailable | Automated database dumps, off-instance backups, documented restore process |
| Map or geocoding provider limits | Address search may slow down or fail | User-friendly error handling, fallback Auckland location, provider abstraction |
| S3 permission errors | Image upload or display fails | Least-privilege bucket policy, deployment secrets, upload logging |
| Email provider failure | Users miss workflow emails | In-app notifications remain authoritative; email is supplementary |
| Self-hosted runner targets wrong server | Deployment updates the wrong environment | Use a dedicated EC2 runner and fixed Compose project name |
| Password changes on an existing PostgreSQL volume | Backend authentication fails | Deployment synchronizes the PostgreSQL role password before migrations |

### Conclusion

**Technically feasible.** The necessary technologies are available, compatible, and already integrated. Remaining risks can be addressed through operational controls rather than major redesign.

## 2. Operational Feasibility

### Objective

Determine whether the platform supports the intended user workflows and can be operated after deployment.

### Supported Operations

#### Renter

- register and select a renter role;
- search approved bicycles;
- use address or current-location nearby search;
- review bicycle, lender rating, price, and deposit details;
- request a booking;
- negotiate handover location;
- confirm deposit, handover, and return;
- accept or dispute a lender compensation request;
- rate the lender.

#### Lender

- register and select a lender role;
- create and manage listings;
- upload photos and ownership evidence;
- respond to booking requests;
- negotiate handover location;
- confirm handover and return;
- submit a damage claim and requested compensation;
- rate the renter.

#### Administrator

- approve or reject listings;
- take down or restore listings;
- ban or unban users;
- review escalated disputes;
- release deposits or approve deductions.

### Operational Strengths

- Role-specific navigation reduces irrelevant actions.
- Status-based booking controls guide users through the workflow.
- Notifications provide updates within the application.
- Email provides supplementary updates for selected workflow events.
- Caddy and Docker restart policies support repeatable operation.
- Health endpoints allow deployment verification.

### Operational Gaps

- Database backup is documented but not yet scheduled automatically.
- Production monitoring currently focuses on deployment health rather than long-term metrics.
- The Postman damage section still represents an earlier workflow.
- The Expo mobile client is a prototype and does not yet implement the complete web workflow.

### Conclusion

**Operationally feasible with controls.** The main workflows are implemented. Backup automation, monitoring, and operational test maintenance remain necessary production-hardening tasks.

## 3. Economic Feasibility

### Objective

Compare expected project costs with the benefits delivered by the assessment prototype.

### Cost Areas

| Area | Cost approach |
| --- | --- |
| Development tools | Git, GitHub, Python, Node.js, Docker, Django, React, PostgreSQL, Leaflet, and Caddy are open source |
| Compute | One small AWS EC2 instance hosts the application and database |
| Database | PostgreSQL runs in Docker on the existing EC2 instance |
| Media | Amazon S3 charges depend on stored data, requests, and transfer |
| Email | Mailgun usage depends on the selected plan and message volume |
| Domain | Existing `isbike.studio` registration |
| CI | GitHub-hosted CI plus an EC2 self-hosted deployment runner |
| Maps | OpenStreetMap-based rendering and external geocoding, subject to provider usage policies |

### Benefits

- Demonstrates a complete software engineering lifecycle.
- Reuses bicycles that would otherwise remain idle.
- Provides lower-cost local transport.
- Supports lower-carbon travel for campus and city journeys.
- Produces reusable deployment, CI/CD, API, and database operations experience.
- Avoids a large initial infrastructure investment.

### Cost-Control Measures

- Use one EC2 instance during the assessment.
- Use Docker named volumes instead of a separate managed database.
- Store uploaded files in S3 rather than on the application container.
- Scale external services only when usage justifies it.
- Keep PostgreSQL inaccessible from the public internet.

### Conclusion

**Economically feasible for the assessment and MVP scale.** The solution primarily uses open-source software and existing low-scale cloud resources. A larger production launch would require a formal cost model for managed database, monitoring, backups, support, and increased traffic.

## 4. Legal Feasibility

### Objective

Determine whether the project can operate without conflicting with privacy, intellectual property, licensing, or platform responsibilities.

### Relevant Areas

| Area | Project consideration |
| --- | --- |
| Personal information | User email, phone number, address, role, ratings, and booking history are stored |
| Location data | Addresses and coordinates are used for search and listing display |
| Uploaded content | Bicycle photos, ownership evidence, and dispute evidence may contain personal or copyrighted material |
| Access control | Ownership and dispute evidence must only be available to authorized parties |
| Account moderation | Staff can ban users and remove listings |
| Third-party services | AWS, Mailgun, OpenStreetMap-related services, GitHub, and domain providers have their own terms |
| Software licences | Open-source dependency licences and attribution obligations must be retained |

### Required Controls

- Publish a privacy notice before real public use.
- Collect only information necessary for the rental workflow.
- Restrict private evidence to owners and authorized staff.
- Define retention and deletion rules for profiles, evidence, bookings, and logs.
- Provide OpenStreetMap attribution in the map interface.
- Prevent secrets and credentials from being committed to Git.
- Define acceptable-use, listing-content, damage, refund, and dispute policies.
- Treat the current payment and deposit functionality as a simulation until a compliant payment provider is integrated.

### Conclusion

**Legally feasible for an educational prototype, subject to compliance work before real commercial operation.** The code contains access controls, but policies, consent wording, retention rules, and formal legal review are outside the current assessment implementation.

## 5. Schedule Feasibility

### Objective

Determine whether the project scope can be delivered within the assessment schedule.

### Three-Sprint Delivery

| Sprint | Scope | Current result |
| --- | --- | --- |
| Sprint 1 | Architecture, Docker, authentication, roles, profiles, CI | Complete |
| Sprint 2 | Listings, media, moderation, search, nearby map | Complete |
| Sprint 3 | Booking lifecycle, deposit, handover, return, claims, ratings, notifications, AWS deployment, documentation | Core scope complete; operational polish remains |

### Schedule Controls

- Work is divided by business capability rather than by isolated technical layer.
- Backend and frontend CI catch integration problems before deployment.
- Docker reduces environment setup differences.
- Requirements traceability identifies incomplete or partial items.
- The public deployment provides an objective assessment milestone.

### Schedule Risks

- Late workflow changes may require backend, frontend, tests, and documentation changes together.
- External service configuration can delay deployment independently of code readiness.
- Infrastructure migration from VPS to AWS introduced runner, DNS, certificate, and database migration work.

### Conclusion

**Schedule feasible.** The system has reached a demonstrable state within three sprints. Remaining work is mainly refinement, operational automation, and documentation maintenance.

## 6. Cultural and Organizational Feasibility

### Objective

Evaluate whether the platform fits the expected behaviour of users and the team's development process.

### User Acceptance Considerations

- Renters need transparent pricing, deposits, bicycle condition, location, and lender reputation.
- Lenders need listing control, renter reputation, evidence handling, and compensation options.
- Administrators need clear moderation and dispute tools.
- Both parties need an understandable workflow and equal confirmation opportunities.

### Team and Process Considerations

- The monorepo allows backend, frontend, deployment, and documentation to evolve together.
- Pull requests and GitHub Actions support team review.
- Three sprint groups provide a shared delivery structure.
- Requirements traceability connects classroom requirements to implementation.

### Potential Resistance

- Users may not trust peer-to-peer rentals without ratings and moderation.
- Deposits and damage claims may be perceived as unfair without clear evidence and decisions.
- Users may reject complex booking states if the UI does not explain the next action.

### Mitigation

- Display ratings and completed rental counts.
- Require evidence for damage claims.
- Allow renters to accept or escalate compensation requests.
- Restrict final staff intervention to escalated cases.
- Keep role-specific dashboards and navigation.

### Conclusion

**Culturally and organizationally feasible.** Trust features and role-specific workflows align with peer-to-peer marketplace expectations, although real-world adoption would require clear policies and user education.

## 7. Market Feasibility

### Objective

Evaluate whether the platform addresses a meaningful user need and has a plausible target audience.

### Target Users

- students requiring short local journeys;
- campus staff and nearby residents;
- bicycle owners with underused bicycles;
- renters seeking lower-cost alternatives to purchasing a bicycle;
- users interested in lower-carbon transport.

### Value Proposition

- nearby pickup;
- lower daily cost than ownership for occasional users;
- additional income or cost recovery for bicycle owners;
- map-based availability;
- trust through approval, ratings, evidence, and moderation;
- lower-carbon travel compared with many motorized trips.

### Alternatives and Competition

Potential alternatives include:

- public bicycle-share services;
- commercial bicycle rental shops;
- second-hand bicycle purchase;
- public transport;
- walking, ride sharing, and private vehicles;
- general peer-to-peer marketplace listings.

The project differentiates itself through individual bicycle ownership, local handover negotiation, peer ratings, and an end-to-end rental workflow.

### Market Risks

- Insufficient bicycle supply in a local area.
- Users may prefer instant station-based rental.
- Trust and damage concerns may reduce participation.
- Insurance and payment limitations restrict commercial readiness.

### Conclusion

**Market feasible as an MVP and assessment prototype.** The concept addresses a recognizable transport and asset-sharing need. Commercial feasibility would require user research, insurance analysis, payment integration, pricing validation, and competitor analysis.

## 8. Resource Feasibility

### Objective

Determine whether the required people, infrastructure, software, and services are available.

### Available Resources

| Resource | Availability |
| --- | --- |
| Source control | GitHub repository and pull-request workflow |
| Compute | AWS EC2 |
| Database | PostgreSQL 16 Docker service with persistent volume |
| Object storage | Amazon S3 |
| Email | Mailgun SMTP |
| Domain and TLS | `isbike.studio` and Caddy automatic HTTPS |
| Development environment | Docker Compose, Python, Node.js |
| Testing | Django test suite, frontend build check, Postman assets |
| Skills | Full-stack development, database migration, Docker, CI/CD, and cloud deployment demonstrated in the repository |

### Resource Constraints

- One EC2 instance creates a single point of failure.
- The database and application currently share the same instance.
- The team must maintain cloud credentials and deployment secrets.
- Time for extensive mobile development, payment integration, insurance, and production analytics is limited.

### Conclusion

**Resource feasible for the defined scope.** Current resources are sufficient for development, assessment demonstration, and low-volume operation. Higher availability and commercial use would require additional infrastructure and specialist support.

## Overall Decision

### Recommendation

**Proceed with the project and complete the remaining operational hardening tasks.**

The platform is technically implemented, economically reasonable at assessment scale, operationally demonstrable, and deliverable within the three-sprint plan.

### Priority Follow-Up Actions

1. Automate PostgreSQL backups and test restoration.
2. Add production monitoring and alerting.
3. Update the Postman damage/dispute workflow.
4. Add privacy, retention, acceptable-use, and dispute policy documents.
5. Expand frontend automated testing.
6. Evaluate managed PostgreSQL or a multi-instance architecture if availability requirements increase.
7. Treat payment, deposit, and compensation as simulated until a compliant payment provider is integrated.
