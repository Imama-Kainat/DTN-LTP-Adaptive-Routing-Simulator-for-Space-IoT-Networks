# 🛰️ DTN-LTP Adaptive Routing Simulator

## Table of Contents
- [What Is This Project?](#what-is-this-project)
- [Real-World Problem It Solves](#real-world-problem-it-solves)
- [Key Concepts Explained Simply](#key-concepts-explained-simply)
- [How The System Works](#how-the-system-works)
- [Technical Architecture](#technical-architecture)
- [Installation & Setup](#installation--setup)
- [Running the Simulator](#running-the-simulator)
- [Understanding the Results](#understanding-the-results)
- [Research Applications](#research-applications)
- [Live Applications](https://dtn-ltp-adaptive-routing-simulator.streamlit.app/)

---

## What Is This Project?

Imagine you're trying to send a text message from Earth to a Mars rover. Unlike your regular phone network:
- **The connection isn't always available** (planets rotate, satellites move)
- **Delays are huge** (messages take 4-24 minutes one way)
- **Links break frequently** (objects move out of range)
- **No immediate confirmation** (can't know if message arrived for many minutes)

This simulator models exactly these challenging networks! It's a **Delay/Disruption Tolerant Network (DTN)** with **Licklider Transmission Protocol (LTP)** - technologies NASA uses for space communications.

### Real-World Applications:
- 🚀 **Space Communications** (Mars rovers, satellites)
- 🌊 **Underwater Networks** (submarine sensors)
- 🏜️ **Remote Areas** (desert monitoring stations)
- 🚗 **Vehicle Networks** (cars sharing traffic data)
- 📡 **Disaster Recovery** (when regular networks fail)

---

## Real-World Problem It Solves

### Traditional Internet vs DTN

**Traditional Internet (like your WiFi):**
```
You → Router → Server → Response (milliseconds)
❌ Needs constant connection
❌ Fails if link breaks
❌ Can't handle long delays
```

**DTN (this project):**
```
Earth Station → Satellite A → Wait... → Satellite B → Mars Rover
✅ Works with interruptions
✅ Stores messages during gaps
✅ Handles hours of delay
✅ Guarantees delivery eventually
```

### The Challenge

Think of it like a relay race where:
- Runners can only pass the baton during specific time windows
- Some runners might drop the baton (transmission errors)
- Important messages need priority
- Everyone must coordinate without a central controller

---

## Key Concepts Explained Simply

### 1. **Delay Tolerant Networking (DTN)**

**Simple Analogy:** Think of the postal service vs instant messaging

- **Instant Messaging (Regular Internet):** Direct, immediate, but needs constant connection
- **Postal Service (DTN):** Can handle delays, stores packages, delivers even if you're not home

**In This Simulator:**
- Messages are called **"bundles"** (like packages)
- Nodes **store bundles** when they can't send them yet
- Bundles **wait for opportunities** to be forwarded
- Each node has a **buffer** (like a mailbox) to hold messages

### 2. **Licklider Transmission Protocol (LTP)**

**Simple Analogy:** Certified mail with tracking

Regular mail → Might get lost, no confirmation
Certified mail → Signed receipt, guaranteed delivery

**What LTP Does:**
- Breaks large messages into **small segments** (easier to send)
- Tracks which segments arrived successfully
- **Retransmits lost segments** automatically
- Confirms delivery with acknowledgments

**Example:**
```
Large File (4096 bytes)
    ↓
LTP breaks it into 4 segments (1024 bytes each)
    ↓
[Segment 1] ✅ Delivered
[Segment 2] ❌ Lost → Resend
[Segment 3] ✅ Delivered  
[Segment 4] ✅ Delivered
    ↓
File reconstructed at destination
```

### 3. **Quality of Service (QoS)**

**Simple Analogy:** Emergency lane on a highway

- 🚑 **Critical:** Ambulance (always goes first)
- 🚗 **High:** Business executives (fast lane)
- 🚙 **Normal:** Regular traffic
- 🚚 **Low:** Delivery trucks (can wait)

**In This Simulator:**
Messages have priority levels:
- **CRITICAL** (0): Space mission commands, medical data
- **HIGH** (1): Important scientific data
- **NORMAL** (2): Standard telemetry
- **LOW** (3): Optional diagnostics

When network is congested, critical messages go first!

### 4. **Contacts (Communication Windows)**

**Simple Analogy:** Train schedule

You can only board a train:
- At specific times (train schedule)
- From specific platforms (communication links)
- For limited duration (train leaves eventually)

**In Space Networks:**
```
🛰️ Satellite A visible from Earth: 10:00 AM - 10:15 AM
🛰️ Satellite B visible from Earth: 10:45 AM - 11:00 AM

Message must wait for next "train" (contact window)
```

### 5. **Routing Protocols**

**Simple Analogy:** Different mail delivery strategies

**Epidemic Routing (Flood everything):**
```
Like giving copies of your party invitation to EVERYONE you meet,
hoping it reaches your friend eventually.
✅ High delivery rate
❌ Wastes resources
```

**Spray and Wait (Limited copies):**
```
Give 5 copies to 5 trusted friends, then stop.
✅ Balanced approach
⚖️ Moderate resource usage
```

**Predictive (Based on schedule):**
```
Check bus schedule, give invitation to friend who takes
the same bus as the party host.
✅ Most efficient
✅ Requires knowledge
```

---

## How The System Works

### Step-by-Step Walkthrough

#### **Step 1: Network Initialization**
```
Create 8 nodes (satellites/ground stations)
Position them in space
Generate contact schedule (when nodes can communicate)
```

#### **Step 2: Message Creation**
```
Source Node (Earth Station) creates a bundle:
  - Destination: Mars Rover (Node 5)
  - Size: 2048 bytes
  - Priority: HIGH
  - Deadline: Deliver within 300 seconds
```

#### **Step 3: Store and Forward**
```
Earth Station (Node 0) stores bundle in buffer
Waits for contact with Satellite A (Node 2)

Contact Window Opens (10:00 AM - 10:15 AM):
  → Earth Station sends bundle to Satellite A
  → LTP breaks it into segments
  → Acknowledges successful segments
  → Retransmits any lost segments
```

#### **Step 4: Relay Through Network**
```
Satellite A receives bundle, stores it
Waits for contact with Satellite B (Node 4)

Next Contact Window (10:45 AM):
  → Satellite A forwards to Satellite B
  → Satellite B eventually contacts Mars Rover
  → Bundle delivered!
```

#### **Step 5: Quality of Service in Action**
```
Satellite A's buffer is full (50 bundles max)
New CRITICAL message arrives
  → System drops a LOW priority bundle
  → Makes room for critical message
  → Critical message gets sent first
```

---

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────┐
│              DTN SIMULATOR CORE                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐    ┌──────────────┐               │
│  │   DTN Node   │    │   DTN Node   │               │
│  │              │    │              │               │
│  │ ┌──────────┐ │    │ ┌──────────┐ │               │
│  │ │  Buffer  │ │    │ │  Buffer  │ │               │
│  │ │ (Storage)│ │    │ │ (Storage)│ │               │
│  │ └──────────┘ │    │ └──────────┘ │               │
│  │              │    │              │               │
│  │ ┌──────────┐ │    │ ┌──────────┐ │               │
│  │ │   LTP    │ │◄───┤ │   LTP    │ │               │
│  │ │  Engine  │ │────►│ │  Engine  │ │               │
│  │ └──────────┘ │    │ └──────────┘ │               │
│  │              │    │              │               │
│  │ ┌──────────┐ │    │ ┌──────────┐ │               │
│  │ │ Routing  │ │    │ │ Routing  │ │               │
│  │ │  Logic   │ │    │ │  Logic   │ │               │
│  │ └──────────┘ │    │ └──────────┘ │               │
│  └──────────────┘    └──────────────┘               │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │         Contact Schedule Manager               │ │
│  │  (Knows when nodes can communicate)            │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │         Metrics & Statistics Logger            │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Data Flow

```
1. BUNDLE CREATION
   [User Data] → [Bundle Object] → [Priority Queue]

2. SEGMENTATION (LTP)
   [Bundle] → [LTP Segments] → [Transmission]
   
3. TRANSMISSION
   [Node A Buffer] → [Contact Window] → [Node B Buffer]
   
4. ACKNOWLEDGMENT
   [Node B] → [ACK Segments] → [Node A]
   [Node A] → [Retransmit Lost] → [Node B]
   
5. FORWARDING
   [Node B] → [Next Hop] → ... → [Destination]
   
6. DELIVERY
   [Final Node] → [Reassemble] → [Delivered!]
```

---

## Installation & Setup

### Prerequisites

```bash
# You only need Python 3.7 or higher
# No external libraries required!
```

### Quick Start

```bash
# 1. Download the simulator
git clone <repository-url>
cd dtn-ltp-simulator

# 2. Run the simulation
python dtn_simulator.py

# That's it! The simulation will run automatically
```

### Configuration

You can customize the simulation by modifying parameters:

```python
config = SimulationConfig(
    num_nodes=8,              # Number of satellites/stations
    simulation_time=500.0,     # How long to run (seconds)
    max_buffer_size=50,        # Messages each node can store
    ltp_segment_size=1024,     # Size of each transmission chunk
    qos_priority_levels=4,     # Number of priority levels
)
```

---

## Running the Simulator

### Basic Execution

```bash
python dtn_simulator.py
```

### What Happens When You Run It

```
1. Console Output:
   ════════════════════════════════════════════════════
   DTN-LTP Simulator initialized
   Creating 8 DTN nodes...
   Generating contact schedule...
   Starting simulation...
   Contact: Node 0 <-> Node 2 at t=15.23s
   Contact: Node 2 <-> Node 5 at t=67.45s
   ...
   Simulation complete
   ════════════════════════════════════════════════════

2. Files Generated:
   📄 dtn_simulator.log           (detailed log)
   📄 dtn_simulation_results.json (data for analysis)
```

### Monitoring Progress

The simulator logs key events:
- **Bundle generation**: When messages are created
- **Contact events**: When nodes communicate
- **Bundle deliveries**: When messages reach destination
- **Statistics**: Every 100 seconds

---

## Understanding the Results

### Console Summary

```
═══════════════════════════════════════════════════════
DTN-LTP SIMULATOR - EXECUTION SUMMARY
═══════════════════════════════════════════════════════

Network Configuration:
  Nodes: 8
  Simulation Duration: 500.0s
  Max Bundle Buffer Size: 50
  LTP Segment Size: 1024 bytes

Performance Metrics:
  Bundles Delivered: 145          ← How many messages reached destination
  Bundles Transmitted: 287        ← Total transmission attempts
  Bundles Dropped: 12             ← Messages lost due to full buffers
  Delivery Success Ratio: 50.52%  ← Efficiency measure
  Average Latency: 87.34 seconds  ← Time from creation to delivery
  Average Buffer Utilization: 23.45 bundles/node
```

### What Each Metric Means

#### **Bundles Delivered**
- **What it is:** Number of messages successfully reached their destination
- **Good values:** Higher is better
- **Typical range:** 40-80% of transmitted bundles

#### **Delivery Success Ratio**
- **What it is:** Percentage of messages that successfully delivered
- **Formula:** (Delivered / Transmitted) × 100
- **Good values:** 
  - 50-70%: Good for challenging networks
  - 70-90%: Excellent
  - <40%: Network congestion issues

#### **Average Latency**
- **What it is:** Average time for a message to reach destination
- **Good values:** 
  - <60 seconds: Fast
  - 60-120 seconds: Normal
  - >200 seconds: Slow (may need optimization)

#### **Bundles Dropped**
- **What it is:** Messages discarded due to full buffers
- **Good values:** Lower is better
- **Causes:** Network congestion, insufficient buffer size

### JSON Report Structure

```json
{
  "configuration": {
    "num_nodes": 8,
    "simulation_time": 500.0,
    ...
  },
  "metrics_timeline": [
    {
      "timestamp": 100.0,
      "total_delivered": 34,
      "avg_latency": 65.2,
      ...
    }
  ],
  "node_statistics": [
    {
      "node_id": 0,
      "bundles_transmitted": 45,
      "bundles_received": 38,
      ...
    }
  ]
}
```

---

## Research Applications

### For Academic Research

This simulator is designed for research in:

1. **Space Communication Networks**
   - Model Mars-Earth communication scenarios
   - Test routing algorithms for deep space missions
   - Evaluate QoS under extreme delays

2. **Mobile Ad-Hoc Networks (MANETs)**
   - Vehicle-to-vehicle communication
   - Emergency response networks
   - Wildlife tracking systems

3. **Internet of Things (IoT)**
   - Sparse sensor networks
   - Underwater monitoring
   - Agricultural remote sensing

4. **Protocol Development**
   - Test new routing strategies
   - Evaluate congestion control
   - Optimize buffer management

### Research Questions You Can Answer

- **How does buffer size affect delivery rate?**
- **Which routing protocol works best under high disruption?**
- **What's the optimal QoS priority strategy?**
- **How does contact duration impact latency?**

### Extending the Simulator

Add new features by modifying:

```python
# Custom routing protocol
class MyCustomRouter(RouteProtocol):
    def select_next_hop(self, bundle, topology):
        # Your logic here
        pass

# Advanced QoS policy
class AdaptiveQoS:
    def prioritize(self, bundles, network_state):
        # Your prioritization logic
        pass
```

---

## Troubleshooting

### Common Issues

**Issue:** "No bundles delivered"
- **Cause:** Insufficient contact windows
- **Solution:** Increase `simulation_time` or `contact_probability`

**Issue:** "High drop rate"
- **Cause:** Buffer overflow
- **Solution:** Increase `max_buffer_size` or reduce traffic

**Issue:** "Very high latency"
- **Cause:** Poor routing or sparse contacts
- **Solution:** Adjust contact schedule or try different routing

---

## Performance Tips

### Optimize for Your Use Case

**For Space Missions (High delay tolerance):**
```python
config = SimulationConfig(
    simulation_time=1000.0,    # Long mission
    bundle_timeout=600.0,       # Patient delivery
    max_buffer_size=100,        # Large buffers
)
```

**For Mobile Networks (Low delay):**
```python
config = SimulationConfig(
    simulation_time=300.0,      # Short interactions
    bundle_timeout=60.0,        # Quick delivery needed
    min_contact_duration=5.0,   # Brief contacts OK
)
```

**For Testing Protocols:**
```python
config = SimulationConfig(
    num_nodes=20,               # Larger network
    base_error_rate=0.05,       # More challenging
    random_seed=42,             # Reproducible results
)
```

---

## Glossary

- **Bundle:** A message/data packet in DTN
- **Contact:** Time window when two nodes can communicate
- **Node:** Network entity (satellite, ground station, etc.)
- **LTP:** Reliable transport protocol for challenged networks
- **QoS:** Quality of Service - priority system for messages
- **Buffer:** Temporary storage for messages waiting to be sent
- **Hop:** One step in a message's journey through the network
- **Latency:** Time delay from creation to delivery
- **Segmentation:** Breaking large messages into smaller pieces

---

## Credits & References

**Based on Research By:**
- Dr. Xingya Liu (Lamar University)
- DTN Research Group (IRTF)
- NASA Space Communication and Navigation

**Standards Implemented:**
- RFC 5050: Bundle Protocol Specification
- RFC 5326: Licklider Transmission Protocol
- CCSDS 734.2-B-1: DTN Bundle Protocol

**Learn More:**
- [DTN Research Group](https://dtnrg.org)
- [NASA DTN Overview](https://www.nasa.gov/directorates/heo/scan/engineering/technology/disruption_tolerant_networking_software_options_Ion)
- [Space Internetworking](https://ipnsig.org)

---

## License & Contact

This simulator is for educational and research purposes.

**Questions?** Open an issue on GitHub or contact the research team.

**Contributing:** Pull requests welcome! See CONTRIBUTING.md

---

**Happy Simulating! 🚀📡**
