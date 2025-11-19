# Invoice Agent Design Document

## Overview

The Invoice Agent is a specialized agent within the Voice-Based Painting Business Agent that manages invoice operations through voice and text commands. The agent provides comprehensive CRUD operations for invoices, integrating with Supabase for data persistence and the conversation context system for maintaining contextual awareness across sessions.

**Design Philosophy**: The Invoice Agent follows a progressive implementation approach, starting with basic CRUD operations and expanding to advanced features like automatic calculations, payment tracking, and analytics. This design supports both the current basic implementation and future enhancements defined in the requirements.

**Integration Points**:
- Supabase database (`api.invoices` table) for invoice persistence
- Conversation context system for maintaining discussion context
- Voice optimization for responses under 800 characters
- AWS Strands multi-agent framework for orchestration

## Architecture

### Agent Structure

The Invoice Agent follows the Strands agent pattern with these key components:

```
InvoiceAgent
├── Conversation Manager (sliding window context)
├── Supabase Client (api schema)
├── Tool Methods (CRUD operations)
└── Response Formatter (voice optimization)
```

**Key Design Decisions**:

1. **Direct Database Access**: The agent directly interfaces with Supabase rather than through an API layer, simplifying the architecture and reducing latency for voice interactions.

2. **Voice-First Design**: All responses are optimized for voice output (≤800 characters), with essential information prioritized over comprehensive details.

3. **Stateless Operations**: Each operation is self-contained, relying on conversation context rather than agent state for continuity.

4. **Progressive Feature Implementation**: Core CRUD operations are implemented first, with advanced features (calculations, payments, analytics) designed but implemented incrementally.


## Components and Interfaces

### InvoiceAgent Class

```python
class InvoiceAgent:
    """
    Specialized agent for invoice CRUD operations.
    Integrates with Supabase and conversation context system.
    """
    
    def __init__(self, supabase_client, conversation_manager):
        self.supabase = supabase_client
        self.conversation_manager = conversation_manager
        self.schema = "api"
        self.table = "invoices"
    
    # Core CRUD operations
    def list_invoices(self) -> str
    def get_invoice_by_number(self, invoice_number: str) -> str
    def get_invoices_by_client(self, client_name: str) -> str
    def create_invoice(self, client_name: str, client_email: str, 
                      total_amount: float, **kwargs) -> str
    def update_invoice_status(self, invoice_number: str, new_status: str) -> str
    def update_invoice(self, invoice_number: str, **fields) -> str
    def delete_invoice(self, invoice_number: str) -> str
    
    # Advanced features (future implementation)
    def calculate_invoice_totals(self, subtotal: float, tax_rate: float, 
                                 discount_amount: float) -> dict
    def record_payment(self, invoice_number: str, amount_paid: float, 
                      paid_date: str) -> str
    def generate_invoice_number(self, year: int = None) -> str
    def search_invoices(self, filters: dict) -> str
    def get_invoice_summary(self, date_range: tuple = None) -> str
```

### Supabase Client Interface

```python
class SupabaseInvoiceClient:
    """
    Handles all database operations for invoices.
    Uses api schema for table operations.
    """
    
    def __init__(self, url: str, key: str):
        self.client = create_client(url, key)
        self.schema = "api"
    
    def select_all(self) -> list
    def select_by_invoice_number(self, invoice_number: str) -> dict
    def select_by_client_name(self, client_name: str) -> list
    def insert(self, invoice_data: dict) -> dict
    def update(self, invoice_number: str, updates: dict) -> dict
    def delete(self, invoice_number: str) -> bool
    def search(self, filters: dict) -> list
```

### Response Formatter

```python
class VoiceResponseFormatter:
    """
    Formats invoice data for voice-optimized output.
    Ensures responses stay under 800 characters.
    """
    
    MAX_LENGTH = 800
    
    @staticmethod
    def format_invoice_list(invoices: list) -> str
    
    @staticmethod
    def format_invoice_details(invoice: dict) -> str
    
    @staticmethod
    def format_confirmation(operation: str, invoice_number: str) -> str
    
    @staticmethod
    def format_error(error_type: str, details: str) -> str
```


## Data Models

### Invoice Schema (api.invoices table)

```sql
CREATE TABLE api.invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    client_id UUID REFERENCES api.contacts(id),
    client_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255),
    project_id UUID REFERENCES api.projects(id),
    
    -- Financial fields
    subtotal DECIMAL(10,2),
    tax_rate DECIMAL(5,4),
    tax_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    amount_paid DECIMAL(10,2) DEFAULT 0,
    balance_due DECIMAL(10,2) NOT NULL,
    
    -- Status and dates
    status VARCHAR(20) DEFAULT 'draft',
    issue_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    paid_date DATE,
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Status Values**: draft, sent, viewed, partial, paid, overdue, cancelled

**Field Relationships**:
- `balance_due = total_amount - amount_paid`
- `total_amount = subtotal + tax_amount - discount_amount`
- `tax_amount = subtotal * tax_rate`

### Invoice Data Transfer Object

```python
@dataclass
class InvoiceDTO:
    """Data transfer object for invoice operations"""
    invoice_number: str
    client_name: str
    client_email: Optional[str]
    total_amount: Decimal
    balance_due: Decimal
    status: str
    issue_date: date
    due_date: Optional[date]
    
    # Optional fields for advanced features
    client_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    subtotal: Optional[Decimal] = None
    tax_rate: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    amount_paid: Optional[Decimal] = None
    paid_date: Optional[date] = None
    notes: Optional[str] = None
```

### Validation Rules

```python
class InvoiceValidator:
    """Validates invoice data before database operations"""
    
    VALID_STATUSES = ['draft', 'sent', 'viewed', 'partial', 'paid', 'overdue', 'cancelled']
    
    @staticmethod
    def validate_status(status: str) -> bool:
        return status in InvoiceValidator.VALID_STATUSES
    
    @staticmethod
    def validate_amounts(total_amount: float, amount_paid: float = 0) -> bool:
        return total_amount >= 0 and amount_paid >= 0 and amount_paid <= total_amount
    
    @staticmethod
    def validate_invoice_number(invoice_number: str) -> bool:
        # Format: INV-YYYY-NNNN or custom format
        return len(invoice_number) > 0 and len(invoice_number) <= 50
    
    @staticmethod
    def validate_email(email: str) -> bool:
        # Basic email validation
        return '@' in email and '.' in email.split('@')[1]
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Invoice retrieval consistency
*For any* invoice that has been successfully created, querying by its invoice_number should return the same invoice data that was stored.
**Validates: Requirements 2.1, 2.2**

### Property 2: Client invoice filtering accuracy
*For any* client_name, all invoices returned by get_invoices_by_client should have a matching client_name field.
**Validates: Requirements 3.1, 3.2**

### Property 3: Default due date calculation
*For any* invoice created without a due_date parameter, the due_date should be exactly 30 days from the issue_date.
**Validates: Requirements 4.3**

### Property 4: Initial status assignment
*For any* newly created invoice, the status field should be set to 'draft' unless explicitly specified otherwise.
**Validates: Requirements 4.4**

### Property 5: Status validation enforcement
*For any* status update operation, only values from the set {draft, sent, viewed, partial, paid, overdue, cancelled} should be accepted; all other values should be rejected with an error.
**Validates: Requirements 5.2, 5.3**

### Property 6: Update field preservation
*For any* invoice update operation that modifies specific fields, all fields not included in the update should remain unchanged.
**Validates: Requirements 6.1, 6.2**

### Property 7: Deletion confirmation consistency
*For any* invoice that is successfully deleted, subsequent queries for that invoice_number should return a "not found" result.
**Validates: Requirements 7.2, 7.3**

### Property 8: Tax calculation accuracy
*For any* invoice with subtotal and tax_rate, the tax_amount should equal subtotal × tax_rate (within floating-point precision).
**Validates: Requirements 11.2**

### Property 9: Total amount calculation
*For any* invoice with subtotal, tax_amount, and discount_amount, the total_amount should equal (subtotal + tax_amount - discount_amount).
**Validates: Requirements 11.4**

### Property 10: Balance due calculation
*For any* invoice, the balance_due should always equal (total_amount - amount_paid).
**Validates: Requirements 12.2**

### Property 11: Automatic paid status
*For any* invoice where amount_paid equals total_amount (balance_due = 0), the status should automatically be set to 'paid'.
**Validates: Requirements 12.3**

### Property 12: Partial payment status
*For any* invoice where 0 < amount_paid < total_amount (balance_due > 0), the status should be set to 'partial'.
**Validates: Requirements 12.4**

### Property 13: Invoice number uniqueness
*For any* two invoices in the system, their invoice_number values must be distinct.
**Validates: Requirements 14.3**

### Property 14: Generated invoice number format
*For any* automatically generated invoice_number, it should follow the format INV-YYYY-NNNN where YYYY is the year and NNNN is a sequential number.
**Validates: Requirements 14.2**

### Property 15: Status-based deletion restriction
*For any* invoice with status in {sent, viewed, partial, paid}, deletion attempts should be rejected with an error message.
**Validates: Requirements 17.2, 17.3**

### Property 16: Draft deletion permission
*For any* invoice with status 'draft', deletion should succeed and remove the record from the database.
**Validates: Requirements 17.2**

### Property 17: Search filter conjunction
*For any* search operation with multiple filters, only invoices matching ALL filter criteria should be returned (AND logic).
**Validates: Requirements 15.5**

### Property 18: Date range filtering
*For any* search with a date range filter, only invoices with dates within the specified range (inclusive) should be returned.
**Validates: Requirements 15.2**

### Property 19: Summary calculation accuracy
*For any* set of invoices, the total invoiced amount should equal the sum of all total_amount values.
**Validates: Requirements 16.1**

### Property 20: Outstanding balance calculation
*For any* set of invoices, the outstanding balance should equal the sum of balance_due for all invoices with status in {draft, sent, viewed, partial, overdue}.
**Validates: Requirements 16.3**


## Error Handling

### Error Categories

**1. Database Connection Errors**
- Supabase client initialization failures
- Network connectivity issues
- Authentication failures

**Handling Strategy**: Return user-friendly error message indicating connection issues, log technical details for debugging.

```python
try:
    result = self.supabase.table(self.table).select("*").execute()
except Exception as e:
    logger.error(f"Database connection error: {str(e)}")
    return "Unable to connect to the database. Please try again later."
```

**2. Validation Errors**
- Invalid status values
- Missing required parameters
- Invalid email formats
- Negative amounts

**Handling Strategy**: Return specific error message explaining the validation rule, suggest correct format.

```python
if not InvoiceValidator.validate_status(new_status):
    return f"Invalid status '{new_status}'. Valid options: {', '.join(VALID_STATUSES)}"
```

**3. Not Found Errors**
- Invoice number doesn't exist
- Client has no invoices
- Empty result sets

**Handling Strategy**: Return clear message indicating what was not found, suggest alternatives.

```python
if not invoice:
    return f"Invoice {invoice_number} not found. Please check the invoice number."
```

**4. Business Logic Errors**
- Attempting to delete non-draft invoices
- Duplicate invoice numbers
- Payment amount exceeds total

**Handling Strategy**: Return error explaining the business rule, suggest corrective action.

```python
if invoice['status'] not in ['draft']:
    return f"Cannot delete invoice {invoice_number} with status '{invoice['status']}'. Consider cancelling instead."
```

### Error Response Format

All error responses follow this structure for consistency:

```python
{
    "success": False,
    "error_type": "validation_error" | "not_found" | "database_error" | "business_logic_error",
    "message": "User-friendly error message",
    "details": "Additional context (optional)"
}
```

For voice responses, only the message is returned, truncated to 800 characters.

### Logging Strategy

```python
import logging

logger = logging.getLogger("InvoiceAgent")

# Log levels:
# ERROR: Database failures, unexpected exceptions
# WARNING: Business logic violations, validation failures
# INFO: Successful operations, state changes
# DEBUG: Detailed operation traces
```


## Testing Strategy

The Invoice Agent employs a dual testing approach combining unit tests for specific scenarios and property-based tests for universal correctness guarantees.

### Unit Testing Approach

Unit tests verify specific examples, integration points, and edge cases:

**Core CRUD Operations**:
- Test creating invoice with all required fields
- Test retrieving invoice by valid invoice_number
- Test updating invoice status with valid status
- Test deleting draft invoice
- Test listing all invoices when database has records

**Edge Cases**:
- Empty database returns appropriate message
- Invalid invoice_number returns not found
- Missing required parameters returns validation error
- Duplicate invoice_number is rejected

**Integration Points**:
- Supabase client connection and authentication
- Conversation context integration
- Response formatting for voice output

**Example Unit Test**:
```python
def test_create_invoice_with_required_fields():
    agent = InvoiceAgent(supabase_client, conversation_manager)
    result = agent.create_invoice(
        client_name="John Doe",
        client_email="john@example.com",
        total_amount=1500.00
    )
    assert "successfully created" in result.lower()
    assert "INV-" in result
```

### Property-Based Testing Approach

Property-based tests verify universal properties across all valid inputs using a property testing library.

**Testing Library**: We'll use **Hypothesis** for Python, which provides powerful property-based testing capabilities with automatic test case generation.

**Configuration**: Each property test will run a minimum of 100 iterations to ensure comprehensive coverage across the input space.

**Test Annotation Format**: Each property test must include a comment explicitly referencing the correctness property:
```python
# Feature: invoice-agent, Property 1: Invoice retrieval consistency
```

**Key Properties to Test**:

1. **Retrieval Consistency** (Property 1): Generate random invoice data, create invoice, retrieve by number, verify data matches.

2. **Client Filtering** (Property 2): Generate invoices with various client names, filter by client, verify all results match.

3. **Status Validation** (Property 5): Generate random status values, attempt updates, verify only valid statuses are accepted.

4. **Calculation Accuracy** (Properties 8, 9, 10): Generate random amounts, verify tax, total, and balance calculations are correct.

5. **Deletion Restrictions** (Properties 15, 16): Generate invoices with various statuses, attempt deletion, verify only drafts can be deleted.

**Example Property Test**:
```python
from hypothesis import given, strategies as st

# Feature: invoice-agent, Property 1: Invoice retrieval consistency
@given(
    client_name=st.text(min_size=1, max_size=100),
    total_amount=st.floats(min_value=0.01, max_value=999999.99)
)
def test_invoice_retrieval_consistency(client_name, total_amount):
    """For any invoice created, retrieval by invoice_number returns same data"""
    agent = InvoiceAgent(supabase_client, conversation_manager)
    
    # Create invoice
    create_result = agent.create_invoice(
        client_name=client_name,
        client_email=f"{client_name}@example.com",
        total_amount=total_amount
    )
    
    # Extract invoice number from result
    invoice_number = extract_invoice_number(create_result)
    
    # Retrieve invoice
    retrieve_result = agent.get_invoice_by_number(invoice_number)
    
    # Verify data matches
    assert client_name in retrieve_result
    assert str(total_amount) in retrieve_result
```

### Test Coverage Goals

- **Unit Tests**: Cover all CRUD operations, error paths, and edge cases
- **Property Tests**: Verify all 20 correctness properties defined in the design
- **Integration Tests**: Verify Supabase integration and conversation context integration
- **Voice Response Tests**: Verify all responses are under 800 characters

### Testing Workflow

1. Write implementation code first
2. Write unit tests for specific scenarios
3. Write property tests for universal properties
4. Run all tests to verify correctness
5. Fix any failures before considering task complete


## Implementation Phases

The Invoice Agent implementation follows a phased approach, building from basic CRUD to advanced features.

### Phase 1: Core CRUD Operations (Current Implementation)

**Scope**: Basic invoice management with essential fields

**Features**:
- List all invoices
- Get invoice by invoice_number
- Get invoices by client_name
- Create invoice with required fields (client_name, client_email, total_amount)
- Update invoice status
- Update invoice fields
- Delete invoice

**Database Fields Used**:
- invoice_number, client_name, client_email
- total_amount, balance_due
- status, issue_date, due_date
- notes, created_at, updated_at

**Validation**:
- Status validation (valid status values)
- Required field validation
- Basic amount validation (non-negative)

### Phase 2: Automatic Calculations

**Scope**: Financial calculations and automatic field updates

**Features**:
- Calculate tax_amount from subtotal and tax_rate
- Calculate total_amount from subtotal, tax, and discount
- Calculate balance_due from total_amount and amount_paid
- Automatic status updates based on payment state

**New Fields**:
- subtotal, tax_rate, tax_amount
- discount_amount, amount_paid

**Business Rules**:
- balance_due = total_amount - amount_paid
- total_amount = subtotal + tax_amount - discount_amount
- Auto-update status to 'paid' when balance_due = 0
- Auto-update status to 'partial' when 0 < balance_due < total_amount

### Phase 3: Payment Tracking

**Scope**: Record and track payments against invoices

**Features**:
- Record payment with amount and date
- Update balance_due automatically
- Track payment history
- Automatic status transitions based on payment

**New Fields**:
- paid_date

**Integration**:
- May integrate with payment processing systems in future
- Payment history could be tracked in separate payments table

### Phase 4: Relationships and Context

**Scope**: Link invoices to clients and projects

**Features**:
- Link invoices to client_id from contacts table
- Link invoices to project_id from projects table
- Auto-populate client details from contacts
- Validate project existence before linking
- Retrieve related project and client information

**New Fields**:
- client_id (foreign key to contacts)
- project_id (foreign key to projects)

**Integration**:
- Requires contacts table implementation
- Requires projects table implementation
- Conversation context integration for "the invoice" references

### Phase 5: Advanced Features

**Scope**: Search, analytics, and automation

**Features**:
- Automatic invoice number generation (INV-YYYY-NNNN format)
- Search and filter by multiple criteria
- Invoice summaries and analytics
- Date range filtering
- Status-based deletion restrictions
- Overdue invoice detection

**Business Rules**:
- Generated invoice numbers must be unique
- Cannot delete invoices with status: sent, viewed, partial, paid
- Can only delete draft invoices
- Suggest cancellation instead of deletion for non-draft invoices

### Phase 6: Conversation Context Integration

**Scope**: Full integration with conversation context system

**Features**:
- Store invoice discussions in conversations table
- Resolve "the invoice" references using conversation context
- Maintain context across voice and text sessions
- Track invoice-related conversations per client

**Integration Points**:
- Conversation context system (Requirement 18)
- Message storage in JSONB format
- Context window management
- Cross-session context persistence


## Voice Optimization

### Response Length Management

All responses must be optimized for voice output with a strict 800-character limit.

**Truncation Strategy**:
```python
def truncate_for_voice(text: str, max_length: int = 800) -> str:
    """Truncate text for voice output while preserving meaning"""
    if len(text) <= max_length:
        return text
    
    # Try to truncate at sentence boundary
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    
    if last_period > max_length * 0.7:  # If we can keep 70% of content
        return truncated[:last_period + 1]
    
    # Otherwise truncate at word boundary
    last_space = truncated.rfind(' ')
    return truncated[:last_space] + "..."
```

### Response Templates

**List Invoices** (multiple results):
```
Found {count} invoices: {invoice_1}, {invoice_2}, {invoice_3}. 
Each showing number, client, amount, and status.
```

**Invoice Details** (single result):
```
Invoice {number} for {client}: ${amount}, balance due ${balance}, status {status}.
```

**Create Confirmation**:
```
Invoice {number} created for {client}, total ${amount}.
```

**Update Confirmation**:
```
Invoice {number} updated: status changed to {new_status}.
```

**Delete Confirmation**:
```
Invoice {number} deleted successfully.
```

**Error Messages**:
```
Invoice {number} not found. Please check the invoice number.
Invalid status '{status}'. Valid options: draft, sent, viewed, partial, paid, overdue, cancelled.
Cannot delete invoice {number} with status '{status}'. Consider cancelling instead.
```

### Field Prioritization for Voice

When listing multiple invoices, include only essential fields:
1. invoice_number (identifier)
2. client_name (who)
3. total_amount (how much)
4. balance_due (what's owed)
5. status (current state)

Omit for voice brevity:
- issue_date, due_date (unless specifically requested)
- notes (too verbose for voice)
- created_at, updated_at (internal metadata)
- client_email (not essential for voice)

### Conversation Context Integration

**Context-Aware Responses**:

When conversation context indicates a previously discussed invoice:
```
User: "What's the status of that invoice?"
Agent: [Checks conversation context for last mentioned invoice_number]
Response: "Invoice INV-2024-0042 for John Doe is currently marked as sent."
```

**Ambiguity Resolution**:
```
User: "Update the invoice to paid"
Agent: [Multiple invoices discussed in context]
Response: "Which invoice would you like to update? I see INV-2024-0042 for John Doe and INV-2024-0043 for Jane Smith in our conversation."
```

**Context Storage**:

All invoice-related messages are stored in the conversation context:
```python
{
    "role": "assistant",
    "content": "Invoice INV-2024-0042 created for John Doe, total $1,500.00",
    "timestamp": "2024-01-15T10:30:00Z",
    "metadata": {
        "agent_name": "InvoiceAgent",
        "invoice_number": "INV-2024-0042",
        "operation": "create"
    }
}
```


## Database Integration

### Supabase Configuration

```python
from supabase import create_client, Client
import os

class SupabaseConfig:
    """Configuration for Supabase connection"""
    
    @staticmethod
    def get_client() -> Client:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        return create_client(
            url,
            key,
            options={
                "postgrest": {"timeout": 10},
                "storage": {"timeout": 10}
            }
        )
```

### Schema Usage

All invoice operations use the `api` schema:

```python
# Correct: Use api schema
result = supabase.table("invoices").select("*").execute()
# This queries api.invoices

# Incorrect: Don't use public schema
result = supabase.schema("public").table("invoices").select("*").execute()
```

### Query Patterns

**Select All**:
```python
response = supabase.table("invoices").select("*").execute()
invoices = response.data
```

**Select by Invoice Number**:
```python
response = supabase.table("invoices")\
    .select("*")\
    .eq("invoice_number", invoice_number)\
    .execute()
invoice = response.data[0] if response.data else None
```

**Select by Client Name**:
```python
response = supabase.table("invoices")\
    .select("*")\
    .eq("client_name", client_name)\
    .execute()
invoices = response.data
```

**Insert**:
```python
invoice_data = {
    "invoice_number": "INV-2024-0001",
    "client_name": "John Doe",
    "client_email": "john@example.com",
    "total_amount": 1500.00,
    "balance_due": 1500.00,
    "status": "draft",
    "due_date": (datetime.now() + timedelta(days=30)).date()
}

response = supabase.table("invoices").insert(invoice_data).execute()
created_invoice = response.data[0]
```

**Update**:
```python
updates = {"status": "sent"}

response = supabase.table("invoices")\
    .update(updates)\
    .eq("invoice_number", invoice_number)\
    .execute()
updated_invoice = response.data[0] if response.data else None
```

**Delete**:
```python
response = supabase.table("invoices")\
    .delete()\
    .eq("invoice_number", invoice_number)\
    .execute()
success = len(response.data) > 0
```

### Transaction Handling

For operations requiring multiple database calls (e.g., payment recording with status update):

```python
def record_payment(self, invoice_number: str, amount_paid: float, paid_date: str) -> str:
    """Record payment and update invoice status atomically"""
    try:
        # Get current invoice
        invoice = self._get_invoice(invoice_number)
        if not invoice:
            return f"Invoice {invoice_number} not found"
        
        # Calculate new balance
        new_balance = invoice['total_amount'] - amount_paid
        
        # Determine new status
        if new_balance <= 0:
            new_status = 'paid'
        elif amount_paid > 0:
            new_status = 'partial'
        else:
            new_status = invoice['status']
        
        # Update invoice (single atomic operation)
        updates = {
            'amount_paid': amount_paid,
            'paid_date': paid_date,
            'balance_due': new_balance,
            'status': new_status
        }
        
        response = self.supabase.table("invoices")\
            .update(updates)\
            .eq("invoice_number", invoice_number)\
            .execute()
        
        return f"Payment of ${amount_paid} recorded for invoice {invoice_number}"
        
    except Exception as e:
        logger.error(f"Payment recording error: {str(e)}")
        return "Unable to record payment. Please try again."
```

### Index Recommendations

For optimal query performance:

```sql
-- Primary key on id (already exists)
CREATE INDEX idx_invoices_invoice_number ON api.invoices(invoice_number);
CREATE INDEX idx_invoices_client_name ON api.invoices(client_name);
CREATE INDEX idx_invoices_status ON api.invoices(status);
CREATE INDEX idx_invoices_due_date ON api.invoices(due_date);
CREATE INDEX idx_invoices_client_id ON api.invoices(client_id);
CREATE INDEX idx_invoices_project_id ON api.invoices(project_id);
```


## Security Considerations

### Authentication and Authorization

**Supabase Authentication**:
- Use SUPABASE_ANON_KEY for client-side operations
- Row-level security (RLS) policies should be configured on api.invoices table
- Future enhancement: User-specific invoice access based on authentication

**Recommended RLS Policies**:
```sql
-- Allow authenticated users to read their own invoices
CREATE POLICY "Users can view own invoices"
ON api.invoices FOR SELECT
USING (auth.uid() = user_id);

-- Allow authenticated users to create invoices
CREATE POLICY "Users can create invoices"
ON api.invoices FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Allow authenticated users to update their own invoices
CREATE POLICY "Users can update own invoices"
ON api.invoices FOR UPDATE
USING (auth.uid() = user_id);

-- Allow authenticated users to delete their own draft invoices
CREATE POLICY "Users can delete own draft invoices"
ON api.invoices FOR DELETE
USING (auth.uid() = user_id AND status = 'draft');
```

### Data Validation

**Input Sanitization**:
- Validate all user inputs before database operations
- Sanitize client_name and notes fields to prevent injection
- Validate email format before storage
- Ensure amounts are non-negative and within reasonable bounds

**SQL Injection Prevention**:
- Supabase client uses parameterized queries automatically
- Never construct raw SQL strings with user input
- Use Supabase query builder methods (.eq(), .select(), etc.)

### Sensitive Data Handling

**PII Protection**:
- client_email is personally identifiable information
- client_name may be sensitive
- notes field may contain sensitive business information

**Best Practices**:
- Don't log sensitive fields in error messages
- Truncate or mask sensitive data in voice responses when appropriate
- Consider encryption at rest for sensitive fields (future enhancement)

### Error Message Security

**Safe Error Messages**:
```python
# Good: Generic error message
return "Unable to process invoice. Please try again."

# Bad: Exposes database structure
return f"Database error: Table 'api.invoices' constraint violation on column 'client_email'"
```

**Logging vs. User Messages**:
```python
try:
    result = self.supabase.table("invoices").insert(data).execute()
except Exception as e:
    # Log detailed error for debugging
    logger.error(f"Invoice creation failed: {str(e)}, data: {data}")
    # Return generic message to user
    return "Unable to create invoice. Please check your information and try again."
```

### Rate Limiting

**Considerations for Voice Interface**:
- Voice commands may trigger rapid successive operations
- Implement rate limiting to prevent abuse
- Consider per-user operation limits

**Future Enhancement**:
```python
from functools import wraps
from time import time

def rate_limit(max_calls: int, time_window: int):
    """Decorator to limit function calls per time window"""
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            # Remove calls outside time window
            calls[:] = [c for c in calls if c > now - time_window]
            
            if len(calls) >= max_calls:
                return "Too many requests. Please wait a moment and try again."
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=10, time_window=60)
def create_invoice(self, ...):
    # Implementation
```


## Performance Considerations

### Query Optimization

**Selective Field Retrieval**:
```python
# Good: Select only needed fields
response = supabase.table("invoices")\
    .select("invoice_number, client_name, total_amount, balance_due, status")\
    .execute()

# Avoid: Select all fields when not needed
response = supabase.table("invoices").select("*").execute()
```

**Pagination for Large Result Sets**:
```python
def list_invoices_paginated(self, page: int = 1, page_size: int = 50) -> str:
    """List invoices with pagination"""
    offset = (page - 1) * page_size
    
    response = supabase.table("invoices")\
        .select("invoice_number, client_name, total_amount, status")\
        .range(offset, offset + page_size - 1)\
        .execute()
    
    return self._format_invoice_list(response.data)
```

**Index Usage**:
- Ensure queries use indexed columns (invoice_number, client_name, status)
- Avoid full table scans for large datasets
- Use .eq() for exact matches, .ilike() for case-insensitive searches

### Caching Strategy

**Conversation Context Caching**:
```python
class InvoiceAgent:
    def __init__(self, supabase_client, conversation_manager):
        self.supabase = supabase_client
        self.conversation_manager = conversation_manager
        self._last_invoice_cache = {}  # Cache last accessed invoice per session
    
    def get_invoice_by_number(self, invoice_number: str) -> str:
        # Check cache first
        if invoice_number in self._last_invoice_cache:
            cached_time, cached_data = self._last_invoice_cache[invoice_number]
            if time.time() - cached_time < 60:  # 1-minute cache
                return self._format_invoice_details(cached_data)
        
        # Fetch from database
        invoice = self._fetch_invoice(invoice_number)
        
        # Update cache
        self._last_invoice_cache[invoice_number] = (time.time(), invoice)
        
        return self._format_invoice_details(invoice)
```

**Cache Invalidation**:
- Invalidate cache on update/delete operations
- Use short TTL (1-5 minutes) for voice interactions
- Clear cache on session end

### Response Time Targets

**Voice Interaction Requirements**:
- Database query: < 500ms
- Response formatting: < 100ms
- Total response time: < 1 second

**Optimization Techniques**:
1. Use database indexes for common queries
2. Limit result set size for list operations
3. Cache frequently accessed invoices
4. Minimize data transfer (select only needed fields)
5. Use connection pooling for database connections

### Memory Management

**Large Result Sets**:
```python
def get_all_invoices_for_export(self) -> list:
    """Retrieve all invoices efficiently for export"""
    page_size = 100
    offset = 0
    all_invoices = []
    
    while True:
        response = supabase.table("invoices")\
            .select("*")\
            .range(offset, offset + page_size - 1)\
            .execute()
        
        if not response.data:
            break
        
        all_invoices.extend(response.data)
        offset += page_size
        
        if len(response.data) < page_size:
            break
    
    return all_invoices
```

**Voice Response Truncation**:
- Always truncate responses to 800 characters
- Summarize large result sets rather than listing all items
- Offer pagination for large lists


## Future Enhancements

### Line Items Support

**Motivation**: Enable detailed invoice breakdowns with multiple line items per invoice.

**Schema Addition**:
```sql
CREATE TABLE api.invoice_line_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID REFERENCES api.invoices(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    line_total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Agent Methods**:
```python
def add_line_item(self, invoice_number: str, description: str, 
                  quantity: float, unit_price: float) -> str
def remove_line_item(self, invoice_number: str, line_item_id: str) -> str
def update_line_item(self, line_item_id: str, **updates) -> str
```

### PDF Generation

**Motivation**: Generate professional PDF invoices for sending to clients.

**Implementation**:
- Use library like ReportLab or WeasyPrint
- Template-based PDF generation
- Include company logo, line items, payment terms
- Store PDF in Supabase Storage

**Agent Method**:
```python
def generate_invoice_pdf(self, invoice_number: str) -> str:
    """Generate PDF and return storage URL"""
```

### Email Integration

**Motivation**: Send invoices directly to clients via email.

**Implementation**:
- Integrate with AWS SES or SendGrid
- Email templates for invoice delivery
- Track email status (sent, opened, bounced)
- Automatic status update to 'sent' when email delivered

**Agent Method**:
```python
def send_invoice_email(self, invoice_number: str, recipient_email: str = None) -> str
```

### Recurring Invoices

**Motivation**: Automate billing for recurring services.

**Schema Addition**:
```sql
CREATE TABLE api.recurring_invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    template_invoice_id UUID REFERENCES api.invoices(id),
    frequency VARCHAR(20), -- monthly, quarterly, annually
    next_invoice_date DATE,
    active BOOLEAN DEFAULT true
);
```

**Agent Methods**:
```python
def create_recurring_invoice(self, invoice_number: str, frequency: str) -> str
def generate_next_recurring_invoice(self, recurring_invoice_id: str) -> str
```

### Payment Gateway Integration

**Motivation**: Accept online payments directly through invoices.

**Implementation**:
- Integrate with Stripe, Square, or PayPal
- Generate payment links for invoices
- Webhook handling for payment notifications
- Automatic status updates on payment receipt

**Agent Methods**:
```python
def generate_payment_link(self, invoice_number: str) -> str
def process_payment_webhook(self, webhook_data: dict) -> str
```

### Multi-Currency Support

**Motivation**: Support international clients with different currencies.

**Schema Changes**:
```sql
ALTER TABLE api.invoices ADD COLUMN currency VARCHAR(3) DEFAULT 'USD';
ALTER TABLE api.invoices ADD COLUMN exchange_rate DECIMAL(10,6);
```

**Implementation**:
- Currency conversion using exchange rate API
- Display amounts in client's preferred currency
- Store base currency and exchange rate for historical accuracy

### Invoice Templates

**Motivation**: Quickly create invoices from predefined templates.

**Schema Addition**:
```sql
CREATE TABLE api.invoice_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    template_name VARCHAR(100) NOT NULL,
    default_terms TEXT,
    default_notes TEXT,
    line_items JSONB
);
```

**Agent Method**:
```python
def create_invoice_from_template(self, template_name: str, client_name: str) -> str
```

### Analytics Dashboard

**Motivation**: Provide business insights from invoice data.

**Metrics**:
- Revenue trends over time
- Average invoice value
- Payment collection rate
- Overdue invoice tracking
- Client payment patterns

**Agent Methods**:
```python
def get_revenue_report(self, start_date: str, end_date: str) -> str
def get_overdue_invoices(self) -> str
def get_client_payment_history(self, client_name: str) -> str
```

### Audit Trail

**Motivation**: Track all changes to invoices for compliance and debugging.

**Schema Addition**:
```sql
CREATE TABLE api.invoice_audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID REFERENCES api.invoices(id),
    action VARCHAR(50), -- created, updated, deleted, status_changed
    changed_fields JSONB,
    old_values JSONB,
    new_values JSONB,
    changed_by UUID,
    changed_at TIMESTAMP DEFAULT NOW()
);
```

**Implementation**:
- Automatic logging on all invoice modifications
- Queryable audit history
- Compliance reporting

