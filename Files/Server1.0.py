import asyncio
import websockets
import json
import os

# Define the path to your payload template file
PAYLOAD_FILE = "payload.html"

async def handle_deploy(websocket):
    print("Client connected to deploy portal bridge.")
    try:
        async for message in websocket:
            data = json.loads(message)
            target_ip = data.get("ip")
            
            print(f"Fetching payload for deployment target: {target_ip}")
            
            # Check if payload.html exists on disk
            if os.path.exists(PAYLOAD_FILE):
                with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
                    template_content = f.read()
                
                # Optional: Replace placeholders in your HTML file with dynamic data
                # e.g., if payload.html has {{ip}}, this swaps it out
                html_content = template_content.replace("{{ip}}", target_ip)
            else:
                # Fallback error message if the file is missing
                html_content = f"""
                <div style="color: #ef4444; padding: 1rem; background: #1e293b; border-radius: 6px;">
                    <strong>Error:</strong> payload.html not found on server disk.
                </div>
                """
            
            # Simulate a brief network/deployment delay
            await asyncio.sleep(1)
            
            # Send the file contents back to the frontend portal
            await websocket.send(json.dumps({
                "status": "Deployed",
                "payload_html": html_content
            }))
            
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")

async def main():
    async with websockets.serve(handle_deploy, "localhost", 8765):
        print("WebSocket payload bridge running on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())