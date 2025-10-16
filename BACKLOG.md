# Prober Integration Backlog

**Status**: Planning / Not Implemented  
**Owner**: Unassigned  
**Priority**: Low (Future Enhancement)

---

## Overview

This document tracks planned integration between the docker-prober-utility and other OpenProject components (config-manager, deploy-manager).

**Current State**: Prober exists as standalone Flask service with NO integration.

**Goal**: Enable live validation and health monitoring within the deployment pipeline.

---

## Backlog Items

### 1. Config Manager Integration

**Epic**: Live Configuration Validation via Prober

**User Story**:  
As a DevOps engineer, I want config-manager to validate configurations against live endpoints, so I can catch deployment issues before they happen.

**Acceptance Criteria**:
- [ ] Config-manager can call prober HTTP endpoints
- [ ] Prober validates Docker daemon connectivity
- [ ] Prober checks port availability
- [ ] Prober validates network connectivity to required endpoints
- [ ] Results displayed in config-manager TUI
- [ ] Validation failures show actionable error messages

**Technical Tasks**:
- [ ] Create `prober_client.py` in config-manager
- [ ] Add prober HTTP client with retry logic
- [ ] Integrate with validation pipeline
- [ ] Add prober_enabled configuration flag (already exists as stub)
- [ ] Write unit tests for prober integration
- [ ] Update documentation with prober workflow

**Estimated Effort**: 6-8 hours

**Dependencies**:
- Prober must be running as service (Docker or standalone)
- Network connectivity between config-manager and prober
- Defined prober API contract

**Reference**:
- config-manager README mentions prober integration (lines 237-244)
- Stub parameter already exists: `prober_enabled=True`

---

### 2. Deploy Manager Integration

**Epic**: Pre-Deployment Validation via Prober

**User Story**:  
As a DevOps engineer, I want deploy-manager to run preflight checks via prober before deploying, so I can prevent deployment failures.

**Acceptance Criteria**:
- [ ] Deploy-manager calls prober before docker-compose up
- [ ] Prober validates system resources (disk, memory, CPU)
- [ ] Prober checks Docker daemon health
- [ ] Prober validates required ports are available
- [ ] Deployment blocked if preflight fails
- [ ] Option to skip preflight (`--no-prober` flag)
- [ ] Preflight results logged

**Technical Tasks**:
- [ ] Implement `ProberRunner.run_preflight()` (currently NotImplementedError)
- [ ] Add prober client library to deploy-manager
- [ ] Integrate with deployment pipeline
- [ ] Add `--no-prober` CLI flag
- [ ] Write unit tests
- [ ] Update documentation

**Estimated Effort**: 8-10 hours

**Dependencies**:
- Prober service running and accessible
- API contract for preflight checks
- Error handling for when prober unavailable

**Reference**:
- deploy-manager README mentions prober integration (lines 339-356)
- Stub class exists: `ProberRunner` in `prober_runner.py`

---

### 3. Prober API Standardization

**Epic**: Define Stable Prober API Contract

**User Story**:  
As an integrator, I need a stable API contract from prober, so I can reliably build integrations.

**Acceptance Criteria**:
- [ ] OpenAPI/Swagger specification for prober endpoints
- [ ] Versioned API (e.g., /v1/probe)
- [ ] Documented request/response schemas
- [ ] Error handling standardized
- [ ] Authentication mechanism (if needed)
- [ ] Rate limiting considerations

**Endpoints to Define**:
```
GET  /health                    → Service health check
GET  /probe                     → Full system probe
POST /probe/validate/ports      → Validate specific ports
POST /probe/validate/docker     → Validate Docker daemon
POST /probe/validate/resources  → Check system resources
GET  /probe/history             → Historical probe data
```

**Technical Tasks**:
- [ ] Create OpenAPI spec (swagger.yml)
- [ ] Implement versioned endpoints
- [ ] Add request validation
- [ ] Standardize error responses
- [ ] Add API documentation
- [ ] Create client library template

**Estimated Effort**: 4-6 hours

**Dependencies**: None

---

### 4. Prober as Python Package

**Epic**: Distribute Prober as Installable Package

**User Story**:  
As a developer, I want to `pip install docker-prober-utility`, so I can use it as a library or service.

**Acceptance Criteria**:
- [ ] Package structure follows Python best practices
- [ ] Installable via pip from GitHub releases
- [ ] Can run as CLI: `docker-prober --help`
- [ ] Can import as library: `from prober import ProberClient`
- [ ] Includes client library for integration
- [ ] Documentation on PyPI (or GitHub)

**Technical Tasks**:
- [x] Add pyproject.toml (DONE)
- [ ] Restructure code into proper package layout
- [ ] Create CLI entry point
- [ ] Create client library module
- [ ] Add __init__.py with exports
- [ ] Write package documentation
- [ ] Test installation workflow
- [ ] Create first release via GitHub Actions

**Estimated Effort**: 4-6 hours

**Dependencies**:
- pyproject.toml exists (completed)
- Build branch and GitHub Actions configured (completed)

---

### 5. Monitoring Dashboard

**Epic**: Web-Based Monitoring Dashboard

**User Story**:  
As a system administrator, I want a web dashboard showing real-time probe data, so I can monitor system health visually.

**Acceptance Criteria**:
- [ ] Web UI shows current probe data
- [ ] Real-time updates (WebSocket or polling)
- [ ] Historical data visualization (graphs)
- [ ] Alert thresholds configurable
- [ ] Export data to JSON/CSV
- [ ] Responsive design (mobile-friendly)

**Technical Tasks**:
- [ ] Create React/Vue frontend (or use Rich TUI in web)
- [ ] Add WebSocket support to Flask
- [ ] Create data persistence (SQLite/PostgreSQL)
- [ ] Build visualization components
- [ ] Add alert configuration
- [ ] Deploy as Docker service

**Estimated Effort**: 12-16 hours

**Priority**: Low (nice-to-have)

---

## Decision Points

### Question 1: Do we actually need prober integration?

**Considerations**:
- Current deployment works without it
- No user complaints about missing validation
- Adds complexity to the system
- Alternative: Use existing Docker/system tools

**Recommendation**: 
- Start with minimal integration (config-manager validation)
- Measure value before expanding
- Consider if native tools (docker inspect, etc.) suffice

### Question 2: Should prober be a service or library?

**Option A: Standalone Service**
- Pros: Language-agnostic, separate concerns, scalable
- Cons: Extra service to manage, network dependency

**Option B: Python Library**
- Pros: Direct integration, no service management, simpler
- Cons: Tight coupling, Python-only

**Recommendation**: Hybrid approach
- Library for simple cases (direct function calls)
- Service for production (separate process, monitoring)

### Question 3: When to implement?

**Trigger Criteria**:
1. User requests live validation feature
2. Deployment failures that prober would catch
3. Dedicated time for enhancement work
4. Clear ROI demonstrated

**Not a Priority If**:
- Current system working well
- No validation gaps identified
- Other features more important
- Limited development resources

---

## Implementation Phases

### Phase 1: Minimal Viable Integration (8 hours)
- Implement config-manager prober client
- Basic connectivity validation
- Error handling
- Documentation

### Phase 2: Deploy Manager Preflight (8 hours)
- Implement ProberRunner
- Pre-deployment validation
- CLI flag support
- Documentation

### Phase 3: API Standardization (4 hours)
- OpenAPI spec
- Versioned endpoints
- Client library

### Phase 4: Productionization (12 hours)
- Package distribution
- Monitoring dashboard
- Historical data
- Advanced features

**Total Estimated Effort**: 32+ hours

---

## Related Documentation

- Config Manager Integration Docs:
  - `external/config-manager/README.md` (lines 237-244)
  - Stub: `prober_client.py` (mentioned, not created)

- Deploy Manager Integration Docs:
  - `external/deploy-manager/README.md` (lines 339-356)
  - Stub: `prober_runner.py` (NotImplementedError)

- Main Orchestrator:
  - `src/openproject_orchestrator/tui_controller.py` (prober_enabled flags)
  - `src/openproject_orchestrator/coordinators/config_coordinator.py`

---

## Notes

**Last Updated**: October 16, 2025  
**Status**: Planning only - No implementation started  
**Next Review**: When integration need is identified  

**Questions/Feedback**: Create issue on GitHub

---

## Quick Start (When Implemented)

This is how integration WOULD work (future state):

```python
# In config-manager
from prober_client import ProberClient

prober = ProberClient("http://localhost:8080")
result = prober.validate_config(config_data)

if result.is_valid:
    print("✓ Configuration validated against live system")
else:
    print(f"✗ Validation failed: {result.errors}")
```

```python
# In deploy-manager
from prober import ProberRunner

runner = ProberRunner(prober_url="http://localhost:8080")
preflight = runner.run_preflight_check(deployment_config)

if not preflight.passed:
    raise PreflightError(f"Deployment blocked: {preflight.failures}")
```

Currently: **None of this exists** - it's all planned future work.
