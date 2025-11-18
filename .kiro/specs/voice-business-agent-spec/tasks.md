# Implementation Plan

- [ ] 1. Set up Supabase authentication and add user_id columns for multi-tenant painting business data
  - Configure Supabase authentication (already exists)
  - Add user_id UUID column to all tables in api schema (contacts, projects, invoices, proposals, appointments, reviews, campaigns, conversations, tasks, goals)
  - Add foreign key constraints to auth.users(id)
  - Add indexes on user_id columns for query performance
  - Enable RLS on all tables in api schema
  - Create RLS policies to filter by user_id = auth.uid()
  - _Requirements: 16.1, 16.4, 16.5_
  - _Note: Database schema already exists in api schema for painting business but RLS is disabled and user_id columns are missing_

- [ ] 1.1 Create api.settings table for painting business configuration
  - Create api.settings table with columns: id (UUID), user_id (UUID), key (text), value (JSONB), description (text), created_at, updated_at
  - Add foreign key constraint: user_id references auth.users(id)
  - Add unique constraint on (user_id, key) to prevent duplicate keys per user
  - Create index on user_id
  - Enable RLS on settings table
  - Create RLS policies for SELECT, INSERT, UPDATE, DELETE filtering by user_id = auth.uid()
  - _Requirements: 12.1, 12.2_
  - _Note: Settings table is for system configuration, while goals table (already exists) is for business goal tracking_

- [ ] 1.2 Add user_id columns to existing painting business tables
  - Add user_id column to api.contacts, api.projects, api.invoices, api.proposals, api.appointments, api.reviews, api.campaigns, api.conversations, api.tasks, api.goals
  - Set user_id as NOT NULL with foreign key to auth.users(id)
  - Create indexes on user_id for all tables
  - _Requirements: 16.3, 16.4, 17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8_

- [ ] 1.3 Enable RLS and create policies for all painting business tables
  - Enable RLS on all tables: ALTER TABLE api.{table_name} ENABLE ROW LEVEL SECURITY
  - Create RLS policies for SELECT, INSERT, UPDATE, DELETE that filter by user_id = auth.uid()
  - Test RLS policies with multiple painting contractor users to ensure data isolation
  - _Requirements: 16.3, 16.4, 17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8_

- [ ]* 1.4 Write property test for RLS policy enforcement
  - **Property 48: Data isolation enforcement**
  - **Validates: Requirements 16.3**

- [ ]* 1.5 Write property test for cross-table relationship validation
  - **Property 58: Cross-table relationship validation**
  - **Validates: Requirements 18.3**

- [ ] 2. Implement Supabase client integration in backend for painting business data
  - Add Supabase Python client to requirements.txt
  - Create Supabase client wrapper with connection management
  - Configure client to use api schema (not public schema) where painting business tables exist
  - Implement user context extraction from JWT tokens
  - Create database operation helpers with automatic user_id filtering for multi-tenant painting business
  - _Requirements: 16.1, 16.2, 16.3_

- [ ] 2.1 Create authentication middleware for WebSocket server
  - Modify WebSocket server to validate JWT tokens on connection
  - Extract user_id from JWT and attach to session context for painting contractor identification
  - Implement token expiration handling and refresh logic
  - Add rate limiting per painting contractor user
  - _Requirements: 16.1, 16.5_

- [ ]* 2.2 Write property test for user authentication
  - **Property 46: User authentication establishment**
  - **Validates: Requirements 16.1**

- [ ]* 2.3 Write property test for token validation
  - **Property 50: Token validation enforcement**
  - **Validates: Requirements 16.5**

- [ ] 2.4 Implement audit logging system for painting business operations
  - Create audit log table in Supabase
  - Implement logging for all painting business database modifications (projects, invoices, etc.)
  - Log security violations and failed validations
  - _Requirements: 18.1, 18.2_

- [ ]* 2.5 Write property test for audit logging
  - **Property 56: Audit logging completeness**
  - **Validates: Requirements 18.1**

- [ ] 3. Update Agent Orchestrator for user context propagation
  - Modify orchestrator to accept user_id parameter in process_query
  - Pass painting contractor user context to all specialized agents
  - Update supervisor agent to include user context in routing to painting business agents
  - _Requirements: 16.2_

- [ ]* 3.1 Write property test for permission validation
  - **Property 47: Permission validation consistency**
  - **Validates: Requirements 16.2**

- [ ] 4. Implement Contacts Agent with database integration for client management
  - Create ContactsAgent class extending Strands Agent
  - Implement tools for CRUD operations on api.contacts table
  - Add search functionality by name, company, email, phone, tags
  - Implement relationship tracking to painting projects, appointments, proposals, reviews, conversations, invoices, tasks
  - Ensure all queries filter by user_id for painting contractor data isolation
  - _Requirements: 4.1, 4.2, 4.3, 4.5_

- [ ]* 4.1 Write property test for contact information completeness
  - **Property 18: Contact information completeness**
  - **Validates: Requirements 4.1**

- [ ]* 4.2 Write property test for contact CRUD operations
  - **Property 19: Contact CRUD operation reliability**
  - **Validates: Requirements 4.2**

- [ ]* 4.3 Write property test for contact data isolation
  - **Property 51: Contact data isolation**
  - **Validates: Requirements 17.1**

- [ ]* 4.4 Write property test for contact search functionality
  - **Property 21: Contact search functionality**
  - **Validates: Requirements 4.5**

- [ ] 5. Implement Projects Agent with database integration for painting project management
  - Create ProjectsAgent class extending Strands Agent
  - Implement tools for CRUD operations on api.projects table
  - Add painting project specification management (paint type, brand, color, coats, primer, square footage)
  - Implement cost tracking (estimated cost, actual cost, budget, variance calculations)
  - Add project status management (pending, in-progress, completed, cancelled, on-hold)
  - Implement relationship tracking to clients, invoices, appointments, tasks, reviews
  - Ensure all queries filter by user_id for painting contractor data isolation
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 5.1 Write property test for project information completeness
  - **Property: Project information completeness**
  - Test that Projects_Agent retrieves complete project details including paint specifications, costs, and dates
  - **Validates: Requirements 5.1**

- [ ]* 5.2 Write property test for project creation
  - **Property: Project creation reliability**
  - Test that Projects_Agent creates projects with all required painting specifications
  - **Validates: Requirements 5.2**

- [ ]* 5.3 Write property test for project cost tracking
  - **Property: Project cost tracking accuracy**
  - Test that Projects_Agent accurately tracks estimated cost, actual cost, and budget variance
  - **Validates: Requirements 5.4**

- [ ]* 5.4 Write property test for project data isolation
  - **Property: Project data isolation**
  - Test that Projects_Agent ensures only user-owned projects are accessible
  - **Validates: Requirements 17.2**

- [ ] 6. Implement Appointments Agent with database integration for painting consultations and work scheduling
  - Create AppointmentsAgent class extending Strands Agent
  - Implement tools for scheduling and appointment management on api.appointments table
  - Add appointment type support (consultation, estimate, painting work)
  - Add conflict detection logic for scheduling
  - Implement status management (scheduled, confirmed, in-progress, completed, cancelled, no-show, rescheduled)
  - Ensure appointments filter by user ownership and client relationships
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ]* 6.1 Write property test for appointment information completeness
  - **Property 22: Appointment information completeness**
  - **Validates: Requirements 6.1**

- [ ]* 6.2 Write property test for appointment creation
  - **Property 23: Appointment creation reliability**
  - **Validates: Requirements 6.2**

- [ ]* 6.3 Write property test for conflict detection
  - **Property 24: Appointment conflict detection**
  - **Validates: Requirements 6.3**

- [ ]* 6.4 Write property test for appointment access control
  - **Property 52: Appointment access control**
  - **Validates: Requirements 17.3**

- [ ] 7. Implement Proposals Agent with database integration for painting estimates
  - Create ProposalsAgent class extending Strands Agent
  - Implement tools for painting proposal creation and tracking on api.proposals table
  - Add scope of work and pricing sections management
  - Add pricing calculation logic (subtotal, tax, discounts, total)
  - Implement status management (draft, sent, viewed, accepted, rejected, expired)
  - Verify user owns client relationship before accessing proposals
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 7.1 Write property test for proposal information completeness
  - **Property 26: Proposal information completeness**
  - **Validates: Requirements 7.1**

- [ ]* 7.2 Write property test for proposal creation
  - **Property 27: Proposal creation reliability**
  - **Validates: Requirements 7.2**

- [ ]* 7.3 Write property test for proposal calculations
  - **Property 28: Proposal calculation accuracy**
  - **Validates: Requirements 7.4**

- [ ]* 7.4 Write property test for proposal ownership verification
  - **Property 53: Proposal ownership verification**
  - **Validates: Requirements 17.4**

- [ ] 8. Implement Invoices Agent with database integration for painting project billing
  - Create InvoicesAgent class extending Strands Agent
  - Implement tools for invoice generation and tracking on api.invoices table
  - Add line items management for painting services and materials
  - Add payment tracking (amount paid, paid date, balance due calculations)
  - Implement invoice calculations (subtotal, tax, discounts, total, balance due)
  - Implement status management (draft, sent, viewed, partial, paid, overdue, cancelled)
  - Ensure invoices filter by user ownership and project/client relationships
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ]* 8.1 Write property test for invoice information completeness
  - **Property: Invoice information completeness**
  - Test that Invoices_Agent retrieves complete invoice details including line items and payment status
  - **Validates: Requirements 8.1**

- [ ]* 8.2 Write property test for invoice creation
  - **Property: Invoice creation reliability**
  - Test that Invoices_Agent creates invoices with client, project, and line items
  - **Validates: Requirements 8.2**

- [ ]* 8.3 Write property test for invoice calculations
  - **Property: Invoice calculation accuracy**
  - Test that Invoices_Agent accurately computes subtotal, tax, discounts, total, and balance due
  - **Validates: Requirements 8.3**

- [ ]* 8.4 Write property test for invoice payment tracking
  - **Property: Invoice payment tracking accuracy**
  - Test that Invoices_Agent correctly updates payment amounts and calculates balance due
  - **Validates: Requirements 8.4**

- [ ]* 8.5 Write property test for invoice data isolation
  - **Property: Invoice data isolation**
  - Test that Invoices_Agent ensures only user-owned invoices are accessible
  - **Validates: Requirements 17.5**

- [ ] 9. Implement Reviews Agent with database integration for painting project feedback
  - Create ReviewsAgent class extending Strands Agent
  - Implement tools for customer review management and response handling on api.reviews table
  - Add analytics calculations for painting projects (average ratings, sentiment analysis, trends)
  - Implement status management (pending, approved, published, responded, flagged)
  - Ensure reviews only accessible via user-owned projects or clients
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 9.1 Write property test for review information completeness
  - **Property 29: Review information completeness**
  - **Validates: Requirements 9.1**

- [ ]* 9.2 Write property test for review response functionality
  - **Property 30: Review response functionality**
  - **Validates: Requirements 9.2**

- [ ]* 9.3 Write property test for review analytics
  - **Property 31: Review analytics accuracy**
  - **Validates: Requirements 9.3**

- [ ]* 9.4 Write property test for review access control
  - **Property 54: Review access control**
  - **Validates: Requirements 17.6**

- [ ] 10. Implement Marketing Agent with database integration for painting service campaigns
  - Create MarketingAgent class extending Strands Agent
  - Implement tools for painting service campaign management and tracking on api.campaigns table
  - Add performance metrics reporting (sent, delivered, open rate, click rate, conversion rate, ROI)
  - Add analytics calculations (revenue, cost effectiveness, optimization recommendations)
  - Implement status management (draft, scheduled, active, paused, completed, cancelled)
  - Restrict access to user-created or assigned campaigns
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ]* 10.1 Write property test for campaign information completeness
  - **Property 32: Campaign information completeness**
  - **Validates: Requirements 10.1**

- [ ]* 10.2 Write property test for campaign performance reporting
  - **Property 33: Campaign performance reporting**
  - **Validates: Requirements 10.2**

- [ ]* 10.3 Write property test for campaign analytics
  - **Property 34: Campaign analytics accuracy**
  - **Validates: Requirements 10.5**

- [ ]* 10.4 Write property test for campaign access restriction
  - **Property 55: Campaign access restriction**
  - **Validates: Requirements 17.7**

- [ ] 11. Implement Tasks Agent with database integration for painting project task management
  - Create TasksAgent class extending Strands Agent
  - Implement tools for task and to-do management on api.tasks table
  - Add task creation with project/client linkage
  - Implement priority management (low, medium, high, urgent)
  - Implement status management (todo, in-progress, completed, cancelled)
  - Add checklist management within tasks for detailed work tracking
  - Ensure tasks filter by user ownership and project/client relationships
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ]* 11.1 Write property test for task information completeness
  - **Property: Task information completeness**
  - Test that Tasks_Agent retrieves complete task details including project linkage and checklists
  - **Validates: Requirements 11.1**

- [ ]* 11.2 Write property test for task creation
  - **Property: Task creation reliability**
  - Test that Tasks_Agent creates tasks with project/client linkage and priority
  - **Validates: Requirements 11.2**

- [ ]* 11.3 Write property test for task checklist management
  - **Property: Task checklist management**
  - Test that Tasks_Agent manages checklist items within tasks
  - **Validates: Requirements 11.5**

- [ ]* 11.4 Write property test for task data isolation
  - **Property: Task data isolation**
  - Test that Tasks_Agent ensures only user-owned tasks are accessible
  - **Validates: Requirements 17.8**

- [ ] 12. Implement Settings Agent with database integration for painting business goals
  - Create SettingsAgent class extending Strands Agent
  - Implement tools for business goal tracking using api.goals table
  - Add goal progress calculation (current_value / target_value * 100)
  - Implement goal status management (active, completed, cancelled, overdue)
  - Add goal analytics (progress trends, recommendations for achieving targets)
  - Ensure all queries filter by user_id for painting contractor data isolation
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_
  - _Note: System configuration settings (api.settings table) can be added later if needed_

- [ ]* 12.1 Write property test for goal tracking accuracy
  - **Property 45: Goal tracking accuracy**
  - Test that Settings_Agent correctly calculates progress_percentage
  - **Validates: Requirements 15.2**

- [ ]* 12.2 Write property test for goal analytics
  - **Property: Goal analytics accuracy**
  - Test that Settings_Agent provides accurate progress trends and recommendations
  - **Validates: Requirements 15.4**

- [ ] 13. Update Supervisor Agent routing for painting business agents
  - Update routing logic to include all 9 painting business agents
  - Add keyword detection for: client contacts, painting projects, appointments, proposals/estimates, invoices/billing, reviews/feedback, marketing/campaigns, tasks/to-dos, settings/goals
  - Ensure user context is passed to all routed queries for painting contractor data isolation
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10, 2.11_

- [ ]* 13.1 Write property tests for query routing accuracy to all painting business agents
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

- [ ]* 13.2 Write property tests for query and response preservation
  - **Property 11: Query preservation through routing**
  - **Property 12: Response preservation through routing**
  - **Validates: Requirements 2.10, 2.11**

- [ ] 14. Implement conversation persistence in database for painting business context
  - Modify voice integration to store messages in api.conversations table
  - Store both voice and text messages in JSONB messages field
  - Link conversations to client_id when discussing painting projects or clients
  - Implement conversation history retrieval for context across sessions
  - Ensure conversations filter by user_id for painting contractor data isolation
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [ ]* 14.1 Write property test for voice-to-text context preservation
  - **Property 39: Voice-to-text context preservation**
  - **Validates: Requirements 14.1**

- [ ]* 14.2 Write property test for text-to-voice context retrieval
  - **Property 40: Text-to-voice context retrieval**
  - **Validates: Requirements 14.2**

- [ ]* 14.3 Write property test for cross-session context maintenance
  - **Property 41: Cross-session context maintenance**
  - **Validates: Requirements 14.4**

- [ ]* 14.4 Write property test for conversation security
  - **Property 59: Conversation security enforcement**
  - **Validates: Requirements 18.4**

- [ ] 15. Implement text input handling in WebSocket server for painting business queries
  - Add message type detection (audio vs text) in WebSocket handler
  - Route text messages directly to Agent Orchestrator (bypass Nova Sonic)
  - Ensure text responses are sent back as text (not audio)
  - Maintain same routing logic for both voice and text painting business queries
  - _Requirements: 13.1, 13.2, 13.3, 13.5_

- [ ]* 15.1 Write property test for text message routing
  - **Property 35: Text message routing**
  - **Validates: Requirements 13.1**

- [ ]* 15.2 Write property test for text query processing
  - **Property 36: Text query processing**
  - **Validates: Requirements 13.2**

- [ ]* 15.3 Write property test for input method consistency
  - **Property 38: Input method consistency**
  - **Validates: Requirements 13.5**

- [ ] 16. Implement frontend authentication UI for painting contractors
  - Create Supabase Auth integration in React frontend
  - Add login/logout UI components for painting contractors
  - Implement JWT token storage and automatic refresh
  - Add session state management across page reloads
  - _Requirements: 16.1_

- [ ] 16.1 Update VoiceAgent component for authenticated connections
  - Modify WebSocket connection to include JWT token in headers
  - Add painting contractor user context to all outgoing messages
  - Handle authentication errors and token expiration
  - _Requirements: 16.1, 16.5_

- [ ] 16.2 Add text input UI to VoiceAgent component
  - Create text input field in chat interface
  - Implement send button and Enter key handling
  - Display text messages in chat history
  - Ensure text and voice messages share same display for painting business queries
  - _Requirements: 13.1, 13.3_

- [ ]* 16.3 Write property test for text response display
  - **Property 37: Text response display**
  - **Validates: Requirements 13.3**

- [ ] 17. Update voice session management for security
  - Add painting contractor user session validation to audio processing
  - Implement session limits and cleanup
  - Add visual indicators for authenticated sessions
  - _Requirements: 1.1, 1.3, 1.5_

- [ ]* 17.1 Write property tests for session management
  - **Property 1: Session lifecycle consistency**
  - **Property 4: Session state visibility**
  - **Validates: Requirements 1.1, 1.3, 1.5**

- [ ] 18. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 19. Integration testing and end-to-end validation for painting business operations
  - Test complete voice flow with authentication for painting contractors
  - Test complete text flow with authentication
  - Test context switching between voice and text for painting business queries
  - Test multi-user data isolation between different painting contractors
  - Verify RLS policies work correctly for all painting business tables
  - Test all 9 painting business agents with real database operations
  - Test painting-specific workflows (project creation → proposal → invoice → review)
  - _Requirements: All_

- [ ]* 19.1 Write integration tests for authentication flows
  - Test JWT token validation and refresh for painting contractors
  - Test session expiration handling
  - Test multi-user concurrent sessions

- [ ]* 19.2 Write integration tests for painting business agent operations
  - Test cross-agent data relationships (projects → invoices, clients → appointments)
  - Test conversation context across sessions for painting business queries
  - Test audit logging for all painting business operations
  - Test painting-specific workflows end-to-end
