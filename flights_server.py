from mcp.server.fastmcp import FastMCP
import os
import json

# Chemin absolu vers le dossier resources
FLIGHTS_PATH = os.path.join(os.path.dirname(__file__), "flights.json")

# Création du serveur
mcp = FastMCP(name="Aéroport Info")

def _load_flights():
    """Charge la liste des vols depuis flights.json"""
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flights", [])



@mcp.resource("flights://today")
def flights_resource():
    """
    Resource qui expose la liste des vols du jour.
    L'URL 'flights://today' sera visible par Copilot/Claude.
    """
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return f.read()



@mcp.tool()
def find_flight(flight_number: str) -> str:
    """Trouve un vol par son numéro (ex: AF1234)"""
    flights = _load_flights()
    for flight in flights:
        if flight.get("flight_number", "").upper() == flight_number.upper():
            return (
                f"✈️ Vol {flight['flight_number']} ({flight['airline']})\n"
                f"{flight['departure_city']} → {flight['arrival_city']}\n"
                f"Départ : {flight['departure_time']} | Arrivée : {flight['arrival_time']}\n"
                f"Statut : {flight['status']}"
            )
    return f"Vol {flight_number} non trouvé."



@mcp.tool()
def flights_to(destination: str) -> str:
    """Liste tous les vols à destination d'une ville aujourd'hui."""
    flights = _load_flights()
    matches = [f for f in flights if destination.lower() in f["arrival_city"].lower()]

    if not matches:
        return f"Aucun vol trouvé vers {destination.title()}."

    result = f"Vols vers {destination.title()} ({len(matches)} trouvé(s)) :\n\n"
    for f in matches:
        result += f"• {f['flight_number']} → {f['arrival_city']} ({f['status']})\n"
    return result



@mcp.tool()
def flights_with_status(status: str) -> str:
    """Retourne les vols avec un statut particulier"""
    flights = _load_flights()
    matches = [f for f in flights if f["status"].lower() == status.lower()]

    if not matches:
        return f"Aucun vol avec le statut '{status}'."

    result = f"Vols avec statut '{status}' ({len(matches)}) :\n\n"
    for f in matches:
        result += f"• {f['flight_number']} → {f['arrival_city']}\n"
    return result



@mcp.tool()
def airline_flights(airline: str) -> str:
    """Liste tous les vols d'une compagnie aérienne"""
    flights = _load_flights()
    matches = [f for f in flights if airline.lower() in f["airline"].lower()]

    if not matches:
        return f"Aucun vol pour la compagnie {airline}."

    result = f"Vols opérés par {airline} :\n\n"
    for f in matches:
        result += f"• {f['flight_number']} → {f['arrival_city']} ({f['status']})\n"
    return result


# Lancement du serveur
if __name__ == "__main__":
    mcp.run(transport="stdio")
