# Implementation Plan

- [ ] 1. Set up database connection and testing infrastructure
  - Create Supabase client configuration module
  - Set up test database connection with environment variables
  - Create pytest configuration for database tests
  - Implement database reset utility for test isolation
  - _Requirements: All requirements (foundation for implementation)_

- [ ]* 1.1 Write unit tests for database connection
  - Test successful connection to Supabase
  - Test connection with invalid credentials
  - Test connection timeout handling
  - _Requirements: All requirements_

- [ ] 2. Create SQL migration script for core tables
  - Write SQL script to create `api` schema
  - Enable uuid-ossp extension
  - Create contacts table with all columns, constraints, and indexes
  - Create projects table with all columns, constraints, foreign keys, and indexes
  - Create settings table with all columns, constraints, and indexes
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 11.1, 11.2, 11.3, 11.4, 12.1, 12.2, 12.3, 12.5, 13.1, 13.3_

- [ ] 2.1 Write unit tests for core table structure
  - Verify contacts table exists with all required columns and correct types
  - Verify projects table exists with all required columns and correct types
  - Verify settings table exists with all required columns and correct types
  - Verify all indexes exist on core tables
  - Verify foreign key constraints exist with correct cascade rules
  - _Requirements: 1.1, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 11.1, 11.2, 12.1, 12.2, 12.3, 12.5_

- [ ]* 2.2 Write property test for UUID auto-generation
  - **Property 2: UUID auto-generation**
  - **Validates: Requirements 1.2**

- [ ]* 2.3 Write property test for optional field NULL support
  - **Property 3: Optional field NULL support**
  - **Validates: Requirements 1.3**

- [ ]* 2.4 Write property test for timestamp auto-generation
  - **Property 4: Timestamp auto-generation**
  - **Validates: Requirements 1.5**

- [ ]* 2.5 Write property test for completion percentage constraint
  - **Property 5: Completion percentage constraint**
  - **Validates: Requirements 2.6**

- [ ]* 2.6 Write property test for foreign key referential integrity
  - **Property 6: Foreign key referential integrity**
  - **Validates: Requirements 2.7, 13.5**

- [ ]* 2.7 Write property test for settings key uniqueness
  - **Property 20: Settings key uniqueness**
  - **Validates: Requirements 11.3**

- [ ] 3. Create SQL migration script for financial tables
  - Create invoices table with all columns, constraints, foreign keys, generated column (balance_due), and indexes
  - Create proposals table with all columns, constraints, foreign keys, and indexes
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 12.1, 12.2, 12.3, 12.4, 13.1, 13.2, 13.3_

- [ ] 3.1 Write unit tests for financial table structure
  - Verify invoices table exists with all required columns and correct types
  - Verify proposals table exists with all required columns and correct types
  - Verify balance_due generated column exists and is computed correctly
  - Verify all indexes exist on financial tables
  - Verify unique indexes on invoice_number and proposal_number
  - Verify foreign key constraints exist with correct cascade rules
  - _Requirements: 3.1, 3.2, 3.4, 4.1, 4.2, 4.3, 4.4, 12.1, 12.2, 12.3, 12.4_

- [ ]* 3.2 Write property test for balance due calculation
  - **Property 7: Balance due calculation accuracy**
  - **Validates: Requirements 3.3**

- [ ]* 3.3 Write property test for invoice status validation
  - **Property 8: Invoice status validation**
  - **Validates: Requirements 3.5**

- [ ]* 3.4 Write property test for proposal status validation
  - **Property 9: Proposal status validation**
  - **Validates: Requirements 4.5**

- [ ] 4. Create SQL migration script for scheduling and feedback tables
  - Create appointments table with all columns, constraints, foreign keys, and indexes
  - Create reviews table with all columns, constraints, foreign keys, and indexes
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 12.1, 12.2, 12.3, 13.1, 13.2, 13.3_

- [ ] 4.1 Write unit tests for scheduling and feedback table structure
  - Verify appointments table exists with all required columns and correct types
  - Verify reviews table exists with all required columns and correct types
  - Verify all indexes exist on these tables
  - Verify foreign key constraints exist with correct cascade rules
  - _Requirements: 5.1, 5.2, 5.3, 5.5, 6.1, 6.3, 6.5, 12.1, 12.2, 12.3_

- [ ]* 4.2 Write property test for appointment status validation
  - **Property 10: Appointment status validation**
  - **Validates: Requirements 5.4**

- [ ]* 4.3 Write property test for review rating constraint
  - **Property 11: Review rating constraint**
  - **Validates: Requirements 6.2**

- [ ]* 4.4 Write property test for review status validation
  - **Property 12: Review status validation**
  - **Validates: Requirements 6.4**

- [ ] 5. Create SQL migration script for operational tables
  - Create campaigns table with all columns, constraints, and indexes
  - Create conversations table with all columns, constraints, foreign keys, and indexes
  - Create tasks table with all columns, constraints, foreign keys, and indexes
  - Create goals table with all columns, constraints, generated column (progress_percentage), and indexes
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 10.1, 10.2, 10.3, 10.4, 10.5, 12.1, 12.2, 12.3, 12.5, 13.1, 13.2, 13.3_

- [ ] 5.1 Write unit tests for operational table structure
  - Verify campaigns table exists with all required columns and correct types
  - Verify conversations table exists with all required columns and correct types
  - Verify tasks table exists with all required columns and correct types
  - Verify goals table exists with all required columns and correct types
  - Verify progress_percentage generated column exists and is computed correctly
  - Verify all indexes exist on operational tables
  - Verify foreign key constraints exist with correct cascade rules
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.6, 8.1, 8.2, 8.5, 9.1, 9.4, 9.5, 10.1, 10.4, 10.5, 12.1, 12.2, 12.3, 12.5_

- [ ]* 5.2 Write property test for campaign status validation
  - **Property 13: Campaign status validation**
  - **Validates: Requirements 7.5**

- [ ]* 5.3 Write property test for conversation status validation
  - **Property 14: Conversation status validation**
  - **Validates: Requirements 8.3**

- [ ]* 5.4 Write property test for conversation priority validation
  - **Property 15: Conversation priority validation**
  - **Validates: Requirements 8.4**

- [ ]* 5.5 Write property test for task status validation
  - **Property 16: Task status validation**
  - **Validates: Requirements 9.2**

- [ ]* 5.6 Write property test for task priority validation
  - **Property 17: Task priority validation**
  - **Validates: Requirements 9.3**

- [ ]* 5.7 Write property test for goal progress calculation
  - **Property 18: Goal progress calculation accuracy**
  - **Validates: Requirements 10.2**

- [ ]* 5.8 Write property test for goal status validation
  - **Property 19: Goal status validation**
  - **Validates: Requirements 10.3**

- [ ] 6. Implement database repository layer
  - Create base repository class with common CRUD operations
  - Implement ContactsRepository with create, read, update, delete, and query methods
  - Implement ProjectsRepository with create, read, update, delete, and query methods
  - Implement InvoicesRepository with create, read, update, delete, and query methods
  - Implement ProposalsRepository with create, read, update, delete, and query methods
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.6, 2.7, 3.1, 3.3, 3.5, 3.6, 3.7, 4.1, 4.5, 4.6_

- [ ]* 6.1 Write unit tests for repository CRUD operations
  - Test ContactsRepository create, read, update, delete operations
  - Test ProjectsRepository create, read, update, delete operations
  - Test InvoicesRepository create, read, update, delete operations
  - Test ProposalsRepository create, read, update, delete operations
  - Test query methods with filters and pagination
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.6, 2.7, 3.1, 3.3, 3.5, 3.6, 3.7, 4.1, 4.5, 4.6_

- [ ] 7. Implement remaining repository classes
  - Implement AppointmentsRepository with create, read, update, delete, and query methods
  - Implement ReviewsRepository with create, read, update, delete, and query methods
  - Implement CampaignsRepository with create, read, update, delete, and query methods
  - Implement ConversationsRepository with create, read, update, delete, and query methods
  - Implement TasksRepository with create, read, update, delete, and query methods
  - Implement GoalsRepository with create, read, update, delete, and query methods
  - Implement SettingsRepository with get, set, delete methods
  - _Requirements: 5.1, 5.4, 5.6, 5.7, 6.1, 6.2, 6.4, 6.6, 6.7, 7.1, 7.5, 8.1, 8.3, 8.4, 8.6, 9.1, 9.2, 9.3, 9.6, 9.7, 10.1, 10.2, 10.3, 11.1, 11.2, 11.3_

- [ ]* 7.1 Write unit tests for remaining repository operations
  - Test AppointmentsRepository CRUD operations
  - Test ReviewsRepository CRUD operations
  - Test CampaignsRepository CRUD operations
  - Test ConversationsRepository CRUD operations
  - Test TasksRepository CRUD operations
  - Test GoalsRepository CRUD operations
  - Test SettingsRepository get, set, delete operations
  - _Requirements: 5.1, 5.4, 5.6, 5.7, 6.1, 6.2, 6.4, 6.6, 6.7, 7.1, 7.5, 8.1, 8.3, 8.4, 8.6, 9.1, 9.2, 9.3, 9.6, 9.7, 10.1, 10.2, 10.3, 11.1, 11.2, 11.3_

- [ ] 8. Implement JSONB data validation utilities
  - Create validator for invoice line_items JSONB structure
  - Create validator for proposal sections JSONB structure
  - Create validator for conversation messages JSONB structure
  - Create validator for task checklist JSONB structure
  - Create validator for campaign content JSONB structure
  - _Requirements: 3.4, 4.3, 7.6, 8.2, 9.5_

- [ ]* 8.1 Write unit tests for JSONB validators
  - Test line_items validator with valid and invalid structures
  - Test sections validator with valid and invalid structures
  - Test messages validator with valid and invalid structures
  - Test checklist validator with valid and invalid structures
  - Test content validator with valid and invalid structures
  - _Requirements: 3.4, 4.3, 7.6, 8.2, 9.5_

- [ ] 9. Implement cascade behavior integration tests
  - Write integration test for contact deletion with related records
  - Write integration test for project deletion with related records
  - Verify all foreign keys are set to NULL as expected
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ]* 9.1 Write property test for cascade behavior on contact deletion
  - **Property 26: Cascade behavior on contact deletion**
  - **Validates: Requirements 13.1**

- [ ]* 9.2 Write property test for cascade behavior on project deletion
  - **Property 27: Cascade behavior on project deletion**
  - **Validates: Requirements 13.2**

- [ ]* 9.3 Write property test for referential integrity enforcement
  - **Property 29: Referential integrity enforcement**
  - **Validates: Requirements 13.5**

- [ ] 10. Create database migration runner and version control
  - Implement migration runner script that executes SQL files in order
  - Create migration version tracking table
  - Implement rollback functionality for failed migrations
  - Add migration status reporting
  - _Requirements: All requirements (migration infrastructure)_

- [ ]* 10.1 Write unit tests for migration runner
  - Test migration execution in correct order
  - Test migration version tracking
  - Test rollback on failed migration
  - Test idempotent migration execution
  - _Requirements: All requirements_

- [ ] 11. Implement query optimization utilities
  - Create query builder for common voice query patterns
  - Implement pagination helper for large result sets
  - Create query performance monitoring utility
  - Add query plan analysis helper (EXPLAIN ANALYZE wrapper)
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ]* 11.1 Write unit tests for query utilities
  - Test query builder generates correct SQL
  - Test pagination helper with various page sizes
  - Test query performance monitoring captures metrics
  - Test query plan analysis parses EXPLAIN output
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 12. Create database seeding utilities for development
  - Implement seed data generator for contacts
  - Implement seed data generator for projects with related records
  - Implement seed data generator for invoices and proposals
  - Implement seed data generator for appointments, reviews, and tasks
  - Create seed script that populates database with realistic test data
  - _Requirements: All requirements (development tooling)_

- [ ] 13. Implement database backup and restore utilities
  - Create backup script that exports all tables to JSON
  - Create restore script that imports JSON data
  - Implement incremental backup for large datasets
  - Add backup verification utility
  - _Requirements: All requirements (operational tooling)_

- [ ] 14. Create database documentation generator
  - Implement script that generates markdown documentation from schema
  - Include table descriptions, column types, constraints, and relationships
  - Generate entity relationship diagram in Mermaid format
  - Create index usage report
  - _Requirements: All requirements (documentation)_

- [ ] 15. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
