# Lessons Learned: DB Agent Project

## Project Overview
This document captures the comprehensive lessons learned while building a CRUD Database Agent using PydanticAI, Supabase, and Docker. The project involved creating a natural language interface for database operations, implementing a complete Docker stack for Supabase, and integrating OpenAI's GPT models for AI-powered database interactions.

**Project Status**: ✅ **Successfully Completed** (2025-08-06)
**Final Architecture**: Middle Ground - Supabase client without complex authentication

## Executive Summary

The project successfully implemented a functional CRUD Database Agent with the following key achievements:
- Natural language interface for database operations using OpenAI GPT-4o-mini
- Simplified Supabase stack without authentication complexity
- Docker-based local development environment
- Modular CRUD tools using PydanticAI framework
- Comprehensive management scripts and documentation

## Table of Contents
1. [Architecture Decisions](#architecture-decisions)
2. [Docker & Container Orchestration](#docker--container-orchestration)
3. [PydanticAI Framework](#pydanticai-framework)
4. [Supabase Integration](#supabase-integration)
5. [Environment Configuration](#environment-configuration)
6. [Authentication & Authorization](#authentication--authorization)
7. [Testing & Debugging](#testing--debugging)
8. [Project Structure & Organization](#project-structure--organization)
9. [Development Workflow](#development-workflow)
10. [Key Takeaways](#key-takeaways)

---

## Architecture Decisions

### The Middle Ground Approach

**Problem**: Initial full Supabase stack with GoTrue authentication was overly complex for development, causing JWT token signing issues and service restart problems.

**Solution**: Implemented a "middle ground" approach that keeps the benefits of Supabase client SDK while removing authentication complexity.

**What We Kept**:
- ✅ Supabase client SDK for clean database operations
- ✅ PostgREST API for REST interface
- ✅ All CRUD tools using `ctx.deps` (Supabase client)
- ✅ Docker orchestration with management scripts
- ✅ Optional Supabase Studio for database management

**What We Removed**:
- ❌ GoTrue auth service (eliminated authentication complexity)
- ❌ Complex JWT validation and user management
- ❌ Auth-related database schemas and migrations
- ❌ User authentication requirements

**Lesson**: Sometimes the "middle ground" is the optimal solution - keeping the benefits of a framework while removing unnecessary complexity for the use case.

## Docker & Container Orchestration

### Key Lessons Learned

1. **Port Conflicts Are Common**: Always check for port conflicts before starting services. We had to change PostgREST from port 3000 to 3001 due to conflicts.

2. **Network Naming Consistency**: Ensure Docker Compose network names are consistent across all services. Mismatched network names cause service startup failures.

3. **Service Dependencies**: Use `depends_on` properly to ensure services start in the correct order. Database must be ready before API services.

4. **Volume Management**: Use named volumes for data persistence. Anonymous volumes can lead to data loss during container recreation.

5. **Management Scripts**: Create comprehensive management scripts (`docker-stack.sh`) for common operations:
   - Start/stop/restart services
   - View logs
   - Database setup
   - Cleanup operations

## PydanticAI Framework

### Key Insights

1. **Model Initialization**: OpenAI models in PydanticAI expect API keys in environment variables, not constructor parameters.
   ```python
   # Correct approach
   os.environ["OPENAI_API_KEY"] = api_key
   model = OpenAIModel(model_name)
   ```

2. **Agent Configuration**: The `Agent` class no longer supports `result_type` parameter in recent versions. Keep initialization simple:
   ```python
   agent = Agent(model=model, system_prompt=SYSTEM_PROMPT)
   ```

3. **Tool Registration**: Use the `@agent.tool()` decorator with retry configuration:
   ```python
   agent.tool(retries=3)(create_customer)
   ```

4. **Context Dependencies**: Use `RunContext[Client]` for typed dependencies, but be flexible about removing type hints if they cause issues.

5. **Async/Sync Handling**: PydanticAI handles async/sync conversion automatically. Use `agent.run_sync()` for synchronous execution.

## Supabase Integration

### Critical Lessons

1. **Client Configuration**: Supabase client works well with simple URL/key configuration:
   ```python
   supabase_url = "http://localhost:3001"  # PostgREST endpoint
   supabase_key = "not_needed_for_development"  # Dummy key for local dev
   ```

2. **PostgREST Configuration**: Key environment variables for PostgREST:
   - `PGRST_DB_URI`: PostgreSQL connection string
   - `PGRST_DB_SCHEMAS`: Database schemas to expose (usually "public")
   - `PGRST_DB_ANON_ROLE`: Database role for anonymous access
   - `PGRST_JWT_SECRET`: JWT secret (can be simple for development)

3. **Database Operations**: Supabase client provides clean, chainable API:
   ```python
   response = ctx.deps.table("customers").insert({...}).execute()
   ```

4. **Schema Management**: Create tables with proper constraints and indexes:
   ```sql
   CREATE TABLE customers (
       id SERIAL PRIMARY KEY,
       email TEXT UNIQUE NOT NULL,
       full_name TEXT NOT NULL,
       bio TEXT NOT NULL,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );
   ```

## Environment Configuration

### Best Practices

1. **Secure Secret Generation**: Use strong, randomly generated secrets for production:
   ```bash
   openssl rand -base64 32  # For JWT secrets
   openssl rand -hex 16     # For passwords
   ```

2. **Environment File Structure**: Organize `.env` files logically:
   ```bash
   # API Keys
   OPENAI_API_KEY=...
   
   # Database
   POSTGRES_PASSWORD=...
   POSTGRES_PORT=5432
   
   # Supabase
   SUPABASE_URL=http://localhost:3001
   SUPABASE_KEY=not_needed_for_development
   ```

3. **Development vs Production**: Use different configurations for different environments. Keep development simple, production secure.

## Authentication & Authorization

### Major Learning: Complexity vs Necessity

1. **GoTrue Complexity**: Full Supabase auth with GoTrue adds significant complexity:
   - JWT token management
   - User registration/login flows
   - Row Level Security (RLS) policies
   - Auth schema migrations

2. **Development Simplification**: For development and prototyping, authentication can be a barrier. Our middle ground approach:
   - Removed GoTrue service entirely
   - Used simple JWT secret for PostgREST
   - No user authentication required
   - Direct database access through PostgREST

3. **When to Add Auth**: Add authentication when:
   - Moving to production
   - Multiple users need access
   - Data security is critical
   - Compliance requirements exist

## Testing & Debugging

### Debugging Strategies

1. **Docker Logs**: Always check container logs for issues:
   ```bash
   docker-compose logs service_name
   ./docker-stack.sh logs
   ```

2. **Service Health Checks**: Verify services are responding:
   ```bash
   curl http://localhost:3001/customers  # PostgREST
   curl http://localhost:5432            # PostgreSQL (will fail, but shows port is open)
   ```

3. **Environment Variable Debugging**: Print environment variables to verify configuration:
   ```python
   print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
   ```

4. **Incremental Testing**: Test components individually:
   - Database connection
   - Supabase client initialization
   - Individual CRUD operations
   - Full agent workflow

## Project Structure & Organization

### Effective Patterns

1. **Modular Tool Structure**: Separate CRUD operations into individual files:
   ```
   tools/
   ├── __init__.py
   ├── create.py
   ├── retrieve.py
   ├── update.py
   └── delete.py
   ```

2. **Configuration Management**: Centralize configuration in dedicated files:
   - `.env` for environment variables
   - `database.py` for database utilities
   - `models.py` for data models

3. **Documentation Structure**: Maintain comprehensive documentation:
   - `README.md` for quick start and overview
   - `DOCKER_SETUP.md` for detailed Docker instructions
   - `lessonslearned.md` for project insights

4. **Management Scripts**: Create utility scripts for common operations:
   - `docker-stack.sh` for Docker management
   - `setup.py` for environment setup

## Development Workflow

### Recommended Process

1. **Start Simple**: Begin with minimal viable setup, add complexity gradually
2. **Test Early**: Verify each component works before integrating
3. **Document Everything**: Capture decisions, issues, and solutions immediately
4. **Version Control**: Commit frequently with descriptive messages
5. **Environment Consistency**: Use same tools and versions across development

## Key Takeaways

### Technical Insights

1. **Middle Ground Solutions**: Sometimes the optimal solution is between extremes - keeping framework benefits while removing unnecessary complexity.

2. **Docker Orchestration**: Container orchestration requires careful attention to networking, dependencies, and port management.

3. **AI Framework Integration**: Modern AI frameworks like PydanticAI are powerful but require understanding of their specific patterns and limitations.

4. **Database Abstraction**: Tools like Supabase provide excellent abstractions, but understanding the underlying technology (PostgreSQL, PostgREST) is crucial.

### Project Management Insights

1. **Iterative Development**: Start with a working prototype, then refine based on actual needs rather than anticipated requirements.

2. **Documentation Investment**: Time spent on documentation pays dividends in debugging, onboarding, and future development.

3. **Tooling Matters**: Good management scripts and automation significantly improve development experience.

4. **Flexibility Over Perfection**: Be willing to adapt the architecture based on practical constraints and requirements.

### Success Factors

1. **Clear Problem Definition**: Understanding exactly what needs to be built prevents over-engineering.

2. **Technology Evaluation**: Choosing the right balance of tools and complexity for the specific use case.

3. **Incremental Progress**: Building and testing components incrementally reduces debugging complexity.

4. **Comprehensive Testing**: Testing at multiple levels (unit, integration, end-to-end) catches issues early.

---

## Final Status

**Project Completion Date**: 2025-08-06
**Final Architecture**: Middle Ground Supabase Implementation
**Status**: ✅ Fully Functional
**Key Achievement**: Successfully balanced framework benefits with development simplicity

The DB Agent project demonstrates that thoughtful architecture decisions, comprehensive documentation, and iterative development can lead to successful AI-powered applications that are both functional and maintainable.

#### 1. **Docker Compose Version Deprecation**
- **Issue**: Docker Compose showed warnings about the `version` field being obsolete
- **Lesson**: Modern Docker Compose no longer requires the `version` field in docker-compose.yml
- **Solution**: Remove `version: '3.8'` from docker-compose.yml files
- **Impact**: Cleaner configuration files and no deprecation warnings

#### 2. **Service Dependencies and Startup Order**
- **Issue**: Services starting before their dependencies were ready
- **Lesson**: Use `depends_on` carefully - it only waits for container start, not service readiness
- **Solution**: Implement health checks and retry logic in application code
- **Best Practice**: Add startup delays and connection retry mechanisms

#### 3. **Kong API Gateway Configuration**
- **Issue**: Kong failed to start due to missing ACL plugin in configuration
- **Error**: `plugin 'acl' not enabled; add it to the 'plugins' configuration property`
- **Lesson**: Kong plugins must be explicitly enabled in environment variables
- **Solution**: Add all required plugins to `KONG_PLUGINS` environment variable
- **Configuration**: `KONG_PLUGINS: "key-auth,cors,acl"`

#### 4. **Volume Persistence Strategy**
- **Lesson**: Database data persistence requires careful volume mapping
- **Implementation**: Used `./volumes/db:/var/lib/postgresql/data` for PostgreSQL data
- **Best Practice**: Create volume directories before starting containers
- **Backup Strategy**: Volume data survives container restarts but not `docker-compose down -v`

#### 5. **Network Configuration**
- **Lesson**: Services need explicit network configuration for inter-service communication
- **Implementation**: Created dedicated `supabase` network with bridge driver
- **Benefit**: Isolated network namespace for security and service discovery

### Docker Management Script Insights

#### 1. **Automation Benefits**
- **Lesson**: Custom management scripts significantly improve developer experience
- **Implementation**: Created `docker-stack.sh` with commands for start, stop, status, logs
- **Features**: Color-coded output, error handling, and automated database setup
- **Impact**: Reduced setup complexity from multiple commands to single script execution

#### 2. **Secret Generation**
- **Lesson**: Automated secret generation improves security and reduces setup friction
- **Implementation**: Used `openssl rand -hex` for generating secure passwords and JWT secrets
- **Best Practice**: Generate different length secrets for different purposes (16 for passwords, 64 for JWT)

---

## PydanticAI Framework

### Key Lessons Learned

#### 1. **Model Initialization Patterns**
- **Issue**: OpenAI model initialization failed with `api_key` parameter
- **Error**: `OpenAIModel.__init__() got an unexpected keyword argument 'api_key'`
- **Lesson**: PydanticAI expects API keys to be set in environment variables, not constructor parameters
- **Solution**: Set `os.environ["OPENAI_API_KEY"]` before creating `OpenAIModel(model_name)`
- **Pattern**: Environment-first configuration approach

#### 2. **Agent Configuration Evolution**
- **Issue**: `result_type` parameter caused initialization errors
- **Error**: `Unknown keyword arguments: result_type`
- **Lesson**: PydanticAI API has evolved, some parameters are no longer supported
- **Solution**: Use minimal Agent configuration: `Agent(model=model, system_prompt=SYSTEM_PROMPT)`
- **Best Practice**: Check current documentation for supported parameters

#### 3. **Tool Registration Patterns**
- **Lesson**: Tools must be registered with the agent using decorators
- **Implementation**: `@agent.tool(retries=3)` decorator for each CRUD function
- **Best Practice**: Set appropriate retry counts for database operations
- **Error Handling**: Tools should return exceptions rather than raising them for better agent handling

#### 4. **Async/Sync Execution Models**
- **Issue**: Event loop conflicts when mixing async and sync code
- **Error**: `This event loop is already running`
- **Lesson**: Choose either fully async or fully sync execution model
- **Solution**: Used `agent.run_sync()` for synchronous execution in test scripts
- **Best Practice**: Avoid mixing async/await with synchronous test frameworks

#### 5. **System Prompt Design**
- **Lesson**: Clear, specific system prompts significantly improve agent performance
- **Implementation**: Detailed tool descriptions and expected behavior patterns
- **Best Practice**: Include examples of expected input/output formats
- **Impact**: Better natural language understanding and more accurate tool selection

---

## Supabase Integration

### Key Lessons Learned

#### 1. **Self-Hosted vs. Cloud Trade-offs**
- **Lesson**: Self-hosted Supabase provides full control but requires more setup complexity
- **Benefits**: No external dependencies, full data control, customizable configuration
- **Challenges**: Manual service orchestration, security configuration, backup management
- **Use Case**: Ideal for development, testing, and on-premises deployments

#### 2. **Service Architecture Understanding**
- **Lesson**: Supabase is a collection of microservices, each with specific roles
- **Components**: PostgreSQL (database), Kong (API gateway), GoTrue (auth), PostgREST (API), Realtime (websockets), Storage (files)
- **Dependencies**: Understanding service interdependencies crucial for troubleshooting
- **Monitoring**: Each service needs individual health monitoring

#### 3. **Database Schema Management**
- **Lesson**: Automated schema setup improves consistency and reduces manual errors
- **Implementation**: SQL scripts in Docker management tools for table creation
- **Security**: Proper role and permission setup essential for API access
- **Best Practice**: Create dedicated roles for different access levels (anon, authenticated, service_role)

#### 4. **API Key Management**
- **Lesson**: Supabase uses JWT-based API keys with different permission levels
- **Types**: `anon` (public), `service_role` (admin), custom roles
- **Security**: Keys must match JWT_SECRET used for signing
- **Best Practice**: Use environment variables for all API keys, never hardcode

#### 5. **Critical JWT Token Signing Issue**
- **Issue**: `JWSError JWSInvalidSignature` when using default/example JWT tokens
- **Root Cause**: Default JWT tokens in documentation are signed with different JWT_SECRET
- **Lesson**: JWT tokens MUST be signed with the same JWT_SECRET used by Supabase services
- **Solution**: Generate custom JWT tokens using your specific JWT_SECRET:
  ```python
  import jwt
  from datetime import datetime, timedelta
  
  payload = {
      'iss': 'supabase',
      'ref': 'stub', 
      'role': 'anon',  # or 'service_role'
      'iat': int(datetime.now().timestamp()),
      'exp': int((datetime.now() + timedelta(days=365*10)).timestamp())
  }
  token = jwt.encode(payload, jwt_secret, algorithm='HS256')
  ```
- **Impact**: This is a critical setup step that's often missed in documentation
- **Prevention**: Always generate JWT tokens after creating JWT_SECRET, never use defaults

#### 5. **Connection Patterns**
- **Lesson**: Different connection methods for different use cases
- **Direct PostgreSQL**: For administrative tasks and bulk operations
- **REST API**: For application-level CRUD operations
- **Realtime**: For live data synchronization
- **Choice**: REST API through Kong gateway provides best security and features

---

## Environment Configuration

### Key Lessons Learned

#### 1. **Environment Variable Hierarchy**
- **Lesson**: Clear environment variable organization prevents configuration errors
- **Structure**: Group related variables (database, JWT, API keys, ports)
- **Documentation**: Comment each variable with purpose and generation method
- **Validation**: Check for required variables at application startup

#### 2. **Secret Generation Best Practices**
- **Lesson**: Different secrets require different entropy levels
- **PostgreSQL Password**: 16-32 hex characters sufficient
- **JWT Secret**: 64+ hex characters for cryptographic security
- **API Keys**: Use provided Supabase defaults for development, generate new for production
- **Tools**: `openssl rand -hex N` provides cryptographically secure random values

#### 3. **Development vs. Production Configuration**
- **Lesson**: Separate configuration strategies needed for different environments
- **Development**: Use default/example values for quick setup
- **Production**: Generate unique secrets, use proper SSL, enable security features
- **Management**: Environment-specific .env files with clear naming conventions

---

## API Gateway & Kong

### Key Lessons Learned

#### 1. **Kong Configuration Complexity**
- **Lesson**: Kong requires detailed configuration for proper Supabase integration
- **Components**: Services, routes, plugins, consumers, ACLs
- **Challenge**: Configuration syntax is specific and error-prone
- **Solution**: Use proven configuration templates and validate thoroughly

#### 2. **Plugin Management**
- **Lesson**: Kong plugins must be explicitly enabled and properly configured
- **Required Plugins**: `key-auth` (authentication), `cors` (cross-origin), `acl` (access control)
- **Configuration**: Environment variable `KONG_PLUGINS` must list all used plugins
- **Debugging**: Plugin errors cause Kong startup failures with cryptic messages

#### 3. **Routing Strategy**
- **Lesson**: Proper route configuration essential for service accessibility
- **Pattern**: `/service/version/endpoint` routing structure
- **Security**: Different authentication requirements for different endpoints
- **Maintenance**: Route changes require Kong restart and configuration validation

---

## Testing & Debugging

### Key Lessons Learned

#### 1. **Async/Sync Testing Challenges**
- **Issue**: Mixing async and sync code in test suites causes event loop conflicts
- **Solution**: Choose consistent execution model throughout test suite
- **Best Practice**: Use `run_sync()` for testing async agents in synchronous test frameworks
- **Tools**: Avoid `asyncio.run()` in test scripts that import async libraries

#### 2. **Database Connection Testing**
- **Lesson**: Test database connectivity before running agent tests
- **Implementation**: Separate connection validation from business logic testing
- **Error Handling**: Graceful degradation when services are unavailable
- **Monitoring**: Log connection attempts and failures for debugging

#### 3. **Service Readiness Validation**
- **Lesson**: Container start doesn't guarantee service readiness
- **Solution**: Implement health checks and retry logic
- **Tools**: Use curl or custom scripts to validate service endpoints
- **Timing**: Allow sufficient startup time for complex services like Kong

#### 4. **Error Message Interpretation**
- **Lesson**: Framework-specific error messages require domain knowledge
- **PydanticAI**: Parameter errors indicate API changes or incorrect usage
- **Kong**: Configuration errors often relate to plugin or routing issues
- **Supabase**: Connection errors may indicate service startup order problems

---

## Project Structure & Organization

### Key Lessons Learned

#### 1. **Modular Architecture Benefits**
- **Lesson**: Separating concerns into modules improves maintainability
- **Structure**: `tools/` for CRUD operations, `models.py` for data structures, `database.py` for connections
- **Benefits**: Easier testing, clearer responsibilities, better code reuse
- **Maintenance**: Changes isolated to specific modules reduce regression risk

#### 2. **Configuration Management**
- **Lesson**: Centralized configuration management reduces errors
- **Implementation**: Single `.env` file with clear variable grouping
- **Documentation**: Comprehensive `.env.example` with generation instructions
- **Validation**: Startup-time validation of required configuration

#### 3. **Documentation Strategy**
- **Lesson**: Multiple documentation types serve different purposes
- **README.md**: Quick start and overview
- **DOCKER_SETUP.md**: Detailed technical setup
- **lessonslearned.md**: Knowledge capture and troubleshooting
- **Code Comments**: Implementation-specific details

---

## Security Considerations

### Key Lessons Learned

#### 1. **Development vs. Production Security**
- **Development**: Disabled RLS, default keys, open access for rapid iteration
- **Production**: Enable RLS, unique secrets, proper authentication, network isolation
- **Transition**: Clear checklist for moving from development to production configuration
- **Documentation**: Security implications clearly documented

#### 2. **API Key Management**
- **Lesson**: Different API keys have different security implications
- **Public Keys**: `anon` key can be exposed in client-side code
- **Private Keys**: `service_role` key must be kept secure, provides admin access
- **Rotation**: Plan for key rotation in production environments

#### 3. **Network Security**
- **Lesson**: Docker networks provide isolation but require proper configuration
- **Implementation**: Dedicated network for Supabase services
- **Exposure**: Only necessary ports exposed to host system
- **Monitoring**: Log access attempts and unusual patterns

---

## Performance & Optimization

### Key Lessons Learned

#### 1. **Container Resource Management**
- **Lesson**: Multiple services require careful resource allocation
- **Monitoring**: Track CPU, memory, and disk usage across all containers
- **Optimization**: Adjust container limits based on actual usage patterns
- **Scaling**: Plan for horizontal scaling of individual services

#### 2. **Database Performance**
- **Lesson**: PostgreSQL configuration affects overall system performance
- **Optimization**: Tune connection pools, query timeouts, and cache settings
- **Monitoring**: Track query performance and connection counts
- **Maintenance**: Regular database maintenance and optimization

#### 3. **API Response Times**
- **Lesson**: Multiple service hops can impact response times
- **Path**: Client → Kong → PostgREST → PostgreSQL
- **Optimization**: Minimize unnecessary middleware, optimize queries
- **Caching**: Implement appropriate caching strategies at each layer

---

## Development Workflow

### Key Lessons Learned

#### 1. **Iterative Development Approach**
- **Lesson**: Start with minimal working system, add complexity incrementally
- **Progression**: Basic agent → Database connection → Docker stack → Full integration
- **Benefits**: Easier debugging, faster feedback cycles, reduced complexity
- **Testing**: Validate each layer before adding the next

#### 2. **Error-Driven Development**
- **Lesson**: Framework errors provide valuable learning opportunities
- **Approach**: Understand error messages, research solutions, document findings
- **Knowledge Base**: Build internal documentation of common issues and solutions
- **Sharing**: Document solutions for team knowledge sharing

#### 3. **Tool Integration Strategy**
- **Lesson**: Choose tools that work well together and have good documentation
- **Evaluation**: Consider learning curve, community support, and long-term viability
- **Integration**: Test tool combinations early to identify compatibility issues
- **Alternatives**: Have backup plans for critical dependencies

---

## Recommendations for Future Projects

### 1. **Technology Stack Decisions**
- **PydanticAI**: Excellent for structured AI applications, but API is evolving rapidly
- **Supabase**: Great for rapid development, self-hosting adds complexity but provides control
- **Docker**: Essential for consistent development environments, invest in good tooling
- **Kong**: Powerful but complex, consider simpler alternatives for basic use cases

### 2. **Development Process**
- **Start Simple**: Begin with minimal viable system, add complexity gradually
- **Document Everything**: Capture decisions, errors, and solutions as you go
- **Automate Early**: Invest in automation scripts and tools from the beginning
- **Test Continuously**: Validate each component before integration

### 3. **Common Pitfalls to Avoid**
- **Framework Assumptions**: Don't assume API stability in rapidly evolving frameworks
- **Configuration Complexity**: Start with simple configurations, add features incrementally
- **Service Dependencies**: Plan for service startup order and failure scenarios
- **Environment Differences**: Test in production-like environments early and often

---

## Conclusion

Building the DB Agent project provided valuable insights into modern AI application development, containerization, and database integration. The key to success was maintaining a systematic approach to problem-solving, thorough documentation of issues and solutions, and building robust automation tools to manage complexity.

The combination of PydanticAI, Supabase, and Docker creates a powerful platform for AI-driven applications, but requires careful attention to configuration details, service dependencies, and security considerations. Future projects can benefit from the lessons learned here, particularly around error handling, testing strategies, and development workflow optimization.

---

*Last Updated: 2025-08-06*
*Project: DB Agent - CRUD Database Agent with PydanticAI*
*Technologies: PydanticAI, Supabase, Docker, Kong, OpenAI GPT*
