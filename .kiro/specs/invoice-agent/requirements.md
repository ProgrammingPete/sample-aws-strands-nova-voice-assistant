# Requirements Document

## Introduction

The Invoice Agent is a specialized agent within the Voice-Based Painting Business Agent that manages invoice generation, payment tracking, and billing operations for completed painting projects. The agent enables painting contractors to create invoices, track payments, manage line items, calculate totals with tax and discounts, and monitor invoice status through voice and text commands. The agent integrates with the Supabase database to store invoice data and maintains relationships with clients and projects.

## Glossary

- **Invoices_Agent**: Specialized agent that manages invoice generation, payment tracking, and billing operations for painting projects
- **Invoice**: A billing document containing client information, line items, amounts, and payment details
- **Line_Item**: An individual charge on an invoice with description, quantity, rate, and amount
- **Invoice_Number**: A unique identifier for each invoice
- **Invoice_Status**: The current state of an invoice (draft, sent, viewed, partial, paid, overdue, cancelled)
- **Payment_Tracking**: Monitoring of amounts paid and balance due on invoices
- **Tax_Calculation**: Computing tax amounts based on subtotal and tax rate
- **Balance_Due**: The remaining amount owed, calculated as total_amount minus amount_paid
- **Payment_Terms**: Conditions for payment including due date and payment methods
- **Invoice_Generation**: Creating a new invoice from client, project, and line item information

## Requirements

### Requirement 1

**User Story:** As a painting contractor, I want to manage invoices and billing through voice commands, so that I can handle payment tracking for completed painting projects.

#### Acceptance Criteria

1. WHEN a user asks about invoices, THE Invoices_Agent SHALL retrieve invoice details including invoice number, client, project, amounts, payment status, and due dates
2. WHEN a user requests to create invoices, THE Invoices_Agent SHALL generate invoices with client information, project reference, line items, and payment terms
3. WHEN invoice calculations are needed, THE Invoices_Agent SHALL compute subtotal, tax amounts, discounts, total amount, amount paid, and balance due
4. WHEN payment tracking is requested, THE Invoices_Agent SHALL update amount paid, paid date, and automatically calculate balance due
5. WHEN invoice status updates are needed, THE Invoices_Agent SHALL update status to draft, sent, viewed, partial, paid, overdue, or cancelled

### Requirement 2

**User Story:** As a painting contractor, I want to create invoices with multiple line items, so that I can bill for different services and materials on a single invoice.

#### Acceptance Criteria

1. WHEN creating an invoice, THE Invoices_Agent SHALL accept multiple line items with description, quantity, rate, and amount
2. WHEN line items are added, THE Invoices_Agent SHALL store them in a JSONB array field for flexible structure
3. WHEN line item amounts are calculated, THE Invoices_Agent SHALL compute amount as quantity multiplied by rate
4. WHEN the subtotal is calculated, THE Invoices_Agent SHALL sum all line item amounts
5. WHEN line items are retrieved, THE Invoices_Agent SHALL return them in the order they were added

### Requirement 3

**User Story:** As a painting contractor, I want invoices to automatically calculate totals with tax and discounts, so that I don't have to do manual calculations.

#### Acceptance Criteria

1. WHEN a subtotal is calculated, THE Invoices_Agent SHALL sum all line item amounts
2. WHEN tax is calculated, THE Invoices_Agent SHALL multiply subtotal by tax_rate to get tax_amount
3. WHEN discounts are applied, THE Invoices_Agent SHALL subtract discount_amount from the subtotal
4. WHEN the total is calculated, THE Invoices_Agent SHALL compute subtotal plus tax_amount minus discount_amount
5. WHEN amounts are displayed, THE Invoices_Agent SHALL format currency values with two decimal places

### Requirement 4

**User Story:** As a painting contractor, I want to track payments on invoices, so that I can monitor which invoices are paid and which have outstanding balances.

#### Acceptance Criteria

1. WHEN a payment is recorded, THE Invoices_Agent SHALL update the amount_paid field
2. WHEN a payment date is recorded, THE Invoices_Agent SHALL update the paid_date field
3. WHEN balance is calculated, THE Invoices_Agent SHALL compute balance_due as total_amount minus amount_paid
4. WHEN an invoice is fully paid, THE Invoices_Agent SHALL automatically update status to paid
5. WHEN an invoice is partially paid, THE Invoices_Agent SHALL update status to partial and show remaining balance

### Requirement 5

**User Story:** As a painting contractor, I want to link invoices to projects and clients, so that I can track billing for specific painting jobs.

#### Acceptance Criteria

1. WHEN creating an invoice, THE Invoices_Agent SHALL accept a project_id to link the invoice to a painting project
2. WHEN creating an invoice, THE Invoices_Agent SHALL accept a client_id to link the invoice to a client
3. WHEN a project is linked, THE Invoices_Agent SHALL retrieve and display project information with the invoice
4. WHEN a client is linked, THE Invoices_Agent SHALL auto-populate client_name and client_email from the contacts table
5. WHEN retrieving project information, THE Invoices_Agent SHALL show all invoices associated with that project

### Requirement 6

**User Story:** As a painting contractor, I want to manage invoice status, so that I can track the lifecycle of each invoice from draft to paid.

#### Acceptance Criteria

1. WHEN an invoice is created, THE Invoices_Agent SHALL set the initial status to draft
2. WHEN an invoice is sent to a client, THE Invoices_Agent SHALL update status to sent
3. WHEN a client views an invoice, THE Invoices_Agent SHALL update status to viewed
4. WHEN an invoice becomes overdue, THE Invoices_Agent SHALL update status to overdue based on due_date
5. WHEN an invoice is cancelled, THE Invoices_Agent SHALL update status to cancelled and prevent further modifications

### Requirement 7

**User Story:** As a painting contractor, I want to search and filter invoices, so that I can quickly find specific invoices or groups of invoices.

#### Acceptance Criteria

1. WHEN searching invoices, THE Invoices_Agent SHALL support queries by invoice_number, client_name, or project
2. WHEN filtering invoices, THE Invoices_Agent SHALL support filtering by status (draft, sent, paid, overdue, etc.)
3. WHEN filtering by date, THE Invoices_Agent SHALL support filtering by issue_date, due_date, or paid_date ranges
4. WHEN filtering by amount, THE Invoices_Agent SHALL support filtering by total_amount or balance_due ranges
5. WHEN multiple filters are applied, THE Invoices_Agent SHALL combine them with AND logic

### Requirement 8

**User Story:** As a painting contractor, I want to generate invoice numbers automatically, so that each invoice has a unique identifier.

#### Acceptance Criteria

1. WHEN an invoice is created, THE Invoices_Agent SHALL generate a unique invoice_number if not provided
2. WHEN invoice numbers are generated, THE Invoices_Agent SHALL follow a consistent format (e.g., INV-YYYY-NNNN)
3. WHEN checking for duplicates, THE Invoices_Agent SHALL ensure invoice_number is unique across all invoices
4. WHEN a custom invoice number is provided, THE Invoices_Agent SHALL validate it doesn't already exist
5. WHEN invoice numbers are displayed, THE Invoices_Agent SHALL show them in a user-friendly format

### Requirement 9

**User Story:** As a painting contractor, I want to add notes and payment terms to invoices, so that I can communicate important information to clients.

#### Acceptance Criteria

1. WHEN creating an invoice, THE Invoices_Agent SHALL accept optional notes field for additional information
2. WHEN creating an invoice, THE Invoices_Agent SHALL accept optional terms field for payment terms and conditions
3. WHEN creating an invoice, THE Invoices_Agent SHALL accept optional payment_method field to specify how payment should be made
4. WHEN retrieving an invoice, THE Invoices_Agent SHALL include notes, terms, and payment_method in the response
5. WHEN updating an invoice, THE Invoices_Agent SHALL allow modification of notes, terms, and payment_method

### Requirement 10

**User Story:** As a painting contractor, I want to set due dates for invoices, so that I can track when payments are expected.

#### Acceptance Criteria

1. WHEN creating an invoice, THE Invoices_Agent SHALL accept a due_date field
2. WHEN no due date is provided, THE Invoices_Agent SHALL calculate a default due_date based on payment terms (e.g., 30 days from issue_date)
3. WHEN checking for overdue invoices, THE Invoices_Agent SHALL compare due_date with the current date
4. WHEN an invoice becomes overdue, THE Invoices_Agent SHALL automatically update status to overdue
5. WHEN retrieving overdue invoices, THE Invoices_Agent SHALL calculate and display days overdue

### Requirement 11

**User Story:** As a painting contractor, I want to update existing invoices, so that I can correct errors or add additional charges.

#### Acceptance Criteria

1. WHEN updating an invoice, THE Invoices_Agent SHALL allow modification of line items, amounts, dates, and status
2. WHEN an invoice status is paid, THE Invoices_Agent SHALL prevent modifications to line items and amounts
3. WHEN an invoice status is cancelled, THE Invoices_Agent SHALL prevent all modifications except notes
4. WHEN line items are modified, THE Invoices_Agent SHALL recalculate subtotal, tax, and total amounts
5. WHEN critical fields are updated, THE Invoices_Agent SHALL update the updated_at timestamp

### Requirement 12

**User Story:** As a painting contractor, I want to delete draft invoices, so that I can remove invoices that were created by mistake.

#### Acceptance Criteria

1. WHEN deleting an invoice, THE Invoices_Agent SHALL only allow deletion of invoices with status draft
2. WHEN an invoice has status sent, viewed, partial, or paid, THE Invoices_Agent SHALL prevent deletion and suggest cancellation instead
3. WHEN an invoice is deleted, THE Invoices_Agent SHALL remove it from the database
4. WHEN deletion is prevented, THE Invoices_Agent SHALL provide a clear error message explaining why
5. WHEN an invoice is cancelled instead of deleted, THE Invoices_Agent SHALL update status to cancelled and retain the record

### Requirement 13

**User Story:** As a painting contractor, I want to see invoice summaries and totals, so that I can understand my billing and revenue at a glance.

#### Acceptance Criteria

1. WHEN requesting invoice summaries, THE Invoices_Agent SHALL calculate total invoiced amount across all invoices
2. WHEN calculating revenue, THE Invoices_Agent SHALL sum amount_paid across all invoices
3. WHEN calculating outstanding balance, THE Invoices_Agent SHALL sum balance_due across all unpaid and partially paid invoices
4. WHEN filtering by date range, THE Invoices_Agent SHALL calculate summaries for invoices within that range
5. WHEN grouping by status, THE Invoices_Agent SHALL provide counts and totals for each status category

### Requirement 14

**User Story:** As a system developer, I want the Invoice Agent to handle errors gracefully, so that users receive helpful feedback when operations fail.

#### Acceptance Criteria

1. WHEN an invoice operation fails, THE Invoices_Agent SHALL provide clear error messages explaining what went wrong
2. WHEN required fields are missing, THE Invoices_Agent SHALL specify which fields are required
3. WHEN validation fails, THE Invoices_Agent SHALL explain the validation rules and suggest corrections
4. WHEN database operations fail, THE Invoices_Agent SHALL log the error and provide a user-friendly message
5. WHEN calculations produce invalid results, THE Invoices_Agent SHALL detect and report the issue

### Requirement 15

**User Story:** As a system developer, I want the Invoice Agent to integrate with the conversation context system, so that invoice discussions maintain context across sessions.

#### Acceptance Criteria

1. WHEN discussing invoices, THE Invoices_Agent SHALL store conversation messages in the conversations table
2. WHEN a user references "the invoice" or "that invoice", THE Invoices_Agent SHALL use conversation context to identify which invoice
3. WHEN switching between voice and text, THE Invoices_Agent SHALL maintain context about which invoices are being discussed
4. WHEN multiple invoices are discussed, THE Invoices_Agent SHALL track context for each invoice separately
5. WHEN conversation history is retrieved, THE Invoices_Agent SHALL include invoice-related messages for context
