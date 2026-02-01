## Admin Commands

### Table of Contents
- [Session list](#session-list)
- [Session terminate](#session-terminate)
- [Session terminate all](#session-terminate-all)
- [User list](#user-list)
- [User delete](#user-delete)
- [Show exchange](#show-exchange)
- [Show market](#show-market)
- [Show symbol](#show-symbol)

---

### Session list
**Command:** `/session list`
**Description:** Lists all active sessions.

| Parameter | Type   | Description                | Required |
|-----------|--------|----------------------------|----------|
| None      | N/A    | This command does not take any parameters. | No       |
**Example Usage:** `/session list`
**Example Response:**
```
Active Sessions:
1. Session ID: 12345, User: admin, Started: 2024-06-01 10:00 AM
2. Session ID: 67890, User: user1, Started
2024-06-01 11:30 AM
```
---
### Session terminate
**Command:** `/session terminate <session_id>`
**Description:** Terminates a specific session by its ID.
| Parameter   | Type   | Description                | Required |
|-------------|--------|----------------------------|----------|
| session_id  | String | The ID of the session to terminate. | Yes      |
**Example Usage:** `/session terminate 12345`
**Example Response:**
```
Session with ID 12345 has been terminated successfully.
```
---
### Session terminate all
**Command:** `/session terminate all`
**Description:** Terminates all active sessions.
| Parameter | Type   | Description                | Required |
|-----------|--------|----------------------------|----------|
| None      | N/A    | This command does not take any parameters. | No       |
**Example Usage:** `/session terminate all` 
**Example Response:**
```
All active sessions have been terminated successfully.
```
---
### User list
**Command:** `/user list`
**Description:** Lists all registered users.
| Parameter | Type   | Description                | Required |
|-----------|--------|----------------------------|----------|
| None      | N/A    | This command does not take any parameters. | No       |
**Example Usage:** `/user list`
**Example Response:**
```
Registered Users:
1. User ID: 1, Username: admin, Role: Administrator
2. User ID: 2, Username: user1, Role: User
```
---
### User delete
**Command:** `/user delete <user_id>`
**Description:** Deletes a specific user by their ID.
| Parameter | Type   | Description                | Required |
|-----------|--------|----------------------------|----------|  
| user_id   | String | The ID of the user to delete. | Yes      |
**Example Usage:** `/user delete 2`
**Example Response:**
```
User with ID 2 has been deleted successfully.
```
---
### Show exchange
**Command:** `/show exchange <exchange_name>`
**Description:** Displays information about a specific exchange.
| Parameter     | Type   | Description                | Required |
|---------------|--------|----------------------------|----------|
| exchange_name | String | The name of the exchange to display information for. | Yes      |
**Example Usage:** `/show exchange HKG`
**Example Response:**
``` 
Exchange Information:
Name: HKG
Location: Hong Kong
Timezone: GMT+8
Trading Hours: 9:30 AM - 4:00 PM
```
---
### Show market
**Command:** `/show market <market_name>`
**Description:** Displays information about a specific market.
| Parameter   | Type   | Description                | Required |
|-------------|--------|----------------------------|----------|
| market_name | String | The name of the market to display information for. | Yes      |
**Example Usage:** `/show market equities`
**Example Response:**
```
Market Information:
Name: Equities
Description: A market for buying and selling shares of companies.
Operating Hours: 9:30 AM - 4:00 PM
```
---
### Show symbol
**Command:** `/show symbol <symbol_name>`
**Description:** Displays information about a specific symbol.
| Parameter   | Type   | Description                | Required |
|-------------|--------|----------------------------|----------|
| symbol_name | String | The name of the symbol to display information for. | Yes      |
**Example Usage:** `/show symbol AAPL`
**Example Response:**
```
Symbol Information:
Name: AAPL
Description: Apple Inc. common stock
Exchange: NASDAQ
Sector: Technology
Market Cap: $2.5 Trillion
```
