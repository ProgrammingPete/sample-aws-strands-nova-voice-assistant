# Requirements Document

## Introduction

The Voice-Based Painting Business Agent is a real-time voice assistant that enables painting contractors to manage their business operations through natural speech. The system uses Amazon Nova Sonic for voice processing, AWS Bedrock for AI reasoning, and a multi-agent architecture to handle different types of painting business queries. Users can speak to the system to manage client contacts, schedule painting appointments, handle project proposals, manage customer reviews, coordinate marketing campaigns, track painting projects and invoices, and configure system settings.

## Glossary

- **Voice_Assistant**: The complete voice-based painting business assistant application
- **Agent_Orchestrator**: The central coordinator that manages the lifecycle of all agents, sets up the environment, and provides the main query processing interface
- **Supervisor_Agent**: The routing agent that directs user queries to appropriate specialized agents
- **Contacts_Agent**: Specialized agent that handles client contact management and customer relationship operations for painting business
- **Projects_Agent**: Specialized agent that manages painting projects including specifications, timelines, costs, and completion tracking
- **Appointments_Agent**: Specialized agent that manages scheduling and calendar operations for painting consultations and project work
- **Proposals_Agent**: Specialized agent that handles painting project proposal creation, tracking, and management
- **Invoices_Agent**: Specialized agent that manages invoice generation, payment tracking, and billing operations for painting projects
- **Reviews_Agent**: Specialized agent that manages customer reviews and feedback for completed painting projects
- **Marketing_Agent**: Specialized agent that handles marketing campaigns and promotional activities for painting services
- **Tasks_Agent**: Specialized agent that manages project-related tasks and to-do items for painting work
- **Settings_Agent**: Specialized agent that manages system configuration, business goals, and user preferences
- **Voice_Session**: An active conversation where the user can speak and receive voice responses
- **WebSocket_Connection**: A persistent, full-duplex communication protocol that enables real-time, bidirectional data exchange between client and server over a single TCP connection, allowing for low-latency streaming of audio data and instant message delivery
- **Audio_Processing**: Converting speech to text and text back to speech
- **Query_Routing**: Determining which agent should handle a user's request
- **User_Authentication**: The process of verifying user identity and establishing secure sessions
- **Data_Isolation**: Security mechanism ensuring users can only access their own business data
- **Row_Level_Security**: Database security feature that filters query results based on user permissions

## Requirements

### Requirement 1

**User Story:** As a painting contractor, I want to start voice conversations with the business assistant, so that I can manage my painting business operations through speech.

#### Acceptance Criteria

1. WHEN a user clicks the start conversation button, THE Voice_Assistant SHALL establish a WebSocket connection and begin capturing audio
2. WHEN a user speaks during an active session, THE Voice_Assistant SHALL process the speech and convert it to text
3. WHEN a user clicks end conversation, THE Voice_Assistant SHALL stop audio capture and close the connection
4. WHEN connection errors occur, THE Voice_Assistant SHALL display error messages and offer restart options
5. WHEN a session is active, THE Voice_Assistant SHALL show visual indicators of the conversation state

### Requirement 2

**User Story:** As a painting contractor, I want my queries routed to the right business specialist, so that I get accurate responses for different types of painting business operations.

#### Acceptance Criteria

1. WHEN a user asks about client contacts or customers, THE Supervisor_Agent SHALL route the query to the Contacts_Agent
2. WHEN a user asks about painting projects or job details, THE Supervisor_Agent SHALL route the query to the Projects_Agent
3. WHEN a user asks about scheduling or appointments, THE Supervisor_Agent SHALL route the query to the Appointments_Agent
4. WHEN a user asks about proposals or estimates, THE Supervisor_Agent SHALL route the query to the Proposals_Agent
5. WHEN a user asks about invoices or billing, THE Supervisor_Agent SHALL route the query to the Invoices_Agent
6. WHEN a user asks about reviews or customer feedback, THE Supervisor_Agent SHALL route the query to the Reviews_Agent
7. WHEN a user asks about marketing or promotional campaigns, THE Supervisor_Agent SHALL route the query to the Marketing_Agent
8. WHEN a user asks about tasks or to-do items, THE Supervisor_Agent SHALL route the query to the Tasks_Agent
9. WHEN a user asks about settings, goals, or configuration, THE Supervisor_Agent SHALL route the query to the Settings_Agent
10. WHEN routing occurs, THE Supervisor_Agent SHALL pass the original query unchanged to the selected agent
11. WHEN an agent responds, THE Supervisor_Agent SHALL return the response without modification

### Requirement 3

**User Story:** As a painting contractor, I want to hear spoken responses from the system, so that I can have natural voice conversations while working on job sites.

#### Acceptance Criteria

1. WHEN an agent generates a text response, THE Voice_Assistant SHALL convert it to speech
2. WHEN speech is generated, THE Voice_Assistant SHALL play the audio through the user's speakers
3. WHEN a user speaks during playback, THE Voice_Assistant SHALL stop the audio and process the new input
4. WHEN speech conversion fails, THE Voice_Assistant SHALL display the text response instead
5. WHEN receiving multiple audio pieces, THE Voice_Assistant SHALL play them smoothly in sequence

### Requirement 4

**User Story:** As a painting contractor, I want to manage client contacts and customer relationships with voice commands, so that I can handle customer interactions hands-free while on job sites.

#### Acceptance Criteria

1. WHEN a user asks about contact information, THE Contacts_Agent SHALL retrieve and report contact details including name, email, phone, company, address, and notes
2. WHEN a user requests to create or update contacts, THE Contacts_Agent SHALL modify the contacts table and confirm completion
3. WHEN a user asks about contact relationships, THE Contacts_Agent SHALL report associated projects, appointments, proposals, reviews, and conversations
4. WHEN contact operations fail, THE Contacts_Agent SHALL provide clear error messages and suggest corrections
5. WHEN searching contacts, THE Contacts_Agent SHALL support queries by name, company, email, phone, or tags

### Requirement 5

**User Story:** As a painting contractor, I want to manage painting projects through voice commands, so that I can track job specifications, timelines, costs, and completion status hands-free.

#### Acceptance Criteria

1. WHEN a user asks about painting projects, THE Projects_Agent SHALL retrieve project details including name, client, status, location, paint specifications, dates, costs, and completion percentage
2. WHEN a user requests to create projects, THE Projects_Agent SHALL create projects with client information, paint specifications (type, brand, color, coats, primer), square footage, and budget
3. WHEN project status updates are requested, THE Projects_Agent SHALL update status to pending, in-progress, completed, cancelled, or on-hold
4. WHEN project cost tracking is needed, THE Projects_Agent SHALL track estimated cost, actual cost, and budget with variance calculations
5. WHEN projects are linked to clients, THE Projects_Agent SHALL maintain client relationships and report associated invoices, appointments, and tasks

### Requirement 6

**User Story:** As a painting contractor, I want to schedule and manage appointments by voice, so that I can coordinate client consultations and painting work without manual calendar management.

#### Acceptance Criteria

1. WHEN a user asks about appointments, THE Appointments_Agent SHALL retrieve appointment details including date, time, location, client information, appointment type, and status
2. WHEN a user requests to schedule appointments, THE Appointments_Agent SHALL create appointments with title, client, date, start/end times, location, and type (consultation, estimate, painting work)
3. WHEN scheduling conflicts occur, THE Appointments_Agent SHALL check existing appointments and suggest alternative times
4. WHEN appointment status changes are requested, THE Appointments_Agent SHALL update status to scheduled, confirmed, in-progress, completed, cancelled, no-show, or rescheduled
5. WHEN appointments are linked to painting projects, THE Appointments_Agent SHALL maintain the project relationship and report project context

### Requirement 7

**User Story:** As a painting contractor, I want to create and track project proposals through voice commands, so that I can manage painting estimates and bids efficiently.

#### Acceptance Criteria

1. WHEN a user asks about proposals, THE Proposals_Agent SHALL retrieve proposal details including title, client, description, scope of work, pricing sections, amounts, and status
2. WHEN a user requests to create proposals, THE Proposals_Agent SHALL generate painting proposals with client information, scope of work, pricing sections, terms and conditions
3. WHEN proposal status updates are requested, THE Proposals_Agent SHALL update status to draft, sent, viewed, accepted, rejected, or expired
4. WHEN proposal calculations are needed, THE Proposals_Agent SHALL compute subtotal, tax amounts, discounts, and total amounts
5. WHEN proposals are linked to clients, THE Proposals_Agent SHALL maintain client relationships and auto-populate client details

### Requirement 8

**User Story:** As a painting contractor, I want to manage invoices and billing through voice commands, so that I can handle payment tracking for completed painting projects.

#### Acceptance Criteria

1. WHEN a user asks about invoices, THE Invoices_Agent SHALL retrieve invoice details including invoice number, client, project, amounts, payment status, and due dates
2. WHEN a user requests to create invoices, THE Invoices_Agent SHALL generate invoices with client information, project reference, line items, and payment terms
3. WHEN invoice calculations are needed, THE Invoices_Agent SHALL compute subtotal, tax amounts, discounts, total amount, amount paid, and balance due
4. WHEN payment tracking is requested, THE Invoices_Agent SHALL update amount paid, paid date, and automatically calculate balance due
5. WHEN invoice status updates are needed, THE Invoices_Agent SHALL update status to draft, sent, viewed, partial, paid, overdue, or cancelled

### Requirement 9

**User Story:** As a painting contractor, I want to manage customer reviews and feedback by voice, so that I can respond to customer input about completed painting projects promptly.

#### Acceptance Criteria

1. WHEN a user asks about reviews, THE Reviews_Agent SHALL retrieve review details including rating (1-5), title, review text, platform, and status
2. WHEN a user requests to respond to reviews, THE Reviews_Agent SHALL create response text and update the response_date and responded_by fields
3. WHEN review analytics are requested, THE Reviews_Agent SHALL calculate average ratings, sentiment analysis, and review trends for painting projects
4. WHEN reviews are linked to painting projects, THE Reviews_Agent SHALL report project context and client information
5. WHEN review status updates are needed, THE Reviews_Agent SHALL update status to pending, approved, published, responded, or flagged

### Requirement 10

**User Story:** As a painting contractor, I want to coordinate marketing activities through voice commands, so that I can manage promotional campaigns for my painting services efficiently.

#### Acceptance Criteria

1. WHEN a user asks about campaigns, THE Marketing_Agent SHALL retrieve campaign details including name, type, status, dates, budget, and performance metrics
2. WHEN a user requests campaign performance, THE Marketing_Agent SHALL report sent count, delivered count, open rate, click rate, conversion rate, and ROI
3. WHEN campaign creation is requested, THE Marketing_Agent SHALL create painting service campaigns with target audience, budget, content, and scheduling information
4. WHEN campaign status updates are needed, THE Marketing_Agent SHALL update status to draft, scheduled, active, paused, completed, or cancelled
5. WHEN campaign analytics are requested, THE Marketing_Agent SHALL calculate revenue generated, cost effectiveness, and provide optimization recommendations

### Requirement 11

**User Story:** As a painting contractor, I want to manage project tasks through voice commands, so that I can track to-do items and work assignments for painting jobs.

#### Acceptance Criteria

1. WHEN a user asks about tasks, THE Tasks_Agent SHALL retrieve task details including title, description, project, client, status, priority, assigned person, and due date
2. WHEN a user requests to create tasks, THE Tasks_Agent SHALL create tasks with project or client linkage, priority level, assignment, and due dates
3. WHEN task status updates are requested, THE Tasks_Agent SHALL update status to todo, in-progress, completed, or cancelled
4. WHEN tasks are linked to painting projects, THE Tasks_Agent SHALL maintain project relationships and report project context
5. WHEN task checklists are needed, THE Tasks_Agent SHALL manage checklist items within tasks for detailed work tracking

### Requirement 12

**User Story:** As a painting contractor, I want to configure system settings through voice commands, so that I can customize the assistant for my painting business needs.

#### Acceptance Criteria

1. WHEN a user asks about current settings, THE Settings_Agent SHALL retrieve and report configuration status
2. WHEN a user requests setting changes, THE Settings_Agent SHALL update configurations and confirm changes
3. WHEN invalid settings are provided, THE Settings_Agent SHALL validate input and suggest corrections
4. WHEN settings affect other agents, THE Settings_Agent SHALL coordinate updates across the system
5. WHEN settings backup is requested, THE Settings_Agent SHALL export and store configuration data

### Requirement 13

**User Story:** As a painting contractor, I want to send text messages directly to the supervisor agent from the frontend, so that I can interact with the system through both voice and text input methods.

#### Acceptance Criteria

1. WHEN a user types a text message in the frontend interface, THE Voice_Assistant SHALL send the text directly to the Supervisor_Agent
2. WHEN text input is received, THE Supervisor_Agent SHALL process the text query and route it to the appropriate specialized agent
3. WHEN a text query is processed, THE Voice_Assistant SHALL display the response as text in the chat interface
4. WHEN both voice and text modes are available, THE Voice_Assistant SHALL allow users to switch between input methods seamlessly
5. WHEN text input is used, THE Voice_Assistant SHALL maintain the same routing and response logic as voice input

### Requirement 14

**User Story:** As a painting contractor, I want voice and text conversations to share the same context, so that I can seamlessly continue conversations regardless of input method.

#### Acceptance Criteria

1. WHEN a user switches from voice to text input, THE Voice_Assistant SHALL store messages in the conversations table and maintain context
2. WHEN a user switches from text to voice input, THE Voice_Assistant SHALL retrieve conversation history from the messages JSONB field
3. WHEN conversation context is maintained, THE Voice_Assistant SHALL reference previous messages stored in the database regardless of input method
4. WHEN agents process queries, THE Voice_Assistant SHALL provide conversation history from the database to maintain context across sessions
5. WHEN conversations are linked to clients, THE Voice_Assistant SHALL associate conversation records with the appropriate client_id for relationship tracking

### Requirement 15

**User Story:** As a painting contractor, I want to track business goals through voice commands, so that I can monitor my painting business performance and progress.

#### Acceptance Criteria

1. WHEN a user asks about business goals, THE Settings_Agent SHALL retrieve and report goals including target values, current progress, and completion percentages
2. WHEN goal tracking is requested, THE Settings_Agent SHALL update current_value and automatically calculate progress_percentage
3. WHEN goal status updates are needed, THE Settings_Agent SHALL update status to active, completed, cancelled, or overdue
4. WHEN goal analytics are requested, THE Settings_Agent SHALL calculate progress trends and provide recommendations for achieving targets
5. WHEN goals are tracked over time, THE Settings_Agent SHALL maintain historical progress data for performance analysis

