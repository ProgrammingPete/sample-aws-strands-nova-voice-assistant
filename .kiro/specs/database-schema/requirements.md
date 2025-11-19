# Requirements Document

## Introduction

The Database Schema provides the foundational data structure for the Voice-Based Painting Business Agent. The system uses Supabase PostgreSQL to store all painting business data including client contacts, painting projects with detailed specifications, appointments, proposals, invoices, reviews, marketing campaigns, tasks, conversations, and business goals. The schema supports complex relationships between entities and enables efficient querying for voice-based interactions.

## Glossary

- **Database_Schema**: The complete structure of tables, columns, relationships, and constraints in the Supabase PostgreSQL database
- **API_Schema**: The PostgreSQL schema namespace containing all painting business tables
- **Foreign_Key**: A database constraint that establishes relationships between tables
- **JSONB_Field**: PostgreSQL JSON binary field type for storing structured data with efficient querying
- **Timestamp_Field**: PostgreSQL timestamptz field for storing date and time with timezone
- **UUID**: Universally Unique Identifier used as primary key for all tables
- **Generated_Column**: A database column whose value is automatically computed from other columns
- **Array_Field**: PostgreSQL array type for storing multiple values in a single column
- **Unique_Constraint**: Database constraint ensuring no duplicate values in specified columns
- **Index**: Database structure to improve query performance on specific columns
- **Cascade_Delete**: Automatic deletion of related records when a parent record is deleted

## Requirements

### Requirement 1

**User Story:** As a database administrator, I want a well-structured contacts table, so that the system can store and query client information efficiently.

#### Acceptance Criteria

1. WHEN the contacts table is created, THE Database_Schema SHALL include columns for id, name, email, phone, company, address, city, state, zip_code, notes, tags, created_at, and updated_at
2. WHEN a contact is created, THE Database_Schema SHALL automatically generate a UUID for the id field
3. WHEN contact data is stored, THE Database_Schema SHALL support optional fields for email, phone, company, and address information
4. WHEN tags are stored, THE Database_Schema SHALL use an array field to support multiple tags per contact
5. WHEN timestamps are recorded, THE Database_Schema SHALL automatically set created_at and updated_at with timezone information

### Requirement 2

**User Story:** As a database administrator, I want a comprehensive projects table, so that the system can track painting projects with detailed specifications.

#### Acceptance Criteria

1. WHEN the projects table is created, THE Database_Schema SHALL include columns for id, project_number, name, client_id, client_name, status, description, location, square_footage, paint specifications, dates, costs, team assignments, and completion tracking
2. WHEN paint specifications are stored, THE Database_Schema SHALL include fields for paint_type, surface_type, paint_brand, paint_color, number_of_coats, and primer_needed
3. WHEN cost tracking is needed, THE Database_Schema SHALL include fields for estimated_cost, actual_cost, and budget
4. WHEN project dates are tracked, THE Database_Schema SHALL include fields for start_date, end_date, estimated_duration_days, and actual_completion_date
5. WHEN team assignments are stored, THE Database_Schema SHALL use an array field for assigned_team members
6. WHEN completion is tracked, THE Database_Schema SHALL include a completion_percentage field with values from 0 to 100
7. WHEN projects link to clients, THE Database_Schema SHALL include a foreign key client_id referencing the contacts table

### Requirement 3

**User Story:** As a database administrator, I want an invoices table with line items support, so that the system can manage billing and payment tracking.

#### Acceptance Criteria

1. WHEN the invoices table is created, THE Database_Schema SHALL include columns for id, invoice_number, client information, project reference, dates, amounts, line items, status, and payment details
2. WHEN invoice amounts are calculated, THE Database_Schema SHALL include fields for subtotal, tax_rate, tax_amount, discount_amount, total_amount, amount_paid
3. WHEN balance is tracked, THE Database_Schema SHALL include a generated column balance_due computed as total_amount minus amount_paid
4. WHEN line items are stored, THE Database_Schema SHALL use a JSONB field to support flexible line item structures
5. WHEN invoice status is tracked, THE Database_Schema SHALL support values: draft, sent, viewed, partial, paid, overdue, cancelled
6. WHEN invoices link to projects, THE Database_Schema SHALL include an optional foreign key project_id referencing the projects table
7. WHEN invoices link to clients, THE Database_Schema SHALL include an optional foreign key client_id referencing the contacts table

### Requirement 4

**User Story:** As a database administrator, I want a proposals table with pricing sections, so that the system can manage painting estimates and bids.

#### Acceptance Criteria

1. WHEN the proposals table is created, THE Database_Schema SHALL include columns for id, proposal_number, title, client information, description, scope_of_work, amounts, sections, dates, status, and terms
2. WHEN proposal amounts are calculated, THE Database_Schema SHALL include fields for subtotal, tax_rate, tax_amount, discount_amount, and total_amount
3. WHEN pricing sections are stored, THE Database_Schema SHALL use a JSONB field to support flexible section structures
4. WHEN proposal dates are tracked, THE Database_Schema SHALL include fields for issue_date, valid_until, and accepted_date
5. WHEN proposal status is tracked, THE Database_Schema SHALL support values: draft, sent, viewed, accepted, rejected, expired
6. WHEN proposals link to clients, THE Database_Schema SHALL include an optional foreign key client_id referencing the contacts table

### Requirement 5

**User Story:** As a database administrator, I want an appointments table with scheduling support, so that the system can manage consultations and painting work schedules.

#### Acceptance Criteria

1. WHEN the appointments table is created, THE Database_Schema SHALL include columns for id, title, client information, project reference, date, time, duration, location, type, status, assignment, and notes
2. WHEN appointment times are stored, THE Database_Schema SHALL include fields for appointment_date, start_time, end_time, and duration_minutes
3. WHEN appointment types are tracked, THE Database_Schema SHALL support storing appointment_type values like consultation, estimate, or painting work
4. WHEN appointment status is tracked, THE Database_Schema SHALL support values: scheduled, confirmed, in-progress, completed, cancelled, no-show, rescheduled
5. WHEN reminders are tracked, THE Database_Schema SHALL include fields for reminder_sent and reminder_sent_at
6. WHEN appointments link to clients, THE Database_Schema SHALL include an optional foreign key client_id referencing the contacts table
7. WHEN appointments link to projects, THE Database_Schema SHALL include an optional foreign key project_id referencing the projects table

### Requirement 6

**User Story:** As a database administrator, I want a reviews table for customer feedback, so that the system can manage reviews and responses for painting projects.

#### Acceptance Criteria

1. WHEN the reviews table is created, THE Database_Schema SHALL include columns for id, client information, project reference, rating, title, review_text, platform, status, response information, and dates
2. WHEN ratings are stored, THE Database_Schema SHALL include a rating field with integer values from 1 to 5
3. WHEN review responses are tracked, THE Database_Schema SHALL include fields for response_text, response_date, and responded_by
4. WHEN review status is tracked, THE Database_Schema SHALL support values: pending, approved, published, responded, flagged
5. WHEN review platforms are tracked, THE Database_Schema SHALL include fields for platform and platform_url
6. WHEN reviews link to clients, THE Database_Schema SHALL include an optional foreign key client_id referencing the contacts table
7. WHEN reviews link to projects, THE Database_Schema SHALL include an optional foreign key project_id referencing the projects table

### Requirement 7

**User Story:** As a database administrator, I want a campaigns table for marketing tracking, so that the system can manage promotional activities and performance metrics.

#### Acceptance Criteria

1. WHEN the campaigns table is created, THE Database_Schema SHALL include columns for id, name, campaign_type, description, dates, status, budget, performance metrics, content, and tags
2. WHEN campaign performance is tracked, THE Database_Schema SHALL include fields for target_audience_count, sent_count, delivered_count, opened_count, clicked_count, converted_count
3. WHEN campaign rates are calculated, THE Database_Schema SHALL include fields for open_rate, click_rate, conversion_rate, and roi
4. WHEN campaign financials are tracked, THE Database_Schema SHALL include fields for budget, actual_cost, and revenue_generated
5. WHEN campaign status is tracked, THE Database_Schema SHALL support values: draft, scheduled, active, paused, completed, cancelled
6. WHEN campaign content is stored, THE Database_Schema SHALL use a JSONB field to support flexible content structures

### Requirement 8

**User Story:** As a database administrator, I want a conversations table for chat history, so that the system can maintain context across voice and text interactions.

#### Acceptance Criteria

1. WHEN the conversations table is created, THE Database_Schema SHALL include columns for id, client information, subject, channel, status, priority, assigned_to, messages, last message tracking, and tags
2. WHEN conversation messages are stored, THE Database_Schema SHALL use a JSONB field to support flexible message structures with role, content, and timestamp
3. WHEN conversation status is tracked, THE Database_Schema SHALL support values: open, pending, resolved, closed
4. WHEN conversation priority is tracked, THE Database_Schema SHALL support values: low, normal, high, urgent
5. WHEN last message is tracked, THE Database_Schema SHALL include fields for last_message_at, last_message_from, and unread_count
6. WHEN conversations link to clients, THE Database_Schema SHALL include an optional foreign key client_id referencing the contacts table

### Requirement 9

**User Story:** As a database administrator, I want a tasks table for project management, so that the system can track to-do items and work assignments.

#### Acceptance Criteria

1. WHEN the tasks table is created, THE Database_Schema SHALL include columns for id, title, description, project reference, client reference, status, priority, assignment, dates, tags, and checklist
2. WHEN task status is tracked, THE Database_Schema SHALL support values: todo, in-progress, completed, cancelled
3. WHEN task priority is tracked, THE Database_Schema SHALL support values: low, medium, high, urgent
4. WHEN task dates are tracked, THE Database_Schema SHALL include fields for due_date and completed_date
5. WHEN task checklists are stored, THE Database_Schema SHALL use a JSONB field to support flexible checklist item structures
6. WHEN tasks link to projects, THE Database_Schema SHALL include an optional foreign key project_id referencing the projects table
7. WHEN tasks link to clients, THE Database_Schema SHALL include an optional foreign key client_id referencing the contacts table

### Requirement 10

**User Story:** As a database administrator, I want a goals table for business tracking, so that the system can monitor painting business performance and progress.

#### Acceptance Criteria

1. WHEN the goals table is created, THE Database_Schema SHALL include columns for id, title, description, goal_type, target_value, current_value, unit, dates, status, and progress_percentage
2. WHEN goal progress is calculated, THE Database_Schema SHALL include a generated column progress_percentage computed as LEAST(100, ROUND((current_value / target_value) * 100))
3. WHEN goal status is tracked, THE Database_Schema SHALL support values: active, completed, cancelled, overdue
4. WHEN goal dates are tracked, THE Database_Schema SHALL include fields for start_date and end_date
5. WHEN goal values are stored, THE Database_Schema SHALL include fields for target_value and current_value as decimal types

### Requirement 11

**User Story:** As a database administrator, I want a settings table for configuration, so that the system can store user preferences and system settings.

#### Acceptance Criteria

1. WHEN the settings table is created, THE Database_Schema SHALL include columns for id, key, value, description, created_at, and updated_at
2. WHEN setting values are stored, THE Database_Schema SHALL use a JSONB field to support flexible value structures
3. WHEN setting keys are stored, THE Database_Schema SHALL enforce a unique constraint on the key field
4. WHEN settings are queried, THE Database_Schema SHALL support efficient lookup by key through indexing

### Requirement 12

**User Story:** As a database administrator, I want proper indexes on all tables, so that voice-based queries can be executed efficiently.

#### Acceptance Criteria

1. WHEN foreign key columns exist, THE Database_Schema SHALL create indexes on client_id, project_id, and other foreign key columns
2. WHEN timestamp queries are common, THE Database_Schema SHALL create indexes on created_at and updated_at columns
3. WHEN status queries are common, THE Database_Schema SHALL create indexes on status columns
4. WHEN unique identifiers exist, THE Database_Schema SHALL create unique indexes on fields like invoice_number, proposal_number, and project_number
5. WHEN text search is needed, THE Database_Schema SHALL create indexes on commonly searched text fields like name, title, and email

### Requirement 13

**User Story:** As a database administrator, I want proper foreign key constraints with cascade rules, so that data integrity is maintained when records are deleted.

#### Acceptance Criteria

1. WHEN a contact is deleted, THE Database_Schema SHALL define cascade behavior for related projects, invoices, proposals, appointments, reviews, conversations, and tasks
2. WHEN a project is deleted, THE Database_Schema SHALL define cascade behavior for related invoices, appointments, reviews, and tasks
3. WHEN foreign keys are created, THE Database_Schema SHALL use ON DELETE SET NULL for optional relationships
4. WHEN foreign keys are created, THE Database_Schema SHALL use ON DELETE CASCADE for dependent relationships where appropriate
5. WHEN referential integrity is enforced, THE Database_Schema SHALL prevent orphaned records through proper constraint definitions
