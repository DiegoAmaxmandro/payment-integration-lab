## XML Authorization (Completed)

First working integration using the Global Payments XML API.

- Successfully authenticated request
- Generated SHA1 hash including card number
- Handled schema and validation errors
- Received successful authorization response

Status: ✅ Working

## XML API Scenario Testing

This project includes a scenario-driven XML API testing flow for the Global Payments / Realex sandbox.

### Current XML scenarios

| Scenario          | Purpose                                                                                                        | Expected Result |
| ----------------- | -------------------------------------------------------------------------------------------------------------- | --------------- |
| `success`         | Sends a valid XML authorization request                                                                        | `00`            |
| `wrong_cvn`       | Sends an invalid CVN format                                                                                    | `509`           |
| `invalid_hash`    | Sends a valid XML request with an incorrect SHA1 hash                                                          | `505`           |
| `duplicate_order` | Reuses the same order ID to simulate duplicate transaction handling. Run twice to trigger the duplicate error. | `501`           |

### How to run

From the project root:

```bash
python integrations/xml/xml_client.py success
python integrations/xml/xml_client.py wrong_cvn
python integrations/xml/xml_client.py invalid_hash
```
