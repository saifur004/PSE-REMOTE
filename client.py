import asyncio
import cv2
from aiortc import RTCPeerConnection, VideoStreamTrack
from aiortc.contrib.signaling import TcpSocketSignaling

# Set your Mobile Hotspot IP (Change this to match your network)
HOTSPOT_IP = "172.20.10.3"
PORT = 5001
class VideoTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)  # Change to 1 or 2 if needed
        if not self.cap.isOpened():
            print("❌ Camera failed to open!")
        else:
            print("✅ Camera opened successfully!")

    async def recv(self):
        ret, frame = self.cap.read()
        if not ret:
            print("❌ Failed to capture video frame")
            return
        print("📸 Sending video frame to WebRTC...")
        return frame

async def run():
    print("🚀 Starting WebRTC Client")
    try:
        # Connect to signaling server
        signaling = TcpSocketSignaling(HOTSPOT_IP, PORT + 1)  # Use port 5001 for client
  # Use correct port
        print(f"📡 Connecting to WebRTC Signaling Server at {HOTSPOT_IP}:{PORT}...")

        pc = RTCPeerConnection()
        pc.addTrack(VideoTrack())

        await pc.setLocalDescription(await pc.createOffer())
        print("📡 WebRTC Offer Created")

        print("📤 Sending WebRTC Offer...")
        try:
            await signaling.send(pc.localDescription)
            print("✅ WebRTC Offer Sent Successfully")
        except Exception as e:
            print(f"❌ Failed to send WebRTC Offer: {e}")
            return

        print("⏳ Waiting for WebRTC Answer...")
        try:
            answer = await signaling.receive()
            print("✅ Received WebRTC Answer:", answer)
            await pc.setRemoteDescription(answer)
            print("🎥 WebRTC Video Streaming Should Start Now!")
        except Exception as e:
            print(f"❌ Failed to receive WebRTC Answer: {e}")
            return

    except Exception as e:
        print(f"❌ WebRTC Error: {e}")

    while True:
        await asyncio.sleep(1)

asyncio.run(run())
