# Activity: Digital Trash or Treasure
**Instructions:** Decide: Keep, Archive, or Delete? Provide a 1-sentence rationale.

| Item | Decision | Rationale |
| :--- | :--- | :--- |
| **1. Old Student Records**<br>(Records from 10 years ago) | **DELETE** | The records exceed the typical retention period (active + 5 years), so they should be securely disposed of to minimize data privacy risks. |
| **2. Expired Session Tokens**<br>(Auth tokens from closed sessions) | **DELETE** | Session tokens are transient data with no operational value after logout; keeping them creates an unnecessary security risk (hijacking). |
| **3. Financial Reports**<br>(Required by law for 5 years) | **ARCHIVE** | These records must be kept for compliance but are likely inactive; moving them to secure, read-only storage protects integrity while freeing up active resources. |
| **4. Server Error Logs**<br>(Logs from the previous quarter) | **DELETE** | Operational logs typically have a short retention window (e.g., 90 days) for debugging; retaining them longer adds little value and potential information disclosure risk. |

---

# Activity: Lifecycle Mapping
**Task:** Map a chosen data scenario through its entire lifecycle.

### Chosen Scenario: **Employee Payroll Records**

**1. Define Retention Setting**
*   **Setting:** Retain for **7 years** after the fiscal year ends.
*   **Why:** To comply with tax laws and labor regulations regarding compensation records and audit requirements.

**2. Identify Archiving Trigger**
*   **Trigger:** End of the fiscal year (December 31st).
*   **Action:** Move records from the active payroll system to secure, encrypted cold storage (e.g., AWS S3 Glacier or an internal secure archive server) with strictly limited access.

**3. Select Disposal Method**
*   **Method:** **Crypto-shredding** (deleting the encryption keys) followed by a **Secure Overwrite** of the storage media.
*   **Why:** Payroll data involves sensitive PII. Crypto-shredding ensures instant unreadability, and overwriting prevents forensic recovery.

**4. Specify Verification**
*   **Method:** **Audit Logs & Negative Query**.
*   **Action:** Generate a system audit log confirming the deletion command execution. Perform a spot-check query on the archive database to confirm the specific records (older than 7 years) allow no results/access.
