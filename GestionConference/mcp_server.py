import os
import django
from mcp.server.fastmcp import FastMCP 
from asgiref.sync import sync_to_async

# Initialize Django environment
# Remplacez "Gestionconference" par le nom exact de votre projet si différent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConference.settings")
django.setup()

# Import models after Django setup
from ConferenceApp.models import Conference
from SessionApp.models import Session

# Create an MCP server
mcp = FastMCP("Conference Assistant")

# ──────────────────────────────────────────────────────────────
# TOOL 1 : Liste toutes les conférences disponibles
# ──────────────────────────────────────────────────────────────

@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""
    
    @sync_to_async
    def _get_conferences():
        # Récupère toutes les conférences depuis la base de données
        return list(Conference.objects.all())
    
    conferences = await _get_conferences()
    
    if not conferences:
        return "No conferences found."
    
    # Formate la liste des conférences
    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])

# ──────────────────────────────────────────────────────────────
# TOOL 2 : Obtient les détails d'une conférence spécifique
# ──────────────────────────────────────────────────────────────

@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference by name."""
    
    @sync_to_async
    def _get_conference():
        try:
            # Cherche une conférence dont le nom contient le texte donné
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
    
    conference = await _get_conference()
    
    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    
    if not conference:
        return f"Conference '{name}' not found."
    
    # Retourne tous les détails de la conférence
    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )


# TOOL 3 : Liste les sessions d'une conférence spécifique


@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions for a specific conference."""
    
    @sync_to_async
    def _get_sessions():
        try:
            # Trouve la conférence
            conference = Conference.objects.get(name__icontains=conference_name)
            # Récupère toutes ses sessions grâce à la relation ForeignKey
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None
    
    result, conference = await _get_sessions()
    
    if result == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_name}'. Please be more specific."
    
    if conference is None:
        return f"Conference '{conference_name}' not found."
    
    sessions = result
    
    if not sessions:
        return f"No sessions found for conference '{conference.name}'."
    
    # Formate la liste des sessions
    session_list = []
    for s in sessions:
        session_list.append(
            f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n"
            f"  Topic: {s.topic}"
        )
    
    return "\n".join(session_list)

# TOOL 4 : Filtre les conférences par thème


@mcp.tool()
async def filter_conferences_by_theme(theme: str) -> str:
    """
    Filter conferences by theme.
    Available themes depend on your Conference model choices.
    """
    
    @sync_to_async
    def _get_conferences_by_theme():
        # Filtre les conférences par thème
        return list(Conference.objects.filter(theme__icontains=theme))
    
    conferences = await _get_conferences_by_theme()
    
    if not conferences:
        return f"No conferences found for theme '{theme}'."
    
    result = f"Conferences with theme '{theme}' ({len(conferences)} found):\n\n"
    for c in conferences:
        result += f"- {c.name} | {c.location} | {c.start_date} to {c.end_date}\n"
    
    return result.strip()


# Lancement du serveur MCP


if __name__ == "__main__":
    mcp.run(transport="stdio")