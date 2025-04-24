## Network Documentation: GEEK-Fitness GmbH Infrastructure Analysis and Expansion Plan

**Learning Field 3**

**Prepared for:** GEEK-Fitness GmbH Management
**Prepared by:** GeekedOut Gmbh
**Class:** IT4-L
**Submission Date:** April 29, 2024

---

**Table of Contents**

1.  Introduction
    1.1. Target Audience and Perspective
    1.2. Project Scope and Objectives
    1.3. Client Information
2.  Main Part
    2.1. As-Is Network Analysis (Ist-Analyse)
    2.1.1. Current Topology Overview
    2.1.2. Key Network Devices
    2.1.3. Existing Services
    2.2. Network Plan (Netzwerkplan)
    2.3. IPv4 Addressing Scheme (IPAM)
    2.4. Switch Configuration and Port Assignment (Switchkonfiguration inkl. Portbelegung)
    2.5. Implementation Plan / Desired State (Soll-Konzept)
    2.5.1. Task 4: Integration of New Devices (Purchasing Department)
    2.5.2. Task 6: Creation of Controlling Subnet/VLAN
    2.6. Test Scenarios
    2.7. Task 5: Leasing vs. Buying Analysis
    2.7.1. Definition of Leasing
    2.7.2. Advantages and Disadvantages
    2.7.3. Cost Comparison
3.  Conclusion
    3.1. Summary of Findings and Recommendations
    3.2. Reflection on Process and Teamwork
4.  Appendix (Optional)
    4.1. Sources
    4.2. Detailed Configuration Snippets (Example)

---

**1. Introduction**

**1.1. Target Audience and Perspective**
This documentation is prepared by GeekedOut Gmbh for the management and relevant IT personnel at GEEK-Fitness GmbH. It provides an analysis of the current network infrastructure based on the provided Cisco Packet Tracer simulation and outlines planned modifications and evaluations as requested.

**1.2. Project Scope and Objectives**
The primary scope of this project is to:

- Analyze and thoroughly document the existing network infrastructure simulated in Packet Tracer.
- Plan and document the integration of a new PC workstation and a wireless tablet into the Purchasing department (Einkauf).
- Plan and document the creation of a new, segregated subnet/VLAN for the Controlling department.
- Evaluate the economic viability of leasing versus purchasing new client systems for the Purchasing department.
- Provide clear, actionable documentation for the client.

**1.3. Client Information**
The client for this project is GEEK-Fitness GmbH.

**2. Main Part**

**2.1. As-Is Network Analysis (Ist-Analyse)**

**2.1.1. Current Topology Overview**
The current network consists of a core layer (`SW-Core`), an access layer with switches dedicated to specific departments/functions (`SW-Verwaltung`, `SW-Finanzen`, `SW-Lager`, `SW-Einkauf`, `SW-Verkauf`, `SW-Server`), and a central router (`R-Internet`) providing inter-VLAN routing and internet connectivity. A separate server farm hosts critical services. Wireless access is provided via dedicated Access Points (APs) for employees, customers, and guests. The network utilizes VLANs to segment traffic logically between departments. Internet connectivity is simulated via an ISP router and external servers.

**2.1.2. Key Network Devices**

- **Routers:**
  - `R-Internet` (Cisco 2911): Performs inter-VLAN routing (Router-on-a-Stick), acts as default gateway for internal networks, connects to ISP, applies ACLs for guest network security.
  - `ISP (Internet)` (Cisco 2811): Simulates the Internet Service Provider, provides DHCP to R-Internet's external interface, routes traffic to simulated external servers.
- **Switches:**
  - `SW-Core` (Cisco 3650-24PS): Multilayer switch acting as the central aggregation point, connecting access switches and the router via trunk links. Handles management VLAN traffic.
  - `SW-Verwaltung`, `SW-Finanzen`, `SW-Lager`, `SW-Einkauf`, `SW-Verkauf` (Cisco 2960-24TT): Access layer switches connecting end devices and APs within specific VLANs. Connect to SW-Core via trunk links.
  - `SW-Server` (Cisco 2960-24TT): Connects the servers in the server VLAN. Connects to R-Internet via a trunk link.
- **Servers (Server-PT):**
  - `DHCP/DNS-Server`: Provides DHCP services (relayed by R-Internet) and DNS resolution for internal hostnames (`bs14.local`, `files.local`) and forwards external queries. IP: `192.168.100.3`.
  - `WEB-Server`: Hosts internal website `bs14.local`/`bs14.net`. IP: `192.168.100.9`.
  - `Fileserver`: Hosts `files.local` (currently only pingable per diagram note). IP: `192.168.100.12`.
  - External Simulation Servers: `DNS 8.8.8.8`, `Web (testnet.lo) 89.12.34.5`, `E-Mail (Post.ta) 55.44.33.22`, `FTP (Files.dat) 45.55.65.75`.
- **Access Points (AccessPoint-PT-AC):**
  - `AP-Mitarbeiter`: Provides employee Wi-Fi (SSID: Mitarbeiter, VLAN 60).
  - `AP-Kunden`: Provides customer Wi-Fi (SSID: Kunden, VLAN 70).
  - `AP-Gäste`: Provides guest Wi-Fi (SSID: Gaeste, VLAN 80).
- **End Devices:** PCs, Laptops, Smartphone, Tablet connected to appropriate wired or wireless networks.

**2.1.3. Existing Services**

- **DHCP:** Centralized service provided by `192.168.100.3` for multiple VLANs via IP helper addresses on `R-Internet`.
- **DNS:** Centralized service by `192.168.100.3` for internal resolution, forwarding to `8.8.8.8` for external names.
- **Inter-VLAN Routing:** Handled by `R-Internet`.
- **Internet Access:** Provided via `R-Internet` and the simulated ISP.
- **Wireless Access:** Segmented SSIDs for different user groups.
- **Web/File/Email Services:** Provided by dedicated servers (internal and simulated external).
- **Security:** Basic ACL (`KD_INTERNET`) restricts guest wireless network access. Standard console and enable passwords are set on routers/switches.


**Figure 1:** GEEK-Fitness GmbH Network Topology (Packet Tracer Simulation)

**Brief Explanation:** The diagram shows the central `R-Internet` router connecting the internal network segments (via `SW-Core` and `SW-Server`) to the simulated `INTERNET`. `SW-Core` acts as the backbone, linking the departmental access switches (`SW-Verwaltung`, `SW-Finanzen`, etc.). Each access switch connects respective end devices (PCs) and potentially Access Points. The server farm connects directly to `SW-Server`, which links to `R-Internet`. Wireless devices connect via the appropriate APs.

**2.3. IPv4 Addressing Scheme (IPAM)**

The network utilizes private IPv4 addressing, primarily in the `10.x.x.x` range, segmented by VLANs. The server network uses the `192.168.100.0/24` range. Addressing is managed centrally via DHCP for most client devices, with static IPs assigned to servers and network infrastructure management interfaces.

| VLAN ID | Name               | Network Address     | Subnet Mask       | Usable Host Range           | Gateway (R-Internet) | Purpose                    |
| :------ | :----------------- | :------------------ | :---------------- | :-------------------------- | :------------------- | :------------------------- |
| 10      | Geschaeftsfuehrung | `10.1.10.0/28`      | `255.255.255.240` | `10.1.10.2` - `10.1.10.14`  | `10.1.10.1`          | Management/Executive       |
| 11      | Verwaltung         | `10.1.11.0/28`      | `255.255.255.240` | `10.1.11.2` - `10.1.11.14`  | `10.1.11.1`          | Administration             |
| 20      | Finanzen           | `10.1.20.0/27`      | `255.255.255.224` | `10.1.20.2` - `10.1.20.30`  | `10.1.20.1`          | Finance                    |
| 30      | Lager              | `10.1.30.0/24`      | `255.255.255.0`   | `10.1.30.2` - `10.1.30.254` | `10.1.30.1`          | Warehouse/Logistics        |
| 40      | Einkauf            | `10.1.40.0/24`      | `255.255.255.0`   | `10.1.40.2` - `10.1.40.254` | `10.1.40.1`          | Purchasing                 |
| 50      | Verkauf            | `10.1.50.0/24`      | `255.255.255.0`   | `10.1.50.2` - `10.1.50.254` | `10.1.50.1`          | Sales                      |
| 60      | WLAN-MA            | `10.1.60.0/24`      | `255.255.255.0`   | `10.1.60.2` - `10.1.60.254` | `10.1.60.1`          | Employee Wi-Fi             |
| 70      | WLAN-KD            | `10.1.70.0/23`      | `255.255.254.0`   | `10.1.70.2` - `10.1.71.254` | `10.1.70.1`          | Customer/Guest Wi-Fi       |
| 80      | WLAN-GA            | `10.1.80.0/24`      | `255.255.255.0`   | `10.1.80.2` - `10.1.80.254` | `10.1.80.1`          | Guest Wi-Fi (Alternative?) |
| 99      | Management         | `10.1.99.0/24` etc. | `255.255.255.x`   | Varies                      | `10.1.99.254`, etc.  | Network Device Management  |
| 100     | Server             | `192.168.100.0/24`  | `255.255.255.0`   | `192.168.100.1` - `253`     | `192.168.100.254`    | Server Farm                |

**2.4. Switch Configuration and Port Assignment (Switchkonfiguration inkl. Portbelegung)**

The following tables detail the significant port configurations for each access switch based on the simulation file. Unused ports are generally configured in VLAN 1 (default) and are administratively shut down for security. Trunk ports carry tagged traffic for multiple VLANs, while access ports carry untagged traffic for a single assigned VLAN.

**SW-Verwaltung (VLANs: 10, 11, 80, 99)**
| Port | Status | Mode | VLAN(s) Allowed/Assigned | Connected Device (Likely) |
| :--------------- | :----- | :----- | :----------------------- | :------------------------ |
| Fa0/1 | Up | Access | 10 | PC-GF01 |
| Fa0/2 - Fa0/10 | Down | Access | 1 | - |
| Fa0/11 | Up | Access | 11 | PC-VW01 |
| Fa0/12 - Fa0/19 | Down | Access | 1 | - |
| Fa0/20 | Up | Access | 80 | AP-Gäste |
| Fa0/21 - Fa0/23 | Down | Access | 1 | - |
| Fa0/24 | Up | Access | 99 | Management-Laptop |
| Gi0/1 | Up | Trunk | 10, 11, 80, 99 | SW-Core |
| Gi0/2 | Up | Access | 99 | Management-Laptop |

**SW-Finanzen (VLANs: 20, 99)**
| Port | Status | Mode | VLAN(s) Allowed/Assigned | Connected Device (Likely) |
| :--------------- | :----- | :----- | :----------------------- | :------------------------ |
| Fa0/1 | Up | Access | 20 | PC-FI01 |
| Fa0/2 | Up | Access | 20 | PC-FI02 |
| Fa0/3 - Fa0/23 | Down | Access | 1 | - |
| Fa0/24 | Up | Access | 99 | (Management) |
| Gi0/1 | Up | Trunk | 20, 99 | SW-Core |
| Gi0/2 | Down | Access | 1 | - |

**SW-Lager (VLANs: 30, 99)**
| Port | Status | Mode | VLAN(s) Allowed/Assigned | Connected Device (Likely) |
| :--------------- | :----- | :----- | :----------------------- | :------------------------ |
| Fa0/1 | Up | Access | 30 | PC-LA01 |
| Fa0/2 | Up | Access | 30 | PC-LA02 |
| Fa0/3 - Fa0/23 | Down | Access | 1 | - |
| Fa0/24 | Up | Access | 99 | (Management) |
| Gi0/1 | Up | Trunk | 30, 99 | SW-Core |
| Gi0/2 | Down | Access | 1 | - |

**SW-Einkauf (VLANs: 40, 99)**
| Port | Status | Mode | VLAN(s) Allowed/Assigned | Connected Device (Likely) |
| :--------------- | :----- | :----- | :----------------------- | :------------------------ |
| Fa0/1 | Up | Access | 40 | PC-EK01 |
| Fa0/2 | Up | Access | 40 | PC-EK02 |
| Fa0/3 - Fa0/23 | Down | Access | 1 | - |
| Fa0/24 | Up | Access | 99 | (Management) |
| Gi0/1 | Up | Trunk | 40, 99 | SW-Core |
| Gi0/2 | Down | Access | 1 | - |

**SW-Verkauf (VLANs: 50, 60, 70, 99)**
| Port | Status | Mode | VLAN(s) Allowed/Assigned | Connected Device (Likely) |
| :--------------- | :----- | :----- | :----------------------- | :------------------------ |
| Fa0/1 | Up | Access | 50 | PC-VK01 |
| Fa0/2 | Up | Access | 50 | PC-VK02 |
| Fa0/3 - Fa0/19 | Down | Access | 1 | - |
| Fa0/20 | Up | Access | 60 | AP-Mitarbeiter |
| Fa0/21 | Up | Access | 70 | AP-Kunden |
| Fa0/22 - Fa0/23 | Down | Access | 1 | - |
| Fa0/24 | Up | Access | 99 | (Management) |
| Gi0/1 | Up | Trunk | 50, 60, 70, 99 | SW-Core |
| Gi0/2 | Down | Access | 1 | - |

**SW-Server (VLANs: 1, 99, 100)**
| Port | Status | Mode | VLAN(s) Allowed/Assigned | Connected Device (Likely) |
| :--------------- | :----- | :----- | :----------------------- | :------------------------ |
| Fa0/1 | Up | Access | 100 | DHCP/DNS-Server |
| Fa0/2 | Up | Access | 100 | WEB-Server |
| Fa0/3 | Up | Access | 100 | Fileserver |
| Fa0/4 - Fa0/23 | Down | Access | 1 | - |
| Fa0/24 | Up | Access | 99 | (Management) |
| Gi0/1 | Up | Trunk | 1, 99, 100 | R-Internet (Gi0/1) |
| Gi0/2 | Up | Access | 1 | (Unused/Security Port? Probably unconnected) |

_(Note: Port assignments are based on typical connections and active links in the simulation. Room/socket information is omitted as per requirements.)_

**2.5. Implementation Plan / Desired State (Soll-Konzept)**

**2.5.1. Task 4: Integration of New Devices (Purchasing Department)**

- **New PC (PC-EK03 for Helmut Schön):**
  1.  Physically connect the new PC to an unused port on `SW-Einkauf`, for example, `FastEthernet0/3`.
  2.  Configure port `Fa0/3` on `SW-Einkauf`:
      ```cisco
      interface FastEthernet0/3
       description PC-EK03_Helmut_Schoen
       switchport mode access
       switchport access vlan 40
       no shutdown
      end
      ```
  3.  Configure the PC's network interface card (NIC) to obtain an IP address via DHCP. It will receive an address from the `10.1.40.0/24` pool served by `192.168.100.3`.
- **New Tablet (Tablet-EK01):**
  1. Create new access point called AP-Einkauf and set SSID to "Einkauf" and WPA2-PSK to "GHMA2020".
  2. Connect the access point physically to an unused port on `SW-Einkauf`, for example, `FastEthernet0/4`.
  3. Configure port `Fa0/4` on `SW-Einkauf`:
     ```cisco
     interface FastEthernet0/4
      description AP-Einkauf
      switchport mode access
      switchport access vlan 60
      no shutdown
     end
     ```
  4. Connect the tablet wirelessly to the SSID "Einkauf".
  5. Use the pre-shared key (PSK) "GHMA2020" for authentication.
  6. The tablet will associate with `AP-Einkauf` (connected to `SW-Einkauf` Fa0/04, VLAN 40) and receive an IP address via DHCP from the `10.1.40.0/24` pool.
