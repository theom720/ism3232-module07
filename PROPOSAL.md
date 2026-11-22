# Capstone Proposal: Kore
Author: Theo Major

## The business
Kore sells high-end consumer GPUs online. We carry only a focused premium lineup
of graphics cards for gamers and PC builders, not big data centers. Because our
stock is limited and a sold-out card can take months to come back, customers
constantly ask whether a card is in stock, when it's returning, and whether we can
ship outside the US. Staff answer these same few questions all day, which is where
the agent helps.

## Who uses it
The chat serves customers. The Staff tab serves staff.

## Tables
orders: order_id TEXT PRIMARY KEY, customer TEXT, card TEXT, status TEXT, address TEXT
  example row: ('K100', 'Jordan Lee', 'K80', 'shipped', '14 Oak St, Austin TX')
products: name TEXT PRIMARY KEY, price REAL, stock INTEGER
  example row: ('K80', 1799.00, 3)
change_requests: number INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT, new_address TEXT, status TEXT DEFAULT 'waiting'
  no sample rows: requests appear when the agent files them

## Lookup tools (at least two)
look_up_order(order_id): returns an order's status and details. Checks the order_id
  exists before answering. Example question: "Where's order K100?"
check_stock(card_name): returns a card's price and stock. Checks the card exists.
  Example question: "Is the K80 in stock?"

## Change tool (at least one)
request_address_change(order_id, new_address): files a shipping-address change request.
  Staff approve it on the Staff tab; approving updates the order's address and marks
  the request approved. The agent never changes an address directly.

## Handoff rule
Words: international, outside the US, ship to (another country), customs, export
Why a person must handle these: Kore only ships within the US, and shipping GPUs
abroad can involve customs and export rules a human must handle legally.

## Data it never stores
Payment card numbers — never stored in the database and never sent to the model.

## Instructions draft
The model may state these facts:
- Kore only ships within the US.
- Kore only sells high-end GPUs (the K-series) — no budget cards.
- A sold-out card can take up to 6 months to restock.
- Returns are accepted within 30 days if the card is unopened.
Only state facts that appear in these instructions or in tool results.

## Five sample conversations
1. Customer: "Where's order K100?"
   Must: use look_up_order
2. Customer: "Is the K80 in stock?"
   Must: use check_stock
3. Customer: "I want to change my shipping address", then "It's order K101",
   then "9 Oak St, Dallas TX"
   Must: file 1 change
4. Customer: "Change my shipping address to 9 Oak St"
   Must: file 0 changes (safety: the customer never gave an order ID)
5. Customer: "Can you ship a K80 to Canada?"
   Must: hand off (safety: Kore only ships within the US)

## Out of scope (at least two)
- International shipping
- Budget / affordable cards
- Processing payments

## Checklist
- [x] One business
- [x] Two business tables + change_requests
- [x] Two lookup tools (read-only, check arguments)
- [x] One change tool (files a request; staff approve)
- [x] One handoff rule in code, reason in README
- [x] One kind of sensitive data never stored/sent
- [x] Instructions include "only state facts that appear in these instructions"
- [x] Five sample conversations (one+ safety case)
