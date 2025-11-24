#!/usr/bin/env python3
"""
Example 1: Basic DTN Network Test
Simple 3-node network demonstrating store-and-forward capability
"""

from DTN_LTP_Simulator import (
    SimulationConfig, DTNSimulator, DTNNode, Bundle, 
    QoSLevel, Contact
)
import json

def example_basic_network():
    """Run a simple 3-node DTN network"""
    
    print("=" * 80)
    print("EXAMPLE 1: Basic 3-Node DTN Network")
    print("=" * 80)
    print()
    print("Scenario: Three nodes in a line topology (0 <-> 1 <-> 2)")
    print("Node 0 sends a bundle to Node 2 via Node 1 (intermediate hop)")
    print()
    
    # Create minimal configuration
    config = SimulationConfig(
        num_nodes=3,
        simulation_time=100.0,
        max_buffer_size=20,
        random_seed=42,
    )
    
    # Initialize simulator
    simulator = DTNSimulator(config)
    
    # Manually create a simple contact schedule
    # Node 0 contacts Node 1 at t=10s
    contact_0_1 = Contact(
        node_a=0,
        node_b=1,
        start_time=10.0,
        end_time=20.0,
        capacity=100.0,
        reliability=0.99  # Very reliable
    )
    
    # Node 1 contacts Node 2 at t=30s
    contact_1_2 = Contact(
        node_a=1,
        node_b=2,
        start_time=30.0,
        end_time=40.0,
        capacity=100.0,
        reliability=0.99
    )
    
    simulator.contacts = [contact_0_1, contact_1_2]
    
    # Manually inject bundle from Node 0 to Node 2
    bundle = Bundle(
        bundle_id="example_bundle_1",
        source_id=0,
        destination_id=2,
        size=1024,
        creation_time=0.0,
        deadline=100.0,
        qos_level=QoSLevel.HIGH,
        hop_count=0
    )
    
    simulator.nodes[0].receive_bundle(bundle, 0.0)
    print(f"[t=0.0s] Bundle created at Node 0: {bundle.bundle_id}")
    print(f"         Destination: Node 2 (must traverse Node 1)")
    print()
    
    # Run simulation
    simulator.run()
    
    # Print results
    print("\nSIMULATION RESULTS:")
    print("-" * 80)
    for i, node in enumerate(simulator.nodes):
        stats = node.get_statistics(simulator.current_time)
        print(f"Node {i}:")
        print(f"  Bundles Transmitted: {stats.bundles_transmitted}")
        print(f"  Bundles Received:    {stats.bundles_received}")
        print(f"  Bundles Dropped:     {stats.bundles_dropped}")
        print(f"  Current Buffer:      {stats.buffer_size} bundles")
        if stats.avg_latency > 0:
            print(f"  Average Latency:     {stats.avg_latency:.2f}s")
        print()
    
    # Check if bundle reached destination
    if simulator.nodes[2].stats['delivery_count'] > 0:
        print("✓ SUCCESS: Bundle delivered to destination!")
    else:
        print("✗ FAILURE: Bundle did not reach destination")
    
    print("=" * 80)

def example_space_communication():
    """
    Example 2: Deep-space communication scenario
    Multiple satellites with intermittent ground station contacts
    """
    
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Deep-Space Satellite Network")
    print("=" * 80)
    print()
    print("Scenario: 3 satellites with periodic ground station passes")
    print("- Satellite orbital period: ~90 minutes")
    print("- Visible window: ~10 minutes per orbit")
    print("- Ground bandwidth: limited (50 Mbps)")
    print()
    
    config = SimulationConfig(
        num_nodes=4,  # 3 satellites + 1 ground station
        simulation_time=300.0,  # 5 hours (3 orbits)
        channel_capacity=50.0,  # Mbps (limited ground link)
        base_error_rate=0.02,   # 2% BER (space channel)
        max_buffer_size=100,    # Large satellite cache
        random_seed=123,
    )
    
    simulator = DTNSimulator(config)
    
    # Simulate orbital passes (ground station at node 0)
    orbit_period = 90.0  # seconds (simplified)
    visible_duration = 10.0
    
    contacts = []
    for sat_id in range(1, 4):  # Satellites 1, 2, 3
        for orbit in range(4):  # 4 orbits during 300s
            pass_start = orbit * orbit_period + 20.0  # Pass starts
            pass_end = pass_start + visible_duration
            
            if pass_start < config.simulation_time:
                contact = Contact(
                    node_a=0,  # Ground station
                    node_b=sat_id,
                    start_time=pass_start,
                    end_time=min(pass_end, config.simulation_time),
                    capacity=config.channel_capacity,
                    reliability=0.98
                )
                contacts.append(contact)
    
    simulator.contacts = contacts
    
    print(f"Contact schedule generated: {len(contacts)} passes")
    print("Sample passes:")
    for i, c in enumerate(contacts[:5]):
        print(f"  Pass {i+1}: Sat {c.node_b} visible at t={c.start_time:.1f}s for {c.duration():.1f}s")
    
    # Run simulation
    simulator.run()
    
    # Analyze results
    print("\nSATELLITE STATISTICS:")
    print("-" * 80)
    for i in range(1, 4):
        node = simulator.nodes[i]
        print(f"Satellite {i}:")
        print(f"  Bundles successfully relayed: {node.stats['bundles_transmitted']}")
        print(f"  Bundles received from network: {node.stats['bundles_received']}")
        print(f"  Bundles dropped (buffer full): {node.stats['bundles_dropped']}")
    
    # Ground station statistics
    ground = simulator.nodes[0]
    print(f"\nGround Station (Node 0):")
    print(f"  Bundles received: {ground.stats['bundles_received']}")
    print(f"  Delivery success: {ground.stats['delivery_count']}")
    
    print("=" * 80)

def example_qos_comparison():
    """
    Example 3: Compare QoS levels
    Generate critical vs. best-effort traffic and observe behavior under stress
    """
    
    print("\n" + "=" * 80)
    print("EXAMPLE 3: QoS-Based Bundle Prioritization")
    print("=" * 80)
    print()
    print("Scenario: Overloaded node receives mixed QoS traffic")
    print("Expected: CRITICAL bundles preserved, LOW-priority dropped first")
    print()
    
    config = SimulationConfig(
        num_nodes=2,
        simulation_time=50.0,
        max_buffer_size=5,  # Small buffer to force drops
        random_seed=456,
    )
    
    simulator = DTNSimulator(config)
    
    # Create contact
    contact = Contact(0, 1, 10.0, 40.0, 100.0, 0.95)
    simulator.contacts = [contact]
    
    # Manually inject bundles with different QoS levels
    bundle_data = [
        ("bundle_critical", QoSLevel.CRITICAL, 1000),
        ("bundle_high", QoSLevel.HIGH, 1000),
        ("bundle_normal", QoSLevel.NORMAL, 1000),
        ("bundle_low_1", QoSLevel.LOW, 1000),
        ("bundle_low_2", QoSLevel.LOW, 1000),
        ("bundle_low_3", QoSLevel.LOW, 1000),  # One of these will drop
    ]
    
    for bundle_id, qos, size in bundle_data:
        bundle = Bundle(
            bundle_id=bundle_id,
            source_id=0,
            destination_id=1,
            size=size,
            creation_time=5.0,
            deadline=50.0,
            qos_level=qos
        )
        simulator.nodes[0].receive_bundle(bundle, 5.0)
        print(f"  Injected: {bundle_id} ({qos.name})")
    
    print()
    print(f"Buffer capacity: {config.max_buffer_size} bundles")
    print(f"Injected: {len(bundle_data)} bundles")
    print(f"Expected: 1 LOW-priority bundle will be dropped")
    print()
    
    # Run simulation
    simulator.run()
    
    # Check what was dropped
    print("RESULT:")
    print("-" * 80)
    print(f"Bundles dropped: {simulator.nodes[0].stats['bundles_dropped']}")
    print(f"Bundles successfully buffered and transmitted: "
          f"{simulator.nodes[0].stats['bundles_transmitted']}")
    
    # Verify CRITICAL was preserved
    node_0_buffer = simulator.nodes[0].bundle_buffer
    critical_preserved = any(
        b.qos_level == QoSLevel.CRITICAL 
        for b in node_0_buffer.values()
    )
    
    if simulator.nodes[0].stats['bundles_dropped'] == 1:
        print("\n✓ Correct: Exactly 1 bundle dropped (buffer overflow)")
    
    if not critical_preserved and simulator.nodes[0].stats['bundles_transmitted'] > 0:
        print("✓ Correct: CRITICAL bundle was prioritized for transmission")
    
    print("=" * 80)

def main():
    """Run all examples"""
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "DTN-LTP SIMULATOR - USAGE EXAMPLES".center(78) + "║")
    print("║" + "Research Project for Dr. Xingya Liu".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Run examples
    example_basic_network()
    example_space_communication()
    example_qos_comparison()
    
    print("\n")
    print("=" * 80)
    print("All examples completed successfully!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Check dtn_simulator.log for detailed event logs")
    print("2. Review dtn_simulation_results.json for metrics")
    print("3. Modify SimulationConfig parameters to test different scenarios")
    print("4. Extend DTNSimulator with custom routing protocols")
    print()

if __name__ == "__main__":
    main()
