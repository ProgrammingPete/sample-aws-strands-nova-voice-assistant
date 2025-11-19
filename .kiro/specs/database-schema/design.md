# Database Schema Design

## Overview

The Database Schema provides the foundational data structure for the Voice-Based Painting Business Agent system. Built on Supabase PostgreSQL, it implements a comprehensive relational model that supports all aspects of a painting business including client management, project tracking, financial operations, scheduling, customer feedback, marketing, and conversational AI context.

The schema is designed to support efficient voice-based queries while maintaining data integrity through proper constraints, indexes, and relationships. All tables use UUID primary keys for scalability and include automatic timestamp tracking for audit purposes.

## Architecture

### Database Platform
- **Platform**: Supabase PostgreSQL
- **Schema Namespace**: `api` (PostgreSQL schema containing all business tables)
- **Primary Key Strategy**: UUID v4 for all tables
- **Timestamp Strategy**: `timestamptz` (timestamp with timezone) for all temporal fields
- **JSON Storage**: JSONB for flexible structured data with efficient querying

### Design Principles

1. **Referential Integrity**: Foreign keys with appropriate cascade rules maintain data consistency
2. **Flexibility**: JSONB fields allow schema evolution without migrations for complex nested data
3. **Performance**: Strategic indexing on foreign keys, timestamps, status fields, and unique identifiers
4. **Audit Trail**: Automatic `created_at` and `updated_at` timestamps on all tables
5. **Voice Query Optimization**: Indexes and structure designed for efficient natural language query patterns
6. **Optional Relationships**: Most foreign keys use `ON DELETE SET NULL` to preserve historical data
7. **Computed Fields**: Generated columns for derived values (balance_due, progress_percentage)

### Entity Relationship Model

The schema implements a hub-and-spoke model with `contacts` as the central entity:

```
contacts (hub)
├── projects → invoices
├── projects → appointments
├── projects → reviews
├── projects → tasks
├── invoices
├── proposals
├── appointments
├── reviews
├── conversations
└── tasks
```

## Components and Interfaces

### Core Tables

#### 1. Contacts Table
Central entity for client and contact management.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `name` (TEXT, NOT NULL): Contact full name
- `email` (TEXT): Email address
- `phone` (TEXT): Phone number
- `company` (TEXT): Company name
- `address` (TEXT): Street address
- `city` (TEXT): City
- `state` (TEXT): State/province
- `zip_code` (TEXT): Postal code
- `notes` (TEXT): Additional notes
- `tags` (TEXT[]): Array of tags for categorization
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Indexes**:
- Primary key on `id`
- Index on `email` for lookup
- Index on `name` for search
- Index on `created_at` for temporal queries

**Design Rationale**: 
- All address fields are optional to accommodate partial information
- Tags array provides flexible categorization without additional tables
- Email and phone are optional as some contacts may only have one method

#### 2. Projects Table
Comprehensive project tracking with detailed specifications.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `project_number` (TEXT, UNIQUE): Human-readable project identifier
- `name` (TEXT, NOT NULL): Project name
- `client_id` (UUID, FK → contacts): Reference to client
- `client_name` (TEXT): Denormalized client name for quick access
- `status` (TEXT): Project status (draft, active, on-hold, completed, cancelled)
- `description` (TEXT): Project description
- `location` (TEXT): Project location
- `square_footage` (DECIMAL): Area to be painted
- `paint_type` (TEXT): Type of paint
- `surface_type` (TEXT): Surface being painted
- `paint_brand` (TEXT): Paint brand
- `paint_color` (TEXT): Paint color
- `number_of_coats` (INTEGER): Number of coats
- `primer_needed` (BOOLEAN): Whether primer is required
- `start_date` (DATE): Project start date
- `end_date` (DATE): Project end date
- `estimated_duration_days` (INTEGER): Estimated duration
- `actual_completion_date` (DATE): Actual completion date
- `estimated_cost` (DECIMAL): Estimated cost
- `actual_cost` (DECIMAL): Actual cost
- `budget` (DECIMAL): Project budget
- `assigned_team` (TEXT[]): Array of team member names
- `completion_percentage` (INTEGER, CHECK 0-100): Progress percentage
- `notes` (TEXT): Additional notes
- `tags` (TEXT[]): Project tags
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Indexes**:
- Primary key on `id`
- Unique index on `project_number`
- Index on `client_id` (foreign key)
- Index on `status` for filtering
- Index on `start_date` and `end_date` for scheduling queries
- Index on `created_at`

**Foreign Keys**:
- `client_id` REFERENCES `contacts(id)` ON DELETE SET NULL

**Design Rationale**:
- Paint specifications are denormalized into the projects table for simplicity
- `client_name` is denormalized to avoid joins in voice queries
- `completion_percentage` has a CHECK constraint to ensure valid range
- Status values are stored as text for flexibility (could be enum in future)
- Separate estimated vs actual fields for cost and completion tracking

#### 3. Invoices Table
Financial tracking with line items and automatic balance calculation.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `invoice_number` (TEXT, UNIQUE, NOT NULL): Human-readable invoice number
- `client_id` (UUID, FK → contacts): Reference to client
- `client_name` (TEXT): Denormalized client name
- `project_id` (UUID, FK → projects): Reference to project
- `project_name` (TEXT): Denormalized project name
- `issue_date` (DATE, NOT NULL): Invoice issue date
- `due_date` (DATE): Payment due date
- `subtotal` (DECIMAL, NOT NULL): Subtotal before tax/discount
- `tax_rate` (DECIMAL): Tax rate as decimal (e.g., 0.08 for 8%)
- `tax_amount` (DECIMAL): Calculated tax amount
- `discount_amount` (DECIMAL): Discount amount
- `total_amount` (DECIMAL, NOT NULL): Total invoice amount
- `amount_paid` (DECIMAL, DEFAULT 0): Amount paid so far
- `balance_due` (DECIMAL, GENERATED): Computed as `total_amount - amount_paid`
- `line_items` (JSONB): Array of line item objects
- `status` (TEXT, NOT NULL): Invoice status (draft, sent, viewed, partial, paid, overdue, cancelled)
- `payment_method` (TEXT): Payment method used
- `payment_date` (DATE): Date payment received
- `notes` (TEXT): Additional notes
- `terms` (TEXT): Payment terms
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Line Items JSONB Structure**:
```json
[
  {
    "description": "Interior wall painting",
    "quantity": 1,
    "unit_price": 1500.00,
    "total": 1500.00
  }
]
```

**Indexes**:
- Primary key on `id`
- Unique index on `invoice_number`
- Index on `client_id` (foreign key)
- Index on `project_id` (foreign key)
- Index on `status` for filtering
- Index on `issue_date` and `due_date`
- Index on `created_at`

**Foreign Keys**:
- `client_id` REFERENCES `contacts(id)` ON DELETE SET NULL
- `project_id` REFERENCES `projects(id)` ON DELETE SET NULL

**Design Rationale**:
- `balance_due` is a generated column to ensure consistency
- Line items use JSONB for flexibility in item structure
- Both client and project references are optional to support standalone invoices
- Status progression: draft → sent → viewed → partial/paid or overdue

#### 4. Proposals Table
Estimate and bid management with pricing sections.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `proposal_number` (TEXT, UNIQUE, NOT NULL): Human-readable proposal number
- `title` (TEXT, NOT NULL): Proposal title
- `client_id` (UUID, FK → contacts): Reference to client
- `client_name` (TEXT): Denormalized client name
- `description` (TEXT): Proposal description
- `scope_of_work` (TEXT): Detailed scope
- `subtotal` (DECIMAL, NOT NULL): Subtotal before tax/discount
- `tax_rate` (DECIMAL): Tax rate
- `tax_amount` (DECIMAL): Tax amount
- `discount_amount` (DECIMAL): Discount amount
- `total_amount` (DECIMAL, NOT NULL): Total proposal amount
- `sections` (JSONB): Pricing sections with line items
- `issue_date` (DATE, NOT NULL): Proposal issue date
- `valid_until` (DATE): Expiration date
- `accepted_date` (DATE): Date accepted by client
- `status` (TEXT, NOT NULL): Proposal status (draft, sent, viewed, accepted, rejected, expired)
- `terms` (TEXT): Terms and conditions
- `notes` (TEXT): Additional notes
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Sections JSONB Structure**:
```json
[
  {
    "section_name": "Interior Painting",
    "items": [
      {
        "description": "Living room walls",
        "quantity": 1,
        "unit_price": 800.00,
        "total": 800.00
      }
    ],
    "section_total": 800.00
  }
]
```

**Indexes**:
- Primary key on `id`
- Unique index on `proposal_number`
- Index on `client_id` (foreign key)
- Index on `status`
- Index on `issue_date` and `valid_until`
- Index on `created_at`

**Foreign Keys**:
- `client_id` REFERENCES `contacts(id)` ON DELETE SET NULL

**Design Rationale**:
- Sections provide hierarchical pricing structure
- Status tracks proposal lifecycle from draft to acceptance/rejection
- `valid_until` enables automatic expiration tracking
- Separate from invoices as proposals may not convert to projects

#### 5. Appointments Table
Scheduling for consultations and painting work.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `title` (TEXT, NOT NULL): Appointment title
- `client_id` (UUID, FK → contacts): Reference to client
- `client_name` (TEXT): Denormalized client name
- `project_id` (UUID, FK → projects): Reference to project
- `project_name` (TEXT): Denormalized project name
- `appointment_date` (DATE, NOT NULL): Appointment date
- `start_time` (TIME, NOT NULL): Start time
- `end_time` (TIME): End time
- `duration_minutes` (INTEGER): Duration in minutes
- `location` (TEXT): Appointment location
- `appointment_type` (TEXT): Type (consultation, estimate, painting, follow-up)
- `status` (TEXT, NOT NULL): Status (scheduled, confirmed, in-progress, completed, cancelled, no-show, rescheduled)
- `assigned_to` (TEXT): Team member assigned
- `reminder_sent` (BOOLEAN, DEFAULT FALSE): Whether reminder was sent
- `reminder_sent_at` (TIMESTAMPTZ): When reminder was sent
- `notes` (TEXT): Additional notes
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Indexes**:
- Primary key on `id`
- Index on `client_id` (foreign key)
- Index on `project_id` (foreign key)
- Index on `appointment_date` and `start_time`
- Index on `status`
- Index on `assigned_to`
- Index on `created_at`

**Foreign Keys**:
- `client_id` REFERENCES `contacts(id)` ON DELETE SET NULL
- `project_id` REFERENCES `projects(id)` ON DELETE SET NULL

**Design Rationale**:
- Separate date and time fields for flexible querying
- `duration_minutes` can be calculated from start/end or stored directly
- Reminder tracking supports automated notification systems
- Both client and project references optional for flexibility

#### 6. Reviews Table
Customer feedback and reputation management.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `client_id` (UUID, FK → contacts): Reference to client
- `client_name` (TEXT): Denormalized client name
- `project_id` (UUID, FK → projects): Reference to project
- `project_name` (TEXT): Denormalized project name
- `rating` (INTEGER, NOT NULL, CHECK 1-5): Star rating
- `title` (TEXT): Review title
- `review_text` (TEXT): Review content
- `platform` (TEXT): Platform (Google, Yelp, Facebook, etc.)
- `platform_url` (TEXT): URL to review
- `status` (TEXT, NOT NULL): Status (pending, approved, published, responded, flagged)
- `response_text` (TEXT): Business response
- `response_date` (DATE): Date of response
- `responded_by` (TEXT): Who responded
- `review_date` (DATE): Date review was posted
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Indexes**:
- Primary key on `id`
- Index on `client_id` (foreign key)
- Index on `project_id` (foreign key)
- Index on `rating`
- Index on `status`
- Index on `review_date`
- Index on `created_at`

**Foreign Keys**:
- `client_id` REFERENCES `contacts(id)` ON DELETE SET NULL
- `project_id` REFERENCES `projects(id)` ON DELETE SET NULL

**Design Rationale**:
- Rating constraint ensures valid 1-5 range
- Platform tracking supports multi-platform reputation management
- Response tracking enables workflow for addressing reviews
- Status workflow: pending → approved → published → responded

#### 7. Campaigns Table
Marketing campaign tracking and analytics.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `name` (TEXT, NOT NULL): Campaign name
- `campaign_type` (TEXT): Type (email, social, direct-mail, referral, etc.)
- `description` (TEXT): Campaign description
- `start_date` (DATE): Campaign start date
- `end_date` (DATE): Campaign end date
- `status` (TEXT, NOT NULL): Status (draft, scheduled, active, paused, completed, cancelled)
- `budget` (DECIMAL): Campaign budget
- `actual_cost` (DECIMAL): Actual cost incurred
- `revenue_generated` (DECIMAL): Revenue attributed to campaign
- `target_audience_count` (INTEGER): Size of target audience
- `sent_count` (INTEGER): Number sent/distributed
- `delivered_count` (INTEGER): Number delivered
- `opened_count` (INTEGER): Number opened (email)
- `clicked_count` (INTEGER): Number clicked
- `converted_count` (INTEGER): Number converted
- `open_rate` (DECIMAL): Open rate percentage
- `click_rate` (DECIMAL): Click rate percentage
- `conversion_rate` (DECIMAL): Conversion rate percentage
- `roi` (DECIMAL): Return on investment
- `content` (JSONB): Campaign content and assets
- `tags` (TEXT[]): Campaign tags
- `notes` (TEXT): Additional notes
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Content JSONB Structure**:
```json
{
  "subject": "Spring Painting Special",
  "body": "...",
  "images": ["url1", "url2"],
  "cta": "Schedule Free Estimate"
}
```

**Indexes**:
- Primary key on `id`
- Index on `campaign_type`
- Index on `status`
- Index on `start_date` and `end_date`
- Index on `created_at`

**Design Rationale**:
- Comprehensive metrics for campaign performance analysis
- JSONB content field supports various campaign types
- Rate fields can be computed or stored for performance
- ROI calculation: (revenue_generated - actual_cost) / actual_cost

#### 8. Conversations Table
Chat history and context for voice/text interactions.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `client_id` (UUID, FK → contacts): Reference to client
- `client_name` (TEXT): Denormalized client name
- `subject` (TEXT): Conversation subject
- `channel` (TEXT): Channel (voice, text, email, phone)
- `status` (TEXT, NOT NULL): Status (open, pending, resolved, closed)
- `priority` (TEXT): Priority (low, normal, high, urgent)
- `assigned_to` (TEXT): Team member assigned
- `messages` (JSONB, NOT NULL): Array of message objects
- `last_message_at` (TIMESTAMPTZ): Timestamp of last message
- `last_message_from` (TEXT): Who sent last message
- `unread_count` (INTEGER, DEFAULT 0): Number of unread messages
- `tags` (TEXT[]): Conversation tags
- `notes` (TEXT): Internal notes
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Messages JSONB Structure**:
```json
[
  {
    "role": "user",
    "content": "I need a quote for painting my house",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  {
    "role": "assistant",
    "content": "I'd be happy to help...",
    "timestamp": "2024-01-15T10:30:15Z"
  }
]
```

**Indexes**:
- Primary key on `id`
- Index on `client_id` (foreign key)
- Index on `status`
- Index on `priority`
- Index on `channel`
- Index on `last_message_at`
- Index on `created_at`

**Foreign Keys**:
- `client_id` REFERENCES `contacts(id)` ON DELETE SET NULL

**Design Rationale**:
- Messages stored as JSONB array for flexible structure
- Supports multi-channel conversations (voice, text, email)
- Last message tracking enables efficient "recent conversations" queries
- Unread count supports notification systems
- Critical for maintaining context in voice-based interactions

#### 9. Tasks Table
Project management and to-do tracking.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `title` (TEXT, NOT NULL): Task title
- `description` (TEXT): Task description
- `project_id` (UUID, FK → projects): Reference to project
- `project_name` (TEXT): Denormalized project name
- `client_id` (UUID, FK → contacts): Reference to client
- `client_name` (TEXT): Denormalized client name
- `status` (TEXT, NOT NULL): Status (todo, in-progress, completed, cancelled)
- `priority` (TEXT): Priority (low, medium, high, urgent)
- `assigned_to` (TEXT): Team member assigned
- `due_date` (DATE): Task due date
- `completed_date` (DATE): Date completed
- `tags` (TEXT[]): Task tags
- `checklist` (JSONB): Checklist items
- `notes` (TEXT): Additional notes
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Checklist JSONB Structure**:
```json
[
  {
    "item": "Purchase paint supplies",
    "completed": true
  },
  {
    "item": "Schedule crew",
    "completed": false
  }
]
```

**Indexes**:
- Primary key on `id`
- Index on `project_id` (foreign key)
- Index on `client_id` (foreign key)
- Index on `status`
- Index on `priority`
- Index on `assigned_to`
- Index on `due_date`
- Index on `created_at`

**Foreign Keys**:
- `project_id` REFERENCES `projects(id)` ON DELETE SET NULL
- `client_id` REFERENCES `contacts(id)` ON DELETE SET NULL

**Design Rationale**:
- Can be associated with project, client, or standalone
- Checklist JSONB provides sub-task tracking
- Priority and status enable task management workflows
- Due date tracking supports deadline management

#### 10. Goals Table
Business performance tracking and KPI monitoring.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `title` (TEXT, NOT NULL): Goal title
- `description` (TEXT): Goal description
- `goal_type` (TEXT): Type (revenue, projects, clients, satisfaction, etc.)
- `target_value` (DECIMAL, NOT NULL): Target value
- `current_value` (DECIMAL, DEFAULT 0): Current value
- `unit` (TEXT): Unit of measurement (dollars, count, percentage)
- `start_date` (DATE): Goal start date
- `end_date` (DATE): Goal end date
- `status` (TEXT, NOT NULL): Status (active, completed, cancelled, overdue)
- `progress_percentage` (INTEGER, GENERATED): Computed as LEAST(100, ROUND((current_value / target_value) * 100))
- `notes` (TEXT): Additional notes
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Indexes**:
- Primary key on `id`
- Index on `goal_type`
- Index on `status`
- Index on `start_date` and `end_date`
- Index on `created_at`

**Design Rationale**:
- `progress_percentage` is generated column for consistency
- Flexible goal types support various business metrics
- Unit field provides context for target/current values
- Status can be automatically updated based on dates and progress

#### 11. Settings Table
System configuration and user preferences.

**Columns**:
- `id` (UUID, PK): Unique identifier
- `key` (TEXT, UNIQUE, NOT NULL): Setting key
- `value` (JSONB, NOT NULL): Setting value
- `description` (TEXT): Setting description
- `created_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())
- `updated_at` (TIMESTAMPTZ, NOT NULL, DEFAULT NOW())

**Indexes**:
- Primary key on `id`
- Unique index on `key`

**Design Rationale**:
- Key-value store pattern for flexible configuration
- JSONB value supports any data type
- Unique constraint on key ensures single source of truth
- Can store user preferences, system config, feature flags, etc.

## Data Models

### Relationship Summary

```
contacts (1) ──< (N) projects
contacts (1) ──< (N) invoices
contacts (1) ──< (N) proposals
contacts (1) ──< (N) appointments
contacts (1) ──< (N) reviews
contacts (1) ──< (N) conversations
contacts (1) ──< (N) tasks

projects (1) ──< (N) invoices
projects (1) ──< (N) appointments
projects (1) ──< (N) reviews
projects (1) ──< (N) tasks
```

### Cascade Rules

**ON DELETE SET NULL** (preserve historical data):
- All foreign keys to `contacts`
- All foreign keys to `projects`

**Rationale**: Setting foreign keys to NULL preserves historical records (invoices, appointments, etc.) even if the client or project is deleted. This maintains data integrity for reporting and audit purposes.

### Generated Columns

1. **invoices.balance_due**
   - Formula: `total_amount - amount_paid`
   - Ensures consistency between amounts
   - Automatically updates when payments are recorded

2. **goals.progress_percentage**
   - Formula: `LEAST(100, ROUND((current_value / target_value) * 100))`
   - Caps at 100% to prevent overflow
   - Automatically updates when current_value changes

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After reviewing all testable criteria from the prework, I've identified the following consolidations to eliminate redundancy:

**Consolidations:**
1. **Foreign Key Constraints**: Requirements 2.7, 3.6, 3.7, 4.6, 5.6, 5.7, 6.6, 6.7, 9.6, 9.7, 8.6 all test foreign key existence and NULL allowance. These can be consolidated into a single comprehensive property about foreign key constraints.

2. **Status Value Validation**: Requirements 3.5, 4.5, 5.4, 6.4, 7.5, 8.3, 8.4, 9.2, 9.3, 10.3 all test valid status/priority values. These can be consolidated into properties grouped by table.

3. **Schema Structure Checks**: Requirements 1.1, 2.1-2.5, 3.1-3.2, 3.4, 4.1-4.4, 5.1-5.3, 5.5, 6.1, 6.3, 6.5, 7.1-7.4, 7.6, 8.1-8.2, 8.5, 9.1, 9.4-9.5, 10.1, 10.4-10.5, 11.1-11.2, 12.1-12.5 are all schema metadata checks. These can be consolidated into a single comprehensive schema validation property.

4. **Cascade Behavior**: Requirements 13.1 and 13.2 test similar cascade behavior and can be combined into a single property about cascade rules.

**Remaining Unique Properties:**
- UUID generation (1.2)
- Optional field support (1.3)
- Timestamp auto-generation (1.5)
- Completion percentage constraint (2.6)
- Balance due calculation (3.3)
- Rating constraint (6.2)
- Progress percentage calculation (10.2)
- Settings key uniqueness (11.3)
- Referential integrity enforcement (13.5)

### Correctness Properties

Property 1: Schema structure completeness
*For any* table in the database schema, all required columns as specified in the requirements SHALL exist with correct data types (TEXT, UUID, INTEGER, DECIMAL, DATE, TIME, TIMESTAMPTZ, BOOLEAN, TEXT[], JSONB)
**Validates: Requirements 1.1, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.4, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.5, 6.1, 6.3, 6.5, 7.1, 7.2, 7.3, 7.4, 7.6, 8.1, 8.2, 8.5, 9.1, 9.4, 9.5, 10.1, 10.4, 10.5, 11.1, 11.2**

Property 2: UUID auto-generation
*For any* record inserted into any table without an explicit id value, the database SHALL automatically generate a valid UUID v4 for the id field
**Validates: Requirements 1.2**

Property 3: Optional field NULL support
*For any* contact record, the fields email, phone, company, address, city, state, and zip_code SHALL accept NULL values without constraint violations
**Validates: Requirements 1.3**

Property 4: Timestamp auto-generation
*For any* record inserted into any table, the database SHALL automatically set created_at and updated_at to the current timestamp with timezone information
**Validates: Requirements 1.5**

Property 5: Completion percentage constraint
*For any* project record where completion_percentage is not NULL, the value SHALL be between 0 and 100 inclusive
**Validates: Requirements 2.6**

Property 6: Foreign key referential integrity
*For any* table with foreign key columns (client_id, project_id), the foreign key constraints SHALL reference the correct parent table (contacts, projects) and allow NULL values for optional relationships
**Validates: Requirements 2.7, 3.6, 3.7, 4.6, 5.6, 5.7, 6.6, 6.7, 8.6, 9.6, 9.7**

Property 7: Balance due calculation accuracy
*For any* invoice record, the balance_due generated column SHALL always equal total_amount minus amount_paid
**Validates: Requirements 3.3**

Property 8: Invoice status validation
*For any* invoice record, the status field SHALL only accept values from the set: draft, sent, viewed, partial, paid, overdue, cancelled
**Validates: Requirements 3.5**

Property 9: Proposal status validation
*For any* proposal record, the status field SHALL only accept values from the set: draft, sent, viewed, accepted, rejected, expired
**Validates: Requirements 4.5**

Property 10: Appointment status validation
*For any* appointment record, the status field SHALL only accept values from the set: scheduled, confirmed, in-progress, completed, cancelled, no-show, rescheduled
**Validates: Requirements 5.4**

Property 11: Review rating constraint
*For any* review record, the rating field SHALL be an integer between 1 and 5 inclusive
**Validates: Requirements 6.2**

Property 12: Review status validation
*For any* review record, the status field SHALL only accept values from the set: pending, approved, published, responded, flagged
**Validates: Requirements 6.4**

Property 13: Campaign status validation
*For any* campaign record, the status field SHALL only accept values from the set: draft, scheduled, active, paused, completed, cancelled
**Validates: Requirements 7.5**

Property 14: Conversation status validation
*For any* conversation record, the status field SHALL only accept values from the set: open, pending, resolved, closed
**Validates: Requirements 8.3**

Property 15: Conversation priority validation
*For any* conversation record, the priority field SHALL only accept values from the set: low, normal, high, urgent
**Validates: Requirements 8.4**

Property 16: Task status validation
*For any* task record, the status field SHALL only accept values from the set: todo, in-progress, completed, cancelled
**Validates: Requirements 9.2**

Property 17: Task priority validation
*For any* task record, the priority field SHALL only accept values from the set: low, medium, high, urgent
**Validates: Requirements 9.3**

Property 18: Goal progress calculation accuracy
*For any* goal record, the progress_percentage generated column SHALL equal LEAST(100, ROUND((current_value / target_value) * 100))
**Validates: Requirements 10.2**

Property 19: Goal status validation
*For any* goal record, the status field SHALL only accept values from the set: active, completed, cancelled, overdue
**Validates: Requirements 10.3**

Property 20: Settings key uniqueness
*For any* two distinct settings records, their key fields SHALL have different values
**Validates: Requirements 11.3**

Property 21: Index existence on foreign keys
*For any* foreign key column (client_id, project_id) in any table, an index SHALL exist on that column
**Validates: Requirements 12.1**

Property 22: Index existence on timestamps
*For any* table with created_at and updated_at columns, indexes SHALL exist on these columns
**Validates: Requirements 12.2**

Property 23: Index existence on status columns
*For any* table with a status column, an index SHALL exist on that column
**Validates: Requirements 12.3**

Property 24: Unique index existence on identifiers
*For any* table with unique identifier columns (invoice_number, proposal_number, project_number), a unique index SHALL exist on that column
**Validates: Requirements 12.4**

Property 25: Index existence on searchable text fields
*For any* table with commonly searched text fields (name, title, email), indexes SHALL exist on these columns
**Validates: Requirements 12.5**

Property 26: Cascade behavior on contact deletion
*For any* contact record that is deleted, all related records in projects, invoices, proposals, appointments, reviews, conversations, and tasks SHALL have their client_id set to NULL
**Validates: Requirements 13.1**

Property 27: Cascade behavior on project deletion
*For any* project record that is deleted, all related records in invoices, appointments, reviews, and tasks SHALL have their project_id set to NULL
**Validates: Requirements 13.2**

Property 28: Foreign key cascade rule definition
*For any* foreign key constraint in the schema, the ON DELETE action SHALL be either SET NULL for optional relationships or CASCADE for dependent relationships
**Validates: Requirements 13.3, 13.4**

Property 29: Referential integrity enforcement
*For any* attempt to insert or update a record with a foreign key value, if that value is not NULL and does not exist in the referenced table, the operation SHALL fail with a constraint violation
**Validates: Requirements 13.5**

## Error Handling

### Database-Level Error Handling

1. **Constraint Violations**
   - CHECK constraints on rating (1-5), completion_percentage (0-100)
   - UNIQUE constraints on invoice_number, proposal_number, project_number, settings.key
   - NOT NULL constraints on required fields
   - Foreign key constraints preventing invalid references

2. **Data Type Validation**
   - PostgreSQL enforces type safety (UUID, INTEGER, DECIMAL, DATE, TIME, TIMESTAMPTZ)
   - JSONB validation ensures valid JSON structure
   - Array type validation for TEXT[] fields

3. **Generated Column Errors**
   - Division by zero protection in progress_percentage (target_value = 0)
   - NULL handling in computed columns

### Application-Level Error Handling

1. **Connection Errors**
   - Database connection failures
   - Timeout handling
   - Connection pool exhaustion

2. **Query Errors**
   - Malformed SQL queries
   - Permission denied errors
   - Transaction rollback scenarios

3. **Data Validation**
   - Pre-insert validation of status values
   - Business logic validation (e.g., due_date before start_date)
   - JSONB structure validation before insertion

### Error Recovery Strategies

1. **Transaction Management**
   - Use transactions for multi-table operations
   - Rollback on constraint violations
   - Savepoints for partial rollback

2. **Retry Logic**
   - Retry on transient connection errors
   - Exponential backoff for connection retries
   - Maximum retry limits

3. **Graceful Degradation**
   - Return partial results on timeout
   - Cache frequently accessed data
   - Queue operations for later retry

## Testing Strategy

### Dual Testing Approach

The database schema will be validated using both unit tests and property-based tests to ensure comprehensive coverage:

- **Unit tests** verify specific examples, edge cases, and schema structure
- **Property-based tests** verify universal properties that should hold across all data
- Together they provide comprehensive coverage: unit tests catch concrete bugs, property tests verify general correctness

### Unit Testing

**Schema Structure Tests**:
- Verify all tables exist in the `api` schema
- Verify all required columns exist with correct data types
- Verify all indexes exist (foreign keys, timestamps, status, unique identifiers, text fields)
- Verify all foreign key constraints exist with correct references and cascade rules
- Verify all CHECK constraints exist (rating 1-5, completion_percentage 0-100)
- Verify all UNIQUE constraints exist (invoice_number, proposal_number, project_number, settings.key)
- Verify generated columns exist (balance_due, progress_percentage)

**JSONB Structure Tests**:
- Verify line_items JSONB accepts valid invoice line item structure
- Verify sections JSONB accepts valid proposal section structure
- Verify messages JSONB accepts valid conversation message structure
- Verify checklist JSONB accepts valid task checklist structure
- Verify content JSONB accepts valid campaign content structure

**Edge Cases**:
- Insert contact with all NULL optional fields
- Insert project with completion_percentage = 0 and 100
- Insert invoice with amount_paid = 0 and amount_paid = total_amount
- Insert goal with current_value = 0 and current_value > target_value
- Insert settings with various JSONB value types (string, number, object, array)

**Integration Tests**:
- Create contact and verify related records can be created
- Delete contact and verify related records have client_id set to NULL
- Delete project and verify related records have project_id set to NULL
- Verify foreign key constraints prevent invalid references

### Property-Based Testing

**Property-Based Testing Library**: We will use **Hypothesis** for Python-based property testing, as it integrates well with pytest and provides excellent support for database testing.

**Configuration**: Each property-based test will run a minimum of 100 iterations to ensure thorough coverage of the input space.

**Test Tagging**: Each property-based test will be tagged with a comment explicitly referencing the correctness property from the design document using this format: `# Feature: database-schema, Property {number}: {property_text}`

**Property Tests**:

1. **Property 2: UUID auto-generation**
   - Generate random contact data without id field
   - Insert into database
   - Verify id is a valid UUID v4
   - Tag: `# Feature: database-schema, Property 2: UUID auto-generation`

2. **Property 3: Optional field NULL support**
   - Generate random contact data with random subset of optional fields as NULL
   - Insert into database
   - Verify insertion succeeds
   - Tag: `# Feature: database-schema, Property 3: Optional field NULL support`

3. **Property 4: Timestamp auto-generation**
   - Generate random record for any table without created_at/updated_at
   - Insert into database
   - Verify created_at and updated_at are set to current timestamp with timezone
   - Tag: `# Feature: database-schema, Property 4: Timestamp auto-generation`

4. **Property 5: Completion percentage constraint**
   - Generate random project with completion_percentage outside 0-100 range
   - Attempt to insert into database
   - Verify insertion fails with CHECK constraint violation
   - Tag: `# Feature: database-schema, Property 5: Completion percentage constraint`

5. **Property 6: Foreign key referential integrity**
   - Generate random record with foreign key to existing parent
   - Insert into database
   - Verify insertion succeeds
   - Generate random record with foreign key to non-existent parent
   - Attempt to insert into database
   - Verify insertion fails with foreign key constraint violation
   - Tag: `# Feature: database-schema, Property 6: Foreign key referential integrity`

6. **Property 7: Balance due calculation accuracy**
   - Generate random invoice with random total_amount and amount_paid
   - Insert into database
   - Query balance_due
   - Verify balance_due equals total_amount - amount_paid
   - Tag: `# Feature: database-schema, Property 7: Balance due calculation accuracy`

7. **Property 8-19: Status/Priority validation**
   - For each table with status or priority field:
     - Generate random record with valid status/priority
     - Insert into database
     - Verify insertion succeeds
     - Generate random record with invalid status/priority
     - Attempt to insert into database
     - Verify insertion fails or is rejected by application logic
   - Tag: `# Feature: database-schema, Property {8-19}: {Table} status/priority validation`

8. **Property 11: Review rating constraint**
   - Generate random review with rating outside 1-5 range
   - Attempt to insert into database
   - Verify insertion fails with CHECK constraint violation
   - Tag: `# Feature: database-schema, Property 11: Review rating constraint`

9. **Property 18: Goal progress calculation accuracy**
   - Generate random goal with random target_value and current_value
   - Insert into database
   - Query progress_percentage
   - Verify progress_percentage equals LEAST(100, ROUND((current_value / target_value) * 100))
   - Tag: `# Feature: database-schema, Property 18: Goal progress calculation accuracy`

10. **Property 20: Settings key uniqueness**
    - Generate random setting with unique key
    - Insert into database
    - Attempt to insert another setting with same key
    - Verify second insertion fails with UNIQUE constraint violation
    - Tag: `# Feature: database-schema, Property 20: Settings key uniqueness`

11. **Property 26-27: Cascade behavior**
    - Generate random contact with related records
    - Delete contact
    - Verify all related records have client_id set to NULL
    - Generate random project with related records
    - Delete project
    - Verify all related records have project_id set to NULL
    - Tag: `# Feature: database-schema, Property {26-27}: Cascade behavior on {entity} deletion`

12. **Property 29: Referential integrity enforcement**
    - Generate random record with non-NULL foreign key to non-existent parent
    - Attempt to insert into database
    - Verify insertion fails with foreign key constraint violation
    - Tag: `# Feature: database-schema, Property 29: Referential integrity enforcement`

### Test Data Generation

**Generators for Property-Based Tests**:
- UUID generator (valid v4 UUIDs)
- Text generator (names, emails, phone numbers, addresses)
- Numeric generator (integers, decimals with constraints)
- Date/time generator (dates, times, timestamps with timezone)
- Array generator (tags, assigned_team)
- JSONB generator (line_items, sections, messages, checklist, content)
- Status/priority generator (valid and invalid values)
- Foreign key generator (existing and non-existent references)

**Test Database**:
- Use separate test database instance
- Reset database state between test runs
- Use transactions for test isolation
- Seed with minimal required data for foreign key tests

### Performance Testing

**Query Performance**:
- Measure query execution time for common voice queries
- Verify indexes improve query performance
- Test with realistic data volumes (1000s of contacts, projects, invoices)

**Index Effectiveness**:
- Verify indexes are used in query plans (EXPLAIN ANALYZE)
- Measure query performance with and without indexes
- Identify missing indexes through slow query analysis

**Scalability Testing**:
- Test with increasing data volumes
- Verify performance remains acceptable
- Identify bottlenecks and optimization opportunities

## Implementation Notes

### Migration Strategy

1. **Initial Schema Creation**
   - Create all tables in correct order (contacts first, then dependent tables)
   - Add all constraints (CHECK, UNIQUE, NOT NULL)
   - Create all indexes
   - Add all foreign keys with cascade rules

2. **Schema Evolution**
   - Use Supabase migrations for schema changes
   - Version control all migration scripts
   - Test migrations on staging before production
   - Support rollback for failed migrations

3. **Data Migration**
   - Plan for data migration if schema changes affect existing data
   - Use transactions for data migration
   - Validate data after migration
   - Maintain backup before migration

### Supabase-Specific Considerations

1. **Row Level Security (RLS)**
   - Consider RLS policies for multi-tenant scenarios
   - Define policies for read/write access
   - Test policies thoroughly

2. **Realtime Subscriptions**
   - Enable realtime for tables that need live updates
   - Consider performance impact of realtime
   - Use filters to reduce subscription load

3. **Storage Integration**
   - Consider using Supabase Storage for file attachments
   - Link storage objects to database records
   - Implement cleanup for orphaned files

4. **Functions and Triggers**
   - Consider triggers for automatic updated_at updates
   - Consider functions for complex business logic
   - Keep triggers simple to avoid performance issues

### Voice Query Optimization

1. **Denormalization**
   - client_name and project_name denormalized in related tables
   - Reduces joins for common voice queries
   - Trade-off: data consistency vs query performance

2. **Indexing Strategy**
   - Indexes on all foreign keys for join performance
   - Indexes on status fields for filtering
   - Indexes on date fields for temporal queries
   - Indexes on text fields for search

3. **Query Patterns**
   - Optimize for "show me recent X" queries
   - Optimize for "find X by name/status" queries
   - Optimize for "what's the status of X" queries
   - Consider materialized views for complex aggregations

### Security Considerations

1. **SQL Injection Prevention**
   - Use parameterized queries exclusively
   - Never concatenate user input into SQL
   - Validate and sanitize all inputs

2. **Access Control**
   - Implement proper authentication
   - Use RLS for row-level access control
   - Audit access to sensitive data

3. **Data Privacy**
   - Consider encryption for sensitive fields
   - Implement data retention policies
   - Support GDPR/privacy compliance (data export, deletion)

4. **Audit Trail**
   - created_at and updated_at provide basic audit trail
   - Consider additional audit table for critical operations
   - Log all schema changes

## Appendix

### SQL Schema Definition

The complete SQL schema will be implemented in Supabase using the following structure:

```sql
-- Create schema
CREATE SCHEMA IF NOT EXISTS api;

-- Set search path
SET search_path TO api, public;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tables will be created in dependency order:
-- 1. contacts (no dependencies)
-- 2. projects (depends on contacts)
-- 3. invoices (depends on contacts, projects)
-- 4. proposals (depends on contacts)
-- 5. appointments (depends on contacts, projects)
-- 6. reviews (depends on contacts, projects)
-- 7. campaigns (no dependencies)
-- 8. conversations (depends on contacts)
-- 9. tasks (depends on contacts, projects)
-- 10. goals (no dependencies)
-- 11. settings (no dependencies)
```

### Example Queries

**Common Voice Query Patterns**:

1. "Show me recent projects"
```sql
SELECT * FROM api.projects 
ORDER BY created_at DESC 
LIMIT 10;
```

2. "Find invoices for client John Doe"
```sql
SELECT * FROM api.invoices 
WHERE client_name ILIKE '%John Doe%' 
ORDER BY issue_date DESC;
```

3. "What's the status of project PRJ-001?"
```sql
SELECT name, status, completion_percentage 
FROM api.projects 
WHERE project_number = 'PRJ-001';
```

4. "Show me overdue invoices"
```sql
SELECT * FROM api.invoices 
WHERE status = 'overdue' 
ORDER BY due_date;
```

5. "Find all appointments for next week"
```sql
SELECT * FROM api.appointments 
WHERE appointment_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
ORDER BY appointment_date, start_time;
```

### Glossary Reference

All terms defined in the requirements glossary apply to this design document. Key terms:
- **Database_Schema**: Complete structure implemented in Supabase PostgreSQL
- **API_Schema**: PostgreSQL schema namespace `api` containing all tables
- **Foreign_Key**: Implemented with appropriate cascade rules (SET NULL or CASCADE)
- **JSONB_Field**: Used for flexible structured data (line_items, sections, messages, etc.)
- **Generated_Column**: Computed columns (balance_due, progress_percentage)
- **Cascade_Delete**: Implemented as ON DELETE SET NULL for optional relationships
