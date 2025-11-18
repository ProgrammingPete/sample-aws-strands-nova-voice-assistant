# Implementation Plan

- [ ] 1. Set up Supabase authentication and add user_id columns
  - Configure Supabase authentication (already exists)
  - Add user_id UUID column to all tables in api schema
  - Add foreign key constraints to auth.users(id)
  - Add indexes on user_id columns for query performance
  - Enable RLS on all tables in api schema
  - Create RLS policies to filter by user_id = auth.uid()
  - _Requirements: 13.1, 13.4, 13.5_
  - _Note: Database schema already exists in api schema but RLS is disabled and user_id columns are missing_

- [ ] 1.1 Create api.settings table
  - Create api.settings table with columns: id (UUID), user_id (UUID), key (text), value (JSONB), description (text), created_at, updated_at
  - Add foreign key constraint: user_id references auth.users(id)
  - Add unique constraint on (user_id, key) to prevent duplicate keys per user
  - Create index on user_id
  - Enable RLS on settings table
  - Create RLS policies for SELECT, INSERT, UPDATE, DELETE filtering by user_id = auth.uid()
  - _Requirements: 12.1, 12.2_

- [ ] 1.2 Add user_id columns to existing tables
  - Add user_id column to api.contacts, api.projects, api.invoices, api.proposals, api.appointments, api.reviews, api.campaigns, api.conversations, api.tasks, api.goals
  - Set user_id as NOT NULL with foreign key to auth.users(id)
  - Create indexes on user_id for all tables
  - _Requirements: 13.3, 13.4, 14.1, 14.2, 14.3, 14.4, 14.5_

- [ ] 1.3 Enable RLS and create policies for all tables
  - Enable RLS on all tables: ALTER TABLE api.{table_name} ENABLE ROW LEVEL SECURITY
  - Create RLS policies for SELECT, INSERT, UPDATE, DELETE that filter by user_id = auth.uid()
  - Test RLS policies with multiple users to ensure data isolation
  - _Requirements: 13.3, 13.4, 14.1, 14.2, 14.3, 14.4, 14.5_

- [ ]* 1.2 Write property test for RLS policy enforcement
  - **Property 48: Data isolation enforcement**
  - **Validates: Requirements 13.3**

- [ ]* 1.3 Write property test for cross-table relationship validation
  - **Property 58: Cross-table relationship validation**
  - **Validates: Requirements 15.3**

- [ ] 2. Implement Supabase client integration in backend
  - Add Supabase Python client to requirements.txt
  - Create Supabase client wrapper with connection management
  - Configure client to use api schema (not public schema)
  - Implement user context extraction from JWT tokens
  - Create database operation helpers with automatic user_id filtering
  - _Requirements: 13.1, 13.2, 13.3_

- [ ] 2.1 Create authentication middleware for WebSocket server
  - Modify WebSocket server to validate JWT tokens on connection
  - Extract user_id from JWT and attach to session context
  - Implement token expiration handling and refresh logic
  - Add rate limiting per user
  - _Requirements: 13.1, 13.5_

- [ ]* 2.2 Write property test for user authentication
  - **Property 46: User authentication establishment**
  - **Validates: Requirements 13.1**

- [ ]* 2.3 Write property test for token validation
  - **Property 50: Token validation enforcement**
  - **Validates: Requirements 13.5**

- [ ] 2.3 Implement audit logging system
  - Create audit log table in Supabase
  - Implement logging for all database modifications
  - Log security violations and failed validations
  - _Requirements: 15.1, 15.2_

- [ ]* 2.4 Write property test for audit logging
  - **Property 56: Audit logging completeness**
  - **Validates: Requirements 15.1**

- [ ] 3. Update Agent Orchestrator for user context propagation
  - Modify orchestrator to accept user_id parameter in process_query
  - Pass user context to all specialized agents
  - Update supervisor agent to include user context in routing
  - _Requirements: 13.2_

- [ ]* 3.1 Write property test for permission validation
  - **Property 47: Permission validation consistency**
  - **Validates: Requirements 13.2**

- [ ] 4. Implement Contacts Agent with database integration
  - Create ContactsAgent class extending Strands Agent
  - Implement tools for CRUD operations on contacts table
  - Add search functionality by name, company, email, phone, tags
  - Implement relationship tracking (projects, appointments, proposals, reviews, conversations, invoices, tasks)
  - Ensure all queries filter by user_id
  - _Requirements: 4.1, 4.2, 4.3, 4.5_
  - _Note: Database includes additional tables (projects, invoices, tasks) not in original requirements_

- [ ]* 4.1 Write property test for contact information completeness
  - **Property 18: Contact information completeness**
  - **Validates: Requirements 4.1**

- [ ]* 4.2 Write property test for contact CRUD operations
  - **Property 19: Contact CRUD operation reliability**
  - **Validates: Requirements 4.2**

- [ ]* 4.3 Write property test for contact data isolation
  - **Property 51: Contact data isolation**
  - **Validates: Requirements 14.1**

- [ ]* 4.4 Write property test for contact search functionality
  - **Property 21: Contact search functionality**
  - **Validates: Requirements 4.5**

- [ ] 5. Implement Appointments Agent with database integration
  - Create AppointmentsAgent class extending Strands Agent
  - Implement tools for scheduling and appointment management
  - Add conflict detection logic for scheduling
  - Implement status management (scheduled, confirmed, completed, cancelled, rescheduled)
  - Ensure appointments filter by user ownership and client relationships
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ]* 5.1 Write property test for appointment information completeness
  - **Property 22: Appointment information completeness**
  - **Validates: Requirements 5.1**

- [ ]* 5.2 Write property test for appointment creation
  - **Property 23: Appointment creation reliability**
  - **Validates: Requirements 5.2**

- [ ]* 5.3 Write property test for conflict detection
  - **Property 24: Appointment conflict detection**
  - **Validates: Requirements 5.3**

- [ ]* 5.4 Write property test for appointment access control
  - **Property 52: Appointment access control**
  - **Validates: Requirements 14.2**

- [ ] 6. Implement Proposals Agent with database integration
  - Create ProposalsAgent class extending Strands Agent
  - Implement tools for proposal creation and tracking
  - Add pricing calculation logic (subtotal, tax, discounts, total)
  - Implement status management (draft, sent, viewed, accepted, rejected, expired)
  - Verify user owns client relationship before accessing proposals
  - _Requirements: 6.1, 6.2, 6.4_

- [ ]* 6.1 Write property test for proposal information completeness
  - **Property 26: Proposal information completeness**
  - **Validates: Requirements 6.1**

- [ ]* 6.2 Write property test for proposal creation
  - **Property 27: Proposal creation reliability**
  - **Validates: Requirements 6.2**

- [ ]* 6.3 Write property test for proposal calculations
  - **Property 28: Proposal calculation accuracy**
  - **Validates: Requirements 6.4**

- [ ]* 6.4 Write property test for proposal ownership verification
  - **Property 53: Proposal ownership verification**
  - **Validates: Requirements 14.3**

- [ ] 7. Implement Reviews Agent with database integration
  - Create ReviewsAgent class extending Strands Agent
  - Implement tools for review management and response handling
  - Add analytics calculations (average ratings, sentiment analysis, trends)
  - Implement status management (pending, approved, published, responded, flagged)
  - Ensure reviews only accessible via user-owned projects or clients
  - _Requirements: 7.1, 7.2, 7.3_

- [ ]* 7.1 Write property test for review information completeness
  - **Property 29: Review information completeness**
  - **Validates: Requirements 7.1**

- [ ]* 7.2 Write property test for review response functionality
  - **Property 30: Review response functionality**
  - **Validates: Requirements 7.2**

- [ ]* 7.3 Write property test for review analytics
  - **Property 31: Review analytics accuracy**
  - **Validates: Requirements 7.3**

- [ ]* 7.4 Write property test for review access control
  - **Property 54: Review access control**
  - **Validates: Requirements 14.4**

- [ ] 8. Implement Marketing Agent with database integration
  - Create MarketingAgent class extending Strands Agent
  - Implement tools for campaign management and tracking
  - Add performance metrics reporting (sent, delivered, open rate, click rate, conversion rate, ROI)
  - Add analytics calculations (revenue, cost effectiveness, optimization recommendations)
  - Restrict access to user-created or assigned campaigns
  - _Requirements: 8.1, 8.2, 8.5_

- [ ]* 8.1 Write property test for campaign information completeness
  - **Property 32: Campaign information completeness**
  - **Validates: Requirements 8.1**

- [ ]* 8.2 Write property test for campaign performance reporting
  - **Property 33: Campaign performance reporting**
  - **Validates: Requirements 8.2**

- [ ]* 8.3 Write property test for campaign analytics
  - **Property 34: Campaign analytics accuracy**
  - **Validates: Requirements 8.5**

- [ ]* 8.4 Write property test for campaign access restriction
  - **Property 55: Campaign access restriction**
  - **Validates: Requirements 14.5**

- [ ] 9. Implement Settings Agent with database integration
  - Create SettingsAgent class extending Strands Agent
  - Implement tools for api.settings operations (get, set, delete by key)
  - Add goal tracking functionality using api.goals table with progress calculation
  - Ensure all queries filter by user_id for data isolation
  - Ensure only authorized users can modify configuration data
  - _Requirements: 12.1, 12.2, 12.4_

- [ ]* 9.1 Write property test for settings retrieval
  - **Property 43: Settings retrieval functionality**
  - Test that Settings_Agent can retrieve configuration from api.settings by key
  - **Validates: Requirements 12.1**

- [ ]* 9.2 Write property test for settings modification
  - **Property 44: Settings modification reliability**
  - Test that Settings_Agent can modify api.settings and confirm changes
  - **Validates: Requirements 12.2**

- [ ]* 9.3 Write property test for goal tracking
  - **Property 45: Goal tracking accuracy**
  - **Validates: Requirements 12.4**

- [ ]* 9.4 Implement additional agents for existing database tables (Projects, Invoices, Tasks)
  - Create ProjectsAgent for painting project management
  - Create InvoicesAgent for invoice operations (note: InvoiceAgent already exists but may need updates)
  - Create TasksAgent for task management
  - These agents are optional as they weren't in original requirements but tables exist in database

- [ ] 10. Update Supervisor Agent routing for business agents
  - Update routing logic to include new business agents
  - Add keyword detection for contacts, appointments, proposals, reviews, marketing, settings
  - Optionally add routing for projects, invoices, tasks if agents are implemented
  - Ensure user context is passed to all routed queries
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8_

- [ ]* 10.1 Write property tests for query routing accuracy
  - **Property 5: Contact query routing accuracy**
  - **Property 6: Appointment query routing accuracy**
  - **Property 7: Proposal query routing accuracy**
  - **Property 8: Review query routing accuracy**
  - **Property 9: Marketing query routing accuracy**
  - **Property 10: Settings query routing accuracy**
  - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**

- [ ]* 10.2 Write property tests for query and response preservation
  - **Property 11: Query preservation through routing**
  - **Property 12: Response preservation through routing**
  - **Validates: Requirements 2.7, 2.8**

- [ ] 11. Implement conversation persistence in database
  - Modify voice integration to store messages in conversations table
  - Store both voice and text messages in JSONB messages field
  - Link conversations to client_id when applicable
  - Implement conversation history retrieval for context
  - _Requirements: 11.1, 11.2, 11.4, 11.5_

- [ ]* 11.1 Write property test for voice-to-text context preservation
  - **Property 39: Voice-to-text context preservation**
  - **Validates: Requirements 11.1**

- [ ]* 11.2 Write property test for text-to-voice context retrieval
  - **Property 40: Text-to-voice context retrieval**
  - **Validates: Requirements 11.2**

- [ ]* 11.3 Write property test for cross-session context maintenance
  - **Property 41: Cross-session context maintenance**
  - **Validates: Requirements 11.4**

- [ ]* 11.4 Write property test for conversation security
  - **Property 59: Conversation security enforcement**
  - **Validates: Requirements 15.4**

- [ ] 12. Implement text input handling in WebSocket server
  - Add message type detection (audio vs text) in WebSocket handler
  - Route text messages directly to Agent Orchestrator (bypass Nova Sonic)
  - Ensure text responses are sent back as text (not audio)
  - Maintain same routing logic for both voice and text
  - _Requirements: 10.1, 10.2, 10.3, 10.5_

- [ ]* 12.1 Write property test for text message routing
  - **Property 35: Text message routing**
  - **Validates: Requirements 10.1**

- [ ]* 12.2 Write property test for text query processing
  - **Property 36: Text query processing**
  - **Validates: Requirements 10.2**

- [ ]* 12.3 Write property test for input method consistency
  - **Property 38: Input method consistency**
  - **Validates: Requirements 10.5**

- [ ] 13. Implement frontend authentication UI
  - Create Supabase Auth integration in React frontend
  - Add login/logout UI components
  - Implement JWT token storage and automatic refresh
  - Add session state management across page reloads
  - _Requirements: 13.1_

- [ ] 13.1 Update VoiceAgent component for authenticated connections
  - Modify WebSocket connection to include JWT token in headers
  - Add user context to all outgoing messages
  - Handle authentication errors and token expiration
  - _Requirements: 13.1, 13.5_

- [ ] 13.2 Add text input UI to VoiceAgent component
  - Create text input field in chat interface
  - Implement send button and Enter key handling
  - Display text messages in chat history
  - Ensure text and voice messages share same display
  - _Requirements: 10.1, 10.3_

- [ ]* 13.3 Write property test for text response display
  - **Property 37: Text response display**
  - **Validates: Requirements 10.3**

- [ ] 14. Update voice session management for security
  - Add user session validation to audio processing
  - Implement session limits and cleanup
  - Add visual indicators for authenticated sessions
  - _Requirements: 1.1, 1.3, 1.5_

- [ ]* 14.1 Write property tests for session management
  - **Property 1: Session lifecycle consistency**
  - **Property 4: Session state visibility**
  - **Validates: Requirements 1.1, 1.3, 1.5**

- [ ] 15. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 16. Integration testing and end-to-end validation
  - Test complete voice flow with authentication
  - Test complete text flow with authentication
  - Test context switching between voice and text
  - Test multi-user data isolation
  - Verify RLS policies work correctly
  - Test all business agents with real database operations
  - _Requirements: All_

- [ ]* 16.1 Write integration tests for authentication flows
  - Test JWT token validation and refresh
  - Test session expiration handling
  - Test multi-user concurrent sessions

- [ ]* 16.2 Write integration tests for business agent operations
  - Test cross-agent data relationships
  - Test conversation context across sessions
  - Test audit logging for all operations
