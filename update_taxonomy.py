import pandas as pd
import sys
import io

# Set UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read the Excel file
df = pd.read_excel('sc_cat_item.xlsx')

# Convert columns to object type to allow string assignment
df['New Name'] = df['New Name'].astype('object')
df['New Category (Topic)'] = df['New Category (Topic)'].astype('object')

# Define the mapping based on the taxonomy document
# Format: (current_name_pattern, new_name, new_category)
mappings = [
    # Access & Identity
    ('Dynamic Lease Tool Okta Access Request',
     'Okta Access - Dynamic Lease Tool (RETIRE - Unused)',
     'Access & Identity → System/Application Access'),

    ('Access to Operational Portal',
     'Request SAS Tools Portal Access',
     'Access & Identity → System/Application Access'),

    ('NetOps BlueCat IPAM',
     'Request BlueCat IPAM Access',
     'Access & Identity → System/Application Access'),

    ('Remote access FER',
     'Request Bastion Access (FER Prod & Edge)',
     'Access & Identity → Remote/Secure Access'),

    ('Tableau Access',
     'Request Tableau Access',
     'Access & Identity → System/Application Access'),

    ('SCC',
     'Request SCC Systems Access',
     'Access & Identity → System/Application Access'),

    ('Operations VPN',
     'Request Operations VPN Access',
     'Access & Identity → Remote/Secure Access'),

    ('Network Infrastructure Access via Ops Terminal Servers',
     'Request Terminal Server Access (Transport Network)',
     'Access & Identity → Remote/Secure Access'),

    ('Network Infrastructure Access Request',
     'Request Terminal Server Access (Transport Network)',
     'Access & Identity → Remote/Secure Access'),

    # Network & Connectivity
    ('Bandwidth Upgrade Request',
     'Backbone Bandwidth Upgrade',
     'Network & Connectivity → Traffic & Capacity'),

    ('Partner Rate Limit',
     'Partner Rate Limit Change',
     'Network & Connectivity → Traffic & Capacity'),

    ('L2XC Routing Request',
     'Provision Layer-2 Cross Connect (EVPN)',
     'Network & Connectivity → Connectivity Services'),

    ('Load Balancer Access',
     'Request Load Balancer Configuration (F5)',
     'Network & Connectivity → Network Device & Platform Changes'),

    ('AWS Cloud Connectivity',
     'Provision Cloud Connectivity (AWS over Transport)',
     'Network & Connectivity → Connectivity Services'),

    ('ISP',
     'Provision Internet Access (Sites & Services)',
     'Network & Connectivity → Connectivity Services'),

    ('3rd party VPN',
     'Provision Customer VPN Access (3rd-Party)',
     'Network & Connectivity → Connectivity Services'),

    ('Meet Me Point',
     'Configure Meet-Me Point (MMP)',
     'Network & Connectivity → Connectivity Services'),

    ('Router/Switch',
     'Request Router/Switch Configuration (Juniper/Cisco)',
     'Network & Connectivity → Network Device & Platform Changes'),

    # Security
    ('Access Port Openings',
     'Firewall Port/Access Change (Palo Alto)',
     'Security → Perimeter & Policy'),

    ('IP Address Blacklisting',
     'IP/DNS Blacklisting',
     'Security → Perimeter & Policy'),

    # Cloud & Compute
    ('New Operations Virtual Machine',
     'Provision New VM/Instance (Operations)',
     'Cloud & Compute → Private/Public Cloud Compute'),

    ('Resource change for existing Operations VM',
     'Modify Existing VM/Instance',
     'Cloud & Compute → Private/Public Cloud Compute'),

    ('Resource change for existing Operations Virtual Machine',
     'Modify Existing VM/Instance',
     'Cloud & Compute → Private/Public Cloud Compute'),

    ('Operations Cloud Hosted Service',
     'Access Request - Operations Cloud Hosted Services',
     'Cloud & Compute → Operations Cloud Hosted Services'),

    ('New Kubernetes Environment',
     'Provision New Kubernetes Cluster (Self-Managed)',
     'Cloud & Compute → Kubernetes'),

    # Satellite & Radio (GX)
    ('GX - Load New Channel, Beam, Map files into NMS',
     'Load New Channel/Beam/Map Files into NMS',
     'Satellite & Radio (GX) → Configuration & Enablement'),

    ('GX - Terminal Beam Switch Diagnostics',
     'Terminal Beam Switch Diagnostics',
     'Satellite & Radio (GX) → Operations Support'),

    ('GX - Enable CM logging',
     'Enable CM Logging',
     'Satellite & Radio (GX) → Configuration & Enablement'),

    ('GX - Enable PP Logging',
     'Enable PP Logging',
     'Satellite & Radio (GX) → Configuration & Enablement'),

    ('GX - Demo support',
     'Demo Support',
     'Satellite & Radio (GX) → Operations Support'),

    ('GX - Terminal Switch Port SVN Addition',
     'Terminal Switch Port SVN Addition',
     'Satellite & Radio (GX) → Configuration & Enablement'),

    ('GX - Terminal Type Addition to Channel',
     'Terminal Type Addition to Channel',
     'Satellite & Radio (GX) → Configuration & Enablement'),

    ('GX - Terminal Type Addition',
     'Terminal Type Addition',
     'Satellite & Radio (GX) → Configuration & Enablement'),

    ('New L-Band Fallback APN',
     'New L-Band Fallback APN',
     'Satellite & Radio (GX) → Fallback & APN'),

    ('Provisioning an ABU Aircraft',
     'Provision ABU Aircraft (Airborne Base Unit)',
     'Satellite & Radio (GX) → Configuration & Enablement'),

    # Voice & Communications
    ('New SIP Trunk',
     'New SIP Trunk (Operations)',
     'Voice & Communications → Voice Core'),

    ('New Distribution Partner for I4 Services',
     'New Distribution Partner (I4 Services)',
     'Voice & Communications → Partners'),

    # Service Support & Tooling
    ('Everbridge and Elog Support',
     'Everbridge / eLog – Changes & Enhancements',
     'Service Support & Tooling → Service Support Systems'),

    ('Service Support Systems – Request For Work',
     'Service Support Systems – Request for Work',
     'Service Support & Tooling → Service Support Systems'),

    ('Service Support Systems - Request For Work',
     'Service Support Systems – Request for Work',
     'Service Support & Tooling → Service Support Systems'),

    ('Update/Add Customer Facing Business Services',
     'Update/Add Customer-Facing Business Services (CMDB/Service Catalog)',
     'Service Support & Tooling → ServiceNow'),

    # Operational Requests (General)
    ('Submit a Network Operations Request',
     'Network Operations – General Request / Enquiry',
     'Operational Requests (General)'),
]

# Apply mappings
for idx, row in df.iterrows():
    current_name = row['Name']

    # Find matching mapping
    for pattern, new_name, new_category in mappings:
        if pattern.lower() in current_name.lower():
            df.at[idx, 'New Name'] = new_name
            df.at[idx, 'New Category (Topic)'] = new_category
            break

# Save to new file
output_file = 'sc_cat_item_updated.xlsx'
df.to_excel(output_file, index=False)

print(f"✓ Updated Excel file saved as: {output_file}")
print(f"\nSummary:")
print(f"- Total items: {len(df)}")
print(f"- Items with new names: {df['New Name'].notna().sum()}")
print(f"- Items with new categories: {df['New Category (Topic)'].notna().sum()}")
print(f"\nItems still needing manual review:")
for idx, row in df.iterrows():
    if pd.isna(row['New Name']):
        print(f"  - {row['Name']}")
