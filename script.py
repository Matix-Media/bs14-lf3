#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ipaddress
import math
import sys
def get_valid_ip_network(prompt_ip, prompt_mask):
   """Fragt nach IP und Maske und gibt ein ipaddress.IPv4Network-Objekt zurück."""
   while True:
       try:
           ip_str = input(prompt_ip).strip()
           mask_str = input(prompt_mask).strip()
           # Versucht, das Netzwerk zu parsen (strict=False erlaubt Host-Bits in der IP)
           network_str = f"{ip_str}/{mask_str}"
           network = ipaddress.ip_network(network_str, strict=False)
           # Wir wollen aber die tatsächliche Netzwerkadresse
           network = ipaddress.ip_network(f"{network.network_address}/{network.prefixlen}", strict=True)
           if not isinstance(network, ipaddress.IPv4Network):
               raise ValueError("Nur IPv4-Adressen werden unterstützt.")
           return network
       except ValueError as e:
           print(f"Ungültige Eingabe: {e}. Bitte erneut versuchen.")
       except Exception as e:
           print(f"Ein unerwarteter Fehler ist aufgetreten: {e}. Bitte erneut versuchen.")
def get_valid_int(prompt, min_val=1):
   """Fragt nach einer positiven Ganzzahl."""
   while True:
       try:
           value_str = input(prompt).strip()
           value = int(value_str)
           if value < min_val:
               raise ValueError(f"Die Zahl muss mindestens {min_val} sein.")
           return value
       except ValueError as e:
           print(f"Ungültige Eingabe: {e}. Bitte eine gültige Zahl eingeben.")
def calculate_subnets(base_network, num_required_subnets):
   """Berechnet die benötigten Subnetze."""
   original_prefix = base_network.prefixlen
   # Berechne, wie viele zusätzliche Bits benötigt werden
   if num_required_subnets <= 0:
       return [], 0 # Keine Subnetze benötigt
   bits_needed = math.ceil(math.log2(num_required_subnets))
   new_prefix = original_prefix + bits_needed
   if new_prefix > 32:
       print(f"Fehler: Es können nicht {num_required_subnets} Subnetze aus dem Netzwerk {base_network} erstellt werden.")
       print(f"Dafür wäre eine Präfixlänge von {new_prefix} notwendig, was für IPv4 ungültig ist (> 32).")
       return None, None # Signalisiert einen Fehler
   try:
       subnets = list(base_network.subnets(new_prefix=new_prefix))
       return subnets, new_prefix
   except ValueError as e:
       print(f"Fehler bei der Subnetzberechnung: {e}")
       return None, None
def print_subnet_info(subnet_list, new_prefix):
   """Gibt die Informationen zu den Subnetzen übersichtlich aus."""
   if not subnet_list:
       print("\nKeine Subnetze zu berechnen oder anzuzeigen.")
       return
   new_mask = subnet_list[0].netmask # Die Maske ist für alle Subnetze gleich
   print("\n--- Ergebnis der Subnetzberechnung ---")
   print(f"Ursprüngliches Netzwerk: {subnet_list[0].supernet(prefixlen_diff=new_prefix-subnet_list[0].supernet().prefixlen)}")
   print(f"Angeforderte Subnetze: {2**(new_prefix-subnet_list[0].supernet().prefixlen)} (mindestens {len(subnet_list)} benötigt)")
   print(f"Neue Subnetzmaske:    {new_mask} (/{new_prefix})")
   print("-" * 70)
   print(f"{'Subnetz':<18} {'Netzwerkadresse':<18} {'Erste Host-IP':<18} {'Letzte Host-IP':<18} {'Broadcast':<18}")
   print("-" * 90)
   for i, subnet in enumerate(subnet_list):
       network_addr = subnet.network_address
       broadcast_addr = subnet.broadcast_address
       hosts = list(subnet.hosts())
       first_host = hosts[0] if hosts else "N/A"
       last_host = hosts[-1] if hosts else "N/A"
       print(f"Subnetz #{i+1:<10} {str(network_addr):<18} {str(first_host):<18} {str(last_host):<18} {str(broadcast_addr):<18}")
   print("-" * 90)
   print(f"Anzahl Hosts pro Subnetz: {subnet_list[0].num_addresses}")
   usable_hosts = max(0, subnet_list[0].num_addresses - 2) # Netz- und Broadcastadresse abziehen
   print(f"Nutzbare Hosts pro Subnetz: {usable_hosts}")
   print("-" * 70)
if __name__ == "__main__":
   print("--- Subnetz Rechner ---")
   base_network = get_valid_ip_network(
       "Geben Sie die Basis-IP-Adresse ein (z.B. 192.168.1.0): ",
       "Geben Sie die Basis-Subnetzmaske ein (z.B. 255.255.255.0 oder /24): "
   )
   desired_subnets = get_valid_int(
       "Geben Sie die gewünschte Anzahl an Subnetzen ein: ",
       min_val=1
   )
   calculated_subnets, new_prefix = calculate_subnets(base_network, desired_subnets)
   if calculated_subnets is not None:
       print_subnet_info(calculated_subnets, new_prefix)
   print("\nProgramm beendet.")
