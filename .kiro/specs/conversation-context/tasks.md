# Implementation Plan

- [ ] 1. Set up database integration and core conversation manager
  - Create ConversationManager class with Supabase client integration
  - Implement get_or_create_conversation method for conversation initialization
  - Implement load_context method with context window support
  - Implement add_message method for storing messages in JSONB array
  - _Requirements: 1.1, 2.1, 2.2, 3.2_

- [ ]* 1.1 Write property test for cross-channel message storage
  - **Property 1: Cross-channel message storage**
  - **Validates: Requirements 1.1**

- [ ]* 1.2 Write property test for message structure validation
  - **Property 6: Message structure validation**
  - **Validates: Requirements 2.1**

- [ ]* 1.3 Write property test for JSONB array storage
  - **Property 7: JSONB array storage**
  - **Validates: Requirements 2.2**

- [ ]* 1.4 Write property test for context window limiting
  - **Property 12: Context window limiting**
  - **Validates: Requirements 3.2, 3.5, 8.2**

- [ ] 2. Implement conversation metadata management
  - Implement associate_client method for client linking
  - Implement update_metadata method for status, priority, subject, tags
  - Add metadata update logic on message addition (last_message_at, last_message_from, unread_count)
  - _Requirements: 1.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 2.1 Write property test for client association storage
  - **Property 5: Client association storage**
  - **Validates: Requirements 1.5, 4.2**

- [ ]* 2.2 Write property test for status value validation
  - **Property 18: Status value validation**
  - **Validates: Requirements 5.2**

- [ ]* 2.3 Write property test for priority value validation
  - **Property 19: Priority value validation**
  - **Validates: Requirements 5.3**

- [ ]* 2.4 Write property test for metadata updates on message addition
  - **Property 20: Metadata updates on message addition**
  - **Validates: Requirements 5.4**

- [ ] 3. Integrate conversation manager with session manager
  - Modify S2SSessionManager to include ConversationManager
  - Implement create_session method to create associated conversation
  - Implement get_conversation_id method for session-to-conversation mapping
  - Implement load_session_context method to retrieve conversation history
  - _Requirements: 3.1, 8.3_

- [ ]* 3.1 Write property test for session-to-conversation mapping
  - **Property 24: Session-to-conversation mapping**
  - **Validates: Requirements 8.3**

- [ ]* 3.2 Write property test for session initialization with history
  - **Property 11: Session initialization with history**
  - **Validates: Requirements 3.1**

- [ ] 4. Integrate conversation context with supervisor agent
  - Modify SupervisorAgent to include ConversationManager
  - Update process_query method to load conversation context
  - Add user message storage before agent processing
  - Add assistant message storage after agent response
  - Ensure context is provided to agent during query processing
  - _Requirements: 1.2, 1.3, 1.4, 3.3, 3.4_

- [ ]* 4.1 Write property test for cross-channel context access
  - **Property 2: Cross-channel context access**
  - **Validates: Requirements 1.2, 6.2, 7.2**

- [ ]* 4.2 Write property test for equal treatment of messages
  - **Property 3: Equal treatment of messages**
  - **Validates: Requirements 1.3, 6.3, 6.4, 7.3, 7.5**

- [ ]* 4.3 Write property test for cross-session persistence
  - **Property 4: Cross-session persistence**
  - **Validates: Requirements 1.4**

- [ ]* 4.4 Write property test for multi-session continuity
  - **Property 13: Multi-session continuity**
  - **Validates: Requirements 3.3**

- [ ]* 4.5 Write property test for context provision to agents
  - **Property 14: Context provision to agents**
  - **Validates: Requirements 3.4, 7.4**

- [ ] 5. Implement message content handling for voice and text
  - Add content_type field to message structure (text or audio)
  - Implement voice transcription storage with content_type="audio"
  - Implement text message storage with content_type="text"
  - Ensure content preservation without modification
  - _Requirements: 2.3, 2.5, 6.1, 7.1_

- [ ]* 5.1 Write property test for optional metadata support
  - **Property 8: Optional metadata support**
  - **Validates: Requirements 2.3**

- [ ]* 5.2 Write property test for content preservation
  - **Property 10: Content preservation**
  - **Validates: Requirements 2.5**

- [ ]* 5.3 Write property test for voice transcription storage
  - **Property 22: Voice transcription storage**
  - **Validates: Requirements 6.1**

- [ ]* 5.4 Write property test for text message storage
  - **Property 23: Text message storage**
  - **Validates: Requirements 7.1**

- [ ] 6. Implement message ordering and chronological retrieval
  - Ensure messages are stored with ISO 8601 timestamps
  - Implement chronological sorting on message retrieval
  - Verify ordering works regardless of insertion order or content_type
  - _Requirements: 2.4_

- [ ]* 6.1 Write property test for chronological message ordering
  - **Property 9: Chronological message ordering**
  - **Validates: Requirements 2.4, 6.5**

- [ ] 7. Implement client association service
  - Create ClientAssociationService class
  - Implement identify_client method with fuzzy name matching
  - Implement link_conversation_to_client method
  - Query contacts table for client matches
  - Handle ambiguous matches gracefully
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ]* 7.1 Write property test for client query retrieval
  - **Property 15: Client query retrieval**
  - **Validates: Requirements 4.3**

- [ ]* 7.2 Write property test for separate conversations per client
  - **Property 16: Separate conversations per client**
  - **Validates: Requirements 4.4**

- [ ] 8. Implement conversation search functionality
  - Implement search_conversations method in ConversationManager
  - Support search by client name, subject, and message content
  - Implement JSONB content search within messages field
  - Add filtering by date range, client_id, status, and tags
  - Implement result ranking by relevance and recency
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 8.1 Write property test for search by multiple criteria
  - **Property 26: Search by multiple criteria**
  - **Validates: Requirements 9.1**

- [ ]* 8.2 Write property test for search result structure
  - **Property 27: Search result structure**
  - **Validates: Requirements 9.2**

- [ ]* 8.3 Write property test for JSONB content search
  - **Property 28: JSONB content search**
  - **Validates: Requirements 9.3**

- [ ]* 8.4 Write property test for search result ranking
  - **Property 29: Search result ranking**
  - **Validates: Requirements 9.4**

- [ ]* 8.5 Write property test for search filtering
  - **Property 30: Search filtering**
  - **Validates: Requirements 9.5**

- [ ] 9. Implement agent-aware context management
  - Add agent_name field to assistant messages
  - Implement agent-specific context filtering in load_context
  - Support loading full conversation history and agent-filtered history
  - Track which agent handled each message
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ]* 9.1 Write property test for agent-specific context filtering
  - **Property 31: Agent-specific context filtering**
  - **Validates: Requirements 10.1, 10.3**

- [ ]* 9.2 Write property test for agent tracking in messages
  - **Property 32: Agent tracking in messages**
  - **Validates: Requirements 10.2, 10.5**

- [ ]* 9.3 Write property test for dual context maintenance
  - **Property 33: Dual context maintenance**
  - **Validates: Requirements 10.4**

- [ ] 10. Implement pagination support for conversation retrieval
  - Add limit and offset parameters to load_context method
  - Implement pagination for search_conversations method
  - Ensure correct subset of messages returned with pagination
  - _Requirements: 8.4_

- [ ]* 10.1 Write property test for pagination support
  - **Property 25: Pagination support**
  - **Validates: Requirements 8.4**

- [ ] 11. Add configuration management for conversation settings
  - Create ConversationConfig dataclass
  - Load configuration from environment variables
  - Support configurable context window size
  - Support configurable cache TTL and search limits
  - _Requirements: 3.2, 3.5, 8.2_

- [ ] 12. Implement in-memory caching for conversation context
  - Create ConversationCache class with TTL support
  - Cache loaded conversations for performance
  - Invalidate cache on message addition and metadata updates
  - _Requirements: 8.5_

- [ ] 13. Add error handling and graceful degradation
  - Implement retry logic with exponential backoff for database errors
  - Add fallback to in-memory storage if database unavailable
  - Handle missing conversations gracefully (return empty context)
  - Validate message structure before insertion
  - Log all errors with context for monitoring
  - _Requirements: All (error handling)_

- [ ] 14. Integrate with voice input handling
  - Update handle_voice_input to store transcribed messages
  - Ensure content_type="audio" for voice messages
  - Link voice sessions to database conversations
  - Test voice-to-text switching with context preservation
  - _Requirements: 1.1, 6.1, 6.2_

- [ ] 15. Integrate with text input handling
  - Update text input handler to store text messages
  - Ensure content_type="text" for text messages
  - Link text sessions to database conversations
  - Test text-to-voice switching with context preservation
  - _Requirements: 1.1, 7.1, 7.2_

- [ ] 16. Update all specialized agents to use conversation context
  - Update EC2Agent to use ConversationManager
  - Update AWSResearcherAgent to use ConversationManager
  - Update InvoiceAgent to use ConversationManager
  - Ensure all agents receive conversation history during query processing
  - _Requirements: 3.4, 10.1_

- [ ] 17. Add monitoring and observability
  - Add metrics for conversation creation rate, message addition rate
  - Add metrics for context load time (p50, p95, p99)
  - Add metrics for search query time
  - Add metrics for database error rate and cache hit rate
  - Set up alerts for high error rates and slow queries
  - _Requirements: 8.1 (performance monitoring)_

- [ ] 18. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

