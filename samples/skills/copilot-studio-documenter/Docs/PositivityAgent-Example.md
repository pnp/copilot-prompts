# Positivity Agent

**Solution Name:** PositivityAgent  
**Version:** 1.0.0.0  
**Publisher:** Paul Bullock  
**Display Name:** Positivity Agent (MCS)

## Overview

Positivity Agent is a Microsoft Copilot Studio agent designed to generate positive statements and help users find motivational quotes to build a positive mindset. The agent provides supportive, uplifting, and empathetic responses to foster user confidence and self-esteem through daily motivation and encouragement.

## Agent Metadata

- **Agent Schema Name:** `ca_agent`
- **Authentication Mode:** 2 (Azure AD)
- **Authentication Trigger:** 1
- **Language:** English (1033)
- **Generative AI:** Enabled
- **Generative Actions:** Enabled
- **Agent Connectable:** Yes

## AI Configuration

The agent leverages advanced AI capabilities:

- **GPT Settings:** Uses default schema `ca_agent.gpt.default`
- **Model Knowledge:** Enabled
- **File Analysis:** Enabled
- **Semantic Search:** Enabled
- **Latest Models:** Disabled (uses stable versions)
- **Recognizer:** Generative AI Recognizer

## GPT Instructions

### System Prompt

The agent operates under the following core instructions:

```
You are an agent to generate positive statements, to help a user find a quote they can use in their day to build a positive mindset.

- Provide positive and motivational responses to user queries.
- Encourage users to build their confidence through supportive and uplifting messages.
- Avoid negative or discouraging language.
- Offer practical advice and tips for maintaining a positive mindset.
- Respond in a friendly, warm, gentle and empathetic tone.

Ensure all interactions are aimed at boosting the user's self-esteem and motivation.
```

### Conversation Starters

The agent offers six predefined conversation starters to guide user interactions:

1. **Motivational Quote** - "Can you share a motivational quote with me?"
2. **Confidence Boost** - "I need a confidence boost. Can you help?"
3. **Positive Mindset** - "How can I maintain a positive mindset?"
4. **Overcoming Challenges** - "I'm facing a challenge. Can you give me some advice?"
5. **Daily Motivation** - "Can you give me some daily motivation?"
6. **Encouragement** - "I need some encouragement. What can you say to lift my spirits?"

## Topics

The agent includes the following built-in conversation topics (topics control conversation flow and dialog branches):

### Standard Topics

| Topic | Purpose |
|-------|---------|
| ConversationStart | Initiates the conversation session |
| Greeting | Welcomes the user and sets a positive tone |
| Signin | Handles user authentication |
| Search | Enables topic routing based on user intent |
| SessionSlides_LbnEorler25kkywv6MWRf | Manages session-specific slide presentations |
| SessionTranscription_Pc97p0Dqh2doJctvkg6tf | Handles session transcription and recording |
| ThankYou | Provides gratitude and closing message |
| Goodbye | Concludes the conversation |
| MultipleTopicsMatched | Routes conversation when multiple topics match user intent |
| Fallback | Default response when no topic matches |
| Escalate | Transfers conversation to human support |
| OnError | Handles errors during conversation |
| ResetConversation | Allows users to restart the conversation |
| EndofConversation | Marks conversation completion |

## Agent Components

### Total Components

The agent contains 14 core topics and 1 GPT instruction component, organized under the customization prefix `ca_agent`.

### External Actions

The agent includes 1 external action component:

- **MicrosoftLearnDocsMCP-MicrosoftLearnDocsMCPServer** - Integration with Microsoft Learn documentation MCP (Model Context Protocol) server for knowledge retrieval

## External Integrations

### Connection References

The agent has no explicit external service connections configured in Customizations.xml. The solution contains minimal customizations and relies primarily on built-in Copilot Studio capabilities.

### Knowledge Sources

No external unstructured file search entities or Dataverse table search configurations are currently configured for this agent.

## Architecture Notes

- **Scope:** Single-agent implementation (no multi-agent orchestration)
- **Customization Prefix:** `ca` (derived from publisher prefix `pkb`)
- **Solution Type:** Unmanaged (suitable for source control)
- **Last Synchronized:** 2026-01-28T21:49:07.843452Z
- **Provisioning Status:** Provisioned
- **Synchronization State:** Synchronized

## Use Cases

The Positivity Agent is ideal for:

- **Employee Wellness Programs** - Providing daily motivation and mental health support
- **Student Support Services** - Offering encouragement and confidence building during stressful periods
- **Corporate Wellness Initiatives** - Supporting positive workplace culture
- **Personal Development** - Helping individuals develop resilience and maintain mental health
- **Motivational Support** - Delivering instant access to motivational quotes and positive guidance

## Deployment Considerations

- The agent uses Azure AD authentication and is production-ready
- Conversations are tracked and synchronized with Copilot Studio backend
- The agent supports semantic search and file analysis for enhanced responses
- All interactions are aimed at positive reinforcement and user empowerment
