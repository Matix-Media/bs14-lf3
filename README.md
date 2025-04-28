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

**2.2. Network Plan (Netzwerkplan)**

_(Insert the provided network diagram image here)_

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

**2.5.2. Task 6: Creation of Controlling Subnet/VLAN**

- **IP Subnet Design:**
  - Requirement: 8 workstations. Need IPs for hosts, network address, broadcast address, and gateway. Minimum required = 8 + 3 = 11 IPs.
  - Smallest standard subnet size fitting 11 IPs is a `/28` (255.255.255.240), providing 16 total IPs (14 usable host IPs).
  - Adjacent to Finance (`10.1.20.0/27`, ends at `10.1.20.31`).
  - New Network: `10.1.20.32/28`
  - Usable Host Range: `10.1.20.33` - `10.1.20.46`
  - Gateway IP: `10.1.20.33` (assigned to router subinterface)
  - Broadcast Address: `10.1.20.47`
- **VLAN Creation:**
  - Assign VLAN ID `21` (assuming it's unused) for Controlling.
  - Create VLAN 21 on `SW-Core` and `SW-Finanzen` (assuming Controlling PCs connect here).
    ```cisco
    ! On SW-Core and SW-Finanzen
    vlan 21
     name Controlling
    exit
    ```
- **Router Configuration (`R-Internet`):**
  1.  Create a new subinterface for VLAN 21:
      ```cisco
      interface GigabitEthernet0/0/0.21
       description Controlling_VLAN_Gateway
       encapsulation dot1Q 21
       ip address 10.1.20.33 255.255.255.240
       ip helper-address 192.168.100.3 ! If DHCP is needed
      end
      ```
  2.  Create an Access Control List (ACL) to restrict traffic:
      ```cisco
      ip access-list extended CONTROLLING_ISOLATION
      exit
      ```
  3.  Configure a new ACL (Access-Control List) for Controlling with the name "CONTROLLING_ISOLATION" with the following permissions:
      - `permit udp any eq bootpc any eq bootps`: This allows any DHCP requests to any DHCP server (This is probably not the most secure method, but I could not get it to work with a more restrictive approach to only the IP of the DHCP server)
      - `permit udp 10.1.20.32 0.0.0.15 eq bootpc host 192.168.100.3 eq bootps`: This was my previous approach for only allowing DHCP requests from my subnet to my specific DHCP server. This approach sadly not work, and I could not find out why.
      - `permit udp host 192.168.100.3 eq bootps 10.1.20.32 0.0.0.15 eq bootpc`: This allows for the DHCP server to speak back to the clients. This acl is actually as restrictive as possible, but it worked surprisingly - not like the inbound restrictive DHCP access criteria
      - `permit ip 10.1.20.32 0.0.0.15 10.1.20.32 0.0.0.15`: This allows any ip communication inside the subnet
      - `deny ip any any`: This denys all communication to other ip addresses that did not match any previous criteria.
  4.  Apply the ACL to the new subinterface (both directions):
      ```cisco
      interface GigabitEthernet0/0/0.21
       ip access-group CONTROLLING_ISOLATION in
      end
      ```
- **Switch Configuration (`SW-Finanzen`):**

  1.  Configure ports Fa0/17-24 for VLAN 21:
      ```cisco
      interface range FastEthernet0/17 - 24
       description Controlling_Workstation
       switchport mode access
       switchport access vlan 21
       spanning-tree portfast
       no shutdown
      end
      ```
  2.  Update trunk links to allow VLAN 21:

      ```cisco
      ! On SW-Finanzen Gi0/1
      interface GigabitEthernet0/1
       switchport trunk allowed vlan add 21
      end

      ! On SW-Core Gi1/0/2 (assuming this connects to SW-Finanzen)
      interface GigabitEthernet1/0/2
       switchport trunk allowed vlan add 21
      end

      ! On SW-Core Gi1/1/1 (connecting to R-Internet)
      interface GigabitEthernet1/1/1
       switchport trunk allowed vlan add 21
      end
      ```

- **DHCP Configuration (`DHCP/DNS-Server`):**
  - Add a new DHCP pool if required (or use static IPs):
    ```text
    Pool Name: Pool-Controlling
    Default Gateway: 10.1.20.33
    DNS Server: 192.168.100.3
    Start IP Address: 10.1.20.34
    Subnet Mask: 255.255.255.240
    Maximum Users: 13
    ```

**2.6. Test Scenarios**

To verify network functionality after analysis and implementation:

1.  **Intra-VLAN Connectivity:** Ping between two PCs within the same VLAN (e.g., PC-VW01 to another PC in VLAN 11 if added, or PC-EK01 to PC-EK02). _Expected Result: Success._
2.  **Inter-VLAN Connectivity:** Ping from a PC in one VLAN to a PC or server in another (e.g., PC-GF01 in VLAN 10 to WEB-Server in VLAN 100). _Expected Result: Success._
3.  **Gateway Ping:** Ping from a PC to its default gateway (e.g., PC-LA01 to `10.1.30.1`). _Expected Result: Success._
4.  **DNS Resolution:** From a PC, use `nslookup bs14.local` and `nslookup www.google.com` (or an external IP like `8.8.8.8`). _Expected Result: Correct IP addresses returned._
5.  **Internet Connectivity:** Ping `8.8.8.8` from an internal PC (e.g., PC-EK01). _Expected Result: Success._
6.  **New Device Verification (Task 4):**
    - Verify PC-EK03 gets a correct DHCP address in the `10.1.40.x` range.
    - Verify Tablet-EK01 connects to SSID "Mitarbeiter" and gets a correct DHCP address in the `10.1.60.x` range.
    - Ping from PC-EK03 and Tablet-EK01 to their gateways, internal servers, and the internet. _Expected Result: Success._
7.  **Controlling Subnet Verification (Task 6):**
    - Connect PCs to ports Fa0/17-24 on `SW-Finanzen`. Verify they get IPs in the `10.1.20.32/28` range (if DHCP configured).
    - Ping between two PCs within the Controlling VLAN (VLAN 21). _Expected Result: Success._
    - Ping from a PC in VLAN 21 to any device outside VLAN 21 (e.g., `10.1.10.1`, `192.168.100.3`, `8.8.8.8`). _Expected Result: Failure (due to ACL)._
    - Ping from a device outside VLAN 21 (e.g., PC-GF01) to a device in VLAN 21. _Expected Result: Failure (due to ACL)._
8.  **Guest WLAN Restrictions (VLAN 70):**
    - Connect KD-Smartphone01 to SSID "Kunden". Verify DHCP assigns an IP in the `10.1.70.0/23` range.
    - Attempt to ping an internal server (e.g., `192.168.100.9`). _Expected Result: Failure._
    - Attempt to ping `8.8.8.8`. _Expected Result: Failure (ICMP likely blocked by ACL)._
    - Attempt to access `http://testnet.lo` (simulated external web) via the web browser. _Expected Result: Success (HTTP allowed by ACL)._
    - Attempt DNS lookup (`nslookup testnet.lo`). _Expected Result: Success (DNS allowed by ACL)._

**2.7. Task 5: Leasing vs. Buying Analysis (Purchasing Department PCs)**

**2.7.1. Definition of Leasing**
Leasing IT equipment involves renting hardware (like PCs) from a provider for a fixed period under a contractual agreement, instead of purchasing it outright. The user pays regular installments (typically monthly) for the right to use the equipment. Ownership usually remains with the leasing company.

**2.7.2. Advantages and Disadvantages**

| Aspect           | Buying                                      | Leasing                                          |
| :--------------- | :------------------------------------------ | :----------------------------------------------- |
| **Ownership**    | Full ownership, asset on balance sheet      | No ownership, equipment returned at end of term  |
| **Upfront Cost** | High initial capital expenditure            | Lower initial outlay, predictable monthly costs  |
| **Total Cost**   | Potentially lower over long term            | Often higher total cost over the lease term      |
| **Technology**   | Risk of obsolescence                        | Easier to upgrade to newer tech at lease end     |
| **Maintenance**  | Company responsible for repairs/maintenance | Often included or available as part of the lease |
| **Flexibility**  | Less flexible to scale up/down quickly      | More flexible to adjust needs at lease renewal   |
| **Disposal**     | Company handles disposal/recycling          | Leasing company handles disposal                 |
| **Tax**          | Depreciation tax benefits                   | Lease payments often fully tax-deductible        |

**2.7.3. Cost Comparison**
_Assumption:_ The Purchasing department requires 5 new PC workstations. A market price for purchasing suitable business PCs including basic software and a 3-year warranty is estimated at €1,200 per unit. Maintenance/support beyond warranty is estimated at €100 per PC per year. If specific figures are unavailable, we use the client's provided total purchase estimate of €10,000 for the department.

- **Purchase Scenario (Using €10,000 assumption for department):**
  - Initial Purchase Cost: €10,000
  - Estimated Annual Maintenance (Years 4+ if applicable, or for issues outside warranty): Needs estimation based on number of PCs. Let's assume 5 PCs \* €100/year = €500/year after warranty.
  - _Total Cost over 3 years (example):_ €10,000 (initial) + potential minor repair costs.
  - _Total Cost over 5 years (example):_ €10,000 + (€500 \* 2 years) = €11,000 + potential repair costs.
- **Leasing Scenario:**
  - Leasing costs vary significantly based on provider, equipment specs, lease term, and included services (support, insurance).
  - _Example Calculation:_ Assume a 3-year lease for 5 PCs costs €40 per PC per month, including full support.
  - Monthly Cost: 5 PCs \* €40/PC/month = €200/month
  - Annual Cost: €200/month \* 12 months = €2,400/year
  - _Total Cost over 3 years:_ €2,400/year \* 3 years = €7,200
  - _Total Cost over 5 years (assuming renewal on similar terms):_ €2,400/year \* 5 years = €12,000

**Assessment:** Based on this example, leasing appears cheaper over a typical 3-year refresh cycle (€7,200 vs €10,000+), especially considering included support often covers issues outside standard purchase warranties. Over a longer 5-year period, the costs become more comparable, but leasing still offers the advantage of easier technology refreshes and predictable budgeting. The tax implications should also be reviewed with the finance department.

**Recommendation:** For predictable costs, included support, and easier technology refreshes, **leasing** is often advantageous for client workstations in a business environment like GEEK-Fitness GmbH, particularly if refresh cycles are typically 3-4 years.

**3. Conclusion**

**3.1. Summary of Findings and Recommendations**
The existing network infrastructure of GEEK-Fitness GmbH is well-segmented using VLANs, providing a good foundation. Key services like DHCP and DNS are centralized. The analysis identified specific configurations for switches, the router, and wireless access points.

The documentation outlines clear steps for integrating the new PC and tablet for the Purchasing department and for creating a new, isolated subnet for the Controlling department, including necessary IP addressing, VLAN creation, router ACLs, and switch port configurations.

The economic analysis suggests that leasing the required PCs for the Purchasing department offers benefits in terms of lower upfront costs, predictable monthly expenses, included support, and easier technology upgrades compared to purchasing, especially over a standard 3-year lifecycle.

**3.2. Reflection on Process and Teamwork**
The analysis and documentation process followed a structured approach. Utilizing Cisco Packet Tracer allowed for accurate visualization and verification of the existing network state. Team collaboration was crucial for dividing tasks and ensuring all requirements were addressed. The iterative process, including potential checkpoint reviews (as required), helps ensure alignment with client needs. Future improvements could involve more detailed performance testing within the simulation.
