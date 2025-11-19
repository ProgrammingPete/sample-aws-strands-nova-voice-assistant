# Conversation Context Design

## Overview

The Conversation Context system provides seamless context management across voice and text interactions in the Voice-Based Painting Business Agent. It enables painting contractors to switch between voice and text input methods without losing conversation flow, maintaining continuity across sessions through persistent database storage.

The system leverages the existing `conversations` table in the Supabase database to store conversation history as JSONB message arrays. Each conversation maintains metadata including client associations, status, priority, and channel information. The design integrates with the AWS Strands multi-agent architecture, providing conversation history to agents through a sliding window context mechanism.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Voice/Text Interface                      │
│  (WebSocket Server + React Frontend)                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Conversation Manager                            │
│  - Load/Save Messages                                        │
│  - Context Window Management                                 │
│  - Client Association                                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Supabase Database                               │
│  conversations table (JSONB messages field)                  │
└─────────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Agent Integration                               │
│  - Supervisor Agent                                          │
│  - Specialized Agents (EC2, Invoice, etc.)                   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Message Input** (Voice or Text)
   - User provides input via WebSocket (voice) or text interface
   - Input is transcribed (if voice) and normalized to text

2. **Context Loading**
   - Conversation Manager retrieves conversation history from database
   - Applies sliding window to limit context size
   - Formats messages for agent consumption

3. **Agent Processing**
   - Agent receives conversation history + current query
   - Processes query with full context
   - Generates response

4. **Message Storage**
   - User message and agent response stored in database
   - Conversation metadata updated (last_message_at, unread_count)
   - Client association maintained if applicable

5. **Response Delivery**
   - Response sent to user via WebSocket (voice) or text
   - Conversation state persisted for next interaction


### Integration with Existing Architecture

The Conversation Context system integrates with the existing AWS Strands multi-agent architecture:

**Current Architecture**:
- `orchestrator.py`: Coordinates agent initialization and lifecycle
- `supervisor_agent.py`: Pure router that routes queries to specialized agents
- Specialized agents: `ec2_agent.py`, `aws_researcher_agent.py`, `invoice_agent.py`
- `conversation_config.py`: Manages conversation context per agent

**Integration Points**:
1. **Conversation Config Enhancement**: Extend `conversation_config.py` to load/save from database
2. **Agent Context Injection**: Provide conversation history to agents during query processing
3. **Session Management**: Link WebSocket sessions to database conversation records
4. **Client Association**: Integrate with invoice agent to identify and link clients

### Design Principles

1. **Persistence First**: All conversation data stored in database immediately
2. **Channel Agnostic**: Voice and text messages treated identically in storage
3. **Context Window**: Sliding window limits context size for performance
4. **Agent Awareness**: Track which agent handled each message
5. **Client Linking**: Associate conversations with clients for relationship tracking
6. **Session Continuity**: Support resuming conversations across sessions
7. **Performance**: Efficient querying with proper indexing and caching

## Components and Interfaces

### 1. Conversation Manager

**Purpose**: Central component for managing conversation lifecycle, context loading, and database operations.

**Location**: `backend/src/voice_based_aws_agent/config/conversation_manager.py` (new file)

**Responsibilities**:
- Load conversation history from database
- Save new messages to database
- Apply context window to limit message count
- Associate conversations with clients
- Update conversation metadata
- Provide conversation history to agents

**Interface**:

```python
class ConversationManager:
    def __init__(self, supabase_client, context_window_size=20):
        """
        Initialize conversation manager.
        
        Args:
            supabase_client: Supabase client instance
            context_window_size: Number of recent messages to include in context
        """
        
    async def get_or_create_conversation(
        self, 
        session_id: str,
        client_id: Optional[str] = None,
        channel: str = "voice"
    ) -> dict:
        """
        Get existing conversation or create new one.
        
        Args:
            session_id: WebSocket session identifier
            client_id: Optional client UUID
            channel: Communication channel (voice, text)
            
        Returns:
            Conversation record with id, messages, metadata
        """
        
    async def load_context(
        self, 
        conversation_id: str,
        agent_name: Optional[str] = None
    ) -> List[dict]:
        """
        Load conversation history with context window applied.
        
        Args:
            conversation_id: Conversation UUID
            agent_name: Optional filter for agent-specific messages
            
        Returns:
            List of message dicts with role, content, timestamp
        """
        
    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        agent_name: Optional[str] = None,
        content_type: str = "text"
    ) -> dict:
        """
        Add message to conversation and save to database.
        
        Args:
            conversation_id: Conversation UUID
            role: "user" or "assistant"
            content: Message text content
            agent_name: Agent that generated response (for assistant messages)
            content_type: "text" or "audio"
            
        Returns:
            Updated conversation record
        """
        
    async def associate_client(
        self,
        conversation_id: str,
        client_id: str,
        client_name: str
    ) -> dict:
        """
        Associate conversation with a client.
        
        Args:
            conversation_id: Conversation UUID
            client_id: Client UUID
            client_name: Client name for denormalization
            
        Returns:
            Updated conversation record
        """
        
    async def update_metadata(
        self,
        conversation_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        subject: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> dict:
        """
        Update conversation metadata.
        
        Args:
            conversation_id: Conversation UUID
            status: Conversation status
            priority: Conversation priority
            subject: Conversation subject
            tags: Conversation tags
            
        Returns:
            Updated conversation record
        """
        
    async def search_conversations(
        self,
        query: Optional[str] = None,
        client_id: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        limit: int = 50
    ) -> List[dict]:
        """
        Search conversations by various criteria.
        
        Args:
            query: Text search in subject or message content
            client_id: Filter by client
            status: Filter by status
            date_from: Filter by start date
            date_to: Filter by end date
            limit: Maximum results
            
        Returns:
            List of matching conversation records
        """
```

**Design Rationale**:
- Async methods for non-blocking database operations
- Context window applied at load time for performance
- Agent-specific filtering supports multi-agent architecture
- Client association supports relationship tracking
- Search functionality enables conversation discovery


### 2. Session Manager Integration

**Purpose**: Link WebSocket sessions to database conversation records.

**Location**: `backend/src/voice_based_aws_agent/utils/voice_integration/s2s_session_manager.py` (modify existing)

**Enhancements**:

```python
class S2SSessionManager:
    def __init__(self, conversation_manager: ConversationManager):
        """Add conversation manager to existing session manager."""
        self.conversation_manager = conversation_manager
        self.session_to_conversation = {}  # Map session_id -> conversation_id
        
    async def create_session(self, session_id: str, channel: str = "voice"):
        """
        Create session and associated conversation.
        
        Args:
            session_id: WebSocket session identifier
            channel: Communication channel (voice, text)
        """
        conversation = await self.conversation_manager.get_or_create_conversation(
            session_id=session_id,
            channel=channel
        )
        self.session_to_conversation[session_id] = conversation['id']
        
    async def get_conversation_id(self, session_id: str) -> Optional[str]:
        """Get conversation ID for session."""
        return self.session_to_conversation.get(session_id)
        
    async def load_session_context(self, session_id: str) -> List[dict]:
        """Load conversation history for session."""
        conversation_id = await self.get_conversation_id(session_id)
        if conversation_id:
            return await self.conversation_manager.load_context(conversation_id)
        return []
```

**Design Rationale**:
- Minimal changes to existing session manager
- Maps ephemeral sessions to persistent conversations
- Enables context loading for each session

### 3. Agent Context Provider

**Purpose**: Inject conversation history into agent processing.

**Location**: `backend/src/voice_based_aws_agent/agents/supervisor_agent.py` (modify existing)

**Enhancements**:

```python
class SupervisorAgent:
    def __init__(self, conversation_manager: ConversationManager):
        """Add conversation manager to supervisor agent."""
        self.conversation_manager = conversation_manager
        
    async def process_query(
        self, 
        query: str, 
        session_id: str,
        conversation_id: Optional[str] = None
    ) -> str:
        """
        Process query with conversation context.
        
        Args:
            query: User query text
            session_id: WebSocket session identifier
            conversation_id: Optional conversation UUID
            
        Returns:
            Agent response text
        """
        # Load conversation history
        if not conversation_id:
            conversation_id = await self.session_manager.get_conversation_id(session_id)
            
        context = await self.conversation_manager.load_context(conversation_id)
        
        # Add user message to conversation
        await self.conversation_manager.add_message(
            conversation_id=conversation_id,
            role="user",
            content=query,
            content_type="text"
        )
        
        # Process with context (existing agent logic)
        response = await self._route_to_agent(query, context)
        
        # Add assistant message to conversation
        await self.conversation_manager.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=response,
            agent_name=self.agent_name,
            content_type="text"
        )
        
        return response
```

**Design Rationale**:
- Transparent context injection into existing agent flow
- Automatic message persistence
- Supports both voice and text channels

### 4. Client Association Service

**Purpose**: Identify clients mentioned in conversations and link them.

**Location**: `backend/src/voice_based_aws_agent/services/client_association.py` (new file)

**Interface**:

```python
class ClientAssociationService:
    def __init__(self, supabase_client, conversation_manager: ConversationManager):
        """Initialize client association service."""
        self.supabase = supabase_client
        self.conversation_manager = conversation_manager
        
    async def identify_client(self, message_content: str) -> Optional[dict]:
        """
        Identify client from message content.
        
        Args:
            message_content: User message text
            
        Returns:
            Client record if identified, None otherwise
        """
        # Search for client names in message
        # Query contacts table for matches
        # Return best match based on confidence
        
    async def link_conversation_to_client(
        self,
        conversation_id: str,
        message_content: str
    ) -> Optional[dict]:
        """
        Identify and link client to conversation.
        
        Args:
            conversation_id: Conversation UUID
            message_content: User message text
            
        Returns:
            Updated conversation record if client linked
        """
        client = await self.identify_client(message_content)
        if client:
            return await self.conversation_manager.associate_client(
                conversation_id=conversation_id,
                client_id=client['id'],
                client_name=client['name']
            )
        return None
```

**Design Rationale**:
- Automatic client identification from natural language
- Fuzzy matching for name variations
- Optional linking (doesn't block conversation flow)

## Data Models

### Message Structure

Messages are stored in the `conversations.messages` JSONB field as an array:

```json
[
  {
    "role": "user",
    "content": "I need a quote for painting my house",
    "timestamp": "2024-01-15T10:30:00Z",
    "content_type": "text",
    "message_id": "msg_abc123"
  },
  {
    "role": "assistant",
    "content": "I'd be happy to help you with a painting quote...",
    "timestamp": "2024-01-15T10:30:15Z",
    "content_type": "text",
    "agent_name": "supervisor_agent",
    "message_id": "msg_def456"
  }
]
```

**Field Definitions**:
- `role`: "user" or "assistant"
- `content`: Message text (transcribed if from voice)
- `timestamp`: ISO 8601 timestamp with timezone
- `content_type`: "text" or "audio" (indicates original input method)
- `agent_name`: Agent that generated response (assistant messages only)
- `message_id`: Unique identifier for message (optional)

### Conversation Record

The `conversations` table record structure (from database schema):

```python
{
    "id": "uuid",
    "client_id": "uuid or null",
    "client_name": "string or null",
    "subject": "string or null",
    "channel": "voice | text | email | phone",
    "status": "open | pending | resolved | closed",
    "priority": "low | normal | high | urgent",
    "assigned_to": "string or null",
    "messages": [...],  # JSONB array
    "last_message_at": "timestamp",
    "last_message_from": "user | assistant",
    "unread_count": 0,
    "tags": ["tag1", "tag2"],
    "notes": "string or null",
    "created_at": "timestamp",
    "updated_at": "timestamp"
}
```

### Context Window Model

The context window limits the number of messages provided to agents:

```python
class ContextWindow:
    def __init__(self, size: int = 20):
        """
        Initialize context window.
        
        Args:
            size: Maximum number of messages to include
        """
        self.size = size
        
    def apply(self, messages: List[dict]) -> List[dict]:
        """
        Apply sliding window to messages.
        
        Args:
            messages: Full message history
            
        Returns:
            Most recent N messages
        """
        return messages[-self.size:] if len(messages) > self.size else messages
```

**Design Rationale**:
- Configurable window size per agent
- Simple sliding window (most recent N messages)
- Prevents context overflow in agent processing
- Default 20 messages balances context and performance


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After reviewing all testable criteria from the prework, I've identified the following consolidations to eliminate redundancy:

**Consolidations:**
1. **Cross-channel context access** (1.2, 6.2, 7.2): All test that switching input methods preserves context access - can be combined into one property
2. **Equal treatment of messages** (1.3, 6.3, 6.4, 7.3, 7.5): All test that voice and text messages are treated equally - can be combined
3. **Context provision to agents** (3.4, 7.4): Both test that agents receive conversation history - can be combined
4. **Context window limiting** (3.2, 3.5, 8.2): All test the sliding window mechanism - can be combined
5. **Chronological ordering** (2.4, 6.5): Both test message ordering - can be combined
6. **Agent tracking** (10.2, 10.5): Both test agent_name storage - can be combined
7. **Agent-specific filtering** (10.1, 10.3): Both test filtering by agent - can be combined

**Remaining Unique Properties:**
- Cross-channel message storage (1.1)
- Cross-session persistence (1.4)
- Client association (1.5, 4.2)
- Message structure validation (2.1)
- JSONB storage format (2.2)
- Optional metadata support (2.3)
- Content preservation (2.5)
- Session initialization (3.1)
- Multi-session continuity (3.3)
- Client identification (4.1 - example)
- Client query (4.3)
- Separate conversations per client (4.4)
- Metadata initialization (5.1)
- Status validation (5.2)
- Priority validation (5.3)
- Metadata updates (5.4)
- Tag storage (5.5)
- Voice transcription storage (6.1)
- Text storage (7.1)
- Session-to-conversation mapping (8.3)
- Pagination (8.4)
- Search functionality (9.1)
- Search result structure (9.2)
- JSONB search (9.3)
- Result ranking (9.4)
- Search filters (9.5)
- Agent context maintenance (10.4)

### Correctness Properties

Property 1: Cross-channel message storage
*For any* conversation, when messages are added via voice or text input, all messages SHALL be stored in the conversations table with the correct content_type marker (text or audio)
**Validates: Requirements 1.1**

Property 2: Cross-channel context access
*For any* conversation with mixed voice and text messages, when loading context for either input method, all previous messages SHALL be retrieved regardless of their original content_type
**Validates: Requirements 1.2, 6.2, 7.2**

Property 3: Equal treatment of messages
*For any* conversation with mixed voice and text messages, when loading context or processing queries, the system SHALL treat voice and text messages identically without filtering by content_type
**Validates: Requirements 1.3, 6.3, 6.4, 7.3, 7.5**

Property 4: Cross-session persistence
*For any* conversation, when a session ends and a new session begins, the conversation history SHALL be loaded from the database and made available to agents
**Validates: Requirements 1.4**

Property 5: Client association storage
*For any* conversation that is linked to a client, the client_id and client_name SHALL be stored in the conversations table
**Validates: Requirements 1.5, 4.2**

Property 6: Message structure validation
*For any* message stored in a conversation, the message SHALL contain fields for role (user or assistant), content (text), and timestamp (ISO 8601 with timezone)
**Validates: Requirements 2.1**

Property 7: JSONB array storage
*For any* conversation, the messages SHALL be stored as a JSONB array in the messages field
**Validates: Requirements 2.2**

Property 8: Optional metadata support
*For any* message, the system SHALL support storing optional metadata fields (agent_name, content_type, message_id) without requiring them
**Validates: Requirements 2.3**

Property 9: Chronological message ordering
*For any* conversation, when messages are retrieved, they SHALL be ordered chronologically by timestamp regardless of insertion order or content_type
**Validates: Requirements 2.4, 6.5**

Property 10: Content preservation
*For any* message stored in a conversation, the content text SHALL be preserved exactly as provided without modification
**Validates: Requirements 2.5**

Property 11: Session initialization with history
*For any* new session associated with an existing conversation, the conversation history SHALL be retrieved from the database during session initialization
**Validates: Requirements 3.1**

Property 12: Context window limiting
*For any* conversation with more messages than the context window size, when loading context, only the most recent N messages SHALL be returned (where N is the window size)
**Validates: Requirements 3.2, 3.5, 8.2**

Property 13: Multi-session continuity
*For any* conversation that spans multiple sessions, all messages from all sessions SHALL be accessible when loading conversation history
**Validates: Requirements 3.3**

Property 14: Context provision to agents
*For any* agent processing a query, the agent SHALL receive the conversation history from the database as part of the query context
**Validates: Requirements 3.4, 7.4**

Property 15: Client query retrieval
*For any* client with associated conversations, when querying conversations by client_id, all conversations linked to that client SHALL be returned
**Validates: Requirements 4.3**

Property 16: Separate conversations per client
*For any* client with multiple conversations, each conversation SHALL maintain a separate conversation record with distinct conversation_id
**Validates: Requirements 4.4**

Property 17: Metadata initialization
*For any* newly created conversation, the fields subject, channel, status, priority, and assigned_to SHALL be initialized (even if NULL)
**Validates: Requirements 5.1**

Property 18: Status value validation
*For any* conversation, the status field SHALL only accept values from the set: open, pending, resolved, closed
**Validates: Requirements 5.2**

Property 19: Priority value validation
*For any* conversation, the priority field SHALL only accept values from the set: low, normal, high, urgent
**Validates: Requirements 5.3**

Property 20: Metadata updates on message addition
*For any* conversation, when a new message is added, the fields last_message_at, last_message_from, and unread_count SHALL be updated accordingly
**Validates: Requirements 5.4**

Property 21: Tag array storage
*For any* conversation, the tags field SHALL support storing an array of zero or more tag strings
**Validates: Requirements 5.5**

Property 22: Voice transcription storage
*For any* voice input message, the transcribed text SHALL be stored in the message content field with content_type set to "audio"
**Validates: Requirements 6.1**

Property 23: Text message storage
*For any* text input message, the text SHALL be stored in the message content field with content_type set to "text"
**Validates: Requirements 7.1**

Property 24: Session-to-conversation mapping
*For any* active session, the system SHALL maintain a mapping from session_id to conversation_id and retrieve the correct conversation for that session
**Validates: Requirements 8.3**

Property 25: Pagination support
*For any* conversation history retrieval with pagination parameters (limit, offset), the system SHALL return the correct subset of messages
**Validates: Requirements 8.4**

Property 26: Search by multiple criteria
*For any* search query with criteria (client name, subject, or message content), the system SHALL return conversations matching any of the specified criteria
**Validates: Requirements 9.1**

Property 27: Search result structure
*For any* search result, the result SHALL include conversation metadata (id, subject, client_name, status, created_at) and relevant message excerpts
**Validates: Requirements 9.2**

Property 28: JSONB content search
*For any* search query targeting message content, the system SHALL search within the JSONB messages array and return conversations containing matching content
**Validates: Requirements 9.3**

Property 29: Search result ranking
*For any* search with multiple matching conversations, results SHALL be ordered by relevance (match quality) and recency (last_message_at)
**Validates: Requirements 9.4**

Property 30: Search filtering
*For any* search query with filters (date range, client_id, status, tags), the system SHALL return only conversations matching all specified filters
**Validates: Requirements 9.5**

Property 31: Agent-specific context filtering
*For any* agent processing a query, when agent-specific context is requested, the system SHALL filter conversation history to include only messages where agent_name matches or role is "user"
**Validates: Requirements 10.1, 10.3**

Property 32: Agent tracking in messages
*For any* assistant message, the agent_name field SHALL be stored to track which agent generated the response
**Validates: Requirements 10.2, 10.5**

Property 33: Dual context maintenance
*For any* conversation with multiple agents involved, the system SHALL maintain both the full conversation history and agent-specific filtered histories
**Validates: Requirements 10.4**


## Error Handling

### Database Errors

1. **Connection Failures**
   - Retry with exponential backoff (3 attempts)
   - Fall back to in-memory conversation storage
   - Log error and alert monitoring
   - Graceful degradation: continue without persistence

2. **Query Errors**
   - Validate conversation_id format before queries
   - Handle missing conversation records gracefully
   - Return empty context if conversation not found
   - Log malformed queries for debugging

3. **JSONB Validation Errors**
   - Validate message structure before insertion
   - Reject malformed messages with clear error
   - Preserve existing messages if update fails
   - Log validation failures

4. **Constraint Violations**
   - Handle foreign key violations (invalid client_id)
   - Validate status/priority values before insertion
   - Return validation errors to caller
   - Don't crash on constraint violations

### Application Errors

1. **Session Management Errors**
   - Handle missing session_id gracefully
   - Create new conversation if mapping not found
   - Clean up orphaned session mappings
   - Log session lifecycle events

2. **Context Loading Errors**
   - Return empty context if load fails
   - Don't block agent processing on context errors
   - Log context loading failures
   - Retry once on transient errors

3. **Client Association Errors**
   - Handle ambiguous client matches
   - Log failed client identifications
   - Don't block conversation on association failures
   - Allow manual client linking

4. **Message Storage Errors**
   - Retry message insertion once
   - Log failed message storage
   - Continue conversation even if storage fails
   - Queue failed messages for retry

### Error Recovery Strategies

1. **Graceful Degradation**
   - Continue without persistence if database unavailable
   - Use in-memory storage as fallback
   - Restore from database when available
   - Minimize user impact

2. **Retry Logic**
   - Exponential backoff for transient errors
   - Maximum 3 retry attempts
   - Different strategies for read vs write
   - Circuit breaker for repeated failures

3. **Fallback Mechanisms**
   - In-memory conversation storage
   - Reduced context window on performance issues
   - Skip optional features (client association, search)
   - Maintain core functionality

4. **Monitoring and Alerting**
   - Log all errors with context
   - Alert on repeated failures
   - Track error rates and patterns
   - Dashboard for conversation health

## Testing Strategy

### Dual Testing Approach

The Conversation Context system will be validated using both unit tests and property-based tests to ensure comprehensive coverage:

- **Unit tests** verify specific examples, edge cases, and integration points
- **Property-based tests** verify universal properties that should hold across all inputs
- Together they provide comprehensive coverage: unit tests catch concrete bugs, property tests verify general correctness

### Unit Testing

**Conversation Manager Tests**:
- Create new conversation with valid parameters
- Load existing conversation by ID
- Add messages to conversation
- Associate conversation with client
- Update conversation metadata
- Search conversations by various criteria

**Session Manager Integration Tests**:
- Create session and associated conversation
- Map session to conversation
- Load context for session
- Handle session cleanup

**Agent Context Provider Tests**:
- Inject context into agent processing
- Store user and assistant messages
- Handle missing conversation gracefully
- Filter context by agent name

**Client Association Tests**:
- Identify client from message content
- Link conversation to client
- Handle ambiguous matches
- Handle no matches

**Edge Cases**:
- Empty conversation (no messages)
- Conversation with single message
- Conversation exceeding context window
- Conversation with all voice messages
- Conversation with all text messages
- Conversation with mixed voice/text
- Conversation with no client association
- Conversation with multiple client mentions

**Integration Tests**:
- End-to-end conversation flow (create, add messages, load context)
- Cross-session persistence (create conversation, end session, start new session, verify context)
- Multi-agent conversation (multiple agents, verify agent-specific context)
- Client association workflow (mention client, verify linking)

### Property-Based Testing

**Property-Based Testing Library**: We will use **Hypothesis** for Python-based property testing, as it integrates well with pytest and provides excellent support for database testing.

**Configuration**: Each property-based test will run a minimum of 100 iterations to ensure thorough coverage of the input space.

**Test Tagging**: Each property-based test will be tagged with a comment explicitly referencing the correctness property from the design document using this format: `# Feature: conversation-context, Property {number}: {property_text}`

**Property Tests**:

1. **Property 1: Cross-channel message storage**
   - Generate random conversation with mixed voice/text messages
   - Store in database
   - Verify all messages have correct content_type
   - Tag: `# Feature: conversation-context, Property 1: Cross-channel message storage`

2. **Property 2: Cross-channel context access**
   - Generate random conversation with mixed voice/text messages
   - Load context for voice session
   - Load context for text session
   - Verify both loads return all messages
   - Tag: `# Feature: conversation-context, Property 2: Cross-channel context access`

3. **Property 3: Equal treatment of messages**
   - Generate random conversation with mixed voice/text messages
   - Load context without filtering
   - Verify no messages are excluded based on content_type
   - Tag: `# Feature: conversation-context, Property 3: Equal treatment of messages`

4. **Property 4: Cross-session persistence**
   - Generate random conversation
   - Simulate session end
   - Simulate new session start
   - Verify all messages are loaded
   - Tag: `# Feature: conversation-context, Property 4: Cross-session persistence`

5. **Property 6: Message structure validation**
   - Generate random messages with required fields
   - Store in conversation
   - Retrieve and verify structure
   - Tag: `# Feature: conversation-context, Property 6: Message structure validation`

6. **Property 9: Chronological message ordering**
   - Generate random messages with random timestamps
   - Insert in random order
   - Retrieve and verify chronological order
   - Tag: `# Feature: conversation-context, Property 9: Chronological message ordering`

7. **Property 10: Content preservation**
   - Generate random message content (including special characters, unicode)
   - Store in conversation
   - Retrieve and verify exact match
   - Tag: `# Feature: conversation-context, Property 10: Content preservation`

8. **Property 12: Context window limiting**
   - Generate conversation with N messages (N > window size)
   - Load context with window size W
   - Verify exactly W most recent messages returned
   - Tag: `# Feature: conversation-context, Property 12: Context window limiting`

9. **Property 18: Status value validation**
   - Generate conversation with valid status
   - Verify storage succeeds
   - Generate conversation with invalid status
   - Verify storage fails or is rejected
   - Tag: `# Feature: conversation-context, Property 18: Status value validation`

10. **Property 19: Priority value validation**
    - Generate conversation with valid priority
    - Verify storage succeeds
    - Generate conversation with invalid priority
    - Verify storage fails or is rejected
    - Tag: `# Feature: conversation-context, Property 19: Priority value validation`

11. **Property 20: Metadata updates on message addition**
    - Generate conversation
    - Add message
    - Verify last_message_at, last_message_from, unread_count updated
    - Tag: `# Feature: conversation-context, Property 20: Metadata updates on message addition`

12. **Property 24: Session-to-conversation mapping**
    - Generate random session_id
    - Create conversation for session
    - Retrieve conversation by session_id
    - Verify correct conversation returned
    - Tag: `# Feature: conversation-context, Property 24: Session-to-conversation mapping`

13. **Property 26: Search by multiple criteria**
    - Generate conversations with known content
    - Search by client name, subject, message content
    - Verify matching conversations returned
    - Tag: `# Feature: conversation-context, Property 26: Search by multiple criteria`

14. **Property 30: Search filtering**
    - Generate conversations with various attributes
    - Apply filters (date range, client_id, status, tags)
    - Verify only matching conversations returned
    - Tag: `# Feature: conversation-context, Property 30: Search filtering`

15. **Property 31: Agent-specific context filtering**
    - Generate conversation with multiple agents
    - Load context filtered by agent_name
    - Verify only relevant messages returned
    - Tag: `# Feature: conversation-context, Property 31: Agent-specific context filtering`

### Test Data Generation

**Generators for Property-Based Tests**:
- Conversation ID generator (valid UUIDs)
- Session ID generator (random strings)
- Message generator (role, content, timestamp, metadata)
- Client ID generator (valid UUIDs)
- Status generator (valid and invalid values)
- Priority generator (valid and invalid values)
- Tag array generator (0-10 tags)
- Timestamp generator (ISO 8601 with timezone)
- Content generator (text with special characters, unicode, long strings)

**Test Database**:
- Use separate test database instance
- Reset database state between test runs
- Use transactions for test isolation
- Seed with minimal required data (test clients)

### Performance Testing

**Context Loading Performance**:
- Measure load time for various conversation sizes
- Verify context window reduces load time
- Test with realistic message counts (100-1000 messages)
- Ensure sub-100ms load time for typical conversations

**Search Performance**:
- Measure search time for various query types
- Verify JSONB indexing improves search performance
- Test with realistic conversation counts (1000-10000 conversations)
- Ensure sub-500ms search time for typical queries

**Message Storage Performance**:
- Measure insertion time for messages
- Test concurrent message additions
- Verify no performance degradation with large conversations
- Ensure sub-50ms insertion time

**Database Query Optimization**:
- Use EXPLAIN ANALYZE to verify index usage
- Identify slow queries and optimize
- Monitor query performance in production
- Set up alerts for slow queries


## Implementation Notes

### Database Schema Integration

The Conversation Context system uses the existing `conversations` table from the database schema:

**Table**: `api.conversations`

**Key Fields**:
- `id` (UUID): Primary key
- `client_id` (UUID): Foreign key to contacts table
- `client_name` (TEXT): Denormalized client name
- `subject` (TEXT): Conversation subject
- `channel` (TEXT): Communication channel (voice, text, email, phone)
- `status` (TEXT): Conversation status (open, pending, resolved, closed)
- `priority` (TEXT): Priority level (low, normal, high, urgent)
- `assigned_to` (TEXT): Team member assigned
- `messages` (JSONB): Array of message objects
- `last_message_at` (TIMESTAMPTZ): Timestamp of last message
- `last_message_from` (TEXT): Who sent last message (user or assistant)
- `unread_count` (INTEGER): Number of unread messages
- `tags` (TEXT[]): Conversation tags
- `notes` (TEXT): Internal notes
- `created_at` (TIMESTAMPTZ): Creation timestamp
- `updated_at` (TIMESTAMPTZ): Last update timestamp

**Indexes** (from database schema):
- Primary key on `id`
- Index on `client_id` (foreign key)
- Index on `status`
- Index on `priority`
- Index on `channel`
- Index on `last_message_at`
- Index on `created_at`

**Foreign Keys**:
- `client_id` REFERENCES `contacts(id)` ON DELETE SET NULL

### Supabase Client Integration

**Connection Setup**:

```python
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """
    Create Supabase client from environment variables.
    
    Environment variables:
    - SUPABASE_URL: Supabase project URL
    - SUPABASE_KEY: Supabase API key
    """
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)
```

**Query Patterns**:

```python
# Insert conversation
conversation = supabase.table('conversations').insert({
    'channel': 'voice',
    'status': 'open',
    'messages': []
}).execute()

# Load conversation
conversation = supabase.table('conversations').select('*').eq('id', conversation_id).single().execute()

# Update messages (append new message)
messages = conversation.data['messages']
messages.append(new_message)
supabase.table('conversations').update({
    'messages': messages,
    'last_message_at': new_message['timestamp'],
    'last_message_from': new_message['role'],
    'updated_at': 'now()'
}).eq('id', conversation_id).execute()

# Search conversations
results = supabase.table('conversations').select('*').ilike('subject', f'%{query}%').execute()
```

### Configuration Management

**Environment Variables**:

```bash
# Supabase connection
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-api-key

# Conversation settings
CONVERSATION_CONTEXT_WINDOW_SIZE=20
CONVERSATION_CACHE_TTL=300  # 5 minutes
CONVERSATION_SEARCH_LIMIT=50
```

**Configuration File** (`backend/src/voice_based_aws_agent/config/conversation_config.py`):

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ConversationConfig:
    """Configuration for conversation context management."""
    
    # Context window size (number of messages)
    context_window_size: int = 20
    
    # Cache TTL in seconds
    cache_ttl: int = 300
    
    # Search result limit
    search_limit: int = 50
    
    # Enable client association
    enable_client_association: bool = True
    
    # Enable agent-specific filtering
    enable_agent_filtering: bool = True
    
    @classmethod
    def from_env(cls) -> 'ConversationConfig':
        """Load configuration from environment variables."""
        return cls(
            context_window_size=int(os.getenv('CONVERSATION_CONTEXT_WINDOW_SIZE', 20)),
            cache_ttl=int(os.getenv('CONVERSATION_CACHE_TTL', 300)),
            search_limit=int(os.getenv('CONVERSATION_SEARCH_LIMIT', 50)),
            enable_client_association=os.getenv('ENABLE_CLIENT_ASSOCIATION', 'true').lower() == 'true',
            enable_agent_filtering=os.getenv('ENABLE_AGENT_FILTERING', 'true').lower() == 'true'
        )
```

### Caching Strategy

**In-Memory Cache**:

```python
from typing import Dict, Optional
from datetime import datetime, timedelta

class ConversationCache:
    """Simple in-memory cache for recent conversations."""
    
    def __init__(self, ttl: int = 300):
        self.cache: Dict[str, tuple[dict, datetime]] = {}
        self.ttl = ttl
        
    def get(self, conversation_id: str) -> Optional[dict]:
        """Get conversation from cache if not expired."""
        if conversation_id in self.cache:
            conversation, timestamp = self.cache[conversation_id]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return conversation
            else:
                del self.cache[conversation_id]
        return None
        
    def set(self, conversation_id: str, conversation: dict):
        """Store conversation in cache."""
        self.cache[conversation_id] = (conversation, datetime.now())
        
    def invalidate(self, conversation_id: str):
        """Remove conversation from cache."""
        if conversation_id in self.cache:
            del self.cache[conversation_id]
```

**Cache Usage**:
- Cache loaded conversations for 5 minutes
- Invalidate cache on message addition
- Invalidate cache on metadata updates
- Don't cache search results (too variable)

### Migration from Existing System

**Current State**:
- Each agent has its own `ConversationManager` (from `conversation_config.py`)
- Conversations stored in memory only
- No persistence across sessions
- No client association

**Migration Steps**:

1. **Phase 1: Add Database Persistence**
   - Implement `ConversationManager` with database backend
   - Keep existing in-memory fallback
   - Test with single agent (supervisor)

2. **Phase 2: Integrate with Session Manager**
   - Link WebSocket sessions to database conversations
   - Test session-to-conversation mapping
   - Verify cross-session persistence

3. **Phase 3: Agent Integration**
   - Update all agents to use new `ConversationManager`
   - Test agent-specific context filtering
   - Verify multi-agent conversations

4. **Phase 4: Client Association**
   - Implement client identification service
   - Test automatic client linking
   - Add manual client linking UI

5. **Phase 5: Search and Discovery**
   - Implement conversation search
   - Add search UI to frontend
   - Test search performance

**Backward Compatibility**:
- Keep existing `ConversationManager` interface
- Add database backend as optional parameter
- Fall back to in-memory if database unavailable
- Gradual rollout per agent

### Voice Integration Specifics

**Transcription Handling**:

```python
async def handle_voice_input(audio_data: bytes, session_id: str):
    """
    Handle voice input with transcription and storage.
    
    Args:
        audio_data: Raw audio bytes
        session_id: WebSocket session identifier
    """
    # Transcribe audio using Nova Sonic
    transcription = await transcribe_audio(audio_data)
    
    # Get conversation for session
    conversation_id = await session_manager.get_conversation_id(session_id)
    
    # Store transcribed message
    await conversation_manager.add_message(
        conversation_id=conversation_id,
        role="user",
        content=transcription,
        content_type="audio"
    )
    
    # Process with agent
    response = await supervisor_agent.process_query(
        query=transcription,
        session_id=session_id,
        conversation_id=conversation_id
    )
    
    return response
```

**Voice Response Truncation**:
- Voice responses truncated to 800 characters (existing behavior)
- Full response stored in database
- Truncation only for TTS output
- User can request full response via text

### Security Considerations

**Data Privacy**:
- Conversation data contains sensitive business information
- Implement row-level security (RLS) in Supabase
- Encrypt sensitive fields if needed
- Audit access to conversation data

**Access Control**:
- Authenticate all database requests
- Use Supabase RLS policies for multi-tenant scenarios
- Limit conversation access to authorized users
- Log all conversation access

**Data Retention**:
- Implement conversation archival policy
- Delete old conversations after retention period
- Support GDPR data export and deletion
- Maintain audit trail of deletions

### Monitoring and Observability

**Metrics to Track**:
- Conversation creation rate
- Message addition rate
- Context load time (p50, p95, p99)
- Search query time (p50, p95, p99)
- Database error rate
- Cache hit rate
- Average conversation length
- Average messages per conversation

**Logging**:
- Log all conversation lifecycle events
- Log all database errors with context
- Log client association attempts
- Log search queries and results
- Use structured logging (JSON format)

**Alerts**:
- Alert on high database error rate
- Alert on slow context loading
- Alert on failed message storage
- Alert on cache misses exceeding threshold

### Future Enhancements

**Potential Improvements**:

1. **Conversation Summarization**
   - Summarize long conversations for context
   - Store summaries in conversation metadata
   - Use summaries for older messages outside window

2. **Semantic Search**
   - Implement vector embeddings for messages
   - Enable semantic search across conversations
   - Find similar conversations

3. **Conversation Analytics**
   - Track conversation metrics (duration, message count, resolution time)
   - Identify common topics and patterns
   - Generate insights for business improvement

4. **Multi-User Conversations**
   - Support multiple users in single conversation
   - Track participant list
   - Handle concurrent message additions

5. **Conversation Branching**
   - Support branching conversations (what-if scenarios)
   - Link related conversations
   - Merge conversation branches

6. **Real-Time Collaboration**
   - Use Supabase Realtime for live updates
   - Show typing indicators
   - Notify on new messages

## Appendix

### Example Conversation Flow

**Scenario**: User asks about a painting project via voice, then switches to text

1. **Voice Input** (Session 1)
   ```
   User (voice): "What's the status of the Johnson house project?"
   → Transcribed: "What's the status of the Johnson house project?"
   → Stored: {role: "user", content: "What's the status...", content_type: "audio"}
   
   Assistant: "The Johnson house project is currently in progress..."
   → Stored: {role: "assistant", content: "The Johnson house...", agent_name: "supervisor_agent"}
   ```

2. **Session Ends**
   - WebSocket connection closed
   - Conversation persisted in database
   - Session mapping cleared

3. **Text Input** (Session 2)
   ```
   User (text): "When will it be completed?"
   → Stored: {role: "user", content: "When will it be completed?", content_type: "text"}
   
   Context Loaded:
   - Previous voice message: "What's the status..."
   - Previous assistant response: "The Johnson house..."
   - Current text message: "When will it be completed?"
   
   Assistant: "Based on the current progress, the Johnson house project should be completed by..."
   → Stored: {role: "assistant", content: "Based on the current...", agent_name: "supervisor_agent"}
   ```

4. **Client Association**
   - System identifies "Johnson" in messages
   - Queries contacts table for matching client
   - Links conversation to Johnson client record
   - Updates conversation.client_id and conversation.client_name

### Glossary Reference

All terms defined in the requirements glossary apply to this design document. Key terms:
- **Voice_Assistant**: The complete voice-based painting business assistant application
- **Conversation_Context**: The historical record of messages and interactions
- **Conversation_History**: The complete sequence of messages stored in the database
- **Message**: A single unit of communication with role, content, and metadata
- **JSONB_Messages_Field**: PostgreSQL JSONB field storing message arrays
- **Context_Window**: The number of recent messages provided to agents (default 20)
- **Cross_Session_Context**: Conversation history persisting across mul