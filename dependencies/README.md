# Dependencies - Prober Service

This directory contains dependency tracking for the Prober service component.

## Files

### Documentation
- **`DEPENDENCIES.md`** - Service monitoring and probing dependencies

## Purpose

The Prober service provides system monitoring and health checking:
- Host information collection
- Service availability monitoring
- Performance metrics gathering
- System health reporting

## Dependency Categories

### Production Dependencies
- **Absolute**: Required for monitoring
  - Python runtime and Flask framework
  - System monitoring libraries (psutil, etc.)
  - Network utilities for connectivity testing
  
- **Ad-Hoc**: Context-dependent
  - Database drivers (for database monitoring)
  - Cloud monitoring APIs (for cloud deployments)
  - Alert notification services (email, Slack, etc.)

### Developer Dependencies
- **Absolute**: Required for development
  - Python development tools
  - Testing frameworks (pytest, etc.)
  - Debugging utilities
  
- **Ad-Hoc**: Optional development tools
  - Performance profiling tools
  - Load testing utilities
  - Monitoring dashboard tools

## Service Architecture

The Prober runs as a lightweight Flask service:
- **REST API** for health check endpoints
- **Background tasks** for continuous monitoring
- **Data collection** from various system sources
- **Reporting** to external monitoring systems

## Monitoring Capabilities

- **Host Information**: CPU, memory, disk usage
- **Service Health**: Container status, port availability
- **Network Connectivity**: External service reachability
- **Performance Metrics**: Response times, throughput
- **Custom Probes**: Configurable health checks

## Integration

- **Used by**: Main orchestration for system health
- **Calls**: System APIs and external services
- **Exposes**: REST endpoints for health data
- **Monitors**: All OpenProject components