from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import paho.mqtt.client as mqtt
import json
import logging
from typing import Dict, Any, Optional
from app.routers import data_router
from app.services.data_service import DataService
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
latest_values: Dict[str, Dict[str, Any]] = {}
mqtt_client = None
connected = False

# HiveMQ broker configuration
BROKER = "broker.hivemq.com"
PORT = 1883
CLIENT_ID = "fastapi-arkitech-client"
TOPIC_PREFIX = "arkitech/ships/vessel1/#"

# Initialize data service
data_service = DataService()

# MQTT callbacks with Paho MQTT v2.0 API
def on_connect(client, userdata, flags, rc, properties=None):
    global connected
    if rc == 0:
        logger.info(f"Connected to HiveMQ broker at {BROKER}:{PORT}")
        connected = True
        # Subscribe to all ship HVAC topics
        client.subscribe(TOPIC_PREFIX)
        logger.info(f"Subscribed to {TOPIC_PREFIX}")
    else:
        logger.error(f"Failed to connect to broker, return code: {rc}")
        connected = False

def on_message(client, userdata, msg):
    try:

        # Decode the topic and message
        topic = msg.topic
        payload = json.loads(msg.payload.decode())
        
        # Store the latest telemetry value in mongodb
        insert_id = data_service.insert_item({
            "topic": topic,
            "payload": payload
        }).inserted_id

        
        logger.info(f"Received on {topic}: {payload} (inserted as {insert_id})")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

# Start MQTT client in a background thread
def start_mqtt_client():
    global mqtt_client
    
    # Use the proper Paho MQTT v2.0 API
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.client_id = CLIENT_ID
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    try:
        logger.info(f"Connecting to HiveMQ broker at {BROKER}:{PORT}...")
        mqtt_client.connect(BROKER, PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        logger.error(f"Error connecting to MQTT broker: {e}")

# Lifespan manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize MQTT client
    start_mqtt_client()
    yield
    # Shutdown: clean up MQTT client
    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        logger.info("MQTT client disconnected")

# Create FastAPI app with lifespan
app = FastAPI(
    title="Arkitech MQTT Integration",
    description="FastAPI application that integrates with HiveMQ MQTT broker to receive ship HVAC data",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Arkitech MQTT Integration API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "mqtt_connected": connected}

app.include_router(data_router.router)
