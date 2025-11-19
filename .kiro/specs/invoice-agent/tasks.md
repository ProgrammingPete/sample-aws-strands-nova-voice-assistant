# Implementation Plan

- [ ] 1. Set up Invoice Agent infrastructure and Supabase integration
  - Create InvoiceAgent class in `backend/src/voice_based_aws_agent/agents/invoice_agent.py`
  - Implement Supabase client initialization with api schema configuration
  - Set up conversation manager integration for context tracking
  - Configure environment variables (SUPABASE_URL, SUPABASE_ANON_KEY)
  - Implement basic error handling and logging infrastructure
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 8.4_

- [ ] 2. Implement core data models and validation
  - [ ] 2.1 Create InvoiceDTO dataclass with all invoice fields
    - Define required fields: invoice_number, client_name, client_email, total_amount, balance_due, status
    - Define optional fields: subtotal, tax_rate, tax_amount, discount_amount, amount_paid, paid_date, notes
    - Include date fields: issue_date, due_date, created_at, updated_at
    - _Requirements: 4.1, 4.2, 6.2_

  - [ ]* 2.2 Write property test for InvoiceDTO validation
    - **Property 1: Invoice retrieval consistency**
    - **Validates: Requirements 2.1, 2.2**

  - [ ] 2.3 Implement InvoiceValidator class
    - Create validate_status method with valid status list
    - Create validate_amounts method for non-negative amount checks
    - Create validate_invoice_number method for format validation
    - Create validate_email method for basic email validation
    - _Requirements: 5.2, 5.3, 8.3_

  - [ ]* 2.4 Write property test for status validation
    - **Property 5: Status validation enforcement**
    - **Validates: Requirements 5.2, 5.3**

- [ ] 3. Implement voice response formatter
  - [ ] 3.1 Create VoiceResponseFormatter class
    - Implement truncate_for_voice method with 800-character limit
    - Implement format_invoice_list for multiple invoice display
    - Implement format_invoice_details for single invoice display
    - Implement format_confirmation for operation confirmations
    - Implement format_error for user-friendly error messages
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ]* 3.2 Write unit tests for response formatting
    - Test truncation at sentence boundaries
    - Test truncation at word boundaries
    - Test 800-character limit enforcement
    - Test essential field inclusion in voice responses
    - _Requirements: 9.1, 9.2_


- [ ] 4. Implement list invoices functionality
  - [ ] 4.1 Create list_invoices method
    - Query all invoices from api.invoices table
    - Select essential fields: invoice_number, client_name, total_amount, balance_due, status
    - Handle empty result set with appropriate message
    - Format response for voice output (under 800 characters)
    - _Requirements: 1.1, 1.2, 1.3, 1.5_

  - [ ]* 4.2 Write unit tests for list_invoices
    - Test with multiple invoices in database
    - Test with empty database
    - Test response length under 800 characters
    - Test essential fields included in response
    - _Requirements: 1.1, 1.2, 1.3_

  - [ ]* 4.3 Write property test for database error handling
    - **Property 7: Deletion confirmation consistency**
    - **Validates: Requirements 7.2, 7.3**

- [ ] 5. Implement get invoice by number functionality
  - [ ] 5.1 Create get_invoice_by_number method
    - Query invoice by invoice_number using .eq() filter
    - Handle invoice not found case
    - Format invoice details for voice output
    - Include client_name, total_amount, balance_due, status
    - _Requirements: 2.1, 2.2, 2.3, 2.5_

  - [ ]* 5.2 Write property test for invoice retrieval
    - **Property 1: Invoice retrieval consistency**
    - **Validates: Requirements 2.1, 2.2**

  - [ ]* 5.3 Write unit tests for get_invoice_by_number
    - Test with valid invoice_number
    - Test with non-existent invoice_number
    - Test response formatting
    - _Requirements: 2.1, 2.2, 2.3_

- [ ] 6. Implement get invoices by client functionality
  - [ ] 6.1 Create get_invoices_by_client method
    - Query invoices filtering by client_name
    - Handle no invoices found for client
    - Format multiple invoice results for voice
    - Include invoice_number, total_amount, balance_due, status for each
    - _Requirements: 3.1, 3.2, 3.3, 3.5_

  - [ ]* 6.2 Write property test for client filtering
    - **Property 2: Client invoice filtering accuracy**
    - **Validates: Requirements 3.1, 3.2**

  - [ ]* 6.3 Write unit tests for get_invoices_by_client
    - Test with client having multiple invoices
    - Test with client having no invoices
    - Test response formatting for voice
    - _Requirements: 3.1, 3.2, 3.3_


- [ ] 7. Implement create invoice functionality
  - [ ] 7.1 Create create_invoice method
    - Accept required parameters: client_name, client_email, total_amount
    - Accept optional parameters: invoice_number, due_date
    - Set default due_date to 30 days from current date if not provided
    - Set initial status to 'draft'
    - Set balance_due equal to total_amount initially
    - Generate invoice_number if not provided (basic implementation)
    - Insert invoice into database
    - Return confirmation with invoice_number and amount
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [ ]* 7.2 Write property test for default due date
    - **Property 3: Default due date calculation**
    - **Validates: Requirements 4.3**

  - [ ]* 7.3 Write property test for initial status
    - **Property 4: Initial status assignment**
    - **Validates: Requirements 4.4**

  - [ ]* 7.4 Write unit tests for create_invoice
    - Test with all required fields
    - Test with optional invoice_number
    - Test with optional due_date
    - Test default due_date calculation (30 days)
    - Test initial status set to 'draft'
    - Test confirmation message format
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 8. Implement update invoice status functionality
  - [ ] 8.1 Create update_invoice_status method
    - Accept invoice_number and new_status parameters
    - Validate status using InvoiceValidator
    - Return error for invalid status with valid options list
    - Update invoice status in database
    - Return confirmation of status change
    - Handle invoice not found case
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ]* 8.2 Write property test for status validation
    - **Property 5: Status validation enforcement**
    - **Validates: Requirements 5.2, 5.3**

  - [ ]* 8.3 Write unit tests for update_invoice_status
    - Test with valid status values
    - Test with invalid status value
    - Test with non-existent invoice
    - Test confirmation message
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_


- [ ] 9. Implement update invoice fields functionality
  - [ ] 9.1 Create update_invoice method
    - Accept invoice_number and variable field parameters
    - Support updating: client_name, client_email, total_amount, balance_due, status, notes, due_date
    - Validate at least one valid field is provided
    - Update only provided fields in database
    - Return confirmation of update
    - Handle invoice not found case
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]* 9.2 Write property test for field preservation
    - **Property 6: Update field preservation**
    - **Validates: Requirements 6.1, 6.2**

  - [ ]* 9.3 Write unit tests for update_invoice
    - Test updating single field
    - Test updating multiple fields
    - Test with no valid fields provided
    - Test with non-existent invoice
    - Test field preservation (unchanged fields remain same)
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 10. Implement delete invoice functionality
  - [ ] 10.1 Create delete_invoice method
    - Accept invoice_number parameter
    - Query invoice from database
    - Delete invoice record
    - Return confirmation of deletion
    - Handle invoice not found case
    - Handle database errors gracefully
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ]* 10.2 Write property test for deletion confirmation
    - **Property 7: Deletion confirmation consistency**
    - **Validates: Requirements 7.2, 7.3**

  - [ ]* 10.3 Write unit tests for delete_invoice
    - Test successful deletion
    - Test with non-existent invoice
    - Test confirmation message
    - Test database error handling
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 11. Checkpoint - Ensure all basic CRUD tests pass
  - Ensure all tests pass, ask the user if questions arise.


- [ ] 12. Implement automatic invoice calculations
  - [ ] 12.1 Create calculate_invoice_totals method
    - Accept subtotal, tax_rate, discount_amount parameters
    - Calculate tax_amount = subtotal × tax_rate
    - Calculate total_amount = subtotal + tax_amount - discount_amount
    - Return dictionary with calculated values
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [ ]* 12.2 Write property test for tax calculation
    - **Property 8: Tax calculation accuracy**
    - **Validates: Requirements 11.2**

  - [ ]* 12.3 Write property test for total calculation
    - **Property 9: Total amount calculation**
    - **Validates: Requirements 11.4**

  - [ ] 12.4 Update create_invoice to support calculation fields
    - Accept optional subtotal, tax_rate, discount_amount parameters
    - Calculate tax_amount and total_amount if subtotal provided
    - Store calculated values in database
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [ ] 12.5 Update update_invoice to recalculate on field changes
    - Recalculate totals when subtotal, tax_rate, or discount_amount changes
    - Update total_amount and balance_due accordingly
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [ ]* 12.6 Write unit tests for calculation methods
    - Test tax calculation with various rates
    - Test total calculation with discount
    - Test total calculation without discount
    - Test currency formatting (two decimal places)
    - _Requirements: 11.2, 11.3, 11.4, 11.5_

- [ ] 13. Implement payment tracking functionality
  - [ ] 13.1 Create record_payment method
    - Accept invoice_number, amount_paid, paid_date parameters
    - Calculate new balance_due = total_amount - amount_paid
    - Auto-update status to 'paid' if balance_due = 0
    - Auto-update status to 'partial' if 0 < balance_due < total_amount
    - Update invoice with payment information
    - Return confirmation with updated balance
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

  - [ ]* 13.2 Write property test for balance calculation
    - **Property 10: Balance due calculation**
    - **Validates: Requirements 12.2**

  - [ ]* 13.3 Write property test for automatic paid status
    - **Property 11: Automatic paid status**
    - **Validates: Requirements 12.3**

  - [ ]* 13.4 Write property test for partial payment status
    - **Property 12: Partial payment status**
    - **Validates: Requirements 12.4**

  - [ ]* 13.5 Write unit tests for record_payment
    - Test full payment (balance_due = 0, status = 'paid')
    - Test partial payment (balance_due > 0, status = 'partial')
    - Test payment information in response
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_


- [ ] 14. Implement automatic invoice number generation
  - [ ] 14.1 Create generate_invoice_number method
    - Generate format: INV-YYYY-NNNN (year + sequential number)
    - Query existing invoices to find highest sequential number for current year
    - Increment sequential number for new invoice
    - Ensure uniqueness by checking against existing invoice_numbers
    - Return generated invoice_number
    - _Requirements: 14.1, 14.2, 14.3_

  - [ ]* 14.2 Write property test for invoice number uniqueness
    - **Property 13: Invoice number uniqueness**
    - **Validates: Requirements 14.3**

  - [ ]* 14.3 Write property test for invoice number format
    - **Property 14: Generated invoice number format**
    - **Validates: Requirements 14.2**

  - [ ] 14.4 Update create_invoice to use auto-generation
    - Call generate_invoice_number if invoice_number not provided
    - Validate custom invoice_number for uniqueness if provided
    - Return error if custom invoice_number already exists
    - _Requirements: 14.1, 14.4, 14.5_

  - [ ]* 14.5 Write unit tests for invoice number generation
    - Test format matches INV-YYYY-NNNN
    - Test sequential numbering within same year
    - Test uniqueness validation
    - Test custom invoice_number validation
    - _Requirements: 14.1, 14.2, 14.3, 14.4_

- [ ] 15. Implement search and filter functionality
  - [ ] 15.1 Create search_invoices method
    - Accept filters dictionary with optional criteria
    - Support status filter (single or multiple statuses)
    - Support date range filters (issue_date, due_date, paid_date)
    - Support amount range filters (total_amount, balance_due)
    - Support client_name partial matching
    - Combine multiple filters with AND logic
    - Return filtered invoice list
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

  - [ ]* 15.2 Write property test for filter conjunction
    - **Property 17: Search filter conjunction**
    - **Validates: Requirements 15.5**

  - [ ]* 15.3 Write property test for date range filtering
    - **Property 18: Date range filtering**
    - **Validates: Requirements 15.2**

  - [ ]* 15.4 Write unit tests for search_invoices
    - Test single filter (status)
    - Test multiple filters combined
    - Test date range filtering
    - Test amount range filtering
    - Test client name partial matching
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_


- [ ] 16. Implement invoice summary and analytics
  - [ ] 16.1 Create get_invoice_summary method
    - Accept optional date_range parameter (start_date, end_date)
    - Calculate total invoiced amount (sum of total_amount)
    - Calculate total revenue (sum of amount_paid)
    - Calculate outstanding balance (sum of balance_due for unpaid/partial invoices)
    - Group counts by status
    - Format summary for voice output
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_

  - [ ]* 16.2 Write property test for summary calculation
    - **Property 19: Summary calculation accuracy**
    - **Validates: Requirements 16.1**

  - [ ]* 16.3 Write property test for outstanding balance
    - **Property 20: Outstanding balance calculation**
    - **Validates: Requirements 16.3**

  - [ ]* 16.4 Write unit tests for get_invoice_summary
    - Test total invoiced amount calculation
    - Test revenue calculation
    - Test outstanding balance calculation
    - Test date range filtering
    - Test status grouping
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_

- [ ] 17. Implement deletion restrictions based on status
  - [ ] 17.1 Update delete_invoice with status checks
    - Check invoice status before deletion
    - Allow deletion only for 'draft' status
    - Prevent deletion for: sent, viewed, partial, paid
    - Return error message suggesting cancellation for non-draft invoices
    - _Requirements: 17.1, 17.2, 17.3, 17.4_

  - [ ]* 17.2 Write property test for status-based deletion
    - **Property 15: Status-based deletion restriction**
    - **Validates: Requirements 17.2, 17.3**

  - [ ]* 17.3 Write property test for draft deletion
    - **Property 16: Draft deletion permission**
    - **Validates: Requirements 17.2**

  - [ ]* 17.4 Write unit tests for deletion restrictions
    - Test deletion allowed for draft status
    - Test deletion prevented for sent status
    - Test deletion prevented for paid status
    - Test error message suggests cancellation
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_


- [ ] 18. Implement conversation context integration
  - [ ] 18.1 Add conversation context storage for invoice operations
    - Store all invoice-related messages in conversation context
    - Include metadata: agent_name, invoice_number, operation type
    - Format messages for JSONB storage
    - _Requirements: 18.1, 18.2_

  - [ ] 18.2 Implement context-aware invoice references
    - Parse conversation history to identify last mentioned invoice_number
    - Resolve "the invoice" or "that invoice" references from context
    - Handle ambiguous references by asking for clarification
    - _Requirements: 18.2, 18.3_

  - [ ] 18.3 Maintain context across voice and text sessions
    - Retrieve conversation history on agent initialization
    - Include previous invoice discussions in context window
    - Support seamless switching between voice and text input
    - _Requirements: 18.3, 18.4_

  - [ ]* 18.4 Write unit tests for context integration
    - Test message storage in conversation context
    - Test invoice reference resolution from context
    - Test ambiguous reference handling
    - Test cross-session context retrieval
    - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

- [ ] 19. Integrate Invoice Agent with orchestrator
  - [ ] 19.1 Register Invoice Agent with supervisor
    - Add InvoiceAgent to agent registry in orchestrator
    - Configure routing rules for invoice-related queries
    - Set up conversation manager for Invoice Agent
    - Test agent initialization and routing
    - _Requirements: 10.1, 10.2_

  - [ ] 19.2 Configure Invoice Agent tools
    - Define tool methods for each CRUD operation
    - Add tool descriptions for supervisor routing
    - Configure tool parameters and return types
    - Test tool invocation from supervisor
    - _Requirements: 10.1, 10.2_

  - [ ]* 19.3 Write integration tests for agent orchestration
    - Test supervisor routes invoice queries to Invoice Agent
    - Test Invoice Agent responds to supervisor
    - Test conversation context flows through orchestrator
    - Test error handling in multi-agent context
    - _Requirements: 10.1, 10.2_

- [ ] 20. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

