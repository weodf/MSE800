# Jira Sprint Plan

## Project Information

**Project Title:**
Peer-to-Peer Bicycle Rental Platform

**Group Name:**
Group-D

**Team Members:**

* Dongfang Wang
* Xiaoning Li

---

## 1. Introduction

This document presents the Jira sprint plan for the Peer-to-Peer Bicycle Rental Platform. The purpose of this plan is to organise the project into manageable development stages and ensure that each team member has clear responsibilities throughout the project.

As a two-person team, we will use Jira to manage our backlog, sprint tasks, user stories, technical work, testing activities, and final documentation. The project will be completed over three one-week sprints. Each sprint has a specific goal and a set of deliverables that support the development of the final MVP.

The plan is designed to help us track progress clearly, reduce confusion during development, and make sure that the most important features are completed first.

---

## 2. Project Management Method

We will manage this project using a Scrum-style sprint workflow in Jira. Although the team is small, using sprints will help us divide the work into smaller and more achievable sections.

The development period will be divided into three sprints:

| Sprint   | Main Focus                                                                             |
| -------- | -------------------------------------------------------------------------------------- |
| Sprint 1 | Project setup, authentication, and user profile                                        |
| Sprint 2 | Bike listing, file upload, search, and listing approval                                |
| Sprint 3 | Booking workflow, deposit logic, damage report, testing, deployment, and documentation |

Each sprint will include planning, development, testing, and review. Both team members will be involved in checking progress and resolving issues.

---

## 3. Jira Issue Types

The Jira board will use different issue types to separate large features from smaller tasks.

| Issue Type | Description                                                |
| ---------- | ---------------------------------------------------------- |
| Epic       | A large project area or major feature group                |
| Story      | A user-focused feature written from the user's perspective |
| Task       | Technical work, setup work, testing, or documentation      |
| Sub-task   | A smaller work item under a story or task                  |
| Bug        | A defect or issue found during development or testing      |

This structure will make the Jira board easier to manage and allow us to track both business features and technical work.

---

## 4. Project Epics

The project will be divided into the following main epics.

| Epic ID | Epic Name                             | Description                                                                           |
| ------- | ------------------------------------- | ------------------------------------------------------------------------------------- |
| EPIC-1  | Project Setup and Environment         | GitHub repository, Docker, backend, frontend, database, and environment configuration |
| EPIC-2  | Authentication and User Profile       | User registration, login, JWT authentication, profile management, and role selection  |
| EPIC-3  | Bike Listing Management               | Bike listing creation, update, deletion, image upload, and ownership evidence upload  |
| EPIC-4  | Search and Listing Approval           | Bike search, filtering, and admin approval or rejection                               |
| EPIC-5  | Booking and Rental Workflow           | Booking request, lender response, handover, return, and rental status tracking        |
| EPIC-6  | Deposit and Damage Report             | Simulated deposit calculation, deposit confirmation, and damage report submission     |
| EPIC-7  | Admin Review and Dashboard            | Admin dispute review, deposit decision, and dashboard pages                           |
| EPIC-8  | Testing, Deployment and Documentation | Testing, CI/CD, deployment preparation, README, final report, and demo materials      |

---

## 5. Jira Workflow

The Jira board will follow a simple workflow suitable for a two-person academic project.

| Status      | Meaning                                                   |
| ----------- | --------------------------------------------------------- |
| To Do       | The issue has been planned but has not started            |
| In Progress | The issue is currently being developed                    |
| Code Review | The issue is ready to be checked by the other team member |
| Testing     | The issue is being tested manually or automatically       |
| Done        | The issue has been completed and accepted                 |

This workflow allows both team members to understand the current progress of each feature and identify blocked or unfinished work quickly.

---

## 6. Sprint Overview

The project will be completed in three one-week sprints.

| Sprint   | Duration | Sprint Goal                                                                            | Estimated Issue Count |
| -------- | -------- | -------------------------------------------------------------------------------------- | --------------------- |
| Sprint 1 | Week 1   | Build the project foundation and authentication flow                                   | 8–10 issues           |
| Sprint 2 | Week 2   | Complete listing, upload, search, and approval features                                | 10–12 issues          |
| Sprint 3 | Week 3   | Complete booking, deposit, damage review, testing, deployment, and final documentation | 16–20 issues          |

The complete Jira project is expected to contain around **35 to 42 issues**.

---

## 7. Sprint 1: Project Setup and Authentication

### Sprint Goal

The goal of Sprint 1 is to create the full-stack project foundation and complete the basic account system.

By the end of this sprint, the application should run locally, and users should be able to register, log in, and choose their role as renter, lender, or both.

### Sprint 1 Issues

| Issue Type | Summary                                                        | Epic                                  | Assignee | Priority | Story Points |
| ---------- | -------------------------------------------------------------- | ------------------------------------- | -------- | -------- | ------------ |
| Task       | Create GitHub repository and define branch workflow            | Project Setup and Environment         | Shared   | High     | 2            |
| Task       | Configure Docker Compose for backend, frontend, and PostgreSQL | Project Setup and Environment         | Member 1 | High     | 3            |
| Task       | Create Django REST Framework backend project                   | Project Setup and Environment         | Member 1 | High     | 3            |
| Task       | Create React Vite frontend project                             | Project Setup and Environment         | Member 2 | High     | 2            |
| Task       | Configure backend and database environment variables           | Project Setup and Environment         | Member 1 | Medium   | 2            |
| Story      | As a user, I want to register an account                       | Authentication and User Profile       | Member 1 | High     | 3            |
| Story      | As a user, I want to log in using JWT authentication           | Authentication and User Profile       | Member 1 | High     | 5            |
| Story      | As a user, I want to choose my role as renter, lender, or both | Authentication and User Profile       | Member 2 | High     | 3            |
| Task       | Build the basic React layout and navigation                    | Project Setup and Environment         | Member 2 | Medium   | 3            |
| Task       | Write initial API endpoint notes                               | Testing, Deployment and Documentation | Shared   | Medium   | 2            |

### Sprint 1 Deliverables

By the end of Sprint 1, we expect to complete:

* GitHub repository setup
* Branch workflow setup
* Docker Compose configuration
* Django backend project setup
* React frontend project setup
* PostgreSQL connection
* User registration
* JWT-based login
* User role selection
* Basic frontend navigation
* Initial API documentation notes

---

## 8. Sprint 2: Bike Listing, Upload, Search, and Approval

### Sprint Goal

The goal of Sprint 2 is to build the main bike listing features. Lenders should be able to create bike listings and upload supporting files, while renters should be able to search for approved bikes.

Admins should also be able to review new listings and approve or reject them.

### Sprint 2 Issues

| Issue Type | Summary                                                                  | Epic                                  | Assignee | Priority | Story Points |
| ---------- | ------------------------------------------------------------------------ | ------------------------------------- | -------- | -------- | ------------ |
| Task       | Create Bike, BikeImage, and OwnershipEvidence models                     | Bike Listing Management               | Member 1 | High     | 5            |
| Story      | As a lender, I want to create a bike listing                             | Bike Listing Management               | Member 1 | High     | 5            |
| Story      | As a lender, I want to upload bike photos                                | Bike Listing Management               | Member 1 | High     | 5            |
| Story      | As a lender, I want to upload ownership evidence                         | Bike Listing Management               | Member 1 | High     | 5            |
| Story      | As a lender, I want to edit and delete my own listings                   | Bike Listing Management               | Member 1 | High     | 5            |
| Task       | Add listing approval status: pending, approved, rejected                 | Search and Listing Approval           | Member 2 | High     | 3            |
| Story      | As an admin, I want to approve or reject bike listings                   | Search and Listing Approval           | Member 2 | High     | 5            |
| Story      | As a renter, I want to search approved bikes                             | Search and Listing Approval           | Member 2 | High     | 5            |
| Task       | Add filters for location, type, size, price, condition, and availability | Search and Listing Approval           | Member 2 | High     | 5            |
| Task       | Build bike detail page                                                   | Bike Listing Management               | Member 2 | Medium   | 3            |
| Task       | Add backend tests for listing permissions and approval                   | Testing, Deployment and Documentation | Shared   | Medium   | 3            |
| Task       | Integrate frontend listing pages with backend APIs                       | Bike Listing Management               | Shared   | High     | 5            |

### Sprint 2 Deliverables

By the end of Sprint 2, we expect to complete:

* Bike listing data models
* Lender bike listing creation
* Bike photo upload
* Ownership evidence upload
* Listing edit and delete permissions
* Listing approval status
* Admin listing approval and rejection
* Renter search for approved bikes
* Search filters
* Bike detail page
* Backend tests for listing permission and approval
* Frontend and backend integration for listing features

---

## 9. Sprint 3: Booking, Deposit, Damage Review, Testing, and Deployment

### Sprint Goal

The goal of Sprint 3 is to complete the main rental workflow and prepare the project for final delivery.

By the end of this sprint, renters should be able to request bookings, lenders should be able to approve or reject requests, and the system should support simulated deposit calculation, handover confirmation, return confirmation, damage reporting, admin review, testing, and deployment preparation.

### Sprint 3 Issues

| Issue Type | Summary                                                                               | Epic                                  | Assignee | Priority | Story Points |
| ---------- | ------------------------------------------------------------------------------------- | ------------------------------------- | -------- | -------- | ------------ |
| Task       | Design Booking model and status transition rules                                      | Booking and Rental Workflow           | Member 2 | High     | 5            |
| Story      | As a renter, I want to create a booking request                                       | Booking and Rental Workflow           | Member 2 | High     | 5            |
| Story      | As a lender, I want to approve or reject booking requests                             | Booking and Rental Workflow           | Member 2 | High     | 5            |
| Task       | Implement booking status transitions                                                  | Booking and Rental Workflow           | Member 2 | High     | 8            |
| Task       | Implement simulated deposit calculation                                               | Deposit and Damage Report             | Member 2 | High     | 3            |
| Story      | As a renter, I want to confirm simulated deposit payment                              | Deposit and Damage Report             | Member 2 | High     | 3            |
| Story      | As a renter and lender, I want to confirm handover                                    | Booking and Rental Workflow           | Member 2 | High     | 5            |
| Story      | As a renter and lender, I want to confirm return                                      | Booking and Rental Workflow           | Member 2 | High     | 5            |
| Story      | As a user, I want to view rental status tracking                                      | Booking and Rental Workflow           | Member 1 | Medium   | 5            |
| Task       | Build renter booking management page                                                  | Booking and Rental Workflow           | Member 1 | High     | 5            |
| Task       | Build lender booking management page                                                  | Booking and Rental Workflow           | Member 1 | High     | 5            |
| Task       | Write tests for booking status transitions and deposit calculation                    | Testing, Deployment and Documentation | Shared   | Medium   | 5            |
| Story      | As a user, I want to submit a damage report with evidence                             | Deposit and Damage Report             | Member 2 | High     | 5            |
| Story      | As an admin, I want to review damage disputes and decide deposit release or deduction | Admin Review and Dashboard            | Member 2 | High     | 8            |
| Task       | Add renter, lender, and admin dashboard views                                         | Admin Review and Dashboard            | Member 1 | Medium   | 5            |
| Task       | Improve frontend validation, loading, empty, and error states                         | Testing, Deployment and Documentation | Member 1 | Medium   | 5            |
| Task       | Complete backend and manual end-to-end tests for key workflows                        | Testing, Deployment and Documentation | Shared   | High     | 8            |
| Task       | Configure GitHub Actions and Docker Compose deployment preparation                    | Testing, Deployment and Documentation | Member 1 | Medium   | 5            |
| Task       | Write README, API documentation, final report, demo script, and screenshots           | Testing, Deployment and Documentation | Shared   | High     | 8            |

### Sprint 3 Deliverables

By the end of Sprint 3, we expect to complete:

* Booking model and status transition logic
* Booking request creation
* Lender booking approval or rejection
* Simulated deposit calculation
* Simulated deposit confirmation
* Handover confirmation
* Return confirmation
* Rental status tracking
* Renter booking management page
* Lender booking management page
* Damage report submission
* Damage evidence upload
* Admin dispute review
* Deposit release or partial deduction decision
* Renter, lender, and admin dashboard views
* Improved frontend validation and error handling
* Loading, empty, and error states
* Backend tests
* Manual end-to-end testing
* GitHub Actions workflow
* Deployment preparation
* README and API documentation
* Final report, demo script, and screenshots

---

## 10. Story Point Estimation

Story points will be used to estimate the relative effort and complexity of each Jira issue.

| Story Points | Meaning                                                               |
| ------------ | --------------------------------------------------------------------- |
| 1            | Very small task                                                       |
| 2            | Small task with limited complexity                                    |
| 3            | Standard task or simple feature                                       |
| 5            | Medium feature requiring backend or frontend integration              |
| 8            | Complex feature involving several modules, APIs, UI work, and testing |
| 13           | Too large and should be split into smaller issues                     |

For this project, each team member should usually take around **18 to 30 story points per sprint**, depending on feature difficulty and available time.

---

## 11. Team Responsibility Plan

Since we are a two-person team, we will divide the work by feature area rather than separating the project strictly into frontend and backend work.

### Member 1 Responsibilities

Member 1 will mainly work on:

* Project environment setup
* Backend foundation
* Authentication support
* User profile features
* Bike listing models and APIs
* Bike image upload
* Ownership evidence upload
* Lender listing management
* Dashboard views
* Deployment configuration
* Testing and documentation support

### Member 2 Responsibilities

Member 2 will mainly work on:

* Frontend project setup
* Role selection interface
* Admin listing approval
* Search and filter interface
* Booking model and APIs
* Booking status transition logic
* Deposit calculation
* Handover and return confirmation
* Damage report feature
* Admin dispute review
* Testing and documentation support

### Shared Responsibilities

Both team members will work together on:

* Requirement discussion
* API contract design
* Code review
* Manual end-to-end testing
* Bug fixing
* README writing
* Final report writing
* Demo script preparation
* Presentation preparation

This division allows both members to contribute to the full project while still keeping ownership of specific modules clear.

---

## 12. Definition of Done

A Jira issue will only be moved to `Done` when it satisfies the following conditions:

* The required feature or technical task has been implemented.
* The issue meets its acceptance criteria.
* Required validations and permissions have been applied.
* Success and error responses are handled properly.
* The feature has been manually tested.
* Important backend logic has automated tests where practical.
* The code has been reviewed by the other team member.
* Related API notes or documentation have been updated.
* The issue has been moved to the `Done` column in Jira.

---

## 13. Example Story: Create Bike Listing

**Issue Type:**
Story

**Summary:**
As a lender, I want to create a bike listing.

**Description:**
As a lender, I want to create a bicycle listing by entering bike details such as title, type, size, condition, location, rental price, original price, purchase date, and description. This allows my bike to be reviewed by an admin and shown to renters after approval.

**Acceptance Criteria:**

* The lender must be logged in.
* The lender can submit the bike listing form.
* Required fields must be validated.
* A new listing is created with the default status `pending`.
* Only the bike owner can edit or delete the listing.
* The API returns clear success and error responses.
* The frontend form is connected to the backend API.

**Epic:**
Bike Listing Management

**Sprint:**
Sprint 2

**Priority:**
High

**Story Points:**
5

**Assignee:**
Member 1

---

## 14. Example Story: Create Booking Request

**Issue Type:**
Story

**Summary:**
As a renter, I want to create a booking request.

**Description:**
As a renter, I want to select an approved bicycle and submit a booking request with a rental start time and end time. This allows the lender to review my request and decide whether to approve or reject it.

**Acceptance Criteria:**

* The renter must be logged in.
* The bike must be approved and available.
* The renter can select rental start and end time.
* The system checks that the end time is after the start time.
* The booking status is initially set to `pending`.
* The lender can view the booking request.
* The renter can view the booking status.
* Invalid requests return clear error messages.

**Epic:**
Booking and Rental Workflow

**Sprint:**
Sprint 3

**Priority:**
High

**Story Points:**
5

**Assignee:**
Member 2

---

## 15. Risk Management

Possible project risks will be reviewed during sprint planning and sprint review.

| Risk                                         | Impact                                         | Mitigation                                                   |
| -------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| The project scope becomes too large          | The MVP may not be completed on time           | Keep advanced features outside the MVP                       |
| Booking status logic becomes complicated     | Bugs may appear in the rental workflow         | Define status transition rules early and test them carefully |
| File upload integration causes issues        | Uploaded evidence may not display correctly    | Start with local media upload before moving to cloud storage |
| Frontend and backend integration is delayed  | Features may work separately but fail together | Agree on API contracts before development                    |
| Deployment problems happen near the deadline | The final demo may be affected                 | Keep a working local demo version at all times               |
| The team has limited development time        | Some features may be rushed                    | Complete must-have features before adding optional features  |

---

## 16. Final Jira Plan Summary

The Jira project will include three sprints and a clear set of epics, stories, tasks, and testing activities.

| Item         | Estimated Count                |
| ------------ | ------------------------------ |
| Sprints      | 3                              |
| Epics        | 8                              |
| Stories      | 18–24                          |
| Tasks        | 12–16                          |
| Bugs         | Added during testing if needed |
| Total Issues | Around 35–42                   |

Each sprint will contain a manageable number of Jira issues. Each team member will normally take around **4 to 10 issues per sprint**, depending on issue complexity and sprint workload.

This Jira plan is suitable for a two-person MSE Master project because it keeps the workload structured, shows clear ownership, and supports steady progress from project setup to final delivery.
