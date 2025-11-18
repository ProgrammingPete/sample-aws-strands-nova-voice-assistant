# Implementation Plan

- [ ] 1. Create api.settings table for painting business configuration
  - Create api.settings table with columns: id (UUID), key (text), value (JSONB), description (text), created_at, updated_at
  - Add unique constraint on key to prevent duplicate keys
  - _Requirements: 12.1, 12.2_
  - _Note: Settings table is for system configuration, while goals table (already exists) is for business goal tracking_

- [ ] 2. Implement Supabase client integration in backend for painting business data
  - Add Supabase Python client to requirements.txt
  - Create Supabase client wrapper with connection management
  - Configure client to use api schema (not public schema) where painting business tables exist
  - Create database operation helpers for painting business

- [ ] 3. Implement Contacts Agent with database integration for client management
  - Create ContactsAgent class extending Strands Agent
  - Implement tools for CRUD operations on api.contacts table
  - Add search functionality by name, company, email, phone, tags
  - Implement relationship tracking to painting projects, appointments, proposals, reviews, conversations, invoices, tasks
  - _Requirements: 4.1, 4.2, 4.3, 4.5_

- [ ]* 3.1 Write property test for contact information completeness
  - **Property 18: Contact information completeness**
  - **Validates: Requirements 4.1**

- [ ]* 3.2 Write property test for contact CRUD operations
  - **Property 19: Contact CRUD operation reliability**
  - **Validates: Requirements 4.2**

- [ ]* 3.3 Write property test for contact search functionality
  - **Property 21: Contact search functionality**
  - **Validates: Requirements 4.5**

- [ ] 4. Implement Projects Agent with database integration for painting project management
  - Create ProjectsAgent class extending Strands Agent
  - Implement tools for CRUD operations on api.projects table
  - Add painting project specification management (paint type, brand, color, coats, primer, square footage)
  - Implement cost tracking (estimated cost, actual cost, budget, variance calculations)
  - Add project status management (pending, in-progress, completed, cancelled, on-hold)
  - Implement relationship tracking to clients, invoices, appointments, tasks, reviews
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 4.1 Write property test for project information completeness
  - **Property: Project information completeness**
  - Test that Projects_Agent retrieves complete project details including paint specifications, costs, and dates
  - **Validates: Requirements 5.1**

- [ ]* 4.2 Write property test for project creation
  - **Property: Project creation reliability**
  - Test that Projects_Agent creates projects with all required painting specifications
  - **Validates: Requirements 5.2**

- [ ]* 4.3 Write property test for project cost tracking
  - **Property: Project cost tracking accuracy**
  - Test that Projects_Agent accurately tracks estimated cost, actual cost, and budget variance
  - **Validates: Requirements 5.4**

- [ ] 5. Implement Appointments Agent with database integration for painting consultations and work scheduling
  - Create AppointmentsAgent class extending Strands Agent
  - Implement tools for scheduling and appointment management on api.appointments table
  - Add appointment type support (consultation, estimate, painting work)
  - Add conflict detection logic for scheduling
  - Implement status management (scheduled, confirmed, in-progress, completed, cancelled, no-show, rescheduled)
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ]* 5.1 Write property test for appointment information completeness
  - **Property 22: Appointment information completeness**
  - **Validates: Requirements 6.1**

- [ ]* 5.2 Write property test for appointment creation
  - **Property 23: Appointment creation reliability**
  - **Validates: Requirements 6.2**

- [ ]* 5.3 Write property test for conflict detection
  - **Property 24: Appointment conflict detection**
  - **Validates: Requirements 6.3**

- [ ] 6. Implement Proposals Agent with database integration for painting estimates
  - Create ProposalsAgent class extending Strands Agent
  - Implement tools for painting proposal creation and tracking on api.proposals table
  - Add scope of work and pricing sections management
  - Add pricing calculation logic (subtotal, tax, discounts, total)
  - Implement status management (draft, sent, viewed, accepted, rejected, expired)
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 6.1 Write property test for proposal information completeness
  - **Property 26: Proposal information completeness**
  - **Validates: Requirements 7.1**

- [ ]* 6.2 Write property test for proposal creation
  - **Property 27: Proposal creation reliability**
  - **Validates: Requirements 7.2**

- [ ]* 6.3 Write property test for proposal calculations
  - **Property 28: Proposal calculation accuracy**
  - **Validates: Requirements 7.4**

- [ ] 7. Implement Invoices Agent with database integration for painting project billing
  - Create InvoicesAgent class extending Strands Agent
  - Implement tools for invoice generation and tracking on api.invoices table
  - Add line items management for painting services and materials
  - Add payment tracking (amount paid, paid date, balance due calculations)
  - Implement invoice calculations (subtotal, tax, discounts, total, balance due)
  - Implement status management (draft, sent, viewed, partial, paid, overdue, cancelled)
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ]* 7.1 Write property test for invoice information completeness
  - **Property: Invoice information completeness**
  - Test that Invoices_Agent retrieves complete invoice details including line items and payment status
  - **Validates: Requirements 8.1**

- [ ]* 7.2 Write property test for invoice creation
  - **Property: Invoice creation reliability**
  - Test that Invoices_Agent creates invoices with client, project, and line items
  - **Validates: Requirements 8.2**

- [ ]* 7.3 Write property test for invoice calculations
  - **Property: Invoice calculation accuracy**
  - Test that Invoices_Agent accurately computes subtotal, tax, discounts, total, and balance due
  - **Validates: Requirements 8.3**

- [ ]* 7.4 Write property test for invoice payment tracking
  - **Property: Invoice payment tracking accuracy**
  - Test that Invoices_Agent correctly updates payment amounts and calculates balance due
  - **Validates: Requirements 8.4**

- [ ] 8. Implement Reviews Agent with database integration for painting project feedback
  - Create ReviewsAgent class extending Strands Agent
  - Implement tools for customer review management and response handling on api.reviews table
  - Add analytics calculations for painting projects (average ratings, sentiment analysis, trends)
  - Implement status management (pending, approved, published, responded, flagged)
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 8.1 Write property test for review information completeness
  - **Property 29: Review information completeness**
  - **Validates: Requirements 9.1**

- [ ]* 8.2 Write property test for review response functionality
  - **Property 30: Review response functionality**
  - **Validates: Requirements 9.2**

- [ ]* 8.3 Write property test for review analytics
  - **Property 31: Review analytics accuracy**
  - **Validates: Requirements 9.3**

- [ ] 9. Implement Marketing Agent with database integration for painting service campaigns
  - Create MarketingAgent class extending Strands Agent
  - Implement tools for painting service campaign management and tracking on api.campaigns table
  - Add performance metrics reporting (sent, delivered, open rate, click rate, conversion rate, ROI)
  - Add analytics calculations (revenue, cost effectiveness, optimization recommendations)
  - Implement status management (draft, scheduled, active, paused, completed, cancelled)
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ]* 9.1 Write property test for campaign information completeness
  - **Property 32: Campaign information completeness**
  - **Validates: Requirements 10.1**

- [ ]* 9.2 Write property test for campaign performance reporting
  - **Property 33: Campaign performance reporting**
  - **Validates: Requirements 10.2**

- [ ]* 9.3 Write property test for campaign analytics
  - **Property 34: Campaign analytics accuracy**
  - **Validates: Requirements 10.5**

- [ ] 10. Implement Tasks Agent with database integration for painting project task management
  - Create TasksAgent class extending Strands Agent
  - Implement tools for task and to-do management on api.tasks table
  - Add task creation with project/client linkage
  - Implement priority management (low, medium, high, urgent)
  - Implement status management (todo, in-progress, completed, cancelled)
  - Add checklist management within tasks for detailed work tracking
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ]* 10.1 Write property test for task information completeness
  - **Property: Task information completeness**
  - Test that Tasks_Agent retrieves complete task details including project linkage and checklists
  - **Validates: Requirements 11.1**

- [ ]* 10.2 Write property test for task creation
  - **Property: Task creation reliability**
  - Test that Tasks_Agent creates tasks with project/client linkage and priority
  - **Validates: Requirements 11.2**

- [ ]* 10.3 Write property test for task checklist management
  - **Property: Task checklist management**
  - Test that Tasks_Agent manages checklist items within tasks
  - **Validates: Requirements 11.5**

- [ ] 11. Implement Settings Agent with database integration for painting business goals
  - Create SettingsAgent class extending Strands Agent
  - Implement tools for business goal tracking using api.goals table
  - Add goal progress calculation (current_value / target_value * 100)
  - Implement goal status management (active, completed, cancelled, overdue)
  - Add goal analytics (progress trends, recommendations for achieving targets)
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_
  - _Note: System configuration settings (api.settings table) can be added later if needed_

- [ ]* 11.1 Write property test for goal tracking accuracy
  - **Property 45: Goal tracking accuracy**
  - Test that Settings_Agent correctly calculates progress_percentage
  - **Validates: Requirements 15.2**

- [ ]* 11.2 Write property test for goal analytics
  - **Property: Goal analytics accuracy**
  - Test that Settings_Agent provides accurate progress trends and recommendations
  - **Validates: Requirements 15.4**

- [ ] 12. Update Supervisor Agent routing for painting business agents
  - Update routing logic to include all 9 painting business agents
  - Add keyword detection for: client contacts, painting projects, appointments, proposals/estimates, invoices/billing, reviews/feedback, marketing/campaigns, tasks/to-dos, settings/goals
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10, 2.11_

- [ ]* 12.1 Write property tests for query routing accuracy to all painting business agents
  - **Property 5: Contact query routing accuracy**
  - **Property 6: Appointment query routing accuracy**
  - **Property 7: Proposal query routing accuracy**
  - **Property 8: Review query routing accuracy**
  - **Property 9: Marketing query routing accuracy**
  - **Property 10: Settings query routing accuracy**
  - **Property: Project query routing accuracy**
  - **Property: Invoice query routing accuracy**
  - **Property: Task query routing accuracy**
  - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9**

- [ ]* 12.2 Write property tests for query and response preservation
  - **Property 11: Query preservation through routing**
  - **Property 12: Response preservation through routing**
  - **Validates: Requirements 2.10, 2.11**

- [ ] 13. Implement conversation persistence in database for painting business context
  - Modify voice integration to store messages in api.conversations table
  - Store both voice and text messages in JSONB messages field
  - Link conversations to client_id when discussing painting projects or clients
  - Implement conversation history retrieval for context across sessions
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [ ]* 13.1 Write property test for voice-to-text context preservation
  - **Property 39: Voice-to-text context preservation**
  - **Validates: Requirements 14.1**

- [ ]* 13.2 Write property test for text-to-voice context retrieval
  - **Property 40: Text-to-voice context retrieval**
  - **Validates: Requirements 14.2**

- [ ]* 13.3 Write property test for cross-session context maintenance
  - **Property 41: Cross-session context maintenance**
  - **Validates: Requirements 14.4**

- [ ] 14. Implement text input handling in WebSocket server for painting business queries
  - Add message type detection (audio vs text) in WebSocket handler
  - Route text messages directly to Agent Orchestrator (bypass Nova Sonic)
  - Ensure text responses are sent back as text (not audio)
  - Maintain same routing logic for both voice and text painting business queries
  - _Requirements: 13.1, 13.2, 13.3, 13.5_

- [ ]* 14.1 Write property test for text message routing
  - **Property 35: Text message routing**
  - **Validates: Requirements 13.1**

- [ ]* 14.2 Write property test for text query processing
  - **Property 36: Text query processing**
  - **Validates: Requirements 13.2**

- [ ]* 14.3 Write property test for input method consistency
  - **Property 38: Input method consistency**
  - **Validates: Requirements 13.5**

- [ ] 15. Add text input UI to VoiceAgent component
  - Create text input field in chat interface
  - Implement send button and Enter key handling
  - Display text messages in chat history
  - Ensure text and voice messages share same display for painting business queries
  - _Requirements: 13.1, 13.3_

- [ ]* 15.1 Write property test for text response display
  - **Property 37: Text response display**
  - **Validates: Requirements 13.3**

- [ ] 16. Update voice session management
  - Implement session limits and cleanup
  - Add visual indicators for active sessions
  - _Requirements: 1.1, 1.3, 1.5_

- [ ]* 16.1 Write property tests for session management
  - **Property 1: Session lifecycle consistency**
  - **Property 4: Session state visibility**
  - **Validates: Requirements 1.1, 1.3, 1.5**

- [ ] 17. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 18. Integration testing and end-to-end validation for painting business operations
  - Test complete voice flow for painting contractors
  - Test complete text flow
  - Test context switching between voice and text for painting business queries
  - Test all 9 painting business agents with real database operations
  - Test painting-specific workflows (project creation → proposal → invoice → review)
  - _Requirements: All_

- [ ]* 18.1 Write integration tests for painting business agent operations
  - Test cross-agent data relationships (projects → invoices, clients → appointments)
  - Test conversation context across sessions for painting business queries
  - Test painting-specific workflows end-to-end
