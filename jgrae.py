from graphviz import Digraph

# Crear un diagrama ERD
erd = Digraph('ERD', filename='er_diagram', format='png')

# Configuración de nodos
erd.attr(rankdir='LR', size='10')

# Nodos (Tablas)
erd.node('Campaigns', '''Campaigns
----------------------
id (PK)
campaign_type
channel
topic
started_at
finished_at
total_count
ab_test
warmup_mode
hour_limit
subject_length
subject_with_personalization
subject_with_deadline
subject_with_emoji
subject_with_bonuses
subject_with_discount
subject_with_saleout
is_test
position''', shape='box')

erd.node('ClientFirstPurchase', '''Client First Purchase
--------------------------------
client_id (PK)
first_purchase_date''', shape='box')

erd.node('Holidays', '''Holidays
----------------------
date (PK)
holiday''', shape='box')

erd.node('Messages', '''Messages
----------------------
id (PK)
message_id
campaign_id (FK)
message_type
client_id (FK)
channel
category
platform
email_provider
stream
date
sent_at
is_opened
opened_first_time_at
opened_last_time_at
is_clicked
clicked_first_time_at
clicked_last_time_at
is_unsubscribed
unsubscribed_at
is_hard_bounced
hard_bounced_at
is_soft_bounced
soft_bounced_at
is_complained
complained_at
is_blocked
blocked_at
is_purchased
purchased_at
created_at
updated_at''', shape='box')

# Relaciones
erd.edge('Messages', 'Campaigns', label='campaign_id (FK)')
erd.edge('Messages', 'ClientFirstPurchase', label='client_id (FK)')

# Renderizar y mostrar el diagrama
erd_path = "/mnt/data/er_diagram.png"
erd.render(erd_path, format="png", cleanup=True)
erd_path
