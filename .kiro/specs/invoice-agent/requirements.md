# Requirements Document

## Introduction

The Invoice Agent is a specialized agent within the Voice-Based Painting Business Agent that manages basic invoice CRUD (Create, Read, Update, Delete) operations for painting business billing. The agent enables painting contractors to create invoices, retrieve invoice information, update invoice details and status, and delete invoices through voice and text commands. The agent integrates with the Supabase database to store invoice data in the `api.invoices` table.

**Current Implementation Status**: The Invoice Agent is implemented with basic CRUD operations. Advanced features like line items, automatic calculations, and payment tracking are defined in the database schema but not yet fully implemented in the agent logic.

## Glossary

- **Invoices_Agent**: Specialized agent that performs CRUD operations on the invoices table in Supabase
- **Invoice**: A billing document containing client information, amounts, and payment details
- **Invoice_Number**: A unique identifier for each invoice (e.g., 'INV-001')
- **Invoice_Status**: The current state of an invoice (draft, sent, viewed, partial, paid, overdue, cancelled)
- **CRUD_Operations**: Create, Read, Update, and Delete operations on invoice records
- **Balance_Due**: The remaining amount owed on an invoice
- **Total_Amount**: The total billing amount for an invoice
- **Due_Date**: The date by which payment is expected

## Requirements

### Requirement 1

**User Story:** As a painting contractor, I want to list all invoices through voice commands, so that I can see all billing records in my system.

#### Acceptance Criteria

1. WHEN a user asks to list all invoices, THE Invoices_Agent SHALL retrieve all invoice records from the database
2. WHEN invoices are retrieved, THE Invoices_Agent SHALL return invoice details including invoice_number, client_name, total_amount, balance_due, and status
3. WHEN no invoices exist, THE Invoices_Agent SHALL return an appropriate message indicating no invoices found
4. WHEN database errors occur, THE Invoices_Agent SHALL return a clear error message
5. WHEN displaying invoices, THE Invoices_Agent SHALL format responses to be under 800 characters for voice optimization

### Requirement 2

**User Story:** As a painting contractor, I want to retrieve specific invoice details by invoice number, so that I can quickly access information about a particular invoice.

#### Acceptance Criteria

1. WHEN a user asks about a specific invoice number, THE Invoices_Agent SHALL query the database using the invoice_number field
2. WHEN an invoice is found, THE Invoices_Agent SHALL return details including client_name, total_amount, balance_due, and status
3. WHEN an invoice is not found, THE Invoices_Agent SHALL return a message indicating the invoice number was not found
4. WHEN database errors occur, THE Invoices_Agent SHALL return a clear error message
5. WHEN displaying invoice details, THE Invoices_Agent SHALL format the response for voice optimization

### Requirement 3

**User Story:** As a painting contractor, I want to retrieve all invoices for a specific client, so that I can see billing history for that client.

#### Acceptance Criteria

1. WHEN a user asks for invoices by client name, THE Invoices_Agent SHALL query the database filtering by client_name
2. WHEN invoices are found, THE Invoices_Agent SHALL return all matching invoice records
3. WHEN no invoices are found for the client, THE Invoices_Agent SHALL return an appropriate message
4. WHEN database errors occur, THE Invoices_Agent SHALL return a clear error message
5. WHEN displaying client invoices, THE Invoices_Agent SHALL include invoice_number, total_amount, balance_due, and status for each invoice

### Requirement 4

**User Story:** As a painting contractor, I want to create new invoices through voice commands, so that I can generate billing documents for completed work.

#### Acceptance Criteria

1. WHEN creating an invoice, THE Invoices_Agent SHALL accept client_name, client_email, and total_amount as required parameters
2. WHEN creating an invoice, THE Invoices_Agent SHALL accept optional invoice_number and due_date parameters
3. WHEN no due_date is provided, THE Invoices_Agent SHALL automatically set due_date to 30 days from the current date
4. WHEN an invoice is created, THE Invoices_Agent SHALL set the initial status to 'draft'
5. WHEN an invoice is successfully created, THE Invoices_Agent SHALL return confirmation with the invoice_number and amount

### Requirement 5

**User Story:** As a painting contractor, I want to update invoice status, so that I can track the lifecycle of invoices from draft to paid.

#### Acceptance Criteria

1. WHEN updating invoice status, THE Invoices_Agent SHALL accept invoice_number and new_status as parameters
2. WHEN validating status, THE Invoices_Agent SHALL only accept valid status values: draft, sent, viewed, partial, paid, overdue, cancelled
3. WHEN an invalid status is provided, THE Invoices_Agent SHALL return an error message listing valid status options
4. WHEN an invoice is found and updated, THE Invoices_Agent SHALL return confirmation of the status change
5. WHEN an invoice is not found, THE Invoices_Agent SHALL return a message indicating the invoice number was not found

### Requirement 6

**User Story:** As a painting contractor, I want to update invoice fields, so that I can correct errors or modify invoice information.

#### Acceptance Criteria

1. WHEN updating an invoice, THE Invoices_Agent SHALL accept invoice_number and any valid field parameters
2. WHEN updating fields, THE Invoices_Agent SHALL support: client_name, client_email, total_amount, balance_due, status, notes, due_date
3. WHEN no valid fields are provided, THE Invoices_Agent SHALL return a message indicating no valid fields to update
4. WHEN an invoice is successfully updated, THE Invoices_Agent SHALL return confirmation
5. WHEN an invoice is not found, THE Invoices_Agent SHALL return a message indicating the invoice number was not found

### Requirement 7

**User Story:** As a painting contractor, I want to delete invoices, so that I can remove incorrect or test invoice records.

#### Acceptance Criteria

1. WHEN deleting an invoice, THE Invoices_Agent SHALL accept invoice_number as a parameter
2. WHEN an invoice is found, THE Invoices_Agent SHALL delete the record from the database
3. WHEN an invoice is successfully deleted, THE Invoices_Agent SHALL return confirmation
4. WHEN an invoice is not found, THE Invoices_Agent SHALL return a message indicating the invoice number was not found
5. WHEN database errors occur, THE Invoices_Agent SHALL return a clear error message

### Requirement 8

**User Story:** As a system developer, I want the Invoice Agent to handle errors gracefully, so that users receive helpful feedback when operations fail.

#### Acceptance Criteria

1. WHEN database connection fails, THE Invoices_Agent SHALL return an error message indicating connection issues
2. WHEN required parameters are missing, THE Invoices_Agent SHALL return an error message specifying what is required
3. WHEN validation fails, THE Invoices_Agent SHALL return an error message explaining the validation rules
4. WHEN exceptions occur, THE Invoices_Agent SHALL log the error details for debugging
5. WHEN errors are returned to users, THE Invoices_Agent SHALL provide user-friendly messages without exposing technical details

### Requirement 9

**User Story:** As a system developer, I want the Invoice Agent to use voice-optimized responses, so that voice interactions are natural and concise.

#### Acceptance Criteria

1. WHEN generating responses, THE Invoices_Agent SHALL limit response length to under 800 characters
2. WHEN displaying invoice details, THE Invoices_Agent SHALL include only essential fields: invoice_number, client_name, total_amount, balance_due, status
3. WHEN listing multiple invoices, THE Invoices_Agent SHALL format responses for easy voice comprehension
4. WHEN errors occur, THE Invoices_Agent SHALL provide concise error messages suitable for voice output
5. WHEN operations succeed, THE Invoices_Agent SHALL provide brief confirmation messages

### Requirement 10

**User Story:** As a system developer, I want the Invoice Agent to integrate with Supabase using the api schema, so that invoice data is stored in the correct database location.

#### Acceptance Criteria

1. WHEN connecting to Supabase, THE Invoices_Agent SHALL use the api schema for all table operations
2. WHEN performing CRUD operations, THE Invoices_Agent SHALL target the api.invoices table
3. WHEN Supabase credentials are missing, THE Invoices_Agent SHALL raise an error indicating SUPABASE_URL and SUPABASE_ANON_KEY must be set
4. WHEN database timeouts occur, THE Invoices_Agent SHALL use configured timeout values (10 seconds for postgrest and storage)
5. WHEN operations complete, THE Invoices_Agent SHALL return Supabase response data to the caller

### Requirement 11

**User Story:** As a painting contractor, I want invoices to automatically calculate totals with tax and discounts, so that I don't have to do manual calculations.

#### Acceptance Criteria

1. WHEN creating or updating an invoice, THE Invoices_Agent SHALL accept subtotal, tax_rate, and discount_amount parameters
2. WHEN tax is calculated, THE Invoices_Agent SHALL multiply subtotal by tax_rate to compute tax_amount
3. WHEN discounts are applied, THE Invoices_Agent SHALL subtract discount_amount from the subtotal
4. WHEN the total is calculated, THE Invoices_Agent SHALL compute subtotal plus tax_amount minus discount_amount as total_amount
5. WHEN amounts are displayed, THE Invoices_Agent SHALL format currency values with two decimal places

### Requirement 12

**User Story:** As a painting contractor, I want to track payments on invoices, so that I can monitor which invoices are paid and which have outstanding balances.

#### Acceptance Criteria

1. WHEN recording a payment, THE Invoices_Agent SHALL accept amount_paid and paid_date parameters
2. WHEN amount_paid is updated, THE Invoices_Agent SHALL automatically recalculate balance_due as total_amount minus amount_paid
3. WHEN an invoice is fully paid (balance_due = 0), THE Invoices_Agent SHALL automatically update status to 'paid'
4. WHEN an invoice is partially paid (balance_due > 0), THE Invoices_Agent SHALL update status to 'partial'
5. WHEN retrieving invoice details, THE Invoices_Agent SHALL include amount_paid, paid_date, and balance_due in the response

### Requirement 13

**User Story:** As a painting contractor, I want to link invoices to projects and clients, so that I can track billing for specific painting jobs.

#### Acceptance Criteria

1. WHEN creating an invoice, THE Invoices_Agent SHALL accept optional project_id to link the invoice to a painting project
2. WHEN creating an invoice, THE Invoices_Agent SHALL accept optional client_id to link the invoice to a client contact
3. WHEN a client_id is provided, THE Invoices_Agent SHALL retrieve client_name and client_email from the contacts table
4. WHEN a project_id is provided, THE Invoices_Agent SHALL validate the project exists and retrieve project details
5. WHEN retrieving invoices, THE Invoices_Agent SHALL include related project and client information

### Requirement 14

**User Story:** As a painting contractor, I want invoice numbers to be generated automatically, so that each invoice has a unique identifier without manual entry.

#### Acceptance Criteria

1. WHEN creating an invoice without an invoice_number, THE Invoices_Agent SHALL automatically generate a unique invoice number
2. WHEN generating invoice numbers, THE Invoices_Agent SHALL follow a consistent format (e.g., INV-YYYY-NNNN where YYYY is year and NNNN is sequential)
3. WHEN checking for uniqueness, THE Invoices_Agent SHALL query existing invoices to ensure no duplicate invoice_number
4. WHEN a custom invoice_number is provided, THE Invoices_Agent SHALL validate it doesn't already exist before creating the invoice
5. WHEN invoice number generation fails, THE Invoices_Agent SHALL return a clear error message

### Requirement 15

**User Story:** As a painting contractor, I want to search and filter invoices by various criteria, so that I can quickly find specific invoices or groups of invoices.

#### Acceptance Criteria

1. WHEN searching invoices, THE Invoices_Agent SHALL support filtering by status (draft, sent, viewed, partial, paid, overdue, cancelled)
2. WHEN searching by date range, THE Invoices_Agent SHALL support filtering by issue_date, due_date, or paid_date ranges
3. WHEN searching by amount, THE Invoices_Agent SHALL support filtering by total_amount or balance_due ranges
4. WHEN searching by client, THE Invoices_Agent SHALL support partial matching on client_name
5. WHEN multiple filters are applied, THE Invoices_Agent SHALL combine them with AND logic to narrow results

### Requirement 16

**User Story:** As a painting contractor, I want to see invoice summaries and analytics, so that I can understand my billing and revenue at a glance.

#### Acceptance Criteria

1. WHEN requesting invoice summaries, THE Invoices_Agent SHALL calculate total invoiced amount by summing total_amount across all invoices
2. WHEN calculating revenue, THE Invoices_Agent SHALL sum amount_paid across all invoices
3. WHEN calculating outstanding balance, THE Invoices_Agent SHALL sum balance_due across all unpaid and partially paid invoices
4. WHEN filtering by date range, THE Invoices_Agent SHALL calculate summaries only for invoices within that range
5. WHEN grouping by status, THE Invoices_Agent SHALL provide counts and total amounts for each status category (draft, sent, paid, overdue, etc.)

### Requirement 17

**User Story:** As a painting contractor, I want deletion restrictions based on invoice status, so that I cannot accidentally delete invoices that have been sent or paid.

#### Acceptance Criteria

1. WHEN attempting to delete an invoice, THE Invoices_Agent SHALL check the invoice status before allowing deletion
2. WHEN an invoice has status 'draft', THE Invoices_Agent SHALL allow deletion and remove the record from the database
3. WHEN an invoice has status 'sent', 'viewed', 'partial', or 'paid', THE Invoices_Agent SHALL prevent deletion and return an error message
4. WHEN deletion is prevented, THE Invoices_Agent SHALL suggest updating status to 'cancelled' instead of deleting
5. WHEN an invoice is cancelled, THE Invoices_Agent SHALL retain the record in the database with status 'cancelled'

### Requirement 18

**User Story:** As a system developer, I want the Invoice Agent to integrate with the conversation context system, so that invoice discussions maintain context across voice and text sessions.

#### Acceptance Criteria

1. WHEN discussing invoices, THE Invoices_Agent SHALL store conversation messages in the conversations table as specified in the **conversation-context** specification
2. WHEN a user references "the invoice" or "that invoice", THE Invoices_Agent SHALL use conversation context to identify which invoice_number is being discussed
3. WHEN switching between voice and text input, THE Invoices_Agent SHALL maintain context about which invoices are being discussed
4. WHEN multiple invoices are discussed in a session, THE Invoices_Agent SHALL track context for each invoice separately
5. WHEN conversation history is retrieved, THE Invoices_Agent SHALL include invoice-related messages to provide context for current queries
