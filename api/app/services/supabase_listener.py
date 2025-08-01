import asyncio
from supabase import acreate_client, AsyncClient
from app.services.websocket_manager import websocket_manager
from app.core.config import settings



class SupabaseListener:
    def __init__(self):
        print('Pong')
        self.supabase = None
        self.running = False
        
    def __await__(self):
        # Call ls the constructor and returns the instance
        return self.create().__await__()

    # A method that creates an instance of the class asynchronously
    async def create(self):
        # Perform some asynchronous initialization tasks
        self.supabase: AsyncClient = await acreate_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        
        # Return the instance
        return self

    async def listen_to_notifications(self):
        if self.running:
            return

        self.running = True
        print("Starting Supabase realtime listener...")

        async def callback(payload):
            print(f"Received change: {payload}")
            if payload["eventType"] == "INSERT":
                record = payload["new"]
                await websocket_manager.broadcast_to_user(
                    str(record["user_id"]),
                    {
                        "type": "new_notification",
                        "notification": {
                            "id": str(record["id"]),
                            "user_id": str(record["user_id"]),
                            "titre": record["titre"],
                            "message": record["message"],
                            "type": record["type"],
                            "lu": record["lu"],
                            "date_envoi": record["date_envoi"]
                        }
                    }
                )

        # Configuration de l'écoute
        changes = await self.supabase.channel("room1").on_postgres_changes("INSERT", schema="public", table="notifications", callback=callback).subscribe()

        try:
            while self.running:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Stopping Supabase listener...")
            self.running = False
            
_instance: SupabaseListener | None = None
_init_lock = asyncio.Lock()
            
async def get_supabase_listener():
    global _instance
    if _instance is None:
        async with _init_lock:
            if _instance is None:
                _instance = await SupabaseListener()
    return _instance

# supabase_listener = get_supabase_listener()