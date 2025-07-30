"""
Configuration management for YukkiChatBot.
This module handles environment variables and bot settings.
"""

import os
from typing import List, Optional

class Config:
    """Configuration class for bot settings"""
    
    def __init__(self):
        # Telegram API credentials
        self.API_ID = int(os.getenv("API_ID", "26176218"))
        self.API_HASH: str = os.getenv("API_HASH", "4a50bc8acb0169930f5914eb88091736")
        self.BOT_TOKEN: str = os.getenv("BOT_TOKEN", "8031287331:AAE5-VXKJdFtLHcTe8NWw05_TDbn2jZdSEY")
        
        # Admins & Owner
        self.ADMIN_IDS: List[int] = self._parse_admin_ids()
        self.OWNER_ID: int = int(os.getenv("OWNER_ID", "1096693642"))
        
        # Bot Mode & Target
        self.BOT_MODE: str = os.getenv("BOT_MODE", "private")  # "private" or "group"
        self.TARGET_GROUP_ID: Optional[int] = self._parse_target_group()
        
        # Message
        self.MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "4096"))
        self.WELCOME_MESSAGE: str = os.getenv("WELCOME_MESSAGE", self._default_welcome_message())
        
        # Storage
        self.DATA_FILE: str = os.getenv("DATA_FILE", "bot_data.json")
        self.AUTO_SAVE_INTERVAL: int = int(os.getenv("AUTO_SAVE_INTERVAL", "300"))
        
        # Rate Limit
        self.RATE_LIMIT_MESSAGES: int = int(os.getenv("RATE_LIMIT_MESSAGES", "10"))
        self.RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
        
        # Validate
        self._validate_config()
    
    def _parse_admin_ids(self) -> List[int]:
        ids = os.getenv("ADMIN_IDS", "")
        if not ids:
            return []
        try:
            return [int(i.strip()) for i in ids.split(",") if i.strip()]
        except ValueError:
            print("⚠️ ADMIN_IDS must be comma-separated integers.")
            return []
    
    def _parse_target_group(self) -> Optional[int]:
        gid = os.getenv("TARGET_GROUP_ID", "")
        try:
            return int(gid) if gid else None
        except ValueError:
            print("⚠️ TARGET_GROUP_ID must be an integer.")
            return None
    
    def _default_welcome_message(self) -> str:
        return (
            "👋 Welcome to Anonymous Feedback Bot!\n\n"
            "📝 Send me any message and I'll forward it anonymously to the administrators.\n"
            "🔒 Your identity will remain completely anonymous.\n\n"
            "ℹ️ Use /help for more information."
        )
    
    def _validate_config(self):
        if not self.API_ID or self.API_ID == 0:
            raise ValueError("API_ID is required and must be a valid integer")
        if not self.API_HASH:
            raise ValueError("API_HASH is required")
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")
        if self.BOT_MODE not in ["private", "group"]:
            raise ValueError("BOT_MODE must be either 'private' or 'group'")
        if self.BOT_MODE == "group" and not self.TARGET_GROUP_ID:
            raise ValueError("TARGET_GROUP_ID must be set in group mode.")
    
    def is_admin(self, user_id: int) -> bool:
        return user_id in self.ADMIN_IDS or user_id == self.OWNER_ID
    
    def is_owner(self, user_id: int) -> bool:
        return user_id == self.OWNER_ID
    
    def get_target_chat_id(self) -> int:
        if self.BOT_MODE == "group" and self.TARGET_GROUP_ID:
            return self.TARGET_GROUP_ID
        elif self.ADMIN_IDS:
            return self.ADMIN_IDS[0]
        return self.OWNER_ID


if __name__ == "__main__":
    config = Config()
    print("✅ Config loaded successfully.")
